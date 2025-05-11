from django.db.models import Count
from apps.posts.models import Application

# 모집 자동 마감
def check_post_closed(post):
    roles_needed = post.roles or {}

    if not roles_needed:
        return False  # roles 정보가 없으면 마감 조건 판단 불가

    # 역할별 신청 인원 집계
    applied = (
        Application.objects.filter(post=post)
        .values('role')
        .annotate(count=Count('id'))
    )
    applied_dict = {item['role']: item['count'] for item in applied}

    # 하나라도 미달이면 마감되지 않음
    for role, max_count in roles_needed.items():
        if applied_dict.get(role, 0) < max_count:
            return False

    # 이미 마감 상태가 아니라면 업데이트
    if not post.is_closed:
        post.is_closed = True
        post.save()

    return True
