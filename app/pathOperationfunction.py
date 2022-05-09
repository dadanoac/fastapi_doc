from enum import Enum
from fastapi import FastAPI, Path, Query

app = FastAPI()

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    return {"item_id:":item_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName = Path(..., title="The name of item")):   # Path도 query 매개변수와 동일하게 매개변수를 선언할 수 있음
    if model_name == ModelName.alexnet:                                             # 경로 매개변수는 무조건 필수임. ...로 필수임을 나타내는게 좋지만, 
        return {"model_name": model_name, "message" : "Deep Learing FTW"}           # None이나 기본값을 지정하더라도 영향을 끼치지 않으고 항상 필수임
    if model_name.value == "renet":
        return {"model_name": model_name, "message" : "is lenet"}                   
    
    return {"model_name": model_name, "message" : "is resnet"}

@app.get("/files/{file_path:path}")
async def read_file(file_path:str):
    return {"file_path": file_path}

