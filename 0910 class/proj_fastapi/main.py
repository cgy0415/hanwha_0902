from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserSchema(BaseModel):
    name: str
    age: int


@app.post("/predict")
def predict(user: UserSchema):

    return {
        "result_message": f"{user.name}님의 나이는 {user.age}살입니다."
    }