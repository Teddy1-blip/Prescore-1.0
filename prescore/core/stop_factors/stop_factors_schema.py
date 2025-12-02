from typing import List, Optional, Dict
from pydantic import BaseModel

class BankStopRules(BaseModel):
    min_age: Optional[int] = None                 # минимальный возраст в месяцах
    stop_regions: List[str] = []                 # стоп-регионы
    allowed_regions: List[str] = []              # разрешенные регионы
    stop_okved: List[str] = []                   # стоп ОКВЭД
    allowed_okved: List[str] = []                # разрешенные ОКВЭД

class StopFactors(BaseModel):
    banks: Dict[str, BankStopRules]
