# moCOMOco



## Table of Contents

1. [📌 Project Introduction](#project-introduction)
2. [🔗 Deployment Link](#deployment-link)
3. [🚀 Key Features](#key-features)
   - [🔐 OAuth2 기반 소셜 로그인 + JWT 인증 시스템](#oauth2-기반-소셜-로그인--jwt-인증-시스템)
   - [📄 게시판 기능 구현](#게시판-기능-구현)
   - [📆 일정 기능 개발](#일정-기능-개발)
   - [💬 실시간 채팅 기능](#실시간-채팅-기능)
   - [⚙️ CI/CD 파이프라인 자동화](#cicd-파이프라인-자동화)
   - [☁️ 서버 인프라 구성 및 운영](#서버-인프라-구성-및-운영)
4. [🛠️ Tech Stack](#tech-stack)
5. [👥 Team & Roles](#team--roles)
6. [🐞 Troubleshooting](#troubleshooting)
7. [📂 Project Structure](#project-structure)
8. [📑 Appendices](#appendices)
   - [📋 API 명세서](#api-명세서)
   - [🗺️ ERD](#erd)
   - [📊 테이블 명세서](#테이블-명세서)
   - [✍️ 사용자 요구사항 정의서](#사용자-요구사항-정의서)

---
<a id="project-introduction"></a>
## 📌 Project Introduction

> **모코모코**는 개발자들이 \*\*모각코( 모여서 각자 코딩 )\*\*을 함께 할 수 있도록 도움을 줄 수 있는 모임 기반 컨텐츠 서비스입니다.
>
> 사용자들이 자유롭게 모각코 모임을 생성하거나 참여할 수 있고,
> 모임별 게시글, 채팅 기능, 모임 장소 정보 공유를 통해 실제 만남과 협업이 원하드로운 구성으로 조정되었습니다.

---

<a id="deployment-link"></a>
## 🔗 Deployment Link

> ### [  moCOMOco ](https://mocomoco.store)

---

<a id="key-features"></a>
## 🚀 Key Features

  <a id="oauth2-기반-소셜-로그인--jwt-인증-시스템"></a>
* 🔐 **OAuth2 기반 소셜 로그인 + JWT 인증 시스템**
  자체 회원가입 없이 **카카오, 네이버 소셜 로그인만 지원**하며,
  로그인 후에는 JWT 토큰을 활용한 인증 처리 (로그인, 로그아웃, 회원탈퇴)

  <a id="게시판-기능-구현"></a>
* 📄 **게시판 기능 구현**
  게시글 작성, 수정, 삭제 기능 제공

  <a id="일정-기능-개발"></a>
* 📆 **일정 기능 개발**
  신청/승인 방식의 일정 등록 및 관리 시스템 구현

  <a id="실시간-채팅-기능"></a>
* 💬 **실시간 채팅 기능**
  Django Channels + WebSocket 기반 1:1 실시간 채팅 및 알림 시스템 구성

  <a id="cicd-파이프라인-자동화"></a>
* ⚙️ **CI/CD 파이프라인 자동화**
  GitHub Actions를 활용한 테스트 및 배포 자동화 구성

  <a id="서버-인프라-구성-및-운영"></a>
* ☁️ **서버 인프라 구성 및 운영**
  AWS EC2, S3, RDS 기반 인프라 환경 구성 및 모니터링 체계 구축


---

<a id="tech-stack"></a>
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


<a id="team--roles"></a>
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
| **송희태**      | 사용자 인증 시스템 (로그인, 로그아웃, 회원탈퇴)<br>소설 로그인 (카카오, 네이버)<br>사용자 정보 관리<br>프로필 이미지 업로드 기능<br>사용자 포지션 관리 시스템                                    |
| **김우중**      | 게시판 기능 (Post) 구현<br>지원서 신청 , 취소 및 역할 기반 유효성 검증<br>일정 등록 , 수정 , 삭제 기능 및 기본 일정 자동 생성<br>즐겨찾기(좋아요) 기능<br>모집 마감 자동화 (django signals)<br>마크다운 렌더링 및 보안 필터링 처리<br>모집글 참여자 , 진행 상태 동적 계산 및 응답 설계                                   |
| **이준호**      | 실시간 채팅 기능 구현<br>채팅 메시지/채팅방 API 개발<br>채팅 기반 알림 시스템 연동<br>알림 조회 및 읽음 처리 API 개발                                                                       |
| **조수민**      | 백엔드 서버 구축<br>AWS EC2 인스턴스 설정 및 서비스 배포<br>Gunicorn + Uvicorn + Nginx 서버 환경 구성<br>PostgreSQL, Redis 환경 설정 및 관리<br>GitHub Actions 통한 CI/CD 자동화 파이프라인 구현<br>팀원개발 이슈 대응 및 오류 해결 지원 |
| **백엔드 4팀**   | 프로젝트 초기 세팅 구성                                                                                                                           |
| **최승일 멘토님** | 주 1회 코드 리뷰와 에러 해결을 도와주셔서,<br>프로젝트 초기 세팅부터 사소한 부분까지 검토해주시고,<br>특정 상황에서 발생하는 에러에 관해서는 해결 방법을 제시해주어 자발적으로 해결할 수 있도록 도움                    |


---

<a id="troubleshooting"></a>
## 🐞 Trouble Shooting

<details>
<summary>👤 김우중 – 모임 마감 처리 및 보안 이슈</summary>

❌ **문제**

모집글 자동 마감 기능 구현 중, 신청 인원이 꽉 찼는데도 `is_closed`가 `True`로 즉시 반영되지 않는 현상 발생.

🔍 **원인 분석**

* Django `post_save` signal 처리 시점과 `.count()`를 사용하는 queryset 평가 지연(lazy evaluation)이 충돌함.
* `Application.objects.filter(...).count()`가 최신 상태 반영 전에 평가되어 현재 인원 < 최대 인원으로 잘못 계산됨.

✅ **해결 방법**

* DB에서 `.count()` 평가 시점을 신청 저장 후로 명확히 고정.
* Queryset을 미리 평가하지 않도록 하고, signal 내에서 `.count()` 호출 전에 정확한 순서로 DB 접근 로직 수정.

✅ **추가 보안 조치**

* 게시판 Markdown 렌더링 중 XSS 이슈를 방지하기 위해 `bleach` 라이브러리를 도입하여 보안 필터링 처리.

</details>

<details>
<summary>👤 송희태 – 인증 및 배포 관련 이슈</summary>

✅ **카카오 로그인 문제**

❌ **문제**: 로그인 연결 실패

🔍 **원인**: Django admin의 도메인이 'example.com'으로 설정되어 있었고 Redirect\_URL과 환경 변수 설정 불일치

✅ **해결**: admin 설정 변경 및 환경 변수 수정으로 일치시킴

---

✅ **서버 배포 이슈**

❌ **문제**: 로컬에서는 작동하나 서버에서는 로그인 불가

🔍 **원인**: Nginx에서 CORS 헤더 덮어쓰기, AWS RDS 타임아웃

✅ **해결**: Nginx 설정 수정, DB 연결 최적화, 환경설정 파일을 prod 설정으로 변경

---

✅ **네이버 로그인 문제**

❌ **문제**: 400 에러 지속 발생

🔍 **원인**: 인가코드를 액세스 토큰으로 변환 과정에서 오류 발생

✅ **해결**: 네이버 개발 문서 정독 후 API 호출 방식 수정

---

✅ **회원 탈퇴 관련 알림 오류**

❌ **문제**: 사용자 탈퇴 시 알림 생성 과정에서 오류 발생

🔍 **원인**: 채팅방 participant 정보 삭제로 인한 참조 오류

✅ **해결**: 탈퇴 처리 순서 조정 및 participant 필드 NULL 허용

---

✅ **로그아웃 문제**

❌ **문제**: 401 에러 발생

🔍 **원인**: URL 패턴 순서 오류

✅ **해결**: URL 패턴 재배치

</details>

<details>
<summary>👤 이준호 – WebSocket 및 알림 오류</summary>

❌ **문제**

* WebSocket 연결 시 301 리디렉션과 500 오류 발생, 즉시 연결 종료
* 채팅 메시지 전송 시 일부 사용자에게 알림 미전달

🔍 **원인 분석**

* Nginx에서 `/ws` 경로에 잘못된 리디렉션 설정 적용
* WebSocket에서 JWT 인증 누락으로 `scope["user"]`가 익명 처리됨
* `NotificationService`에서 알림 수신자 필터 조건 누락

✅ **해결 방법**

* `/ws/` 경로에 정확한 WebSocket 프록시 설정 적용
* JWT 인증 미들웨어 추가 및 알림 수신자 필터링 로직 보완

</details>

<details>
<summary>👤 조수민 – 서버 인프라 및 WebSocket 배포 이슈</summary>

✅ **WebSocket 통신 실패**

❌ **문제**: WebSocket 요청이 Django로 도달하지 않음

🔍 **원인**: Nginx 설정에 `/ws/` 경로 누락 및 `Upgrade`, `Connection` 헤더 미설정

✅ **해결**: WebSocket 경로 별도 location 블록 추가 및 헤더 설정 후 nginx 재시작

```nginx
location /ws/ {
    proxy_pass http://127.0.0.1:8001;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "Upgrade";
    proxy_set_header Host $host;
    proxy_read_timeout 86400;
}
```

✅ **Gunicorn + Uvicorn 구성 문제**

❌ **문제**: Gunicorn에서 ASGI 처리를 제대로 못하는 현상 발생

🔍 **원인**: 일반 Gunicorn Worker 사용으로 WebSocket 연결 실패

✅ **해결**: `UvicornWorker`로 worker 클래스를 명시하여 Gunicorn이 ASGI 서버로 동작하도록 수정

```bash
gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker
```

✅ **개발 서버 가상환경 활성화 이슈**

❌ **문제**: CI/CD 파이프라인에서 `poetry install` 실행 시 가상환경이 활성화되지 않아 실행 오류 발생

🔍 **원인**: Ubuntu 기본 환경에서 poetry 바이너리 경로가 `$PATH`에 등록되지 않아 명령어 인식 실패

✅ **해결**: `.bashrc` 파일에 명시적으로 경로 추가 후 `source`로 적용하거나, GitHub Actions에서 환경변수 수동 지정

```bash
# ~/.bashrc 마지막 줄에 추가
export PATH="$HOME/.local/bin:$PATH"

# 적용
source ~/.bashrc
```

---
</details>

<a id="project-structure"></a>
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

<a id="appendices"></a>
## Appendices
- [API 명세서](https://docs.google.com/spreadsheets/d/1F6xNcYVO3vJ38lsJw_J3GF30JE0AERvMfNzOfwWoeyE/edit?gid=1565530336#gid=1565530336)
- [ERD](https://dbdiagram.io/d/67e5ea9e4f7afba18481a7c7)
- [테이블 명세서](https://docs.google.com/spreadsheets/d/1_dZHSUO7f2W8TbmoRWCSNq3oXzqNW03tCdp4vUhwu4w/edit?gid=0#gid=0)
- [사용자 요구사항 정의서](https://docs.google.com/spreadsheets/d/10pRKf7R6h8pqu2bZXpOhcKV4o6SFsKuUjfmEoLp117A/edit?gid=300631716#gid=300631716)
