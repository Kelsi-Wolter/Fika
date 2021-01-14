

"""Calls Google Places API and returns place details search for each place ID"""

import googlemaps
import json
import os

# Create instance of Google maps request using API key
# Can take key out after seeding database
gmaps = googlemaps.Client('AIzaSyA7kGblloOwNaoFbgZlb3DNRaz-SxRG7SI')


# List of coffee roaster place IDs
place_ids = [
                'ChIJx0Pj78UE9ocR0RGv_kVzK0s',
                'ChIJWcfLCviI9YcR5jiT1hbJK3U', 
                'ChIJV67Si5Mn9ocRX7c1aeh0Fpc',
                'ChIJAbkBsJkts1IRNj7L1NnbGUg',
                'ChIJr2WxIeIzs1IRP_yfK1DjOoE',
                'ChIJ0cRRS0kts1IRIPm_KaYaRSM',
                'ChIJIboB_Doo9ocRrDBso-gIF8k',
                'ChIJSbDcfhjV94cRNK4i7Fef_7Y',
                'ChIJtQFIcrwss1IR2d6g5J5goMY',
                'ChIJVctrQLk_s1IRjejI4TuiLGA',
                'ChIJb0hUeqots1IRBdpaXkAoTt8',
                'ChIJAdmh1Jkts1IRsjkOVAe3S3U',
                'ChIJG7xp558ts1IRLe7pAThX3ug',
                'ChIJIbgloXbU94cRux5kDChUAgI',
                'ChIJY8w2QUUm9ocR8ppRfDgUX_0',
                'ChIJ_4onGLgss1IRwrDvJj4dpCg',
                'ChIJ8SdsjT4r9ocRe-oreXwEBEU',
                
    
                'ChIJAQDAwtZSrlIRBDSDAdzoufI',
                'ChIJO3rqvldNrlIRdN8X7uCSi8Y',
                'ChIJ0bMRkRvCtlIRmD_SooEJq4c',

                'ChIJoY8dD3Vf94cRMo1AFxzMuhM',
                'ChIJ6yZ38_07sVIR9jB4sdR80B8',
                'ChIJl-9eENstuFIRMEU1LLE6Upc',
                'ChIJ686CRCktuFIRH87e8Ki0kYo',
                'ChIJV7ZjmE0OuFIRKQognbDKbkI',
                'ChIJIedYFk89tlIRZs5lpVFENnM',
                'ChIJ-_TuMC90yVIRVMUotEblBnw',
                'ChIJ7WFSiIo9v1IRskGfX8wA7Ms',
                'ChIJbWxLtCYzplIR4Kz0pCH_f1k',
                'ChIJHQ64IjIltFIRkBR2VWpLu4o',
                'ChIJa44iG8FT9ocRraV6DN3avYA',
                'ChIJze6FQkBB94cRIYDIRIp4Yy8',
                'ChIJ8x5O0gdt-YcR9ghTbtkhVkI',
                # 'ChIJVYUOBnPf-4cRFWtVxT1CkqcPf', causes error with google request
                'ChIJ4cbScHl_9ocRQnga1z8gRr8',
                'ChIJC19CVHJ_84cRCR05pa3bC1E',
                'ChIJMVt08CBe94cRTfmaGme8sHw',
                'ChIJU5IDRlahtFIRT3e9Y1zWgiQ',
                'ChIJhxR7xdZSrlIRrqiRSNu1RFc']


# PLACE DETAILS DATA CALLS 

place_details_dict = {}

def create_details_dict():
    '''Loop through list of IDs and create dict with API response for each ID


        new dictionary will have place ID as key and dict of each field (key-name) with value stored,
        also checks each field to ensure there is data available, will set to 'Unavailable' if not supplied
        by API'''
        
    for roaster in place_ids:

    
        # Sends request to API for specified fields on each roaster ID
        response = gmaps.place(roaster, fields=['name', 'website', 'formatted_address', 'formatted_phone_number', 'opening_hours', 'geometry'])

                                                                
        # Keys into response "result" key to use as values for each roaster ID key
        details = response['result']

        # Adds each roaster to dictionary and sets value to 'details'
        place_details_dict[roaster] = details

        # Checks for value at each field, sets to 'Unavailable' if no data present (helps prevent key errors when seeding)
        # Name value
        if place_details_dict[roaster].get('name') is None:
            place_details_dict[roaster]['name'] = 'Unavailable'

        # Website value
        if place_details_dict[roaster].get('website') is None:
            place_details_dict[roaster]['website'] = 'Unavailable'

        # Address value
        if place_details_dict[roaster].get('formatted_address') is None:
            place_details_dict[roaster]['formatted_address'] = 'Unavailable'

        # Phone number value
        if place_details_dict[roaster].get('formatted_phone_number') is None:
            place_details_dict[roaster]['formatted_phone_number'] = 'Unavailable'

        # Hours value, also keys into hours to get the "weekday text" key-value pair to use as value for 'hours'
        if place_details_dict[roaster].get('opening_hours') is None:
            place_details_dict[roaster]['opening_hours'] = 'Unavailable'
        else:
            hours = place_details_dict[roaster]['opening_hours']['weekday_text']

            place_details_dict[roaster]['opening_hours'] = hours

        # Lat/Long, also keys into lat/long from 'geometry'
        if place_details_dict[roaster].get('geometry') is None:
            place_details_dict[roaster]['geometry'] = 'Unavailable'
        else:
            location = place_details_dict[roaster]['geometry']['location']
            place_details_dict[roaster]['geometry'] = location


    return place_details_dict

# This json translation is no longer necessary as data input for server changed
# def create_json(dict):
#     return json.dumps(dict, sort_keys=True, indent=4)


# PHOTO DATA CALLS

def store_photo(photo, n):
    '''Gets photo response using photo_reference and writes as jpg file'''

    response = gmaps.places_photo(photo, 600, 400)

    # n = str(n)
    f = open(n + '_title_photo' + '.jpg', 'wb')
    for chunk in response:
        if chunk:
            f.write(chunk)
    f.close()

    return True

def create_photo_dir(roaster_place_ID):
    '''Gets photo reference for photo in place_details response, which provides 10 photo references
    
    
    Uses store_photo function and increments number for file name'''

    response = gmaps.place(roaster_place_ID, fields=['photo'])
    photos = response['result']['photos']
    n = 0
    for photo in photos:
        photo = photo['photo_reference']
        store_photo(photo, n)
        # print(photo, n)
        n += 1

def create_title_photo(roaster_place_ID):
    '''Takes place details response and indexes in to one of the photos to store, uses place ID in file name'''

    response = gmaps.place(roaster_place_ID, fields=['photo'])
    photos = response['result']['photos']
    n = roaster_place_ID
    photo = photos[0]['photo_reference']
    store_photo(photo, n)

    

