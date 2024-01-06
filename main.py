from fastapi import FastAPI               # FastAPI의 역할 : 자동으로 API 문서를 생성하고, swagger UI나 ReDoc과 같은 도구를 통해 시각적으로 확인할 수 있게 도와줌
app = FastAPI()

from databases.connections import Settings

settings = Settings()
@app.on_event("startup")
async def init_db():
    await settings.initialize_database()

from routes.gadgets import router as event_router                   # 경로에 따라 다른 핸들러 함수가 실행되어야 할 경우, 제대로 동작하지 않을 수 있기 때문에 router의 변수 이름을 변경해줘야 함 
from routes.positionings import router as second_router
from routes.users import router as users_router
from routes.homes import router as home_router

app.include_router(event_router, prefix="/gadget")
app.include_router(second_router, prefix="/positioning")
app.include_router(users_router, prefix="/users")
app.include_router(home_router, prefix="/home")

from fastapi import Request                                 # Request : client가 보내는 요청에 포함된 다양한 정보를 서버에서 처리하기 위해 사용 / Request에 포함된 정보: 헤더(인증 토큰이나 클라이언트의 사용자 에이전트 정보 등이 포함), 바디(클라이언트가 요청에 함께 전송한 데이터를 확인, 주로 POST 또는 PUT 요청에서 사용, JSON, 폼 데이터 등의 형식으로 데이터 전송), 경로(경로 매개변수를 통해 동적인 경로 처리가 가능), 쿼리 매개변수(URL 뒤에 ?를 통해 전달되며, 필요한 매개변수로 데이터를 전달할 수 있음)
from fastapi.templating import Jinja2Templates              # Jinja2 Templates: FastAPI에서 HTML 템플릿을 사용하여 동적인 웹 페이지를 생성하는 데 사용되는 도구

from fastapi.middleware.cors import CORSMiddleware              #cors : 웹 애플리케이션에서 다른 도메인의 리소스에 접근할 수 있는 권한을 부여하기 위한 정책
# No 'Access-Control-Allow-Origin'                              # cors 미들웨어를 사용하여 다른 도메인 간의 데이터 교환을 허용함으로써 웹 애플리케이션 간의 통신을 가능하게 할 수 있음
# CORS 설정
app.add_middleware(
    CORSMiddleware,             # "*"를 사용하였기 때문에 모든 오리진, 메서드, 헤더를 허용
    allow_origins=["*"],  # 실제 운영 환경에서는 접근 가능한 도메인만 허용하는 것이 좋습니다.
    allow_methods=["*"],
    allow_headers=["*"],
)

# Jinja2Templates 사용 단계
# 1. HTML 템플릿 파일 작성
# 2. Jinja2Templates 객체 생성
# 3. 템플릿 렌더링
# 4. 클라이언트에게 응답 전송

# html 들이 있는 폴더 위치              
templates = Jinja2Templates(directory="templates/")    # 2. Jinja2Templates 객체 생성

@app.get("/")                       # / 경로로 GET 요청이 들어왔을 때 실행 # 첫화면에 get을 사용하는 이유는 사용자에게 어떤 내용을 가져오거나 표시해야 할 때 사용하기 때문
async def root(Request:Request):
    return templates.TemplateResponse("main.html",{'request':Request})

# @app.get("/") : 루트 경로에 대한 GET 요청을 처리하는 핸들러 함수를 등록하는데 사용되는 데코레이터
# async def root(Request:Request): : Request 객체(클라이언트의 요청 정보를 담고 있는 FastAPI의 내장 클래스)를 매개변수로 받는 핸들러 함수
# return templates.TemplateResponse("main.html",{'request':Request}) main.html 파일을 템플릿 파일로 로드하고 렌더링/ 'request'라는 변수에 Request 객체를 전달하여 템플릿에서 해당 객체의 정보를 사용할 수 있도록 함 / {} 안에는 템플릿에 전달할 변수들을 지정

@app.post("/")                      # / 경로로 POST 요청이 들어왔을 때 실행
async def root(Request:Request):
    return templates.TemplateResponse("main.html",{'request':Request})
