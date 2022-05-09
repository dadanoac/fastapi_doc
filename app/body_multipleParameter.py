from typing import Optional
from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    
class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):        #Item과 User 두개의 Pydantic model을 사용하는 body parameter를 선언했다.
    results = {"item_id": item_id, "item": item, "user": user}
    return results

@app.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Item, user: User, importance: int = Body(...)   # 경로 및 쿼리 매개변수와 마찬가지로 Body를 통해 singular value data에 대해 validation을 할 수 있다.
):                                                                      # Body함수를 사용하지 않으면 쿼리매개변수로 인식한다.
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results