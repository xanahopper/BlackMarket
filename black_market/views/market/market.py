from flask import Blueprint
#from black_market.ext import db
#from black_market.models.models import Course

bp = Blueprint('market', __name__)


@bp.route('/')
def index():
    return "Hello, Welcome to NSD Black Market!"


@bp.route('/course')
def get_all_courses():
    return 'Here are all the courses!'


@bp.route('/course/<int:id>')
def get_course(id=None):
    courses = {'1': 'Microeconomics',
               '2': 'Macroeconomics',
               '3': 'Econometrics'}
    name = courses.get(id)
    if not name:
        return "The course you are looking for is not in the list."
    return "This is course {id}: {name}".format(id=id, name=name)
