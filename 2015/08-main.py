#!/usr/local/bin/python3
import ast
import re
data = None

with open('./08-data.txt') as f:
    data = f.read()
data = data.splitlines()
raw = 0
decoded = 0
encoded = 0
# data = [r'"m\"kt12\\qnw"']
# data = [r'mk"xt']

for line in data:
    o = line
    raw += len(line)
    
    # decode
    ds = ast.literal_eval(o)
    d = len(ds)
    
    # encode
    es = re.compile(r'\\').sub(r'\\\\', line)
    es = re.compile(r'"').sub(r'\\"', es)
    es = r'"' + es + r'"'
    e = len(es)

    # print(o, '->', ds, '->', es)
    decoded += d
    encoded += e

# print('same:', same)
print('raw:', raw)
print('decoded: ', decoded)
print('encoded: ', encoded)
print('diff (r-d):', raw - decoded)
print('diff (e-r):', encoded - raw)

"""
https://media.ccc.de/v/c4.openchaos.2018.06.glitching-the-switch
"""