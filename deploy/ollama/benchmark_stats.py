import os, sys, json, re
import pandas as pd
baseDir = os.environ["HOME"] + "/lav/src/blender_twin/deploy/ollama/data/"
fL = os.listdir(baseDir)

headL = ['model','tokens_per_second','total_tokens','processing_time']
resL = []
for f in fL:
    with open(baseDir + f) as fl:
        d = json.loads(fl.read())
    l = [d[k] for k in headL]
    resL.append(l)
    ls = ",".join([str(x) for x in l])


headL = ['model','tokens_per_second','token_rate','time_rate']
benD = pd.DataFrame(resL,columns=headL)
benD['token_rate'] = benD['token_rate'] / benD['token_rate'].max() * benD['tokens_per_second'].mean()
benD['time_rate'] = benD['time_rate'] / benD['time_rate'].max() * benD['tokens_per_second'].mean()
#print(benD.set_index('model').T)
print(benD.to_string(index=False))
