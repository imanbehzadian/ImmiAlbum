#!/usr/bin/env python
# coding: utf-8

# In[1]:


#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
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


# In[2]:


from __future__ import print_function
import os.path
import pprint
import pandas as pd
from numpy import array_split
from math  import ceil
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

global google_slides , google_photos, PRESENTATION_ID ,PAGE_ID


SCOPES = ['https://www.googleapis.com/auth/presentations','https://www.googleapis.com/auth/photoslibrary.readonly']


PRESENTATION_ID = '1YC3cDTJ0T2n0CYXKvtNTCccblIDkwUVjP28z4YMQWyU'


creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())


# In[3]:



google_slides = build('slides', 'v1', credentials=creds)
google_photos = build('photoslibrary', 'v1', credentials=creds,static_discovery=False)

# Call the Slides API
presentation = google_slides.presentations().get(
    presentationId=PRESENTATION_ID).execute()
slides = presentation.get('slides')
PAGE_ID = presentation['slides'][1]['objectId']
#PAGE_ID = 'ge5ae558ac8_0_119'

print('The presentation contains {} slides:'.format(len(slides)))
for i, slide in enumerate(slides):
    print('- Slide #{} contains {} elements.'.format(
        i + 1, len(slide.get('pageElements'))))

# Call the Photos API

response_albums_list = google_photos.albums().list().execute()
albums_list = response_albums_list.get('albums')

ALBUM_ID = next(filter(lambda x: "Naghiman" in x['title'], albums_list))['id']
#ALBUM_ID = 'AL7J-NVXv8pcciIj8Ir4B8-U3bkmhxDTI5pEaHGS1bEIlOb2ouLBuCVM5vr-1n5-2lgHuey2jJCC'

album = google_photos.albums().get(
    albumId = ALBUM_ID).execute()

print(f"Naghiman's album id is : {ALBUM_ID} ")    
    


# In[3]:


# Search Google photos by Album ID for all MediaItems
   


#request_body = {
#    'albumId': ALBUM_ID,
#    'pageSize': 100
#}

#response_search = google_photos.mediaItems().search(body=request_body).execute()

#lstMediaItems = response_search.get('mediaItems')
#nextPageToken = response_search.get('nextPageToken')

#while nextPageToken:
#    request_body['pageToken'] = nextPageToken

#    response_search = google_photos.mediaItems().search(body=request_body).execute()
#    lstMediaItems.extend(response_search.get('mediaItems'))
#    nextPageToken = response_search.get('nextPageToken')    
#    print(f"Number of items processed:{len(lstMediaItems)}", end='\r')


#df_search_result = pd.DataFrame(lstMediaItems) 


# In[4]:


def response_media_items_by_filter(request_body: dict):
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
   


# In[5]:


# Duplicate a Slide based on the template


def Duplicator(PAGE_ID,pID):
    requests = []
    
    for i in range(pID):
        requests.append(
                        {
                            'duplicateObject':{
                                   'objectId': PAGE_ID,
                                  'objectIds': {PAGE_ID: 'Page' + str(pID - i)
                                               }
                                }
                        }
                     )



    # Execute the request.
    body = {
        'requests': requests
    }
    response = google_slides.presentations()         .batchUpdate(presentationId=PRESENTATION_ID, body = body).execute()
    duplicate_slide_response = response.get('replies')[0].get('duplicateObject')

    presentation = google_slides.presentations().get(
        presentationId=PRESENTATION_ID).execute()
    slides = presentation.get('slides')

    print('Duplicated completed. The presentation now contains {} slides:'.format(len(slides)))
    for i, slide in enumerate(slides):
        print('- Slide #{} with the id of {} contains {} elements.'.format(
            i + 1,slide.get('objectId'), len(slide.get('pageElements'))))
    return None


# In[6]:


def Replacer(photo_desc,pID):
    print(pID)
    row,_ = photo_desc.shape
    row = min(4,row)
    slideObj =google_slides.presentations().get(presentationId=PRESENTATION_ID
           ).execute().get('slides')[pID]
    slide = slideObj['objectId']
    print(f'** Get slide {slide}, search for image placeholder')
    obj = None
    i=-1
    ImagePH = []
    numElem = len(slideObj['pageElements'])
    for obj in slideObj['pageElements']:
        i+=1
        try:
            if  'placeholderrrrrrrrr' in obj['shape']['text']['textElements'][1]['textRun']['content']:
                ImagePH.append(obj)
        except:
            pass
        
#    print(f'Number of identified placeholders: {len(ImagePH)} out of all {numElem} the elements')
#    print('Replacing placeholder text and pictures')
    for i in range(row):
        reqs = [
            {'replaceAllText': {
                'containsText': {'text': f'Placeholder text boxxxxxxx {i+1}'},
                'replaceText': photo_desc['description'].iloc[i],
                'pageObjectIds': [slide]
            }},
            {'createImage': {
                'url': photo_desc['baseUrl'].iloc[i],
                'elementProperties': {
                    'pageObjectId': slide,
                    'size': ImagePH[i]['size'],
                    'transform': ImagePH[i]['transform'],
                }
            }},
            {'deleteObject': {'objectId': ImagePH[i]['objectId']}},
        ]
        google_slides.presentations().batchUpdate(body={'requests': reqs},
                presentationId=PRESENTATION_ID).execute()
#    print('DONE')
    return None


# In[7]:


### Main
request_body = {
    'albumId': ALBUM_ID,
    'pageSize': 100
}

df_search_result = response_media_items_by_filter(request_body)
photo_desc =  df_search_result[df_search_result['description'].isna() == False].head(10)
x,_ = photo_desc.shape
page_count = ceil(x/4)
photo_sets = array_split(photo_desc,page_count)
Duplicator(PAGE_ID,page_count)

for i in range(page_count):
    Replacer(photo_sets[i],i+2)


# In[ ]:




