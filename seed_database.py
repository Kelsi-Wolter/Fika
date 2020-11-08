'''Script to seed database'''

import os
import json
from random import choice, randint

import crud
import model
import server

os.system('dropdb MNroasters')
os.system('createdb MNroasters')

model.connect_to_db(server.app)
model.db.create_all()


with open('data/new_data.json') as f:
    roaster_data = json.loads(f.read())

list_of_roasters = []
for roaster in roaster_data:

    name, address, phone_number, website = (roaster_data[roaster]['name'], 
                                                        roaster_data[roaster]['formatted_address'],
                                                        roaster_data[roaster]['formatted_phone_number'],
                                                        roaster_data[roaster]['website'])
                                                        

    hours = roaster_data[roaster]['opening_hours']
    # Remove '\\u2013 from hours'
    if hours != 'Unavailable':
        stripped_hours = []

        # Loop through each string in 'hours' and split by space character, returns list of
        # strings with day-name, time, and am/pm values, looks for \\u2013 and removes from list
        for day in hours:
            sections = (day.split(' '))
            if "\\u2013" in sections:
                sections.remove("\\u2013")

            # Joins strings with day-name, times and am/pm back into one long string, adds to
            # new list of weekday hours
            stripped_day = ' '.join(sections)
            stripped_hours.append(stripped_day)

            hours = stripped_hours


                                                      
    db_roaster = crud.create_roaster(name=name, address=address, phone_number=phone_number, hours=hours,
                    image=None, website=website, coffee_link=None, shipping_link=None, avg_rating=None)
    
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

#Create 1 (goal for 2-3) list for each user

for user in list_of_users:
    # Not sure if I need both list type and list name at this point, may need further down the road for
    # functionality with moving data from one list (i.e. 'Want to try') to a different list (i.e. "Favorites")
    # wrote code for only choosing list name right now
    # list_type = choice(['Favorites', 'Want to Try', 'Already Visited'])
    #     if list_type == 'Favorites':
    #         list_name = 'Favorites List'
    #     elif list_type == 'Want to Try':
    #         list_name = 'Places I Want To Try'
    #     elif list_type == 'Already Visited':
    #         list_name = 'Roasters I Have Already Tried'

    list_name = choice(['Favorites List', 'Places I Want to Try', 'Roasters I Have Already Tried'])
    list_name2 = choice(['Favorites List', 'Places I Want to Try', 'Roasters I Have Already Tried'])
   
    db_list1 = crud.create_list(list_type=None, list_name=list_name, user=user)
    db_list2 = crud.create_list(list_type=None, list_name=list_name2, user=user)
    

    # Create 4 entries for each list
    for n in range(4):
        entry_list = db_list1
        roaster = choice(list_of_roasters)
        score = randint(1,5)
        note = choice(['Great dark roast.', 'Cute packaging.', 'Sent friendly note with delivery.',
        'Too many options.', 'Very fruity taste.', 'Very chocolatey taste.', 'So smooth.',
        'High caffeine content!', 'Great for pour-overs!', 'Great smell, better taste!'])

        entry = crud.create_entry(entry_list=entry_list, roaster=roaster, score=score, note=note)




# TODO: fix attributes for roasters (links, image, avg rating) and add additional lists for each user