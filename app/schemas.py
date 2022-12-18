from pydantic import BaseModel


class XrplTransfer(BaseModel):
    source_seed: str
    source_sequence: int
    destination_address: str
    value: float


class NFTokenMintData(BaseModel):
    seed: str
    sequence: int
    uri: str
    transfer_fee: int


class NFTokenTransferData(BaseModel):
    seed: str
    sequence: int
    nftoken_id: str
    amount: int
    owner: str
