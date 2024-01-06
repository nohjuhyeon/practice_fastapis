from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

'''
from pymongo import MongoClient
# connect mongodb -> 접속 자원에 대한 class 입력
# mongoclient = MongoClient('mongodb://localhost:27017')
mongoclient = MongoClient('mongodb://localhost:27017')
# database 연결
db_local = mongoclient["toy_fastapis"]
# collection 작업
collection = db_local['users']
'''


router = APIRouter()

templates = Jinja2Templates(directory="templates/")

# 회원 가입 form    /users/form
@router.post("/form", response_class=HTMLResponse) # 펑션 호출 방식
async def insert(request:Request):
    await request.form()
    print(dict(await request.form()))
    return templates.TemplateResponse(name="users/inserts.html"
                                      , context={'request':request
                                                 ,'first':5, 'second':6})

@router.get("/form", response_class=HTMLResponse) # 펑션 호출 방식
async def insert(request:Request):
    print(dict(request._query_params))
    return templates.TemplateResponse(name="users/inserts.html"
                                      ,context={'request':request,'first':5, 'second':6})

@router.post("/login", response_class=HTMLResponse) # 펑션 호출 방식
async def insert(request:Request):
    form_data = await request.form()
    dict_form_data = dict(form_data)
    print(dict(await request.form()))
    return templates.TemplateResponse(name="users/login.html"
                                      , context={'request':request
                                                 , 'form_data' : dict_form_data })

@router.get("/login", response_class=HTMLResponse) # 펑션 호출 방식
async def login_get(request:Request):
    print(dict(request._query_params))
    return templates.TemplateResponse(name="users/login.html", context={'request':request})

# 회원 가입 /users/insert -> users/login.html
@router.get("/insert") # 펑션 호출 방식
async def insert_get(request:Request):
    print(dict(request._query_params)) # get에만 query_parpam 이 동작함. 왜?
    return templates.TemplateResponse(name="users/login.html", context={'request':request})

@router.post("/insert") # 펑션 호출 방식
async def insert_post(request:Request):
    user_dict = dict(await request.form())
    print(user_dict)

    # 저장
    user = User(**user_dict)   #여기 부분 왜 필요핟러ㅏ. model 폴더에 있는 user이긴 함. 변수 유저가 나온다고 함.
    await collection_user.save(user)

    #리스트 정보
    user_list = await collection_user.get_all()
    return templates.TemplateResponse(name="users/list_jinja.html"
                                      , context={'request':request
                                                 ,'users' : user_list})

# 회원 리스트 /users/list -> users/list.html
@router.post("/list") # 펑션 호출 방식
async def list_post(request:Request):
    await request.form()
    print(dict(await request.form()))
    return templates.TemplateResponse(name="users/list.html", context={'request':request})

from databases.connections import Database

from models.users import User # 컬랙션을 연결하고, 컬렉션에 저장/불러오기 하는 방법 

collection_user = Database(User)

@router.get("/list") # 펑션 호출 방식
async def list(request:Request):
    print(dict(request._query_params))
    user_list = await collection_user.get_all()
    return templates.TemplateResponse(name="users/list_jinja.html"
                                      , context={'request':request
                                                 , 'users' :user_list})   

from beanie import PydanticObjectId

# 회원 상세정보 /users/read -> users/reads.html
# Path parameters : /users/read/id or /users/read/uniqe_name
@router.get("/read/{object_id}") # 펑션 호출 방식
async def reads(request:Request, object_id:PydanticObjectId):
    print(dict(request._query_params))
    user = await collection_user.get(object_id)
    return templates.TemplateResponse(name="users/reads.html"
                                      , context={'request':request
                                                 ,'user':user})


@router.post("/read/{object_id}") # 펑션 호출 방식
async def reads(request:Request, object_id:PydanticObjectId):
    await request.form()
    print(dict(await request.form()))
    user = await collection_user.get(object_id)

    return templates.TemplateResponse(name="users/reads.html", context={'request':request,'user':user})

# form_datas = await request.form()
    # dict(form_datas)

'''
[GET 방식에서 딕셔너리 형식으로 파라미터를 뽑아오는 과정]
    request._query_params
    # QueryParams('name=jisu&email=ohjisu320%40gmail.com')
    request._query_params._dict
    # {'name': 'jisu', 'email': 'ohjisu320@gmail.com'}
    dict(request._query_params)
    # {'name': 'jisu', 'email': 'ohjisu320@gmail.com'}
[POST 방식에서 딕셔너리 형식으로 formdata를 뽑아오는 과정]
    request._query_params
    # post 방식은 parameter에 정보를 불러오지 않기에 작동되지 않음
    # QueryParams('')
    await request.form()
    # FormData([('name', 'jisu'), ('email', 'ohjisu320@gmail.com')])
    dict(await request.form())
    # {'name': 'jisu', 'email': 'ohjisu320@gmail.com'}
'''

'''
get or post (입력 유무)
- get : 입력 X, 값을 넘겨야 된다면 path param 
- post : 입력 O, query params
'''