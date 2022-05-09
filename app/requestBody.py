# client에서 API로 데이터를 보낼때는 request body로 보낸다.
# API에서 client로 데이터를 보낼 때는 respond body로 보낸다.
# API는 거의 항상 response body를 보내야 하지만, client는 항상 request body로 보낼 필요는 없다.
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

# pydantic의 BaseModel을 상속받아 data model을 선언할 수 있다.
# query 매개변수와 마찬가지로 기본값을 가지고 있거나 None으로 선언된 경우, 그 변수는 optional이 된다.
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    
app = FastAPI()

# 필요에 따라 request body, path/query parameter를 동시에 선언할 수도 있다.
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict