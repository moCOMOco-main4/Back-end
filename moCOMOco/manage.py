"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드 (manage.py 기준 상위 디렉토리 위치)
load_dotenv(Path(__file__).resolve().parent / ".env")

def main():
    """Run administrative tasks."""
    env = os.getenv("DJANGO_ENV", "dev")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{env}")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()