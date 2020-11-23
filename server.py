from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, LoginForm, NewUserForm, User, db, List, Entry, Roaster
import crud, json

from jinja2 import StrictUndefined

from datetime import datetime
# from flask_login import LoginManager



app = Flask(__name__)
app.secret_key = "kelsi's_project"


# Home page
@app.route('/')
def homepage():
    '''View Homepage'''

    return render_template('homepage.html')

# Roaster Routes
@app.route('/roaster_directory')
def roaster_directory():
    '''Display list of roasters'''

    # input = request.args.get("rating")

    # if input != None:
    #     input = int(input)
    #     all_the_roasters = crud.get_roasters_by_rating(rating=input)
    # else:
    all_the_roasters = crud.return_all_roasters()  
    
    # Gets title photo using API call in front end, no longer using
    # for roaster in all_the_roasters:
    #     photos = crud.create_photos(roaster.place_id)
    #     title_photo = photos[0]
    #     setattr(roaster, 'image', title_photo)

    return render_template('roaster_directory.html', roasters=all_the_roasters)

@app.route('/filter')
def filter_roasters():
    '''Show roasters that meet the criteria of the user input for filter'''

    input = request.args.get("rating")
    input = int(input)
    all_the_roasters = crud.get_roasters_by_rating(rating=input)

    # Get title photo w/API call in front-end, no longer using
    # for roaster in all_the_roasters:
    #     photos = crud.create_photos(roaster.place_id)
    #     title_photo = photos[0]
    #     setattr(roaster, 'image', title_photo)

    return render_template('filtered_roasters.html', roasters=all_the_roasters)


@app.route('/roaster_directory/<roaster_id>')
def roaster_details_page(roaster_id):
    '''Show details of a particular roaster'''

    roaster = crud.get_roaster_by_id(roaster_id)

    schedule = roaster.hours
    schedule = schedule.strip('{}').replace('"','').split(",")

    avg_rating = roaster.avg_user_rating
    if avg_rating == 0:
        avg_rating = 'No reviews yet!'

    # avg_rating = crud.calculate_avg_rating(roaster_id)

    photos = crud.create_photos(roaster.place_id)
    # photos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    return render_template('roaster_details.html', roaster=roaster, schedule=schedule, avg_rating=avg_rating, photos=photos)

# User login and account routes
@app.route('/login', methods=["GET", "POST"])
def login_to_account():
    '''Log in page for users'''

    form = LoginForm()

    email = form.email.data
    pw = form.password.data

    
    if form.validate_on_submit():
        user = crud.get_user_by_email(email)
        if user:
            user_pw, user_id = crud.get_user_info(email)
            if pw == user_pw:
                session['user'] = user_id
                return redirect(f'/account/{user_id}')
            else:
                flash('Incorrect password! Please try again.')
        else:         
            flash('Please create an account.')
            return redirect('/create_account')

    return render_template('login.html', form=form)


@app.route('/log_out')
def log_user_out():
    del session['user']

    return redirect('/')


@app.route('/account/<user_id>')
def user_account_page(user_id):
    '''Show user's account page'''

    # Retrieve user from DB by ID, retrieve lists and list entries from user object
    user = crud.get_user_by_id(user_id)
    user_lists = crud.get_lists_by_user_id(user_id)
    list1, list2 = user_lists[0], user_lists[1]

    list1_entries = crud.get_entries_by_list_id(list1.list_id)
    list2_entries = crud.get_entries_by_list_id(list2.list_id)

    return render_template('account.html', user=user, list1=list1, list2=list2, list1_entries=list1_entries, list2_entries=list2_entries)

# New user routes
@app.route('/create_account', methods=["GET", "POST"])
def new_account_page():
    '''Show form to enter details to create new account, create new user & auto-populate lists upon form submit'''

    new_user_form = NewUserForm()

    fname = new_user_form.fname.data
    lname = new_user_form.lname.data
    email = new_user_form.email.data
    pw = new_user_form.password.data

    user = crud.get_user_by_email(email)

    if new_user_form.validate_on_submit():

        if user:

            flash('Account already exists! Please login to continue.')
            return redirect ('/login')

        else:
            new_user = crud.create_user(fname, lname, email, pw)
            crud.create_list(list_name='My Favorites', user=new_user)
            crud.create_list(list_name='My Roasters', user=new_user)

            flash('Account created! Please log in.')
            return redirect ('/login')
    else:

        return render_template('create_account.html', form=new_user_form)

@app.route('/add_to_fav_list')
def add_to_fav_list():
    '''Add roaster as entry to user's favorite list'''

    roaster_id = request.args.get("roaster")

    roaster = crud.get_roaster_by_id(roaster_id)

    user_id = session['user']

    fav_list = crud.get_list_by_name(user_id=user_id, name='My Favorites')

    new_entry = crud.create_entry(entry_list=fav_list, roaster=roaster, score=None, note=None)
    return f'{roaster.name} was added to your {fav_list.list_name} list!'

@app.route('/add_to_roaster_list')
def add_to_roaster_list():
    '''Add roaster as entry to user's roaster list'''

    roaster_id = request.args.get("roaster")

    roaster = crud.get_roaster_by_id(roaster_id)

    user_id = session['user']

    roaster_list = crud.get_list_by_name(user_id=user_id, name='My Roasters')

    new_entry = crud.create_entry(entry_list=roaster_list, roaster=roaster, score=None, note=None)
    return f'{roaster.name} was added to your {roaster_list.list_name} list!'


@app.route('/move_entry', methods=["POST"])
def move_entry():
    '''Move entry from one list to the other'''

    #use entry ID to call entry
    entry_id = request.form.get("entry")
    entry = crud.get_entry_by_entry_id(entry_id)

    #find current list id for entry
    current_list = entry.list_id

    # Find list_id to change entry to (new_list)
    lists = crud.get_lists_by_user_id(session['user'])

    for li in lists:
        list_id = li.list_id
        if list_id != current_list:
            new_list = list_id
    
    # Update entry in DB
    updated_entry = crud.change_list_id(entry=entry, new_list=new_list)


    return f'{entry.roaster.name} was moved to your Roasters List!'

@app.route('/delete_entry', methods=["POST"])
def delete_entry():
    '''Delete entry from DB list'''

    #use entry ID to call entry
    entry_id = request.form.get("entry")
    entry = crud.get_entry_by_entry_id(entry_id)

    db.session.delete(entry)
    db.session.commit()

    return f'Your entry has been deleted!'


@app.route('/add_entry_rating', methods=["POST"])
def enter_rating_for_entry():
    '''User adding rating to entry for roaster'''

    entry_id = request.form.get("entry")
    rating = request.form.get("input")

    entry = crud.get_entry_by_entry_id(entry_id)

    updated_entry = crud.add_rating_to_entry(entry=entry, rating=rating)

    crud.calculate_avg_rating(entry.roaster_id)

    return f'Your entry for {entry.roaster.name} has been updated!'

@app.route('/add_entry_note', methods=["POST"])
def enter_entry_note():
    '''User adding note to entry for roaster'''

    entry_id = request.form.get("entry")
    note = request.form.get("input")


    entry = crud.get_entry_by_entry_id(entry_id)

    updated_entry = crud.add_note_to_entry(entry=entry, note=note)

    return f'Your entry for {entry.roaster.name} has been updated!'



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)


# @app.route('/test', methods=["POST", "GET"])
# def testing():

#     roaster = crud.get_roaster_by_id(1)
#     photos = crud.create_photos(roaster.place_id)
#     title_photo = photos[0]

#     img = https://maps.googleapis.com/maps/api/place/photo?key=AIzaSyA7kGblloOwNaoFbgZlb3DNRaz-SxRG7SI&maxwidth=800&photoreference=

#     setattr(roaster, 'image', title_photo)

#     return render_template('test.html', roaster=roaster)

# @app.route('/edit_score_entry', methods=["POST"])
# def add_score_to_entry():
#     '''Add score to entry in DB'''

#     #use entry ID to call entry
#     entry_id = request.form.get("entry")
#     entry = crud.get_entry_by_entry_id(entry_id)

    
# ****Old route for logging in user*******
# @app.route('/user_logging_in', methods=["POST"])
# def user_login():
#     '''Check that user exists and redirect to account page if email and password matches'''

#     # Retrieve input from form
#     email = request.form.get('user_email_login')
#     pw = request.form.get('user_password_login')

#     # Check for email in DB to see if user exists
#     user = crud.get_user_by_email(email)     
    
#     # If user exists, validate password and redirect to account page using user_id
#     if user:
#         user_pw, user_id = crud.get_user_info(email)
#         if pw == user_pw:
            
#             session['user_login'] = {'id': user.user_id, 'first_name': user.first_name, 'last_name': user.last_name}
#             return redirect(f'/account/{user_id}')
    
#         else:
            
#             return redirect('/login')
    
#     # If user does not exist, redirect to create an account page
#     else:
#         flash('Please create an account.')
#         return redirect('/create_account')



# ****Old route for adding new user*******
# @app.route('/new_user', methods=['POST'])
# def register_user():
#     '''Take input from form and create new user login'''

#     fname = request.form.get('fname_create')
#     lname = request.form.get('lname_create')
#     email = request.form.get('email_create')
#     pw = request.form.get('pw_create')
    
#     user = crud.get_user_by_email(email)


#     if user:
#         flash('Account already exists! Please login to continue.')
#         return redirect ('/login')

#     else:
#         crud.create_user(fname, lname, email, pw)

#         flash('Account created! Please log in.')
#         return redirect ('/login')


# ************Routes for list creation************
# @app.route('/create_new_list')
# def create_new_list():

#     all_the_roasters = crud.return_all_roasters()
#     user = crud.get_user_by_id(session['user'])

#     return render_template('new_list.html', roasters=all_the_roasters, user=user)

# @app.route('/account/<user_id>/add_new_list')
# def commit_new_list(user_id):
#     list_name = request.args.get('list_type')
#     user = crud.get_user_by_id(user_id)
    
#     if roasters == True:

#     #     for entry in roasters:
#         roaster_id = request.args.get('roasters')
#         print(roaster_id)

#     #         crud.create_entry(list_id, roaster_id, score)
#     # Need jQuery in here to display more info upon clicking a box for a roaster, so that
#     # user can input a score/note right on that same page

#     created_list = crud.create_list(list_type=None, list_name=list_name, user=user)


#     return redirect(f'/account/{user.user_id}')

