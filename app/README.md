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

## Body - Nested Models
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

# 2022-05-11
## Declare Request Example Data
앱에서 받을 수 있는 데이터의 예를 선언한다?
방법이 몇가지 있다.
1. Pydantic의 Chema_extra 이용  
``` python
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }
```
선언된 extra info는 Json schema에 추가되어 API doc에 사용된다.  
2. Field arguments 이용
``` python
class Item(BaseModel):
    name: str = Field(..., example="Foo")
    description: Optional[str] = Field(None, example="A very nice Item")
    price: float = Field(..., example=35.4)
    tax: Optional[float] = Field(None, example=3.2)
```
 
extra arguments는 오직 문서용으로, validation을 거치지 않는다.  
3. example and examples in OpenAPI
example과 examples는 Path(), Query(), Header(), Cookie(), Body(), Form()그리고 File()에 사용 가능하다.
``` python
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        ...,
        example={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results
```
## Extra Data Types
현재까지 아래 데이터 타입들을 사용해왔다.
- int
- float
- str
- bool
하지만 더욱 복잡한 데이터들을 사용할 수 있으며, 그것들도 마찬가지로 동일한 기능들을 사용할 수 있다.
- 에디터 서포트
- Request를 의한 Data conversion
- response data를 위한 Data conversion 
- Data validation.
- Automatic annotation and documentation.
추가 데이터 타입들은 다음과 같다.
- UUID
  - 표준 "Universally Unique Identifier", 수많은 데이터베이스와 시스템에서 ID로 사용된다.
  - request와 response에서 str로 표현된다.
- datetime.datetime
  - 파이썬의 datetime.datetime.
  - request와 response에서 ISO 8601 포맷의 str로 표시된다.(예, 2008-09-15T15:53:00+05:00)
- datetime.date
  - 파이썬의 datetime.date
  - request와 response에서 ISO 8601 포맷의 str로 표시된다.(예, 2008-09-15)
- datetime.time
  - 파이썬의 datetime.time
  - request와 response에서 ISO 8601 포맷의 str로 표시된다.(예, 15:53:00.003)
- datetime.timedelta
  - 파이썬의 datetime.timedelta
  - request와 response에서 총 seconds의 float으로 표시된다.
  - pydantic 또한 "ISO 8601 diff encoding"으로 표시하는것을 허용한다.
- frozenset
  - requeset와 reponse에서 set으로 표시된다.
    - request에서는 list로 읽은 후, 반복을 제거하여 set으로 converting 한다.
    - reponse에서는 set이 list로 converting된다.
    - 생산된 schema에서 set value는 unique하다고 기술한다(JSON schema의 uniqueItems)
- bytes
  - 파이썬의 bytes
  - request와 response에서 str로 다뤄진다.
  - 생성된 schema에선 binary "format"의 str임을 기술한다.
- Decimal 
  - 파이썬의 Decimal
  - request와 response에서 float과 같게 다뤄진다.  
pydantic data types은 여기서 볼 수 있다.[Pydantic data types](https://pydantic-docs.helpmanual.io/usage/types/).   

# 22-05-14
## Cokie Parameter
Query나 Path 파라미터를 선언하는 것과 같은 방법으로 Cookie 파라미터를 선언할 수 있다.
``` python
from typing import Union

from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: Union[str, None] = Cookie(default=None)):
    return {"ads_id": ads_id}
```
Cookie는 Path와 Query의 자매변수이다. 같은 Param class로부터 상속을 받는다.
cookie 파라미터를 선언할때, Cookie를 사용하지 않으면 query로 해석한다.

## 헤더 매개변수
``` python
rom typing import Optional

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Optional[str] = Header(default=None)):
    return {"User-Agent": user_agent}
```
Header또한 Path, Query 및 Cookie와 마찬가지로 Param클래스로부터 상속받음  
대부분의 표주 ㄴ헤더는 '-'로 구분된다. 하지만 python에서 '-'가 유효하지 않으므로, Header는 '_'에서 '-'로 변환하여 추출하고 기록한다.
또한 HTTP 헤더는 대소문자를 구분하지 않으므로 'snake_case'로 선언할 수 있다.

``` python
from typing import List, Optional

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(x_token: Optional[List[str]] = Header(default=None)):
    return {"X-Token values": x_token}
```
중복 헤더를 받을 수 있다. 중복헤더는 리스트 형태로 값을 수신한다.

## Response Model
모든 경로 작업에서 response_model 매개변수를 사용하여 응답에 사용되는 모델을 선언할 수 있다.
- @app.get()
- @app.post()
- @app.put()
- @app.delete()
- etc.

``` python
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []


@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
```

응답 모델은 함수 반환 유형 주석 대신 이 매개변수에서 선언된다. 경로 함수는 실제로 해당 응답 모델을 반환하지 않고 dict, 데이터베이스 객체 또는 기타 모델을 반환한 다음 response_model을 사용하여 필드의 제한 및 직렬화를 수행하기 때문이다.
``` python
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user
```
이런 방식으로 response_model의 type을 선언하여 데이터를 필터링 할 수 있다. 
