__author__ = 'alixmccabe'
import user
import restaurant
import locu_setup
import api
import restaurant_attribute_parser
import restaurant


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

def get_cat_restaurant(categories,location):
    categories = str(categories)
    response = api.get_restaurant(categories,location)

    name = restaurant_attribute_parser.get_name(response)
    address = restaurant_attribute_parser.get_address(response)
    locality = restaurant_attribute_parser.get_locality(response)
    attribute_categories = restaurant_attribute_parser.get_categories(response)
    image = restaurant_attribute_parser.get_image(response)
    price = get_top_rest
    unenc_name = restaurant_attribute_parser.get_name_nonenc(response)

    best_rest = restaurant.Restaurant(name, address, locality, categories, price, image, unenc_name)
    print 'Your Restaurant is: ' + best_rest.name +' in ' + locality + '!'

if __name__ == '__main__':
    users = user.create_users()
    user_rests = user.get_users_restaurants(users)
    location = 'boston'
    score_dict = get_rest_score_dict(user_rests)
    sorted_rests = get_best_rests(score_dict)
    print get_cat_restaurant(sorted_rests,location)
    
   