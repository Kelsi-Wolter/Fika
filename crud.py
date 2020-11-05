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
    '''Query for user by email, return password associated with account'''

    user = User.query.filter_by(email=email).first()
    user_pw = user.password
    user_id = user.user_id

    return user_pw, user_id

def get_user_by_id(user_id):
    return User.query.get(user_id)


    

def create_roaster(name, address, phone_number, hours, image, website, coffee_link, shipping_link, avg_rating):

    roaster = Roaster(name=name, address=address, phone_number=phone_number, hours=hours,
    image=image, website=website, coffee_link=coffee_link, shipping_link=shipping_link,
    avg_rating=avg_rating)

    db.session.add(roaster)
    db.session.commit()

    return roaster

def return_all_roasters():
    '''Queries for all roaster instances'''

    return Roaster.query.all()

def get_roaster_by_id(roaster_id):
    '''Query for roaster by roaster ID number'''

    return Roaster.query.get(roaster_id)


def create_list(list_type, list_name, user):

    new_list = List(list_type=list_type, list_name=list_name, user=user)

    db.session.add(new_list)
    db.session.commit()

    return new_list

def create_entry(entry_list, roaster, score, note):

    entry = Entry(entry_list=entry_list, roaster=roaster, score=score, note=note)

    db.session.add(entry)
    db.session.commit()

    return entry
