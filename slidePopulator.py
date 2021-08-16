#!/usr/bin/env python
# coding: utf-8

# In[1]:


def Duplicator(google_slides,PRESENTATION_ID,PAGE_ID,pID):
    requests = []
# Duplicate a Slide based on the template

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


# In[ ]:


def Replacer(google_slides,PRESENTATION_ID,photo_desc,pID):
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

    return None

