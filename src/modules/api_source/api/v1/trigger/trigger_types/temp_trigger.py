from enum import Enum
from pydantic import BaseModel

import operator

from src.modules.api_source.api.v1.trigger.trigger_types.base_class import TriggerBaseClass


class Operator(str, Enum):
    lt = "<"
    gt = ">"
    eq = "="


OPERATOR_FUNC = {
    Operator.lt: operator.lt,
    Operator.gt: operator.gt,
    Operator.eq: operator.eq,
}


class TempParams(BaseModel):
    temp: float
    op: Operator


class TempTrigger(TriggerBaseClass):
    def __call__(self, payload: dict, params: dict) -> bool:
        p = TempParams(**params)
        return OPERATOR_FUNC[p.op](payload.get("temp", 0), p.temp)

    @classmethod
    def describe(cls):
        return {
            "temp": "Число — температура в градусах",
            "op": "Оператор сравнения: curr > temp,  curr < temp , curr = temp"
        }
#
#
# trigger = TempTrigger()
#
# payload = {"temp": 44}  # допустим, сейчас 28 градусов
# params = {"temp": 30, "op": ">"}  # условие: "если температура ниже 30"
#
# result = trigger(payload, params)
# print(result)  # → True
