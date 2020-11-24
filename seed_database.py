'''Script to seed database'''

import os
import json
from random import choice, randint

import crud
import model
import server
import places_data

os.system('dropdb MNroasters')
os.system('createdb MNroasters')

model.connect_to_db(server.app)
model.db.create_all()

# Uses places_data to create json file and then reads the json file to create roaster_data - inefficient 
# with open('data/newer_data.txt') as f:
#     roaster_data = f.read()

    # roaster_data = json.loads(f.read())


# Uses places_data module to seed database instead of a json file
roaster_data = places_data.create_details_dict()

list_of_roasters = []
for roaster in roaster_data:
    print(roaster)


    name, address, phone_number, website, place_id, hours, lat, lng = (roaster_data[roaster]['name'], 
                                                        roaster_data[roaster]['formatted_address'],
                                                        roaster_data[roaster]['formatted_phone_number'],
                                                        roaster_data[roaster]['website'],
                                                        roaster,
                                                        roaster_data[roaster]['opening_hours'],
                                                        roaster_data[roaster]['geometry']['lat'],
                                                        roaster_data[roaster]['geometry']['lng'])
                                                        
    # Old code for formatting the opening hours 
    # hours = roaster_data[roaster]['opening_hours']
    # Remove '\\u2013 from hours'
    # if hours != 'Unavailable':
    #     stripped_hours = []

    #     # Loop through each string in 'hours' and split by space character, returns list of
    #     # strings with day-name, time, and am/pm values, looks for \\u2013 and removes from list
    #     for day in hours:
    #         sections = (day.split(' '))
    #         if "\\u2013" in sections:
    #             sections.remove("\\u2013")

    #         # Joins strings with day-name, times and am/pm back into one long string, adds to
    #         # new list of weekday hours
    #         stripped_day = ' '.join(sections)
    #         stripped_hours.append(stripped_day)

    #         hours = stripped_hours
    
    # images = crud.create_photos(place_id)

                                                      
    db_roaster = crud.create_roaster(name=name, address=address, phone_number=phone_number, hours=hours,
                    website=website, place_id=place_id, avg_user_rating=None, lat=lat, lng=lng)

    list_of_roasters.append(db_roaster)



list_of_users = []

# Create 10 users; 
for n in range(10):
    email = f'user{n}@test.com' 
    password = 'test'
    first_name = choice(['Jane', 'John', 'Zella', 'Jordan', 'Nick', 'Rachel', 'Thomas', 'Trish', 'Micah', 'Jack'])
    last_name = choice(['Wolter', 'Adair', 'Morgan', 'Lewis', 'Hepper', 'Marin', 'Knutsen', 'Wagner', 'Torke'])

    user = crud.create_user(first_name, last_name, email, password)

    list_of_users.append(user)

#Create Favorites and Roasters list for each user
for user in list_of_users:
   
    db_list1 = crud.create_list(list_name='My Favorites', user=user)
    db_list2 = crud.create_list(list_name='My Roasters', user=user)
    
    rated_roasters = []
    
    # Create 4 entries for 'My Roasters' list
    for n in range(4):
        
        # For each entry, make random choice from roasters list, remove that choice from the list but add to separate list (so can add
        # those roasters back to master list later), generate score and make random choice for note, instantiate entry and loop through
        # 4 times 
        roaster = choice(list_of_roasters)
        list_of_roasters.pop(list_of_roasters.index(roaster))
        rated_roasters.append(roaster)
        score = randint(1,5)
        note = choice(['Great dark roast.', 'Cute packaging.', 'Sent friendly note with delivery.',
        'Too many options.', 'Very fruity taste.', 'Very chocolatey taste.', 'So smooth.',
        'High caffeine content!', 'Great for pour-overs!', 'Great smell, better taste!'])


        entry = crud.create_entry(entry_list=db_list2, roaster=roaster, score=score, note=note)

    # Create 1 entry for 'My Favorites' list
    # Make random choice from limited list of roasters (has popped roasters from loop above removed), make random choice for note, instantiate
    # entry for favorites list
    roaster_fav = choice(list_of_roasters)
    note = choice(['Love this coffee!', "Best dark roast I've tasted!", "So many great options!"])    
    entry_fav = crud.create_entry(entry_list=db_list1, roaster=roaster_fav, score=5, note=note)

    # Loop through the removed roasters and add back to master list
    for roaster in rated_roasters:
        list_of_roasters.append(roaster)

for roaster in list_of_roasters:
    roaster_id = roaster.roaster_id
    avg_rating = crud.calculate_avg_rating(roaster_id)
    roaster.avg_user_rating = avg_rating
    


