from datetime import datetime

from pydantic import BaseModel, Field

class Transaction(BaseModel):
    transaction_id:str=Field(min_length=1)
    timestamp:datetime
    company_id:str=Field(min_length=1)
    vendor_id:str=Field(min_length=1)
    amount:float=Field(gt=0)
    currency:str=Field(
        min_length=3,
        max_length=3,
        pattern=r"^[A-Z]{3}",
    )
    description:str=Field(min_length=1)
    sector:str=Field(min_length=1)