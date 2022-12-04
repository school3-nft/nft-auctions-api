from pydantic import BaseModel


class XrplTransfer(BaseModel):
    source_seed: str
    source_sequence: int
    destination_address: str
    value: float