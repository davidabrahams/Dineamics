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
    return 20 - rank

def get_rest_score_dict(list_of_lists_of_restaurants):
    rest_to_score = {}

    for list in list_of_lists_of_restaurants:
        for i, restaurant in enumerate(list):

            for j, category in restaurant.categories:
                category = category.encode('utf-8')
                key = category

                if key not in rest_to_score:
                    rest_to_score[category] = rank_to_score(i)

                else:
                    print 'Duplicate'
                    rest_to_score[category] += rank_to_score(i)

    return rest_to_score

def get_best_rests(score_dict):
    scored_rests = [(k,v) for k,v in score_dict.iteritems()]
    sort = sorted(scored_rests, reverse=True, key=lambda x: x[1])

    return sort

def get_top_categories(sorted_rests):
    categories = []
    for tup in sorted_rests:
        categories.append(tup[0])
    return categories

def get_top_rest(best_rests):
    top_rest = best_rests[0][0]
    top_rest.price = locu_setup.get_price_of_mains(top_rest.unencoded_name, top_rest.locality)
    return best_rests[0][0]

def get_cat_restaurant(categories,location,price):
    if len(categories)<=4:
        categories = str(categories[0:3])
    else:
        categories = categories
    
    print categories
    responses = api.get_restaurants(categories,location)
    best_rests = []

    database = locu_database.load(FILE_NAME)
    #TODO: search each restaurant in database with new categories
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

        price = locu_setup.get_price_of_mains(menu)

        rest = restaurant.Restaurant(name, address, locality, categories, price, image, unenc_name)
        best_rests.append(rest)

    return best_rests

def get_best_restaurant(best_rests,price):
    #TODO: NOT FUCKING WORKING SHIT
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

    print 'Your Restaurant is: ' + best_rest.name +' in ' + best_rest.locality + ' for $' + str(best_rest.price) + '!!'

if __name__ == '__main__':
    users = user.create_users()
    user_rests = user.get_users_restaurants(users)
    location = user.optimize_price_location(users)[1]
    price = user.optimize_price_location(users)[0]
    score_dict = get_rest_score_dict(user_rests)
    sorted_rests = get_best_rests(score_dict)
    best_rests = get_cat_restaurant(sorted_rests,location,price)
    print get_best_restaurant(best_rests,price)
    #TODO: 
    #create optimizing price/location programs
    #feed in optimized price and location from users
    
   