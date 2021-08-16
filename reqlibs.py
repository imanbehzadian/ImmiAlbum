#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#  #pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
  #pip install pprint

 #To create credentials.json go to GCP >> Apps & Services >> Creditentials >> Oath2.0 >> Desktop App >> Download Json and rename
 # visit https://developers.google.com/drive/api/v3/quickstart/python and maybe you need this too: https://developers.google.com/workspace/guides/create-credentials
 # Good help pages:
    # Sldies Elements :https://developers.google.com/slides/api/concepts/page-elements
    # Basic Read: https://developers.google.com/slides/api/samples/reading
    # Basic Write: https://developers.google.com/slides/api/samples/writing
    # Add Image: https://developers.google.com/slides/api/guides/add-image
    # Google photos build service: https://stackoverflow.com/questions/66689941/google-photos-api-new-version
    # Google Photos: https://www.youtube.com/watch?v=lj1uzJQnX38 & https://www.youtube.com/watch?v=BQXl8lJ-zbY
    # Google photos analysis : https://medium.com/@najeem/analyzing-my-google-photos-library-with-python-and-pandas-bcb746c2d0f2


# In[4]:


import os.path
#from __future__ import print_function
import pprint
import pandas as pd
from numpy import array_split
from math  import ceil
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json
import glob
print('import libs: done!')




# In[ ]:




