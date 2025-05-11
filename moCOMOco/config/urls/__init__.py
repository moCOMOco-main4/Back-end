import os

# 기본적으로 개발 환경 URL 사용
from .urls_base import *

# 환경 변수에 따라 배포 환경 URL 사용
if os.environ.get("DJANGO_SETTINGS_MODULE") == "config.settings.prod":
    from .urls_prod import *
