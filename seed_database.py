'''Script to seed database'''

import os
import json
from random import choice, randint

import crud
import model
import server

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

list_of_users = []
# Create 10 users; 
for n in range(10):
    email = f'user{n}@test.com' 
    password = 'test'
    first_name = choice([Jane, John, Zella, Jordan, Nick, Rachel, Thomas, Trish, Micah, Jack])
    last_name = choice([Wolter, Adair, Morgan, Lewis, Hepper, Marin, Knutsen, Wagner, Torke])

    user = crud.create_user(first_name, last_name, email, password)

    list_of_users.append(user)

#Create 2 lists for each user

for user in list_of_users:
    list_type = choice(['Favorites', 'Want to Try', 'Already Visited'])
        if list_type == 'Favorites':
            list_name = 'Favorites List'
        elif list_type == 'Want to Try':
            list_name = 'Places I Want To Try'
        elif list_type == 'Already Visited':
            list_name = 'Roasters I Have Already Tried'
    
    new_list = List(list_type=list_type, list_name=list_name, user=user)

    for n in range(4):
        entry_list = new_list
        roaster = choice(list_of_roasters***)
        score = randint(1,5)
        note = choice(['Great dark roast.', 'Cute packaging.', 'Sent friendly note with delivery.',
        'Too many options.', 'Very fruity taste.', 'Very chocolatey taste.', 'So smooth.',
        'High caffeine content!', 'Great for pour-overs!', 'Great smell, better taste!'])

        entry = Entry(entry_list=entry_list, roaster=roaster, score=score, note=note)

        crud.create_entry(entry)




    # for _ in range(10):
    #     random_movie = choice(movies_in_db)
    #     score = randint(1, 5)

    #     crud.create_rating(user, random_movie, score)