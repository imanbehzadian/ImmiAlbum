#!/usr/bin/env python
# coding: utf-8

# In[1]:



import pandas as pd
import numpy as np
import json
import glob


# In[4]:


def PJ_searcher():
    jsonfiles = []
    for file in glob.glob('../*/Google Photos/Naghiman/*.json'):
        jsonfiles.append(file)

    try:
        pictures = pd.DataFrame(columns=['title', 'description','date','lat', 'long'])
        for j in jsonfiles:
            with open('./'+ j ) as f:
                data = json.load(f)
            x= pd.json_normalize(data)
            x=x[['title', 'description','photoTakenTime.formatted','geoData.latitude', 'geoData.longitude']]
            x.columns=['title', 'description','date','lat', 'long']
            pictures = pictures.append(x)

        pictures = pictures.reset_index(drop = True)

    except: 
        print(f'failed to parse a jason file hence ignored it: {j}')
        pass

    #desc_pics = pictures[pictures['description'] != '']
    return(pictures)


# In[19]:




