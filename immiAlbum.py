#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('python -m venv ./immi-env')


# In[2]:


get_ipython().system('source ./immi-env/bin/activate')


# In[3]:


#!pip install path.py
#export PYTHONPATH="${PYTHONPATH}:/Users/imanbehzadian/Documents/Python/Google photos/ImmiAlbum/"
import os
from os import path
#os.getcwd()
#sys.path.append('/Users/imanbehzadian/Documents/Python/Google photos/ImmiAlbum/')


# In[3]:


from math  import ceil
from numpy import array_split

import APIconnect as APIc
import GooglePhotosSearch as GP
import PJsonConverter
import slidePopulator as SP


# In[4]:


get_ipython().system('pip freeze > requirement.txt')

#!pip intalled -r requirement.txt   # to use the requirement file for pip


# In[8]:



def main():
    """Shows basic usage of the Drive v3 API and google photos API.
    Create an album on google slide by direct API connections between google photos and slides. 
    it will have 4 picutres per page with the picture description underneath and with google map 
    API in the corner to show the location and a timeline.
    """

    
    SCOPES = ['https://www.googleapis.com/auth/presentations','https://www.googleapis.com/auth/photoslibrary.readonly']
    PRESENTATION_ID = '1YC3cDTJ0T2n0CYXKvtNTCccblIDkwUVjP28z4YMQWyU'
    album_title = 'Naghiman'
        
    creds = APIc.creds_gen(SCOPES)
    service = APIc.APIconnection(creds,PRESENTATION_ID,album_title) 
    service.connection_refresh()
    
    request_body = {
        'albumId': service.ALBUM_ID,
        'pageSize': 100
        }


    df_search_result = GP.response_media_items_by_filter(service.google_photos,request_body)
    photo_desc =  df_search_result[df_search_result['description'].isna() == False].head(20)
    x,_ = photo_desc.shape
    page_count = ceil(x/4)
    photo_sets = array_split(photo_desc,page_count)
    SP.Duplicator(service.google_slides,service.PRESENTATION_ID,service.PAGE_ID,page_count)

    for i in range(page_count):
        SP.Replacer(service.google_slides,service.PRESENTATION_ID,photo_sets[i],i+2)
    return None


# In[9]:


if __name__ == '__main__':
    main()

