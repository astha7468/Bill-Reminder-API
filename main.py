from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

bills: list["Bill"] = []


class BillCreate(BaseModel):
    name: str
    amount: float
    due_date: date
    status: str


class Bill(BaseModel):
    id: int
    name: str
    amount: float
    due_date: date
    status: str


class BillUpdate(BaseModel):
    name: str
    amount: float
    due_date: date
    status: str


@app.get("/")
def home():
    return {"message": "Bill Reminder is running"}


@app.get("/bills")
def get_bills():
    return bills


@app.get("/bills/{bill_id}")
def get_bill(bill_id: int):
    for bill in bills:
        if bill.id == bill_id:
            return bill
    raise HTTPException(status_code=404, detail="Bill not found")


@app.post("/bills")
def add_bill(bill: BillCreate):
    new_bill = Bill(
        id=len(bills) + 1,
        name=bill.name,
        amount=bill.amount,
        due_date=bill.due_date,
        status=bill.status,
    )
    bills.append(new_bill)
    return new_bill 

@app.put("/bills/{bill_id}")
def update_bill(bill_id: int, updated_bill: BillUpdate):
    for bill in bills:
        if bill.id == bill_id:
            bill.name = updated_bill.name
            bill.amount = updated_bill.amount
            bill.due_date = updated_bill.due_date
            bill.status = updated_bill.status
            return bill

    raise HTTPException(status_code=404, detail="Bill not found")


@app.delete("/bills/{bill_id}")
def delete_bill(bill_id: int):
    for bill in bills:
        if bill.id == bill_id:
            bills.remove(bill)
            return {"message": "Bill deleted successfully"}

    raise HTTPException(status_code=404, detail="Bill not found")