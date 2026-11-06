from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, messaging
import os
import json

cred_json = os.environ.get('FIREBASE_CREDENTIALS')
if cred_json:
    cred_dict = json.loads(cred_json)
    cred = credentials.Certificate(cred_dict)
else:
    cred_path = os.path.join(os.path.dirname(__file__), 'service-account.json')
    cred = credentials.Certificate(cred_path)

firebase_admin.initialize_app(cred)

app = FastAPI(title="SAMAKE-RESTO API")

class NotificationRequest(BaseModel):
    token: str
    titre: str
    corps: str
    data: dict = {}

@app.get("/")
def read_root():
    return {"status": "ok", "service": "SAMAKE-RESTO API"}

@app.post("/send-notification")
def send_notification(req: NotificationRequest):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=req.titre,
                body=req.corps,
            ),
            data=req.data,
            token=req.token,
        )
        response = messaging.send(message)
        return {"success": True, "message_id": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
