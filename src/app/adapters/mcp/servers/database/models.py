from datetime import date

from pydantic import BaseModel

class MonthlyStatistic(BaseModel):
    finished_month: date
    count: int