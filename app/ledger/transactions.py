from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment
from xrpl import utils
from xrpl.asyncio import transaction


JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"

async def transfer_xrpl(
    source_seed: str, source_sequence: int, 
    destination_address: str, value: float
    ) -> dict:
    client = AsyncJsonRpcClient(JSON_RPC_URL)
    source_wallet = Wallet(seed=source_seed, sequence=source_sequence)
    payment = Payment(
        account=source_wallet.classic_address,
        amount=utils.xrp_to_drops(value),
        destination=destination_address,
    )

    signed_tx = await transaction.safe_sign_and_autofill_transaction(
        payment, source_wallet, client)
    tx_id = signed_tx.get_hash()
    print("Transaction cost:", utils.drops_to_xrp(signed_tx.fee), "XRP")
    print("Identifying hash:", tx_id)

    try:
        tx_response = await transaction.send_reliable_submission(signed_tx, client)
    except transaction.XRPLReliableSubmissionException as e:            
        return {'error': e}

    tx_data = tx_response.to_dict()
    transaction_result = tx_data['result']['meta']['TransactionResult']
    result = {
        'transaction_result': transaction_result,
    }

    if transaction_result == 'tesSUCCESS':
        nodes_data = tx_data['result']['meta']['AffectedNodes']
        result.update({
            'source_sequence': nodes_data[1]['ModifiedNode']['FinalFields']['Sequence'],
            'source_balance': utils.drops_to_xrp(
                nodes_data[1]['ModifiedNode']['FinalFields']['Balance']),
            'destination_balance': utils.drops_to_xrp(
                nodes_data[0]['ModifiedNode']['FinalFields']['Balance'])
        })
    
    return result
