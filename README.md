# moCOMOco

## 프로젝트 소개

> ** 모코모코**는 개발자들이 **모각코(모여서 각자 코딩)**를 함께 할 수 있도록 도와주는 모임 기반 커뮤니티 서비스입니다.
사용자들이 자유롭게 모각코 모임을 생성하거나 참여할 수 있고, 모임별 게시글, 채팅 기능, 모임 장소 정보 공유를 통해 실제 만남과 협업이 원활하게 이루어질 수 있도록 구성되어 있습니다.

## 주요 기능

* **JWT 기반 사용자 인증 시스템 구축**: 회원가입, 로그인, 로그아웃, 회원탈퇴 기능 구현
* **게시판 기능 구현**: 게시글 작성, 수정, 삭제, 댓글 기능, 게시글 통계 및 자동 태그 분류 기능 구현
* **일정 기능 개발**: 신청/승인 기반의 일정 등록 및 관리 시스템 구현 (게임 기반 시나리오 포함)
* **채팅 기능 구현**: Django Channels + WebSocket 기반 실시간 1:1 채팅 구현 및 알림 시스템 구축
* **CI/CD 파이프라인 자동화**: GitHub Actions 통한 테스트 및 배포 자동화
* **서버 구축 및 운영 환경**: AWS EC2, S3, RDS 기반 인프라 환경 구성 및 모니터링 체계 확보

---

## 기술 스택

| 분류      | 기술                                  |
| ------- | ----------------------------------- |
| 언어      | Python                              |
| 웹 프레임워크 | Django, Django REST Framework       |
| DB      | PostgreSQL, SQLite (개발용)            |
| 비동기 처리  | Django Channels, Uvicorn, WebSocket |
| 메시지 브로커 | Redis                               |
| 인증/보안   | JWT, OAuth2                         |
| 배포      | AWS EC2, S3, RDS, Nginx, Gunicorn   |
| 테스트/문서화 | GitHub Actions, Postman             |

---

## 시스템 아키텍처

![architecture diagram](https://github.com/user-attachments/assets/d5d7e9d1-54de-4c25-a1ec-4a2726a53cee)


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

![2025년 5월 21일 오전 12_58_53](https://github.com/user-attachments/assets/12b43c4e-712c-41d1-9ca3-40c8e7828b4b)


## 부록

- [API 명세서]([./docs/api-specification.md](https://docs.google.com/spreadsheets/d/1F6xNcYVO3vJ38lsJw_J3GF30JE0AERvMfNzOfwWoeyE/edit?gid=1565530336#gid=1565530336))
- [ERD](./docs/erd-diagram.png)
- [테이블 명세서]([./docs/table-definition.xlsx](https://docs.google.com/spreadsheets/d/1_dZHSUO7f2W8TbmoRWCSNq3oXzqNW03tCdp4vUhwu4w/edit?gid=0#gid=0))
- [사용자 요구사항 정의서]([./docs/user-requirements.md](https://docs.google.com/spreadsheets/d/10pRKf7R6h8pqu2bZXpOhcKV4o6SFsKuUjfmEoLp117A/edit?gid=300631716#gid=300631716))
