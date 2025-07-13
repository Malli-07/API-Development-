from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

BASE_URL = "https://kpa.suvidhaen.com"

class LoginRequest(BaseModel):
    phone: str
    password: str

class FormSubmitRequest(BaseModel):
    token: str
    form_data: dict

@app.post("/api/login")
def login(data: LoginRequest):
    url = f"{BASE_URL}/auth/login"
    payload = {"phone": data.phone, "password": data.password}

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/form-submit")
def submit_form(data: FormSubmitRequest):
    url = f"{BASE_URL}/form/submit"
    headers = {"Authorization": f"Bearer {data.token}"}

    try:
        response = requests.post(url, json=data.form_data, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
