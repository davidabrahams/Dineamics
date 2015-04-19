__author__ = 'alixmccabe'
import user
import restaurant
import locu_setup
import api
import restaurant_attribute_parser
import restaurant
import locu_database

FILE_NAME = 'database.txt'


def rank_to_score(rank):
    return 40 - rank


def get_cat_score_dict(list_of_lists_of_restaurants):
    cat_to_score = {}

    for list in list_of_lists_of_restaurants:
        for i, restaurant in enumerate(list):
            for category in restaurant.categories:
                category = category.encode('utf-8')
                key = category.lower()
                if key not in cat_to_score:
                    cat_to_score[key] = rank_to_score(i)
                else:
                    cat_to_score[key] += rank_to_score(i)

    return cat_to_score


def get_sorted_cats_as_list(score_dict):
    scored_cats = [(k, v) for k, v in score_dict.iteritems()]
    sort = sorted(scored_cats, reverse=True, key=lambda x: x[1])

    return sort


def extract_cats_from_list(sorted_cats):
    categories = []
    for cat, score in sorted_cats:
        categories.append(cat)
    return categories


def get_cat_restaurant(cat_dict, location, price):
    sorted_cats = get_sorted_cats_as_list(cat_dict)
    categories = extract_cats_from_list(sorted_cats)

    if len(categories) > 3:
        categories = categories[0:3]
    string_to_search = ' '.join(categories)

    print 'Querying yelp using the categories: ' + string_to_search + '. Location: ' + location + '...'
    responses = api.get_restaurant_responses(string_to_search, location)
    best_rests = []

    database = locu_database.load(FILE_NAME)
    # TODO: search each restaurant in database with new categories
    #select restaurant with closest price
    for i, response in enumerate(responses):

        name = restaurant_attribute_parser.get_name(response)
        address = restaurant_attribute_parser.get_address(response)
        locality = restaurant_attribute_parser.get_locality(response)
        attribute_categories = restaurant_attribute_parser.get_categories(response)
        image = restaurant_attribute_parser.get_image(response)
        unenc_name = restaurant_attribute_parser.get_name_nonenc(response)

        if ((unenc_name, locality)) in database.data:
            print 'Found ' + unenc_name + ' in database!'
            menu = database.data[(unenc_name, locality)]
        else:
            print 'Querying Locu for ' + unenc_name + '...'
            menu = locu_setup.get_menu(unenc_name, locality)
            database.data[(unenc_name, locality)] = menu

        rest_price = locu_setup.get_price_of_mains(menu)

        rest = restaurant.Restaurant(name, address, locality, attribute_categories, rest_price, image, unenc_name)
        best_rests.append(rest)
    print 'Saving database...'
    print
    database.save(FILE_NAME)
    return best_rests


def get_best_restaurant(best_rests, price):
    # TODO: NOT FUCKING WORKING SHIT
    best_rest = best_rests[0]

    for i, restaurant in enumerate(best_rests):
        print restaurant.price
        if restaurant.price == None:
            best_rest = best_rest

        elif restaurant.price < price:
            best_rest = restaurant
            price = restaurant.price

        else:
            best_rest = best_rest

    print 'Your Restaurant is: ' + best_rest.name + ' in ' + best_rest.locality + ' for $' + str(best_rest.price) + '!!'


if __name__ == '__main__':
    users = user.create_users()
    user_rests = user.get_users_restaurants(users)
    price, location = user.optimize_price_location(users)
    score_dict = get_cat_score_dict(user_rests)
    best_rests = get_cat_restaurant(score_dict, location, price)
    for rest in best_rests:
        print str(rest)
    # print get_best_restaurant(best_rests, price)
    # TODO:
    #create optimizing price/location programs
    #feed in optimized price and location from users
    
   