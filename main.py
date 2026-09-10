from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import os


app = FastAPI()


# =========================
# 1. Pydantic 데이터 모델
# =========================

class UserSchema(BaseModel):
    name: str
    age: int
    gender: str


class ItemSchema(BaseModel):
    name: str
    characteristic: str


# =========================
# 2. JSON DB 관리 클래스
# =========================

class JSONDatabase:

    def __init__(self, filename: str):
        self.filename = filename

        # 파일이 없으면 처음 생성
        if not os.path.exists(self.filename):
            self.save({
                "users": {},
                "items": {}
            })


    # JSON 파일 읽기
    def load(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            return json.load(file)


    # JSON 파일 저장
    def save(self, data):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )


# DB 객체 생성
db = JSONDatabase("data.json")


# =========================
# 3. HOME
# =========================

@app.get("/")
def home():
    return {
        "message": "출석부 API 서버입니다."
    }


# ============================================
# USER CRUD
# ============================================


# CREATE - User 생성
@app.post("/users/{user_id}")
def create_user(user_id: int, user: UserSchema):

    data = db.load()

    if str(user_id) in data["users"]:
        raise HTTPException(
            status_code=400,
            detail="이미 존재하는 user_id입니다."
        )

    data["users"][str(user_id)] = user.model_dump()

    db.save(data)

    return {
        "message": "User created",
        "user_id": user_id,
        "user": user
    }


# READ - User 전체 조회
@app.get("/users")
def get_all_users():

    data = db.load()

    return {
        "users": data["users"]
    }


# READ - User 한 명 조회
@app.get("/users/{user_id}")
def get_user(user_id: int):

    data = db.load()

    if str(user_id) not in data["users"]:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return data["users"][str(user_id)]


# UPDATE - User 수정
@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserSchema):

    data = db.load()

    if str(user_id) not in data["users"]:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    data["users"][str(user_id)] = user.model_dump()

    db.save(data)

    return {
        "message": "User updated",
        "user": user
    }


# DELETE - User 삭제
@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    data = db.load()

    if str(user_id) not in data["users"]:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    del data["users"][str(user_id)]

    db.save(data)

    return {
        "message": "User deleted"
    }


# ============================================
# ITEM CRUD
# ============================================


# CREATE - Item 생성
@app.post("/items/{item_id}")
def create_item(item_id: int, item: ItemSchema):

    data = db.load()

    if str(item_id) in data["items"]:
        raise HTTPException(
            status_code=400,
            detail="이미 존재하는 item_id입니다."
        )

    data["items"][str(item_id)] = item.model_dump()

    db.save(data)

    return {
        "message": "Item created",
        "item_id": item_id,
        "item": item
    }


# READ - Item 전체 조회
@app.get("/items")
def get_all_items():

    data = db.load()

    return {
        "items": data["items"]
    }


# READ - Item 하나 조회
@app.get("/items/{item_id}")
def get_item(item_id: int):

    data = db.load()

    if str(item_id) not in data["items"]:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return data["items"][str(item_id)]


# UPDATE - Item 수정
@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemSchema):

    data = db.load()

    if str(item_id) not in data["items"]:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    data["items"][str(item_id)] = item.model_dump()

    db.save(data)

    return {
        "message": "Item updated",
        "item": item
    }


# DELETE - Item 삭제
@app.delete("/items/{item_id}")
def delete_item(item_id: int):

    data = db.load()

    if str(item_id) not in data["items"]:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    del data["items"][str(item_id)]

    db.save(data)

    return {
        "message": "Item deleted"
    }