'''CRUD operations'''

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


    

def create_roaster(name, address, phone_number, hours, image, website, coffee_link, shipping_link):

    roaster = Roaster(name=name, address=address, phone_number=phone_number, hours=hours,
    image=image, website=website, coffee_link=coffee_link, shipping_link=shipping_link)

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
    ''' Calculate average score from all the scores entered for each individual roaster'''

    # # Query for all roaster objects
    # list_of_roasters = Roaster.query.all()
    
    # # Loop through the list of roaster objects and set roaster_id to each roaster's ID number
    # for roaster in list_of_roasters:
    #     roaster_id = roaster.roaster_id

    # Query for all entry objects associated with a roaster ID, and set to variable 'reviews'
    reviews = Entry.query.filter_by(roaster_id=roaster_id).all()

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
            sum += score
        
        roaster_avg = sum / total_reviews

        return round(roaster_avg, 2)


def create_list(list_type, list_name, user):

    new_list = List(list_type=list_type, list_name=list_name, user=user)

    db.session.add(new_list)
    db.session.commit()

    return new_list

def get_lists_by_user_id(user_id):
    lists = List.query.filter_by(user_id=user_id).all()
    list_entries = []
    for list in lists:
        list_entries.append(list.entries)
    
    return lists, list_entries

def create_entry(entry_list, roaster, score, note):

    entry = Entry(entry_list=entry_list, roaster=roaster, score=score, note=note)

    db.session.add(entry)
    db.session.commit()

    return entry
