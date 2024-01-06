from typing import Any, List, Optional
from beanie import init_beanie, PydanticObjectId
from models.users import User
from motor.motor_asyncio import AsyncIOMotorClient # 데이터 베이스에 연결하는데 사용
from pydantic_settings import BaseSettings 
# basesetting 사용하기 위해서는 pydantic_setting이 필요

# 비니는 몽고디비에 연결하기 위한 패키지를 연결해놓음

class Settings(BaseSettings):                                                       # 환경 설정을 관리하는 용도                                  
    DATABASE_URL: Optional[str] = None                                              
    # DATABASE_URL = "mongodb:/     /localhost:27017/toy_fastapis" 원래 이게 있었음
    # 실제로 github에 올릴 때는 해킹의 위험성이 있기 때문에 .env의 형식으로 변경
    # mongoclient와 database의 의미를 같이 가지게 됨
    async def initialize_database(self):                                            # 데이터베이스를 초기화하는 작업을 수행하는 함수 정의
        client = AsyncIOMotorClient(self.DATABASE_URL)                              # AsyncIOMotorClient(self.DATABASE_URL): 비동기적으로 mongoDB 데이터베이스에 연결하고 상호작용할 수 있도록 도와줌
        await init_beanie(database=client.get_default_database(),                   # init_beanie(): 데이터베이스의 초기화 작업을 수행 # client.default_database() : 기본 데이터베이스에 연결 # documents_models=[] : 해당하는 문서 모델 초기화
                          document_models=[User]) #model에 있는 user
        # 요기에 collection들을 넣으면 됨 어떤 collection을 관리할 것인지
        
    class Config:
        env_file = ".env"                                                       # database_url이 none으로 설정되어 있는 경우 .env 파일에 설정된 database_url 값으로 데이터베이스가 연결됨

class Database : # 이건 우리가 만든거란다
    #model 은 collection 사실 이해못함 좀 알아봐야할듯 이런 젠장ㅠ
    def __init__(self, model) -> None:
        self.model = model
        pass

    # 전체 리스트
    async def get_all(self) :
        documents = await self.model.find_all().to_list() # = find({})              # 모든 데이터를 리스트의 형태로 가져옴
        pass
        return documents
    
    # 상세보기
    async def get(self, id: PydanticObjectId) -> Any:   # pydantic 라이브러리에서 제공하는 데이터 유효성 검사를 위한 특별한 타입, 이 타입은 MongoDB의 ObjectId 값을 표현하고 유효성을 검사하는데 사용됨
        doc = await self.model.get(id)                  # = find_one()          # id가 동일한 데이터베이스의 데이터를 가져올 때 사용
        if doc:                                             # 만약 문서가 존재하면 값을 가져오고 아닐 경우 False를 반환
            return doc
        return False
    
    # 저장하기
    async def save(self, document) -> None:
        await document.create()
        return None
