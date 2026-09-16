from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# 데이터 형식
class ItemSchema(BaseModel):
    name: str
    price: int


# 임시 데이터
items = {
    1: ItemSchema(name="사과", price=1000),
    2: ItemSchema(name="바나나", price=2000)
}


@app.get("/")
def home():
    return {"message": "FastAPI server is running"}

# CREATE - 생성
@app.post("/items/{item_id}")
def create_item(item_id: int, item: ItemSchema):
    items[item_id] = item

    return {
        "message": "Item created",
        "item": item
    }

# READ - 조회(전체) #스스로 추가한 코드
@app.get("/items/")
def get_all_items():
    return {
        "message": "전체 목록 조회 완료", 
        "items": items
    }


# READ - 조회(단일)
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        return {"message": "Item not found"}

    return items[item_id]


# UPDATE - 수정
@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemSchema):
    if item_id not in items:
        return {"message": "Item not found"}

    items[item_id] = item

    return {
        "message": "Item updated",
        "item": item
    }


# DELETE - 삭제
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        return {"message": "Item not found"}

    del items[item_id]

    return {
        "message": "Item deleted"
    }