# 2022-05-07
## starlette
    Starlette는 다른 파이썬 웹 프레임워크, 예를 들면 Sanic, Flask, Django 등과 비교하면 가볍고 강력한 ASGI(Asynchronous Server Gateway Interface) 프레임워크/툴킷이다. 한편 fastapi는 Starlette를 한번 감싸기 때문에 Stalette를 직접 사용하는 것보다는 성능이 떨어질 수밖에 없다. 하지만 개발 속도를 폭증시켜주는 등 fastapi의 장점은 이 모든 것을 상쇄시킬 수 있다. 

## Pydantic
    pydantic은 타입 애너테이션을 사용해서 데이터를 검증하고 설정들을 관리하는 라이브러리이다. pydantic은 런타임 환경에서 타입을 강제하고 타입이 유효하지 않을 때 에러를 발생시켜준다. FastAPI, Project Jupyter, Microsoft, AWS 등 많은 곳에서 사용된다.

## async/wait
    result - 아래와 같이 await과 함께 호출해야 하는 third party library를 사용할 때에는 
``` python
await some_library()
```
    아래와 같이 경로매개변수 함수를 async def로 선언해야 한다.
``` python
@app.get('/')
    async def read_results():
        results = await some_library()
        return results
```
    하지만 await을 지원하지 않는 third party library와 communication할 때에는 await으로 선언하지 않는다.
``` python
@app.get('/')
    def results():
        results = some_library()
        return results
```
    아무것과도 communication하지 않으면 aync def를 사용한다.  
    그냥 잘 모르겠으면 def를 사용한다.  
    자세히는 차후에 따로 스터디를 하는 것으로..

## 경로매개변수
    url의 경로를 통해 변수를 받음 
``` python 
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
```
## 쿼리매개변수

## Body

# 2022-05-09
## Body-Fields
앞선 내용에서 path, query 매개변수와 body에선 각각 Path, Query, Body를 통해 값을 validation 및 metadata를 입력했다.   
이와 마찬가지로 pydantic model은 Field를 통해 값을 validation 및 metadata를 입력한다.
``` python
from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
```
Field는 fastapi가 아닌 pydanctic에서 import한다.  
Field도 Query, Path, Body와 같이 동작하며, 같은 parameter를 가진다.  
원래 두개 이상의 body parameter를 사용해야 JSON에 key가 표시되는데,  
Body에서 embed=True로 하면 single body parameter라도 JSON에 key와 함께 표시된다.

# Body - Nested Models
fastapi에서는 pydantic을 통해 중첩모델을 사용할 수 있다.
``` python
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: list = []


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```
비어있는 리스트 형식의 변수 tags를 추가하였다.  
typing 모듈의 List를 import하면
``` python
tags: List[str] = [] 
```
형식으로 리스트의 타입을 선언할 수 있다.  
마찬가지로 Set에도 적용할 수 있다.
``` python
tags: Set[str] = set()
```
아래와 같이 pydantic model에서 submodel을 type으로 사용할 수도 있다.(image)
url을 str type대신 HttpUrl로 선언하면, url에 대한 validation을 하고 JSON schema /OpenAPI에서 문서화된다.
``` python
from typing import Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []
    image: Optional[Image] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

혹은 타입을 submodel들의 List로 선언할 수도 있다.
``` python
images: Optionl[List[Image]] = None
```

body parameter를 dict로 선언할 수도 있다. 유효한 필드/속성 이름이 무엇인지 미리 알 필요가 없으므로(Pydantic 모델의 경우처럼) 아직 모르는 키를 수신하려는 경우에 유용하다.
``` python
from typing import Dict

from fastapi import FastAPI

app = FastAPI()


@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights
```