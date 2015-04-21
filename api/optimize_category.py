__author__ = 'alixmccabe'
import user
import restaurant
import locu_setup
import api
import restaurant_attribute_parser
import restaurant
import locu_database
import math
FILE_NAME = 'database.txt'


def rank_to_score(rank):
    return 40 - rank

def get_rest_score_dict(list_of_lists_of_restaurants, weights):
    rest_to_score = {}
    for list, weight in zip(list_of_lists_of_restaurants, weights):
        for i, restaurant in enumerate(list):
            if restaurant in rest_to_score:
                rest_to_score[restaurant] = rest_to_score[restaurant] + rank_to_score(i) * weight
            else:
                rest_to_score[restaurant] = rank_to_score(i) * weight

    return rest_to_score

def get_cat_score_dict(list_of_lists_of_restaurants):
    cat_to_score = {}

    for list in list_of_lists_of_restaurants:
        for i, restaurant in enumerate(list):
            print restaurant.name + 'has categories ' + str(restaurant.categories)
            for category in restaurant.categories:
                category = category.encode('utf-8')
                key = category.lower()
                if key not in cat_to_score:
                    cat_to_score[key] = rank_to_score(i)
                else:
                    cat_to_score[key] += rank_to_score(i)
        print

    return cat_to_score


def get_sorted_as_list(score_dict):
    scored_cats = [(k, v) for k, v in score_dict.iteritems()]
    sort = sorted(scored_cats, reverse=True, key=lambda x: x[1])

    return sort


def extract_from_list(sorted_cats):
    categories = []
    for cat, score in sorted_cats:
        categories.append(cat)
    return categories


def get_best_restaurants(users):
    users_to_test = list(users)
    weights = [1.0] * len(users_to_test)
    user_rests = user.get_users_restaurants(users)
    cat_dict = get_cat_score_dict(user_rests)
    sorted_as_list = get_sorted_as_list(cat_dict)
    categories = extract_from_list(sorted_as_list)
    price, location = user.average_price_location(users)
    new_cats = []
    current_terms = [u.term for u in users]
    index = 0
    while len(new_cats) < 5 and index < len(categories):
        if categories[index] not in current_terms:
            new_cats.append(categories[index])
        index += 1
    for c in new_cats:
        users_to_test.append(user.User(c, location, price))
        weights.append(cat_dict[c] / cat_dict[new_cats[0]])
    rests_to_score = user.get_users_restaurants(users_to_test)
    print "Using weights: " + str(weights)
    rest_score_dict = get_rest_score_dict(rests_to_score, weights)
    return extract_from_list(get_sorted_as_list(rest_score_dict))


if __name__ == '__main__':

    users = user.create_users()
    for rest in get_best_restaurants(users):
        print rest
    
   