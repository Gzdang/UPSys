import os
from utils import load_json

res = {"ours":0, "tex":0, "painter":0, "paint3d": 0}

for path in os.listdir("summary/results_b"):
    js = load_json("summary/results_b/" + path)
    for c in js:
        res[c] = res[c] + 1

sum = 0
for key in res.keys():
    sum += res[key]
print(f"total submit: {sum//20}, total questions: {sum}")

for key in res.keys():
    print(f"{key}: {(100 * res[key]/sum):.1f}%")