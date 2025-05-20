# moCOMOco

## 📌 프로젝트 소개

> **모코모코**는 개발자들이 \*\*모각코( 모여서 각자 코딩 )\*\*을 함께 할 수 있도록 도움을 줄 수 있는 모임 기반 컨텐츠 서비스입니다.
>
> 사용자들이 자유롭게 모각코 모임을 생성하거나 참여할 수 있고,
> 모임별 게시글, 채팅 기능, 모임 장소 정보 공유를 통해 실제 만남과 협업이 원하드로운 구성으로 조정되었습니다.

---
## 🔗 배포 링크

> ### [  moCOMOco ](https://mocomoco.store)

---

## 🚀 주요 기능

* 🔐 **JWT 기본 사용자 인증 시스템 구성**
  회원가입, 로그인, 로그아웃, 회원탈퇴 기능 구현

* 📄 **게시판 기능 구현**
  게시글 작성, 수정, 삭제, 댓글 기능, 게시글 통계 및 자동 태그 분류 기능 구현

* 📆 **일정 기능 개발**
  신청/승인 기반의 일정 등록 및 관리 시스템 구성 ( 게임 기본 시나리오 포함 )

* 💬 **채팅 기능 구현**
  Django Channels + WebSocket 기반 실시간 1:1 채팅 구현 및 알림 시스템 구성

* ⚙️ **CI/CD 파이프라인 자동화**
  GitHub Actions 통한 테스트 및 배포 자동화

* ☁️ **서버 구성 및 운영 환경**
  AWS EC2, S3, RDS 기반 인프라 환경 구성 및 모니터링 체계 확답

---

## 🛠️ 기술 스택

<table>
  <tr>
    <td><img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" width="40"/></td>
    <td><img src="https://static.djangoproject.com/img/logos/django-logo-negative.svg" width="60"/></td>
    <td><img src="https://www.postgresql.org/media/img/about/press/elephant.png" width="40"/></td>
    <td><img src="https://raw.githubusercontent.com/encode/uvicorn/master/docs/uvicorn.png" width="60"/></td>
    <td><img src="https://cdn.iconscout.com/icon/free/png-256/nginx-3-1174926.png" width="60"/></td>
    <td><img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="40"/></td>
    <td><img src="https://a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_1200x630.png" width="80"/></td>
    <td><img src="https://cdn-icons-png.flaticon.com/512/919/919836.png" width="40"/></td>
    <td><img src="https://cdn.icon-icons.com/icons2/2699/PNG/512/gunicorn_logo_icon_171025.png" width="60"/></td>
  </tr>
</table>

| 🧱 분류   | 🪰 기술 내용                                                                              |
| ------- | -------------------------------------------          |
| 언어      | `Python`                                    |
| 웹 프레임워크 | `Django`, `Django REST Framework`           |
| 데이터베이스  | `PostgreSQL`, `SQLite ( 개발용 )`              |
| 비동기 처리  | `Django Channels`, `Uvicorn`, `WebSocket`   |
| 메시지 브로커 | `Redis`                                     |
| 인증/보안   | `JWT`, `OAuth2`                             |
| 배포/인프라  | `AWS EC2`, `S3`, `RDS`, `Gunicorn`, `Nginx` |
| 테스트/문서화 | `GitHub Actions`, `Postman`                 |



---

## 시스템 아키텍처

![architecture diagram](https://github.com/user-attachments/assets/de155d73-3673-450c-9947-c71160f12728)


---

## 팀 구성 및 역할


| 이름       | 역할 |
|------------|------|
| **송희태** | 사용자 인증 시스템(회원가입, 로그인, 로그아웃, 회원탈퇴),<br>소셜 로그인(카카오, 네이버),<br>사용자 정보 관리 기능, 프로필 이미지 업로드 기능,<br>회원 차단 기능 및 검색 시스템 구현 |
| **김우중** | 게시판 기능(Post) 구현,<br>게시글 작성, 수정, 삭제 기능 및 댓글 유효성 검증,<br>일정 자동 생성(Django signals),<br>게시글 통계, 주차 기능 및 캘린더 자동 생성 |
| **이준호** | 채팅 메시지 시스템 및 알림 API 개발,<br>게임 기반 일정 시스템 연동,<br>회원 조회 및 목록 처리 API 개발 |
| **조수민** | AWS EC2 인스턴스 설정 및 서비스 배포,<br>Gunicorn + Uvicorn + Nginx 서버 환경 구성,<br>PostgreSQL, Redis 환경 세팅 및 관리,<br>GitHub Actions 통한 CI/CD 자동화 파이프라인 구현 |
| **백엔드 4팀** | 초기 세팅 구성 |
| **최승일 멘토님** | 서버 설정 및 환경 구성, 에러 대응 등 기술 지원 |

---

## 프로젝트 구조
```
Back-end/
├── README.md
├── moCOMOco
│ ├── apps
│ │ ├── app_users
│ │ ├── chat
│ │ ├── notifications
│ │ └── posts
│ ├── config
│ ├── db.sqlite3
│ ├── manage.py
│ └── .env
├── poetry.lock
└── pyproject.toml
```

## 부록

- [API 명세서](https://docs.google.com/spreadsheets/d/1F6xNcYVO3vJ38lsJw_J3GF30JE0AERvMfNzOfwWoeyE/edit?gid=1565530336#gid=1565530336)
- [ERD](https://www.erdcloud.com/d/LAzPDR6vwpJzNSWBR)
- [테이블 명세서](https://docs.google.com/spreadsheets/d/1_dZHSUO7f2W8TbmoRWCSNq3oXzqNW03tCdp4vUhwu4w/edit?gid=0#gid=0)
- [사용자 요구사항 정의서](https://docs.google.com/spreadsheets/d/10pRKf7R6h8pqu2bZXpOhcKV4o6SFsKuUjfmEoLp117A/edit?gid=300631716#gid=300631716)
