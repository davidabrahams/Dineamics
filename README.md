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

## Optimization Algorithm

The following is a code excerpt showing how we optimize the restaurants based on multiple users.

	def get_best_restaurants(users):
	    """
	    :param users: a list of Users
	    :return: The top restaurants, optimized for the user group.
	    """
	    users_to_test = list(users)
	    # set the initial user weights to 1.0
	    weights = [1.0] * len(users_to_test)

	    # find the top categories for the users by first getting their restaurants
	    user_rests = user.get_users_restaurants(users)
	    # then getting the top categories
	    cat_dict = get_cat_score_dict(user_rests)
	    categories = extract_from_list(get_sorted_as_list(cat_dict))

	    # get the average price and location for users
	    price, location = user.average_price_location(users)

	    # search for up to 3 additional categories
	    new_cats = []
	    current_terms = [u.term.lower() for u in users]
	    index = 0
	    count = 0
	    while count < 3 and index < len(categories):
	        if categories[index] not in current_terms:
	            count += 1
	        new_cats.append(categories[index])
	        index += 1
	    for c in new_cats:
	        users_to_test.append(user.User(c, location, price))
	        weights.append((cat_dict[c] + 0.0) / cat_dict[new_cats[0]])

	    # get the restaurants from our original users and the top categories
	    rests_to_score = user.get_users_restaurants(users_to_test)
	    print "Using weights: " + str(weights)

	    # return the top restaurants
	    rest_score_dict = get_rest_score_dict(rests_to_score, users, weights)
	    return extract_from_list(get_sorted_as_list(rest_score_dict))

## Contributors

David Abrahams, TJ Kim, Alix McCabe, Hannah Twigg-Smith,