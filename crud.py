'''CRUD operations'''

import googlemaps
from model import db, User, List, Roaster, Entry, connect_to_db


#Connect to DB
if __name__ == '__main__':
    from server import app
    connect_to_db(app)


#Functions

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


    

def create_roaster(name, address, phone_number, hours, place_id, website, coffee_link, shipping_link, images, avg_user_rating):

    roaster = Roaster(name=name, address=address, phone_number=phone_number, hours=hours,
    place_id=place_id, website=website, coffee_link=coffee_link, shipping_link=shipping_link, images=images, avg_user_rating=avg_user_rating)

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
        return f'No user reviews yet!'

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
    roasters = Roaster.query.filter(Roaster.avg_user_rating>=rating).all()
    return roasters


def create_photos(roaster_place_ID):
    gmaps = googlemaps.Client('AIzaSyA7kGblloOwNaoFbgZlb3DNRaz-SxRG7SI')
    roaster_photos = []
    # for roaster in place_ids:
        # Sends request to API for specified fields on each roaster ID
    response = gmaps.place(roaster_place_ID, fields=['photo'])
    # Keys into response "result" key to use as values for each roaster ID key
    if response['result'].get('photos') is None:
        roaster_photos = 'Unavailable'
    else:
        photos = response['result']['photos']
        # photos_dict[roaster] = []

        for photo in photos:
            roaster_photos.append(photo['photo_reference'])
    
    return roaster_photos


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
