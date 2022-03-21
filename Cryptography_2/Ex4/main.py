# -----------------------------------------------------------
# Simple university project for cryptography course
# Demonstrates hashing features
#
# (C) 2022 Jacek Jendrzejewski, Poland
# -----------------------------------------------------------

import timeit
import plotly.express as px
import hashlib

fileCount = 8
testData = {}

for i in range(fileCount):
    
    fileName = f"message{(i+1)}";
    filePath = f"{fileName}.txt"
    length = 0
    hasher = hashlib.sha256()
    
    print(f"Started hashing: {fileName}")
    with open(filePath, 'rb') as fileData:
        # length = len(fileData)
                
        data_chunk = fileData.read(1024)
        startTime = timeit.default_timer()

        while data_chunk:
              hasher.update(data_chunk)
              length += len(data_chunk)
              data_chunk = fileData.read(1024)
              
    tookTime = timeit.default_timer() - startTime 
    testData[f"{fileName} - {length}"] = tookTime

fig = px.bar(x=testData.keys(), y = testData.values())
fig.update_xaxes(type='category')
fig.show()