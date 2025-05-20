# moCOMOco

## 📌 Project Introduction

> **모코모코**는 개발자들이 \*\*모각코( 모여서 각자 코딩 )\*\*을 함께 할 수 있도록 도움을 줄 수 있는 모임 기반 컨텐츠 서비스입니다.
>
> 사용자들이 자유롭게 모각코 모임을 생성하거나 참여할 수 있고,
> 모임별 게시글, 채팅 기능, 모임 장소 정보 공유를 통해 실제 만남과 협업이 원하드로운 구성으로 조정되었습니다.

---
## 🔗 Deployment Link

> ### [  moCOMOco ](https://mocomoco.store)

---

## 🚀 Key Features


* 🔐 **OAuth2 기반 소셜 로그인 + JWT 인증 시스템**
  자체 회원가입 없이 **카카오, 네이버 소셜 로그인만 지원**하며,
  로그인 후에는 JWT 토큰을 활용한 인증 처리 (로그인, 로그아웃, 회원탈퇴)

* 📄 **게시판 기능 구현**
  게시글 작성, 수정, 삭제 기능 제공

* 📆 **일정 기능 개발**
  신청/승인 방식의 일정 등록 및 관리 시스템 구현

* 💬 **실시간 채팅 기능**
  Django Channels + WebSocket 기반 1:1 실시간 채팅 및 알림 시스템 구성

* ⚙️ **CI/CD 파이프라인 자동화**
  GitHub Actions를 활용한 테스트 및 배포 자동화 구성

* ☁️ **서버 인프라 구성 및 운영**
  AWS EC2, S3, RDS 기반 인프라 환경 구성 및 모니터링 체계 구축


---

## 🛠️ Tech Stack

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

## System Architecture

![architecture diagram](https://github.com/user-attachments/assets/de155d73-3673-450c-9947-c71160f12728)


---

## Team & Roles
<table>
    <tbody>
        <tr>
            <td>
                <a href="https://github.com/WOOJOUNG-KIM">
                    <img src="https://avatars.githubusercontent.com/WOOJOUNG-KIM" width="100" height="100"/>
                </a>  
            </td>
            <td>
                <a href="https://github.com/Alex424525">
                    <img src="https://avatars.githubusercontent.com/Alex424525" width="100" height="100"/>
                </a>  
            </td>
            <td>
                <a href="https://github.com/JunHo-L">
                    <img src="https://avatars.githubusercontent.com/JunHo-L" width="100" height="100"/>
                </a>  
            </td>
            <td>
                <a href="https://github.com/workface">
                    <img src="https://avatars.githubusercontent.com/workface" width="100" height="100"/>
                </a>  
            </td>
        </tr>
        <tr>
            <th>
                <a href="https://github.com/seonysun">김우중</a>
            </th>
            <th>
                <a href="https://github.com/Gu-Sul">송희태</a>
            </th>
            <th>
                <a href="https://github.com/neuliii">이준호</a>
            </th>
            <th>
                <a href="https://github.com/namul21">조수민</a>
            </th>
        </tr>
        <tr>
            <th>
                BackEnd
            </th>
            <th>
                BackEnd
            </th>
            <th>
                BackEnd
            </th>
            <th>
                BackEnd
            </th>
        </tr>
    </tbody>


| 이름           | 역할 설명                                                                                                                                   |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| **송희태**      | 사용자 인증 시스템 (로그인, 로그아웃, 회원탈퇴)<br>소설 로그인 (카카오, 네이버)<br>사용자 정보 관리, 프로필 이미지 업로드 기능<br>회원 차단 및 검색 시스템 구현                                     |
| **김우중**      | 게시판 기능 (Post) 구현<br>게시물 작성, 수정, 삭제 및 댓글 유향성 검증<br>일정 자동 생성 (Django signals)<br>게시물 통계, 주차 및 캔리더 자동 생성                                   |
| **이준호**      | 채팅 메시지 시스템 및 알람 API 개발<br>게임 기반 일정 시스템 연동<br>회원 조회 및 목록 API 개발                                                                          |
| **조수민**      | AWS EC2 인스턴스 설정 및 서비스 배포<br>Gunicorn + Uvicorn + Nginx 서버 환경 구성<br>PostgreSQL, Redis 환경 설정 및 관리<br>GitHub Actions 통한 CI/CD 자동화 파이프라인 구현 |
| **백엔드 4팀**   | 프로젝트 초기 세팅 구성                                                                                                                           |
| **최승일 멘토님** | 주 1회 코드 리뷰와 에러 해결을 도와주셔서,<br>프로젝트 초기 세팅부터 사소한 부분까지 검토해주시고,<br>특정 상황에서 발생하는 에러에 관해서는 해결 방법을 제시해주어 자발적으로 해결할 수 있도록 도움                    |


---

## Project Structure
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

## Appendices
- [API 명세서](https://docs.google.com/spreadsheets/d/1F6xNcYVO3vJ38lsJw_J3GF30JE0AERvMfNzOfwWoeyE/edit?gid=1565530336#gid=1565530336)
- [ERD](https://www.erdcloud.com/d/LAzPDR6vwpJzNSWBR)
- [테이블 명세서](https://docs.google.com/spreadsheets/d/1_dZHSUO7f2W8TbmoRWCSNq3oXzqNW03tCdp4vUhwu4w/edit?gid=0#gid=0)
- [사용자 요구사항 정의서](https://docs.google.com/spreadsheets/d/10pRKf7R6h8pqu2bZXpOhcKV4o6SFsKuUjfmEoLp117A/edit?gid=300631716#gid=300631716)
