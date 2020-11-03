from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
# import crud

from jinja2 import StrictUndefined

from datetime import datetime

app = Flask(__name__)
app.secret_key = 'SECRET KEY GOES HERE'