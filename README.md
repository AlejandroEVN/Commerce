## AlejandroEVN

### Project Commerce 

This is an commerce web application, very much like ebay. Allows users to upload the items they want to sell, place bids on other items, add them to their watchlist 
and add comments on an item.

This was the second project made with Django.
The goal for this project was to practice with Django models, managing the data coming from the front end
and the interactions with HTML templates, e.g. by creating custom template tags.

#### Demo
<img src="./auctions/demo/commerce-demo1.gif" width="960" height="540" />
<img src="./auctions/demo/commerce-demo2.gif" width="960" height="540" />
<img src="./auctions/demo/commerce-demo3.gif" width="960" height="540" />
#### Routes

`url: /`
Main page. Displays two lists. One contains the active listings, whereas the second one contains the closed listings.

`url: /login` `url: /register`
Renders corresponding HTML.

`url: /logout`

`url: /add_listing`
Allows users to add a listing to the database. Redirects to `url: /`.

`url: /listing/<str:item_id>`
Renders HTML page that shows the requested listing item.

`url: /listing/<str:item_id>/<str:message>`
Returns listing page with a message (when an error occurs or similar).

`url: /add_to_watchlist/<str:item_id>` `url: /remove_from_watchlist/<str:item_id>` 
Allows the user to add/remove a listing to their watchlist. Redirects to watchlist page.

`url: /watchlist`  
Shows a list with the users watchlisted items.

`url: /add_comment/<str:item_id>`  
Allows users to add comment in the item's listing page. Redirects to said page.

`url: /add_bid/<str:item_id>`  
Allows users to place a bid on an listing. Redirects to the listing's page.

`url: /close_auction/<str:item_id>`  
Allows the owner of the listing to close the auction. Redirects to main page.

`url: /categories/search`  
Allows users to look for a listing of the selected category.

#### Installation

- Clone into your machine
- Open a terminal
- Cd into projects' folder
- Run `pip install requirements.txt` (ideally in a virtual environment)
- Run `py manage.py runserver`
- Open browser and navigate to `127.0.0.1:<your Django local port>`

#### Tech Stack
- Python
- Django
- Bootstrap
- Sass
