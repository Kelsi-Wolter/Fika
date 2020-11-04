'''CRUD operations'''

from model import db, User, List, Roaster, Entry, connect_to_db


#Connect to DB
if __name__ == '__main__':
    from server import app
    connect_to_db(app)

#Functions

def create_user(first_name, last_name, email, password):

def create_roaster(name, address, phone_number, hours, image, website, coffee_link, shipping_link, avg_rating):

def create_list(list_type, list_name, user)

def create_entry(entry_list, roaster, score, note):

