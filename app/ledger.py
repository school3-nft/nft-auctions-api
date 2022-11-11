from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.asyncio.wallet import generate_faucet_wallet
from xrpl.models.requests.account_info import AccountInfo


JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"

async def generate_ledger_account():
    client = AsyncJsonRpcClient(JSON_RPC_URL)
    wallet = await generate_faucet_wallet(client, debug=True)
    acct_info = AccountInfo(
        account=wallet.classic_address,
        ledger_index="validated",
        strict=True,
    )
    result = await client.request(acct_info)
    data = result.to_dict()
    account_data = {
        'account_address': data['result']['account_data']['Account'],
        'account_balance': data['result']['account_data']['Balance'],
    }
    return account_data
