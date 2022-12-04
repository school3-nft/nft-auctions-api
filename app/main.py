from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.ledger import accounts, transactions
from . import schemas


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
    account_info = await accounts.generate_ledger_account()
    return account_info


@app.get('/account-data')
async def account_data(seed: str, sequence: int):
    data = await accounts.get_ledger_account_data(seed=seed, sequence=sequence)
    return data


@app.post('/transfer-xrpl')
async def transfer_xrpl(transfer: schemas.XrplTransfer):
    response = await transactions.transfer_xrpl(
        source_seed=transfer.source_seed, source_sequence=transfer.source_sequence,
        destination_address=transfer.destination_address, value=transfer.value
    )
    return response
    