# Introduction

Sport Catalog is a Flask web application that allows users to browse sporting good items in categories, as well as add, edit, and delete items.
## Dependencies:
* Python Libraries - Flask (1.0.2), SQLAlchemy, random, string, oauth2client, http2lib, json, requests
* SQLite
## Project Contents
* catalog.py - main application
* client_secrets.json - client secrets file for Google authentication
* database_setup.py - file to create SQLite database and populate with tables
* lotsofitems.py - sample data file
* static directory - CSS file
* templates directory - HTML files for displays
## Templates
* categories.html - shows all categories
* deleteitem.html - page to delete items
* edititem.html - page to edit items
* item.html - page to show item details
* items.html - show all items for a category
* layout.html - general display HTML
* login.html - login for Google sign-in
* newitem.html - page to create a new item 

# Installation Instructions

* Google OAuth service setup
* Sign-in requires a Google account. You can create one at https://accounts.google.com/signup/v2/

# Operating Instructions

## Database Setup:
  1. Make sure SQLite is installed
  2. Run database_setup.py to create the necessary tables
  3. Optionally, lotsofitems.py can be run to populate the database with sample data

## Application:
* To run the application, simply run the catalog.py file and view the application in a web browser.


# Flask Catalog Application

This Flask web application allows users to browse sporting good items in categories, as well as add, edit, and delete items.

## Usage

To run the application, simply run the catalog.py file and view the application in a web browser.
