from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
import csv


# --------------------------------
# FastAPI 서버 생성
# --------------------------------

app = FastAPI()


# --------------------------------
# Pydantic Schema
# --------------------------------

class PassengerSchema(BaseModel):
    PassengerId: int
    Pclass: int
    Name: str
    Sex: str
    Age: float | None = None
    SibSp: int
    Parch: int
    Ticket: str
    Fare: float
    Cabin: str | None = None
    Embarked: str | None = None


# --------------------------------
# JSON Database
# --------------------------------

class JSONDatabase:

    def __init__(self, filename: str):
        self.filename = filename

        # data.json이 없으면 새로 생성
        if not os.path.exists(self.filename):
            self.save({
                "passengers": {}
            })

    def load(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, data):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )


# 데이터베이스 생성
db = JSONDatabase("data.json")


# --------------------------------
# CSV → JSON 변환
# --------------------------------

def csv_to_json(csv_filename: str):

    data = db.load()

    # 이미 승객 데이터가 있으면 다시 넣지 않음
    if len(data["passengers"]) > 0:
        return

    # CSV 파일 열기
    with open(
        csv_filename,
        "r",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            passenger_id = int(row["PassengerId"])

            passenger = {
                "PassengerId": passenger_id,
                "Pclass": int(row["Pclass"]),
                "Name": row["Name"],
                "Sex": row["Sex"],

                # Age가 비어있는 경우 None
                "Age": (
                    float(row["Age"])
                    if row["Age"] != ""
                    else None
                ),

                "SibSp": int(row["SibSp"]),
                "Parch": int(row["Parch"]),
                "Ticket": row["Ticket"],
                "Fare": float(row["Fare"]) if row["Fare"] else 0.0,

                # Cabin이 비어있는 경우 None
                "Cabin": (
                    row["Cabin"]
                    if row["Cabin"] != ""
                    else None
                ),

                # Embarked가 비어있는 경우 None
                "Embarked": (
                    row["Embarked"]
                    if row["Embarked"] != ""
                    else None
                )
            }

            # PassengerId를 key로 저장
            data["passengers"][str(passenger_id)] = passenger

    # JSON 파일 저장
    db.save(data)


# --------------------------------
# CSV 파일을 JSON으로 변환
# --------------------------------

csv_to_json("titanic.csv")


# --------------------------------
# 기본 페이지
# --------------------------------

@app.get("/")
def home():

    return {
        "message": "타이타닉 승객 정보 API 서버입니다."
    }


# ================================================
# PASSENGER CRUD
# ================================================


# --------------------------------
# 승객 생성
# --------------------------------

@app.post("/passengers/{passenger_id}")
def create_passenger(
    passenger_id: int,
    passenger: PassengerSchema
):

    data = db.load()

    # 이미 존재하는 PassengerId인지 확인
    if str(passenger_id) in data["passengers"]:

        raise HTTPException(
            status_code=400,
            detail="이미 존재하는 PassengerId입니다."
        )

    # 데이터 저장
    data["passengers"][str(passenger_id)] = passenger.model_dump()

    db.save(data)

    return {
        "message": "Passenger created",
        "PassengerId": passenger_id,
        "passenger": passenger
    }


# --------------------------------
# 모든 승객 조회
# --------------------------------

@app.get("/passengers")
def get_all_passengers():

    data = db.load()

    return {
        "passengers": data["passengers"]
    }


# --------------------------------
# 특정 승객 조회
# --------------------------------

@app.get("/passengers/{passenger_id}")
def get_passenger(passenger_id: int):

    data = db.load()

    # 승객이 존재하지 않는 경우
    if str(passenger_id) not in data["passengers"]:

        raise HTTPException(
            status_code=404,
            detail="Passenger not found"
        )

    return data["passengers"][str(passenger_id)]


# --------------------------------
# 승객 정보 수정
# --------------------------------

@app.put("/passengers/{passenger_id}")
def update_passenger(
    passenger_id: int,
    passenger: PassengerSchema
):

    data = db.load()

    # 승객이 존재하지 않는 경우
    if str(passenger_id) not in data["passengers"]:

        raise HTTPException(
            status_code=404,
            detail="Passenger not found"
        )

    # 데이터 수정
    data["passengers"][str(passenger_id)] = passenger.model_dump()

    db.save(data)

    return {
        "message": "Passenger updated",
        "passenger": passenger
    }


# --------------------------------
# 승객 삭제
# --------------------------------

@app.delete("/passengers/{passenger_id}")
def delete_passenger(passenger_id: int):

    data = db.load()

    # 승객이 존재하지 않는 경우
    if str(passenger_id) not in data["passengers"]:

        raise HTTPException(
            status_code=404,
            detail="Passenger not found"
        )

    # 승객 삭제
    del data["passengers"][str(passenger_id)]

    db.save(data)

    return {
        "message": "Passenger deleted",
        "PassengerId": passenger_id
    }