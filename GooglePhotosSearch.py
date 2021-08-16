#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd


# In[ ]:


def response_media_items_by_filter(google_photos, request_body: dict):
    # Search Google photos by Album ID for all MediaItems
    try:
        response_search = google_photos.mediaItems().search(body=request_body).execute()
        lstMediaItems = response_search.get('mediaItems')
        nextPageToken = response_search.get('nextPageToken')

        while nextPageToken:
            request_body['pageToken'] = nextPageToken
            response_search = google_photos.mediaItems().search(body=request_body).execute()
            lstMediaItems.extend(response_search.get('mediaItems'))
            nextPageToken = response_search.get('nextPageToken')    
            print(f"Number of items processed:{len(lstMediaItems)}", end='\r')

        df_search_result = pd.DataFrame(lstMediaItems)    
        return df_search_result   
        
    except Exception as e:
        print('Error in connecting to the Google Photos Album')
        print(e)
        return None

