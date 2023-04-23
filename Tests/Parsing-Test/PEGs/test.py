import time
import rx7 as rx
from pprint import pprint
rx.cls()
t = rx.record()
# t = time.time
# t = time.perf_counter








rx.cls()
rx.terminal.run("canopy include.peg --lang python")


import include


x = include.parse("include hello,ramin, asdf , adsf   ")

print(x.pkgs.text.split(","))
x = list(map(str.strip,x.pkgs.text.split(",")))

print(x)
















t.lap()
print()
print(t)