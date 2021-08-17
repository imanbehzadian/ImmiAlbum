#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# In[8]:




def creds_gen(SCOPES):
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds


# In[9]:


#def connection_builder(creds,PRESENTATION_ID,album_title):
#    google_slides = build('slides', 'v1', credentials=creds)
#    google_photos = build('photoslibrary', 'v1', credentials=creds,static_discovery=False)

    # Call the Slides API
#    presentation = google_slides.presentations().get(
#        presentationId=PRESENTATION_ID).execute()
#    slides = presentation.get('slides')
#    PAGE_ID = presentation['slides'][1]['objectId']
    #PAGE_ID = 'ge5ae558ac8_0_119'

#    print('The presentation contains {} slides:'.format(len(slides)))
#    for i, slide in enumerate(slides):
#        print('- Slide #{} contains {} elements.'.format(
#            i + 1, len(slide.get('pageElements'))))

    # Call the Photos API
#    response_albums_list = google_photos.albums().list().execute()
#    albums_list = response_albums_list.get('albums')

#    ALBUM_ID = next(filter(lambda x: album_title in x['title'], albums_list))['id']
#    #ALBUM_ID = 'AL7J-NVXv8pcciIj8Ir4B8-U3bkmhxDTI5pEaHGS1bEIlOb2ouLBuCVM5vr-1n5-2lgHuey2jJCC'
#    album = google_photos.albums().get(
#        albumId = ALBUM_ID).execute()
#    print(f"{album_title} album id is : {ALBUM_ID} ")    
#    
#    return google_slides, google_photos , presentation, PAGE_ID ,ALBUM_ID
    


# In[10]:


class APIconnection:

    def __init__(self, creds,PRESENTATION_ID,album_title):
        self.creds = creds
        self.PRESENTATION_ID = PRESENTATION_ID
        self.album_title = album_title

    def connection_refresh(self):
        self.google_slides = build('slides', 'v1', credentials=self.creds)
        self.google_photos = build('photoslibrary', 'v1', credentials=self.creds,static_discovery=False) 
        
        self.presentation = self.google_slides.presentations().get(presentationId=self.PRESENTATION_ID).execute()
        self.PAGE_ID = self.presentation['slides'][1]['objectId']
        #PAGE_ID = 'ge5ae558ac8_0_119'

        response_albums_list = self.google_photos.albums().list().execute()
        albums_list = response_albums_list.get('albums')
        self.ALBUM_ID = next(filter(lambda x: self.album_title in x['title'], albums_list))['id']
        #ALBUM_ID = 'AL7J-NVXv8pcciIj8Ir4B8-U3bkmhxDTI5pEaHGS1bEIlOb2ouLBuCVM5vr-1n5-2lgHuey2jJCC'

        return None
    
    def connection_ID(self):
        try:
            print(f"Page ID = {self.PAGE_ID} \n Album ID = {self.ALBUM_ID}")
        except:
            print("First establish a connection using connection_refresh() method")
            pass
        return None

    def connection_check(self):
        try:        
            # Call the Slides API
            slides = self.presentation.get('slides')
            print('The presentation contains {} slides:'.format(len(slides)))
            for i, slide in enumerate(slides):
                print('- Slide #{} contains {} elements.'.format(
                    i + 1, len(slide.get('pageElements'))))

            # Call the Photos API
            album = google_photos.albums().get(
                albumId = ALBUM_ID).execute()
            print(f"{album_title} album id is : {ALBUM_ID} ")    
        except:
            print("First establish a connection using connection_refresh() method")
            pass
            
        return None 

