from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.ledger import accounts, transactions, tokens
from . import schemas


app = FastAPI(
    docs_url='/api/docs',
    root_path='/api/')

router = APIRouter(prefix='/api')

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


@router.get('/')
async def hello():
    return {'msg': 'Hello!'}


@router.get('/create-user')
async def create_user():
    account_info = await accounts.generate_ledger_account()
    return account_info


@router.get('/account-data')
async def account_data(seed: str, sequence: int):
    data = await accounts.get_ledger_account_data(seed=seed, sequence=sequence)
    return data


@router.get('/account-balance')
async def account_balance(seed: str, sequence: int):
    data = await accounts.get_ledger_account_data(seed=seed, sequence=sequence)
    return {
        'balance': data['account_balance']
    }


@router.get('/account-nfts')
async def account_nfts(seed: str, sequence: int):
    data = await tokens.get_nfts(seed=seed, sequence=sequence)
    return data


@router.post('/transfer-xrp')
async def transfer_xrpl(transfer: schemas.XrplTransfer):
    response = await transactions.transfer_xrpl(
        source_seed=transfer.source_seed, source_sequence=transfer.source_sequence,
        destination_address=transfer.destination_address, value=transfer.value
    )
    return response
    

@router.post('/mint-nft')
async def mint_nft(mint_data: schemas.NFTokenMintData):
    response = await tokens.mint_nft(
        seed=mint_data.seed, sequence=mint_data.sequence,
        uri=mint_data.uri, transfer_fee=mint_data.transfer_fee
    )
    return response


@router.post('/transfer-nft')
async def transfer_nft(transfer_data: schemas.NFTokenTransferData):
    response = await tokens.transfer_nft(
        seed=transfer_data.seed, sequence=transfer_data.sequence,
        nftoken_id=transfer_data.nftoken_id, amount=transfer_data.amount,
        owner=transfer_data.owner
    )
    return response

app.include_router(router)
