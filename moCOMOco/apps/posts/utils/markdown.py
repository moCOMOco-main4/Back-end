import markdown
import bleach
from django.utils.safestring import mark_safe
from typing import List


def render_markdown(text: str) -> str:
    # 1단계: 마크다운 → HTML
    html = markdown.markdown(text)

    # 2단계: 허용 태그 목록 정의
    allowed_tags: List[str] = [
        "p", "strong", "em", "ul", "ol", "li", "br",
        "blockquote", "code", "pre", "a", "h1", "h2", "h3"
    ]

    # 3단계: 허용 속성 정의 (링크만 허용)
    allowed_attributes = {
        "a": ["href", "title"]
    }

    # 4단계: bleach로 HTML 필터링 (스크립트 태그 제거 등)
    cleaned_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True  # 허용되지 않은 태그는 아예 제거
    )

    # 5단계: Django가 HTML로 인식하도록 mark_safe 처리
    return mark_safe(cleaned_html)
