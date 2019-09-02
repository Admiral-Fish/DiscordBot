from enum import Enum
import os
import sys

class EnvType(Enum):
    STRING = 0
    INT = 1
    STRING_LIST = 2
    INT_LIST = 3

def getVariable(env, type=EnvType.STRING):
    val = os.environ.get(env)

    if val is None:
        sys.exit()

    if type == EnvType.STRING:
        return val
    elif type == EnvType.INT:
        return int(val)
    elif type == EnvType.STRING_LIST:
        return val.split(",")
    elif type == EnvType.INT_LIST:
        return [ int(v) for v in val.split(",") ]

    return None