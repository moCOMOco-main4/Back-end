# moCOMOco

## 프로젝트 소개
[개발하는 사람들끼리 모여서 프로젝트 진행하는 모임]

## 개발 환경 설정

### 사전 요구사항
- Python 3.13
- Poetry
- PostgreSQL

### 가상환경 및 의존성 설치
1. Poetry 설치
```bash
curl -sSL https://install.python-poetry.org | python3 -

가상환경 생성 및 활성화

bashpoetry env use 3.13
poetry shell

의존성 설치

bashpoetry install
데이터베이스 설정

PostgreSQL 설치 및 데이터베이스 생성

bashcreatedb django_db

.env 파일 생성


.env.example 파일을 복사하여 실제 값으로 수정

마이그레이션 및 서버 실행
bashpython manage.py makemigrations
python manage.py migrate
python manage.py runserver
개발 가이드라인

Black을 사용한 코드 포맷팅
Isort를 사용한 import 정렬
pytest를 사용한 테스트

CI/CD

GitHub Actions를 통한 자동 테스트 및 코드 품질 검사

탐장:김우중
[팀원 이름 및 역할]
팀원1:송희태
팀원2:이준호
팀원3:조수민

라이선스
[django,python,git,git hub,postagesql,sqlite3,aws]
=======
# MOCOMOCO/backend_project
>>>>>>> 3bd72c25393269372095372aeb1b2930027d19fc
