from xrpl.models import transactions, requests, amounts, currencies
from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.asyncio import transaction
from xrpl.wallet import Wallet
from xrpl.utils.str_conversions import str_to_hex, hex_to_str
from xrpl.utils import xrp_to_drops


JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"

async def mint_nft(
    seed: str, sequence: int, uri: str, transfer_fee: int
    ) -> dict:
    client =  AsyncJsonRpcClient(JSON_RPC_URL)
    wallet = Wallet(seed=seed, sequence=sequence)
    tx_mint_nft = transactions.NFTokenMint(
        account=wallet.classic_address,
        uri=str_to_hex(uri),
        flags=8,
        transfer_fee=transfer_fee,
        nftoken_taxon=0,
        sequence=sequence,
        fee="10"
    )

    tx_mint_signed = await transaction.safe_sign_and_submit_transaction(
        tx_mint_nft, wallet, client)

    res_data = tx_mint_signed.to_dict()
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
    seller_seed: str, seller_sequence: int,
    buyer_seed: str, buyer_sequence: int,
    nftoken_id: str, amount: int
    ) -> dict:
    client = AsyncJsonRpcClient(JSON_RPC_URL)
    seller_wallet = Wallet(seed=seller_seed, sequence=seller_sequence)
    buyer_wallet = Wallet(seed=buyer_seed, sequence=buyer_sequence)
    tx_create_sell_offer = transactions.NFTokenCreateOffer(
        account=seller_wallet.classic_address,
        flags=0x00000001,
        nftoken_id=nftoken_id,
        amount=xrp_to_drops(amount),
        destination=buyer_wallet.classic_address
    )
    tx_create_buy_offer = transactions.NFTokenCreateOffer(
        account=buyer_wallet.classic_address,
        nftoken_id=nftoken_id,
        amount=xrp_to_drops(amount),
        owner=seller_wallet.classic_address
    )
    sell_tx_res = await transaction.safe_sign_and_submit_transaction(
        tx_create_sell_offer, seller_wallet, client)
    buy_tx_res = await transaction.safe_sign_and_submit_transaction(
        tx_create_buy_offer, buyer_wallet, client)

    offers_req = requests.NFTBuyOffers(
        nft_id=nftoken_id
    )
    offers_res = await client.request(offers_req)

    tx_seller_accept_offer = transactions.NFTokenAcceptOffer(
        account=seller_wallet.classic_address,
        nftoken_buy_offer=offers_res.to_dict()['result']['offers'][0]['nft_offer_index']
    )
    tx_buyer_accept_offer = transactions.NFTokenAcceptOffer(
        account=buyer_wallet.classic_address,
        nftoken_sell_offer=offers_res.to_dict()['result']['offers'][0]['nft_offer_index']
    )
    seller_accept_res = await transaction.safe_sign_and_submit_transaction(
        tx_seller_accept_offer, seller_wallet, client)
    buyer_accept_res = await transaction.safe_sign_and_submit_transaction(
        tx_buyer_accept_offer, buyer_wallet, client)

    response = {
        'status': buyer_accept_res.to_dict()['status'],
    }

    return response
