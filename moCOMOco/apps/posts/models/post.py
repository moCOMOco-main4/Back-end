from django.db import models
from django.conf import settings

# 모집글 카테고리 선택지 (드롭다운 형태)
CATEGORY_CHOICES = [
    ('meeting', '모집'),
    ('project', '프로젝트'),
]


# 모집글(Post) 모델
class Post(models.Model):
    # 작성자 (User와 연결)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )

    # 제목 / 본문
    title = models.CharField(max_length=100)
    content = models.TextField()

    # 카테고리 (meeting, project 중 선택)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=15)

    # 장소 정보
    place_name = models.CharField(max_length=100)
    address = models.TextField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    # 썸네일 이미지 (선택 사항)
    image = models.ImageField(
        upload_to='posts/images/',
        null=True,
        blank=True
    )

    # 모집 날짜 (모각코 예정일 등)
    date = models.DateTimeField(default=5)

    # 최대 인원 수 (전체 참가자 수 기준)
    max_people = models.PositiveIntegerField()

    # 모집 마감 여부 (True면 마감)
    is_closed = models.BooleanField(default=False)

    # 역할별 인원 구성 (프론트, 백엔드, 디자이너 등)
    # 예시: {"frontend": 1, "backend": 2}
    roles = models.JSONField(default=dict)

    # 생성일 / 수정일 자동 저장
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 최신 글이 위로 오도록 정렬
        ordering = ['-created_at']
