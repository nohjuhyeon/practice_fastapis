from typing import Optional, List

from beanie import Document, Link
# from pydantic import BaseModel, EmailStr

# 개발자 실수로 들어가는 field 제한
class User(Document): # 상속을 위한 것
    name: Optional[str] = None
    email: Optional[str] = None

    pswd: Optional[str] = None
    manager: Optional[str] = None
    sellist1 : Optional[str] = None
    text : Optional[str] = None
  
    class Settings:
        name = "users" # collection의 이름
  
  # beanie는 mongoDB를 비동기적으로 다루기 위한 라이브러리
      