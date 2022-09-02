import datetime

from fastapi import FastAPI, Path, Query, HTTPException, status
from datetime import date
from pydantic import BaseModel, validator

from typing import Optional

from mangum import Mangum

app = FastAPI()

clients = {
    1: {
           "name": "Torrie Wilson",
           "dob": date(1985, 2, 5),
           "loan_amount": 50,
           },
    12355500002: {
        "name": "Steve Austin",
        "dob": date(1985, 2, 5),
        "loan_amount": 50,
         },
    2393: {
        "name": "Bret Hitman Hart",
        "dob": date(1985, 2, 5),
        "loan_amount": 50,
         },
    }


@app.get("/")
def home():
    welcome = 'Welcome to the BANK API! Please use the following API endpoints: /about | /get-all-clients | /get-client/{client_id} | /get-by-name?name={client_full_name}'
    return welcome


@app.get("/about")
def about():
    return f"Welcome to my bank, let me know how can i help you"


@app.get("/get-all-clients")
def get_all_clients():
    return clients


@app.get("/get-client/{client_id}")
def get_client(client_id: int = Path(None, description="Client's ID", gt=0)):
    if client_id not in clients:
        raise HTTPException(status_code=466, detail="Client with such ID does not exist!")
    else:
        return clients[client_id]


@app.get("/get-by-name")
def get_client(name: str = None):
    for i in clients:
        if clients[i]["name"] == name:
            return clients[i]
    # return {"Data": "Hey Russ, Can't Find Anything"}
    # Or you can raise Exception for Pythonic way:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No customer with such name in our bank")


class Client(BaseModel):
    name: Optional[str] = "First and Last Name"
    dob: Optional[datetime.date]
    loan_amount: Optional[int] = "Between 1 and 100"

    @validator('loan_amount')
    def loan_validation(amount):
        assert amount > 0 and amount < 101, 'Loan must be between 1 and 100'
        return amount

    @validator('dob')
    def age_validation(dob):
        # Get today's date object
        today = date.today()

        # A bool that represents if today's day/month precedes the birth day/month
        one_or_zero = ((today.month, today.day) < (dob.month, dob.day))

        # Calculate the difference in years from the date object's components
        year_difference = today.year - dob.year

        # The difference in years is not enough.
        # To get it right, subtract 1 or 0 based on if today precedes the
        # birthdate's month/day.

        # To do this, subtract the 'one_or_zero' boolean
        # from 'year_difference'. (This converts
        # True to 1 and False to 0 under the hood.)
        age = year_difference - one_or_zero

        assert age >= 16 and age <= 90, f'Your age is {age} years old and does not comply with our bank policy'
        return dob


@app.post("/create-client/{client_id}")
def create_client(client_id: int, client: Client):
    if client_id in clients:
        return {"Error": "Item ID already exists"}
    clients[client_id] = {"name": client.name, "dob": client.dob, "loan_amount": client.loan_amount}
    return clients[client_id]


@app.put("/update-client/{client_id}")
def update_client(client_id: int, client: Client):
    if client_id not in clients:
        return {"Error": "This client does not exist!"}

    clients[client_id].update(client)
    return clients[client_id]


@app.delete("/delete-client")
def delete_client(client_id: int = Query(..., description="The ID to delete", gt=0)):
    if client_id not in clients:
        return {"Error": "Client DOES NOT exists"}

    del clients[client_id]
    return {"Success": "Client has been deleted"}


handler = Mangum(app)
