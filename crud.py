'''CRUD operations'''

import googlemaps
from model import db, User, List, Roaster, Entry, connect_to_db
from random import choice


#Connect to DB
if __name__ == '__main__':
    from server import app
    connect_to_db(app)


#Functions

''' User Functions '''

def create_user(first_name, last_name, email, password):

    user = User(first_name=first_name, last_name=last_name, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def get_user_by_email(email):
    '''Query for user by email, return 'None' if no user with that email'''

    return User.query.filter_by(email=email).first()

def get_user_info(email):
    '''Query for user by email, return password and ID associated with account'''

    user = User.query.filter_by(email=email).first()
    user_pw = user.password
    user_id = user.user_id

    return user_pw, user_id

def get_user_by_id(user_id):
    return User.query.get(user_id)


''' Roaster Functions '''    

def create_roaster(name, address, phone_number, hours, place_id, website, avg_user_rating, lat, lng):

    roaster = Roaster(name=name, address=address, phone_number=phone_number, hours=hours,
    place_id=place_id, website=website, avg_user_rating=avg_user_rating, lat=lat, lng=lng)

    db.session.add(roaster)
    db.session.commit()

    return roaster

def return_all_roasters():
    '''Queries for all roaster instances'''

    return Roaster.query.all()

def get_roaster_by_id(roaster_id):
    '''Query for roaster by roaster ID number'''

    return Roaster.query.get(roaster_id)

def calculate_avg_rating(roaster_id):
    ''' Calculate average score from all the scores entered for an individual roaster'''

    # # Query for all roaster objects
    # list_of_roasters = Roaster.query.all()
    
    # # Loop through the list of roaster objects and set roaster_id to each roaster's ID number
    # for roaster in list_of_roasters:
    #     roaster_id = roaster.roaster_id

    # Query for all entry objects associated with a roaster ID, and set to variable 'reviews'
    reviews = Entry.query.filter_by(roaster_id=roaster_id).all()
    roaster = Roaster.query.filter_by(roaster_id=roaster_id).one()

    # Get total number of entries for each roaster
    total_reviews = len(reviews)
    # If no reviews for roaster yet, return message
    if total_reviews == 0:
        roaster_avg = 0
        # return f'No user reviews yet!'

    # Loop through the entry objects for each roaster and capture the score value, add up all scores
    # and then divide by the total number of entries to get average rating
    else:
        sum = 0
        for review in reviews:
            
            score = review.score
            if score != None:
                sum += score
        
        roaster_avg = round( (sum / total_reviews), 2)

        db.session.commit()

        return roaster_avg

def get_roasters_by_rating(rating):
    '''Returns list of roaster objects meeting rating criteria'''

    roasters = Roaster.query.filter(Roaster.avg_user_rating>=rating).all()
    return roasters

def create_photos(roaster_place_ID):
    '''Makes request to API for photo references, which can be used to make
    photo call in front-end'''

    # Sends request to API for place details response for specified roaster place ID
    gmaps = googlemaps.Client('AIzaSyA7kGblloOwNaoFbgZlb3DNRaz-SxRG7SI')
    roaster_photos = []
    response = gmaps.place(roaster_place_ID, fields=['photo'])
    
    # Determines if response contains any photo information for roaster
    if response['result'].get('photos') is None:
        roaster_photos = 'Unavailable'
    # Keys into photo details response and creates list of photo reference ID's 
    # for roaster, returns list
    else:
        photos = response['result']['photos']
        for photo in photos[1::]:
            roaster_photos.append(photo['photo_reference'])
    
    return roaster_photos

def get_user_review_by_roaster(roaster_id):
    '''Queries for entries made for roaster, returns random choice of entry's note value and note author(user)'''

    entries = Entry.query.filter_by(roaster_id=roaster_id).all()
    if entries:
        review = choice(entries)
        note = review.note
        author = review.entry_list.user.first_name + ' ' + review.entry_list.user.last_name
    else:
        review = None
        note = None
        author = None


    return note, author



''' List Functions '''

def create_list(list_name, user):

    new_list = List(list_name=list_name, user=user)

    db.session.add(new_list)
    db.session.commit()

    return new_list

def get_lists_by_user_id(user_id):
        
    return List.query.filter_by(user_id=user_id).all()


def get_entries_by_list_id(list_id):
    entries = Entry.query.filter_by(list_id=list_id).all()
    if entries == []:
        return f'This list is empty!'
    else:
        return entries

def get_list_by_name(user_id, name):
    return List.query.filter_by(user_id=user_id, list_name=name).one()

def get_list_by_list_id(list_id):
    return List.query.filter_by(list_id=list_id).one()


''' Entry Functions '''

def create_entry(entry_list, roaster, score, note):

    entry = Entry(entry_list=entry_list, roaster=roaster, score=score, note=note)

    db.session.add(entry)
    db.session.commit()

    return entry

def get_entry_by_entry_id(entry_id):
    return Entry.query.filter_by(entry_id=entry_id).one()

def change_list_id(entry, new_list):
    entry.list_id = new_list
    db.session.commit()

    return entry

def add_rating_to_entry(entry, rating):
    entry.score = rating
    db.session.commit()

    return entry

def add_note_to_entry(entry, note):
    entry.note = note
    db.session.commit()

    return entry
