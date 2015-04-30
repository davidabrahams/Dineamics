## Synopsis

Dineamics is a mobile-optimized web app that allows multiple users to input their cuisine preference, price range, and location, and returns a single restaurant with the intent of satisfying each user’s desires. Dineamics tells the users the average price at this restaurant, and redirects them to the restaurant’s Yelp page if they request more information on the restaurant. If the users do not like the Dineamics recommended restaurant, they have the option of getting a new suggestion.

## Motivation

When choosing where to eat out, the process is fairly simple. You either go to your favorite restaurant, or wherever is convenient and cheap, or maybe you search Yelp for the cuisine you are in the mood for. However, if two friends are choosing where to eat together, the process becomes much more problematic. You both have different price points, cuisine preferences, and priorities. Groups of friends tend to either keep suggesting restaurants, none of which anyone can agree upon, or worse, no one makes any suggestions at all. We decided to create a technical solution to this real life problem.

## Running our app

Our application has been tested using Python 2.7. To run our application locally, run

    $ python app/app.py

In a web browser, navigate to the address specified by your terminal output. For me, this was

    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    * Restarting with stat

Certain dependencies may need to be filled. Try the following commands to install the Python packages necessary:

    $ pip install oauth2
    $ pip install unidecode
    $ pip install flask

## Contributors

David Abrahams, TJ Kim, Alix McCabe, Hannah Twigg-Smith,