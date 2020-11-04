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

def create_roaster(name, address, phone_number, hours, image, website, coffee_link, shipping_link, avg_rating):

    roaster = Roaster(name=name, address=address, phone_number=phone_number, hours=hours,
    image=image, website=website, coffee_link=coffee_link, shipping_link=shipping_link,
    avg_rating=avg_rating)

    db.session.add(roaster)
    db.session.commit()

    return roaster

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
