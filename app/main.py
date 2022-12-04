from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.ledger.accounts import generate_ledger_account


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def hello():
    return {'msg': 'Hello!'}


@app.get('/create-user')
async def create_user():
    account_info = await generate_ledger_account()
    return account_info
