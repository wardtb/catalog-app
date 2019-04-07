from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    flash
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = \
    json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

# Database connection code

engine = create_engine('postgresql:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Routing

# Authentication


@app.route('/login')
def showLogin():
    ''' Displays login page

    Returns:
        login page
    '''

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# The gconnect and gdisconnect functions for Google authenthication


@app.route('/gconnect', methods=['POST'])
def gconnect():
    ''' Connects to Google authentication

    Returns:
        Redirect to homepage with success or error message

    '''
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that access toke and ID match login session
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = \
          make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;'
    'border-radius: 150px;'
    '-webkit-border-radius: 150px;'
    '-moz-border-radius: 150px;">'
    print "done!"
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.created_date.desc()).limit(10)
    return render_template(
        "categories.html",
        categories=categories,
        items=items)


@app.route('/gdisconnect')
def gdisconnect():
    ''' Disconnects from Google authentication

    Returns:
        Redirect to homepage with success or error message

    '''
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        categories = session.query(Category).all()
        items = session.query(Item).order_by(Item.created_date.desc()).limit(10)
        return render_template(
            "categories.html",
            categories=categories,
            items=items)
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
@app.route('/categories/')
def showCategories():
    ''' Shows all categories in the database as well as the 10 most recently
    edited items across all categories.

    Returns:
        page with categories
    '''
    # Get necessary information from database
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.created_date.desc()).limit(10)

    # Handle GET request
    return render_template(
        "categories.html",
        categories=categories,
        items=items,
        login_session=login_session)


@app.route('/categories/<int:category>/')
@app.route('/categories/<int:category>/items/')
def showItems(category):
    ''' Shows all items from a given category in the database.

    Args:
        category: category to display items

    Returns:
        page with items from category
    '''
    # Get necessary information from database
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category_id=category).all()
    category = session.query(Category).filter_by(id=category).first()

    # Handle GET request
    return render_template(
        "items.html",
        category=category,
        items=items,
        categories=categories,
        login_session=login_session)


@app.route('/categories/<int:category>/items/<int:item>/')
def showItem(category, item):

    ''' Shows an item in the database.

    Args:
        category: category of item to show
        item: item to be displayed

    Returns:
        page with item details
    '''
    # Get necessary information from database
    categories = session.query(Category).all()
    itemToShow = session.query(Item).filter_by(id=item).first()
    itemCategory = session.query(Category).filter_by(id=category).first()

    # Handle GET request
    return render_template(
        "item.html",
        category=itemCategory,
        item=itemToShow,
        categories=categories,
        login_session=login_session)


@app.route(
    '/categories/<int:category>/items/<int:item>/edit',
    methods=['GET', 'POST'])
def editItem(category, item):

    ''' Edits an item in the database.

    Args:
        category: category of item to edit
        item: item to be edited

    Returns:
        on GET: page to edit an item
        on POST: Redirect to all items in the item's category
    '''

    # Only allow logged in users to edit items
    if 'username' not in login_session:
        return redirect('/login')

    # Get necessary information from database
    categories = session.query(Category).all()
    itemToEdit = session.query(Item).filter_by(id=item).first()
    itemCategory = session.query(Category).filter_by(id=category).first()
    user = session.query(User).filter_by(id=itemToEdit.user_id).first()

    # Handle POST request
    if request.method == 'POST':
        if request.form['name']:
            itemToEdit.name = request.form['name']
        if request.form['description']:
            itemToEdit.description = request.form['description']
        if user.email != login_session['email']:
            flash("You are not authorized to edit this item")
            return redirect(url_for('newItem', category=category))
        session.add(itemToEdit)
        session.commit()
        flash("item updated")
        return redirect(url_for('showItems', category=category))

    # Handle GET request
    else:
        return render_template(
            "edititem.html",
            category=itemCategory,
            item=itemToEdit,
            categories=categories,
            login_session=login_session)


@app.route(
    '/categories/<int:category>/items/<int:item>/delete',
    methods=['GET', 'POST'])
def deleteItem(category, item):
    ''' Deletes an item in the database upon user confirmation.

    Args:
        category: category of item to delete
        item: item to be deleted

    Returns:
        page with remaining items in category
    '''
    # Only allow logged in users to delete items
    if 'username' not in login_session:
        return redirect('/login')

    # Get necessary information from database
    categories = session.query(Category).all()
    itemToDelete = session.query(Item).filter_by(id=item).first()
    itemCategory = session.query(Category).filter_by(id=category).first()
    user = session.query(User).filter_by(id=itemToDelete.user_id).first()
    # Handle POST request
    if request.method == 'POST':
        if user.email != login_session['email']:
            flash("You are not authorized to delete this item")
            return redirect(url_for(
                'showItem',
                category=category,
                item=itemToDelete.id
            ))
        session.delete(itemToDelete)
        session.commit()
        flash("item deleted")
        return redirect(url_for('showItems', category=category))

    # Handle GET request
    else:
        return render_template(
            "deleteitem.html",
            category=itemCategory,
            item=itemToDelete,
            categories=categories,
            login_session=login_session)


@app.route('/categories/<int:category>/items/new', methods=['GET', 'POST'])
def newItem(category):
    ''' Creates an item in the database.

    Args:
        category: category of item to create

    Returns:
        page with all items in category
    '''
    # Only allow logged in users to delete items
    if 'username' not in login_session:
        return redirect('/login')

    # Get necessary information from database
    categories = session.query(Category).all()
    itemCategory = session.query(Category).filter_by(id=category).first()

    # Handle POST request
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'],
            user_id=1,
            category_id=category,
            description=request.form['description'])
        session.add(newItem)
        session.commit()
        flash("item successfully created")
        return redirect(url_for('showItems', category=category))

    # Handle GET request
    else:
        return render_template(
            "newitem.html",
            category=itemCategory,
            categories=categories,
            login_session=login_session)

# JSON format of Catalogs and Items


@app.route('/catalog.json')
def showJSON():
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return jsonify(
        Items=[i.serialize for i in items],
        Categories=[j.serialize for j in categories])

# Threading is disabled due to issues with SQLAlchemy not using threading
# Secret Key set to "super_secret_key" only for development purposes
# Secret Key must be changed for production use.


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='52.43.135.40', port=80, threaded=False)
