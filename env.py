import os
import sys

def getVariable(env):
    val = os.environ.get(env)

    if val is None:
        sys.exit()

    return val