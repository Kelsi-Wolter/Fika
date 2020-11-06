from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

from datetime import datetime

app = Flask(__name__)
app.secret_key = "kelsi's_project"

@app.route('/')
def homepage():
    '''View Homepage'''

    return render_template('homepage.html')

@app.route('/roaster_directory')
def roaster_directory():
    '''Display list of roasters'''

    all_the_roasters = crud.return_all_roasters()

    return render_template('roaster_directory.html', roasters=all_the_roasters)

@app.route('/roaster_directory/<roaster_id>')
def roaster_details_page(roaster_id):
    '''Show details of a particular roaster'''

    roaster = crud.get_roaster_by_id(roaster_id)

    schedule = roaster.hours

    avg_rating = crud.calculate_avg_rating(roaster_id)

    return render_template('roaster_details.html', roaster=roaster, schedule=schedule, avg_rating=avg_rating)

@app.route('/login')
def login_to_account():
    '''Log in page for users'''

    return render_template('login.html')

@app.route('/create_account')
def new_account_page():
    '''Show form to enter details to create new account'''

    return render_template('create_account.html')

@app.route('/new_user', methods=['POST', 'GET'])
def register_user():
    '''Take input from form and create new user login'''

    fname = request.form.get('fname_create')
    lname = request.form.get('lname_create')
    email = request.form.get('email_create')
    pw = request.form.get('pw_create')
    
    user = crud.get_user_by_email(email)


    if user:
        flash('Account already exists! Please login to continue.')
    else:
        crud.create_user(fname, lname, email, pw)
        flash('Account created! Please log in.')

    return redirect('/account')


@app.route('/user_logging_in', methods=["POST"])
def user_login():
    '''Check that user exists and redirect to account page if email and password matches'''

    email = request.form.get('user_email_login')
    pw = request.form.get('user_password_login')

    user = crud.get_user_by_email(email)
    user_pw, user_id = crud.get_user_info(email)
    
    if user:
        if pw == user_pw:
            flash('Welcome Back!')
            session['user'] = user
            return redirect(f'/account/{user_id}')
        else:
            flash('Incorrect password, please try again.')
            return redirect('/login')
    else:
        flash('Please create an account.')
        return redirect('/')

@app.route('/account/<user_id>')
def user_account_page(user_id):
    '''Show user's account page'''

    user = crud.get_user_by_id(user_id)
    user_lists, user_list_entries = crud.get_lists_by_user_id(user_id)

    return render_template('account.html', user=user, lists=user_lists, entries=user_list_entries)


# Below route and function needs to be re-written to display user-specific page
# @app.route('/account')
# def account_homepage():

#     return render_template('account.html')




if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)