from pydantic import  BaseModel
from typing   import Optional
class Product(BaseModel):
    id : Optional[int]
    name : str
    description : str
    price :float
    quantity:int 