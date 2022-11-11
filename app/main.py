from fastapi import FastAPI

from .ledger import generate_ledger_account


app = FastAPI()

@app.get('/')
async def hello():
    return {'msg': 'Hello!'}


@app.get('/create-user')
async def create_user():
    account_info = await generate_ledger_account()
    return account_info
