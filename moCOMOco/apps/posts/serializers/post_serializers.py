from apps.posts.utils.markdown import render_markdown
from apps.posts.models.post_like import PostLike
from apps.posts.models.schedule import Schedule
from rest_framework import serializers
from apps.posts.models.post import Post
from apps.posts.models.application import Application
from apps.posts.serializers.schedule_serializers import ScheduleCreateSerializer

# 한글 역할 -> 영어 역할 매핑
POSITION_REVERSE_MAP = {
    "백엔드": "backend",
    "프론트엔드": "frontend",
    "풀스택": "fullstack",
    "디자이너": "designer"
}


# 모집글 생성용 (post)
class PostCreateListSerializer(serializers.ModelSerializer):
    # 역할군 인원 수 (프론트에서 개별 입력)
    backend = serializers.IntegerField(required=False, write_only=True, default=0)
    frontend = serializers.IntegerField(required=False, write_only=True, default=0)
    designer = serializers.IntegerField(required=False, write_only=True, default=0)
    fullstack = serializers.IntegerField(required=False, write_only=True, default=0)
    image = serializers.ImageField(required=False, allow_null=True)
    schedule = ScheduleCreateSerializer(required=False)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'category',
            'place_name', 'address', 'latitude', 'longitude',
            'image', 'date', 'max_people', 'is_closed',
            'backend', 'frontend', 'designer', 'fullstack',
            'schedule'
        ]
        read_only_fields = ['is_closed']

    def create(self, validated_data):
        user = self.context['user']
        schedule_data = validated_data.pop('schedule', None)

        roles = {
            "backend": validated_data.pop("backend", 0),
            "frontend": validated_data.pop("frontend", 0),
            "designer": validated_data.pop("designer", 0),
            "fullstack": validated_data.pop("fullstack", 0),
        }
        # 역할군 의 합을 max_people로 설정
        validated_data['max_people'] = sum(roles.values())

        writer_role = POSITION_REVERSE_MAP.get(getattr(user, 'position_name', ''), None)
        if not writer_role:
            raise serializers.ValidationError('작성자의 포지션 정보가 유효하지 않습니다.')

        post = Post.objects.create(
            **validated_data,
            roles=roles,
            writer_role=writer_role,
            user=user
        )

        # 일정 자동 생성 (프론트가 schedule 명시 안해도 생성되도록)
        if schedule_data:
            Schedule.objects.create(post=post, **schedule_data)
        elif post.date:
            Schedule.objects.create(
                post=post,
                date=post.date,
                memo=f"{post.title} 일정"  # 또는 "기본 일정" 등으로 커스터마이징 가능
            )

        return post

# 모집글 목록 조회용 (get)
class PostListSerializer(serializers.ModelSerializer):
    people_status = serializers.SerializerMethodField()
    role_status = serializers.SerializerMethodField()
    is_writer = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'category',
            'place_name', 'address', 'date',
            'image', 'is_closed', 'max_people',
            'people_status', 'role_status',
            'is_writer', 'is_applied', 'is_liked',
        ]

    def get_people_status(self, obj):
        current = Application.objects.filter(post=obj).count()

        return current + 1

    def get_role_status(self, obj):
        from collections import defaultdict

        # 역할별 신청 인원 수 계산
        role_counts = defaultdict(int)
        for app in Application.objects.filter(post=obj):
            role_counts[app.role] += 1

        # 작성자도 포함
        if obj.writer_role:
            role_counts[obj.writer_role] += 1

        # 남은 인원 계산
        remaining = {}
        for role, max_count in obj.roles.items():
            remaining[role] = max(0, max_count - role_counts.get(role, 0))

        return remaining

    def get_is_writer(self, obj):
        request = self.context.get('request')
        return request.user == obj.user if request and request.user.is_authenticated else False

    def get_is_applied(self, obj):
        request = self.context.get('request')
        return Application.objects.filter(post=obj, user=request.user).exists() if request and request.user.is_authenticated else False

    def get_is_liked(self, obj):
        request = self.context.get('request')
        return PostLike.objects.filter(post=obj, user=request.user).exists() if request and request.user.is_authenticated else False

# 모집글 상세 조회용 (전체 정보 포함)
class PostDetailSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()
    current_people = serializers.SerializerMethodField()
    people_status = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()
    role_status = serializers.SerializerMethodField()
    is_writer = serializers.SerializerMethodField()
    content_html = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'content_html', 'category',
            'place_name', 'address', 'latitude', 'longitude',
            'image', 'date', 'max_people', 'is_closed',
            'created_at', 'updated_at',
            'writer', 'is_liked', 'is_applied',
            'current_people', 'people_status',
            'participants', 'role_status',
            'is_writer'
        ]

    def get_writer(self, obj):
        # 작성자 정보: id, 닉네임, 프로필 이미지
        return {
            "id": obj.user.id,
            "nickname": obj.user.nickname,
            "profile_image": obj.user.profile_image if obj.user.profile_image else None
        }

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return PostLike.objects.filter(user=user, post=obj).exists()

    def get_is_applied(self, obj):
        user = self.context['request'].user
        return Application.objects.filter(user=user, post=obj).exists()

    def get_current_people(self, obj):
        return Application.objects.filter(post=obj).count() + 1

    def get_people_status(self, obj):
        return Application.objects.filter(post=obj).count() + 1

    def get_participants(self, obj):
        # 참여자 요약 정보 리스트 (id, 닉네임, 프로필)
        participants = [
            {
                "id": app.user.id,
                "nickname": app.user.nickname,
                "profile_image": app.user.profile_image if app.user.profile_image else None
            }
            for app in Application.objects.filter(post=obj).select_related('user')
        ]

        # 작성자가 이미 포함되지 않은 경우에만 수동 삽입
        if obj.user.id not in [p['id'] for p in participants]:
            participants.insert(0, {
                "id": obj.user.id,
                "nickname": obj.user.nickname,
                "profile_image": obj.user.profile_image if obj.user.profile_image else None
            })

        return participants

    def get_role_status(self, obj):
        from collections import defaultdict
        role_counts = defaultdict(int)

        for app in Application.objects.filter(post=obj):
            role_counts[app.role] += 1

        if obj.writer_role:
            role_counts[obj.writer_role] += 1

        remaining = {}
        for role, max_count in obj.roles.items():
            remaining[role] = max(0, max_count - role_counts.get(role, 0))

        return remaining

    def get_is_writer(self, obj):
        request = self.context.get('request')
        return request.user == obj.user if request and request.user.is_authenticated else False

    def get_content_html(self, obj):
        return render_markdown(obj.content)

# 모집글 수정용
class PostUpdateSerializer(serializers.ModelSerializer):
    # 수정 시에도 역할별 인원 받기
    backend = serializers.IntegerField(required=False, default=0)
    frontend = serializers.IntegerField(required=False, default=0)
    designer = serializers.IntegerField(required=False, default=0)
    fullstack = serializers.IntegerField(required=False, default=0)

    class Meta:
        model = Post
        fields = [
            'title', 'content', 'category',
            'place_name', 'address', 'latitude', 'longitude',
            'image', 'date', 'max_people', 'is_closed',
            'backend', 'frontend', 'designer', 'fullstack'
        ]

    def update(self, instance, validated_data):
        roles = {
            "backend": validated_data.pop("backend", 0),
            "frontend": validated_data.pop("frontend", 0),
            "designer": validated_data.pop("designer", 0),
            "fullstack": validated_data.pop("fullstack", 0),
        }
        # 역할군의 합을 max_people로 설정
        validated_data['max_people'] = sum(roles.values())

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.roles = roles
        instance.save()
        return instance



# 참여비율 기반 간단 상세 조회
class PostSimpleDetailSerializer(serializers.ModelSerializer):
    current_people = serializers.SerializerMethodField()  # 현재 신청자 수
    status = serializers.SerializerMethodField()          # UI용 상태: 모집중 / 모집완료

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'category',
            'place_name', 'image',
            'max_people', 'current_people',
            'is_closed', 'status',
        ]

    def get_current_people(self, obj):
        return Application.objects.filter(post=obj).count()

    def get_status(self, obj):
        current = self.get_current_people(obj)
        return "모집완료" if current >= obj.max_people else "모집중"

class PostListSerializerWithParticipants(PostListSerializer):
    participants = serializers.SerializerMethodField()
    people_status = serializers.SerializerMethodField()

    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ['participants', 'people_status']

    def get_participants(self, obj):
        applications = Application.objects.filter(post=obj).select_related('user')

        participant_list = [
            {
                "id": app.user.id,
                "nickname": app.user.nickname,
                "profile_image": app.user.profile_image if app.user.profile_image else None
            }
            for app in applications
        ]

        # 작성자가 이미 포함되지 않았다면 추가
        if obj.user.id not in [p['id'] for p in participant_list]:
            participant_list.insert(0, {
                "id": obj.user.id,
                "nickname": obj.user.nickname,
                "profile_image": obj.user.profile_image if obj.user.profile_image else None
            })

        return participant_list