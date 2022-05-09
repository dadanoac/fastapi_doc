from typing import Optional, List
from fastapi import FastAPI, Query


app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, { "item_name": "Bar"}, {"item_name": "Baz"}]
@app.get("/items/")                                                 # def에서 경로매개변수가 아닌 다른 매개변수를 선언하면 쿼리매개변수로 자동 해석
async def read_item(skip: int=0, limit: Optional[int] = None):      # http://127.0.0.1:8000/items/?skip=0&limit=10 형식의 url을 갖는다
    return fake_items_db[skip : skip + limit]                       # limit = None이므로 선택적이라는 것을 표시. Optional은 Fastapi에서 
                                                                    # 사용되지는 않지만 편집기에서 오류를 찾아낼 수 있게 도와줌
                                                                    # 반대로 쿼리매개변수의 기본값 혹은 None을 입력하지 않으면 필수입력변수가 됨
#여러 경로/쿼리 매개변수를 선언할 수도 있음
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = Query(None, min_length=3, max_length=50), short: bool = False    # 쿼리 매개변수에 명시적으로 Query를 입력해 줄 수도 있음.
):                                                                                                                  # Query를 사용할 경우 변수에 대한 validation을 할 수 있음. 
    item = {"item_id": item_id, "owner_id": user_id}                                                                # regex="^fixedquery$"와 같이 정규표현식도 사용 가능.
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            item.update(
                {"description:": "This is an amazing item that has a long description"}
            )
        )
    return item

# Query를 사용할 때에는 쿼리매개변수를 필수로 하기 위해선 None 대신 ...을 입력한다. 혹은 그자리에 기본값을 선언할 수도 있다.
@app.get("/items/")
async def read_items(q: str = Query(..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# 쿼리매개변수에서 list를 입력받을 수도 있다.
# url은 http://localhost:8000/users/?q=foo&q=bar 의 형식을 갖는다.
# 쿼리매개변수에서 list를 사용할 때에는 Query를 사용해야 한다. 그러지않으면 request body로 인식한다.
@app.get("/users/")
async def read_users(
    q: Optional[List[str]] = Query(
        None,                                               # Query(["foo", "bar"])와 같이 기본값을 선언할 수도 있다.
        title="Query string",                               # title, description 혹은 alias를 선언할 수 있다.
        description="Qeury string description",             
        alias="item-query",                                 # alias를 사용하면 url에서 http://127.0.0.1:8000/users/?item-query=foo&item-query=bar 의 형식으로 사용할 수 있다.
        deprecated=True)):                                  # 더이상 사용하고 싶지 않은 변수가 있지만, 클라이언트가 아직 사용중 이기에 아직은 그대로 둬야할 때, 
    query_users = {"q": q}                                  # deprecated=True로 하면 doc에서 명시적으로 deprecated로 표시된다.
    return query_users                                      # 혹은 include_in_schema=False로 선언하여 OpenAPI schema와 doc에서 제외할 수도 있다.