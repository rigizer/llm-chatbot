# FastAPI 세팅

## Local 개발환경 세팅

### 상세 설명

- 권장 환경
  - OS: Windows 11 (x86) 이상
  - Python: 3.13 이상
  - RAM: 16GB 이상

### 가상환경 설정

- cd 명령어를 이용해 backend 디렉토리로 이동
- 가상환경 생성
  ```
  python -m venv .venv
  ```
  - 최초 1회만 진행
- 가상환경 활성화 (작업 전 진행)
  ```
  ./.venv/Scripts/activate
  ```
  - 터미널 맨 좌측에 초록색으로 `(.venv)`가 떠 있다면 가상환경 활성화 된 상태
  - `PSSecurityException` 오류 발생 시 해결 방법
    - Powershell을 `관리자 권한으로 실행`
    - 다음 명령어 입력
      ```
      Set-ExecutionPolicy Unrestricted
      ```
    - 실행 규칙 변경에 대한 안내가 뜨면 `a`를 입력 후 `엔터 키`
    - 이후 `Unrestricted`가 뜨면 Powershell 창 종료
    - VSCode 내의 터미널 또한 종료 후 재실행 해야하므로, VSCode 창도 모두 종료 후 재실행
  - VSCode 가상환경 활성화
    - VSCode 최상단 내의 검색창에 `> Python: 인터프리터 선택` 입력 후 엔터
      - 꺾쇠(`>`)까지 모두 입력해야 함
    - backend 디렉토리 내의 `.\.venv\Scripts\python.exe` 선택
    - 우측 하단에 `3.13.0 (.venv)`으로 설정되어 있는지 확인
      - 단, Python 버전 숫자는 다를 수 있음
- 패키지 목록 requirements에 저장
  ```
  pip freeze > requirements.txt
  ```
- 패키지 목록 일괄 설치
  ```
  pip install -r requirements.txt
  ```
- 가상환경 비활성화 (작업 후 진행)
  ```
  deactivate
  ```
- 사용 패키지 목록
  - `pip install fastapi`
  - `pip install "uvicorn[standard]"`

### 프로젝트 실행

- FastAPI 실행
  ```
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload
  ```
  - Chrome 웹 브라우저 혹은 `Postman`에 다음 주소 입력하여 API 확인 (GET 메소드)
  ```
  http://127.0.0.1:8000
  ```
- API Docs 확인
  ```
  http://127.0.0.1:8000/docs
  ```

## Deploy 배포환경 세팅

### dockerhub 프로젝트 등록 (최초 1회)

- [https://hub.docker.com/](https://hub.docker.com/) 사이트 접속
- Repositories 메뉴에서 `Create a repository` 버튼 클릭
- Repository Name 지정 (예: llm-chatbot)
- `Create` 버튼 클릭

### 프로젝트 빌드
- docker 로그인 (최초 1회)
  ```
  docker login -u (dockerhub 아이디)
  ```
  - 괄호까지 모두 제거 후 dockerhub 아이디 입력
  - `Password: `가 뜨면 dockerhub 비밀번호 입력
  - 비밀번호를 입력하는 과정은 화면에 뜨지 않으므로 그대로 비밀번호 입력 후 엔터
  - 로그인이 완료되면 맨 마지막에 `Login Succeeded`가 뜸

- docker 컨테이너 빌드
  - buildx 컨테이너 생성 (최초 1회)
  ```
  docker buildx create --use --name mybuilder
  ```
  - 멀티 플랫폼 타겟 빌드
  ```
  docker buildx build --platform linux/amd64,linux/arm64 -t rigizer/llm-chatbot:latest --push .
  ```
- docker 컨테이너 실행
  ```
  docker stop backend || true
  ```
  ```
  docker rm backend || true
  ```
  ```
  docker rmi rigizer/llm-chatbot:latest || true
  ```
  ```
  docker pull rigizer/llm-chatbot:latest
  ```
  ```
  docker run -d --restart always -e TZ=Asia/Seoul -p 8000:8000/tcp --name backend rigizer/llm-chatbot:latest
  ```
- docker 컨테이너 종료
  ```
  docker stop backend
  ```
- docker 컨테이너 삭제
  ```
  docker rm backend
  ```
- docker 이미지 삭제
  ```
  docker rmi backend
  ```