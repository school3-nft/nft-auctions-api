from xrpl.models import transactions, requests, amounts, currencies
from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.asyncio import transaction
from xrpl.wallet import Wallet
from xrpl.utils.str_conversions import str_to_hex, hex_to_str
from xrpl.utils import xrp_to_drops

import asyncio


JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"

async def mint_nft(
    seed: str, sequence: int, uri: str, transfer_fee: int
    ) -> dict:
    client = AsyncJsonRpcClient(JSON_RPC_URL)
    wallet = Wallet(seed=seed, sequence=sequence)
    tx_mint_nft = transactions.NFTokenMint(
        account=wallet.classic_address,
        uri=str_to_hex(uri),
        flags=8,
        transfer_fee=transfer_fee,
        nftoken_taxon=0,
        sequence=sequence,
        fee="0"
    )
    tx_res = await transaction.safe_sign_and_submit_transaction(
        tx_mint_nft, wallet, client)
    res_data = tx_res.to_dict()
    response = {
        'status': res_data['status'],
        'fee': res_data['result']['tx_json']['Fee'],
        'uri': hex_to_str(res_data['result']['tx_json']['URI']),
        'hash': res_data['result']['tx_json']['hash'],
    }
    return response


async def get_nfts(seed: str, sequence: int) -> dict:
    client = AsyncJsonRpcClient(JSON_RPC_URL)
    wallet = Wallet(seed=seed, sequence=sequence)
    req = requests.AccountNFTs(
        account=wallet.classic_address
    )
    res = await client.request(req)
    response = {
        'account_nfts': res.to_dict()['result']['account_nfts']
    }
    return response


async def transfer_nft(
    seed: str, sequence: int, owner: str,
    nftoken_id: str, amount: int
    ) -> dict:
    client = AsyncJsonRpcClient(JSON_RPC_URL)
    wallet = Wallet(seed=seed, sequence=sequence)
    tx_create_offer = transactions.NFTokenCreateOffer(
        account=wallet.classic_address,
        nftoken_id=nftoken_id,
        amount=xrp_to_drops(amount),
        owner=owner
    )
    tx_res = await transaction.safe_sign_and_submit_transaction(
        tx_create_offer, wallet, client)

    buy_offers = requests.NFTBuyOffers(
        nft_id=nftoken_id
    )

    tx_accept_offer = transactions.NFTokenAcceptOffer(
        account=owner,
        nftoken_buy_offer=""
    )
    return buy_offers


if __name__=="__main__":
    nfts = asyncio.run(mint_nft("sEdTKSzXHhRAJBTogYJ6brHkWjL6Ria", 33501756, "https://ipfs.io/ipfs/QmbWqxBEKC3P8tqsKc98xmWNzrzDtRLMiMPL8wBuTGsMnR", 5000))
    print(nfts)
    #res = asyncio.run(get_nfts("sEdTKSzXHhRAJBTogYJ6brHkWjL6Ria", 33501756))
    #print(res)
