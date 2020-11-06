

"""Tests for the places module."""

import googlemaps
import json

class mydict(dict):
        def __str__(self):
            return json.dumps(self)

gmaps = googlemaps.Client(key='AIzaSyCKsaVDGM4cDg-jmkub7gGXzww4sHZmRRA')

place_ids = ['ChIJx0Pj78UE9ocR0RGv_kVzK0s', 'ChIJWcfLCviI9YcR5jiT1hbJK3U', 'ChIJV67Si5Mn9ocRX7c1aeh0Fpc',
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
                'ChIJ8SdsjT4r9ocRe-oreXwEBEU']

place_details_dict = {}

def create_dict_of_place_details():
        
    for roaster in place_ids:
    

        response = gmaps.place(roaster, fields=['name', 'website', 'formatted_address',
                                                                'formatted_phone_number', 'opening_hours'])
        
        details = response['result']

        
        place_details_dict[roaster] = details

        if place_details_dict[roaster].get('opening_hours') is not None:
            hours = place_details_dict[roaster]['opening_hours']['weekday_text']
            place_details_dict[roaster]['opening_hours'] = hours
        else:
            place_details_dict[roaster]['opening_hours'] = 'Unavailable'

    return place_details_dict

json_file = json.dumps(place_details_dict)