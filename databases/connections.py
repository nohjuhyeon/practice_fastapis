from typing import Any, List, Optional
from beanie import init_beanie, PydanticObjectId
from models.users import User
from motor.motor_asyncio import AsyncIOMotorClient # 데이터 베이스에 연결하는데 사용
from pydantic_settings import BaseSettings 
# basesetting 사용하기 위해서는 pydantic_setting이 필요

# 비니는 몽고디비에 연결하기 위한 패키지를 연결해놓음

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    # DATABASE_URL = "mongodb:/     /localhost:27017/toy_fastapis" 원래 이게 있었음
    # 실제로 github에 올릴 때는 해킹의 위험성이 있기 때문에 .env의 형식으로 변경
    # mongoclient와 database의 의미를 같이 가지게 됨
    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(),
                          document_models=[User]) #model에 있는 user
        # 요기에 collection들을 넣으면 됨 어떤 collection을 관리할 것인지
        
    class Config:
        env_file = ".env"

class Database : # 이건 우리가 만든거란다
    #model 은 collection 사실 이해못함 좀 알아봐야할듯 이런 젠장ㅠ
    def __init__(self, model) -> None:
        self.model = model
        pass

    # 전체 리스트
    async def get_all(self) :
        documents = await self.model.find_all().to_list() # = find({})
        pass
        return documents
    
    # 상세보기
    async def get(self, id: PydanticObjectId) -> Any:   #pydanticObjectID가 뭐락ㅎ....?
        doc = await self.model.get(id) # = find_one()
        if doc:
            return doc
        return False
    
    # 저장하기
    async def save(self, document) -> None:
        await document.create()
        return None
