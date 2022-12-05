from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.asyncio.wallet import generate_faucet_wallet
from xrpl.models.requests.account_info import AccountInfo
from xrpl.wallet import Wallet
from xrpl import utils


JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
DEFAULT_ACCOUNT_BALANCE = "1000000000" # in drops

async def generate_ledger_account() -> dict:
    client = AsyncJsonRpcClient(JSON_RPC_URL)
    wallet = await generate_faucet_wallet(client, debug=True)
    account_data = {
        'account_address': wallet.classic_address,
        'account_balance': utils.drops_to_xrp(DEFAULT_ACCOUNT_BALANCE),
        'seed': wallet.seed,
        'sequence': wallet.sequence,
        'public_key': wallet.public_key,
        'private_key': wallet.private_key
    }
    return account_data


async def get_ledger_account_data(seed: str, sequence: int) -> dict:
    client = AsyncJsonRpcClient(JSON_RPC_URL)
    wallet = Wallet(seed=seed, sequence=sequence)
    acct_info = AccountInfo(
        account=wallet.classic_address,
        ledger_index="validated",
        strict=True,
    )
    response = await client.request(acct_info)
    full_data = response.to_dict()
    data = {
        'account_address': wallet.classic_address,
        'account_balance': utils.drops_to_xrp(
            full_data['result']['account_data']['Balance']),
        'seed': wallet.seed,
        'sequence': wallet.sequence,
        'public_key': wallet.public_key,
        'private_key': wallet.private_key
    }
    return data
