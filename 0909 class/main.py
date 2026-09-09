from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_sale: bool = False


users = {
    1: "Rosa",
    2: "John",
    3: "Jane"
}

students = {
    1: "Rosa",
    2: "John",
    3: "Jane"
}

app =  FastAPI()


@app.get("/")
async def root():
    return {"message": "하이 world~"}

#http://127.0.0.1:8000/hello
@app.get("/hello")
def read_root():
    return {"Hello": "World"}

#http://127.0.0.1:8000/items/              #폐쇄망이면 로컬 호스트 붙잡아서 해야함 (postman/swagger 공부)
@app.post("/items/")
async def create_item(item: Item):
    return {
        "message": "상품이 등록되었습니다", 
        "받은_데이터": item,
    }

#http://127.0.0.1:8000/users/2
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    print(users)


    if user_id not in users:
        return {"message": "User not found"}

    del users[user_id]

    return {"message": f"User {user_id} deleted"}

@app.put("/students/{student_id}")
def update_student(student_id: int, name: str):

    if student_id not in students:
        return {"message": "Student not found"}

    students[student_id] = name

    return {
        "message": "Student updated successfully",
        "student_id": student_id,
        "name": name
    }