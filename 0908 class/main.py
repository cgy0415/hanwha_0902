#First steps
from fastapi import FastAPI

#FastAPI "instance"생성
app = FastAPI()

#경로 설정
#https://example.com/items/foo에서 경로는 /items/foo임

#API 만들때 특정 HTTP method 사용해서 specific action 함
# POST: to create data.
# GET: to read data.
# PUT: to update data.
# DELETE: to delete data.
# OpenAPI에서는 각각의 HTTP method를 operation이라고 함 

#defining path operation decorator
@app.get("/")
#defining path operation fuction 
async def root():
    return {"message": "Hello World"}

##async는 비동기함수인데 제3의 라이브러리를 사용하는데 await을 사용하라고 할떄 async def 를 사용할 수 있고 await은 async def 안쪽에만 사용할 수 있음
# @app.get('/')
# async def read_results():
#     results = await some_library()
#     return results

##제3자 라이브러리가 DB, API, 파일 시스템 등과 같은 대상과 통신하면서도 await을 지원하지 않는다면 그냥 def 이용하면 됨
# @app.get('/')
# def results():
#     results = some_library()
#     return results

#경로 매개변수
from fastapi import FastAPI

app = FastAPI()


@app.get("/users/me") #순서가 중요하기 떄문에 me 먼저와야됨
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

#Enum: 경로 매개변수를 받는 경로 작업이 있는데 유효한 경로 매개변수값을 미리 정의하고 싶을떄
from enum import Enum

from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

#쿼리 매개변수: 경로 매개변수의 일부가 아닌 다른 함수 매개변수를 선언하면 해당 매개변수는 자동으로 "쿼리" 매개변수로 해석
from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

#http://127.0.0.1:8000/items/?skip=0&limit=10에서 쿼리 매개변수는 
# skip: with a value of 0
# limit: with a value of 10