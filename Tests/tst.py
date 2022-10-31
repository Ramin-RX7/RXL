import time
import sys
import os

t= time.time()

# import runpy
# runpy.run_path("tst2.py")

# __import__("runpy").run_path("tst2.py")

from runpy import run_path
run_path("tst2.py")


x = time.time()-t
print(x)



"""
#] argparse: 28ms
#] decopt:   16ms (without schema)  (Schema: 26ms)
#] click:    60ms
#] invoke:   11ms
"""

