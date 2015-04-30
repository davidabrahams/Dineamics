__author__ = 'alixmccabe'
FILE_NAME = 'database.txt'

import user

def rank_to_score(rank):
    """
    :param rank: The rank of a restaurant, returned by a Yelp API query (ie, the first restaurant would be rank 0, the second rank 1)
    :return: A score for how many points to give that restaurant. 40 for the best, 39 for second, etc.
    """
    return 40 - rank

def rank_to_score_price(rank, user_price, rest_price):
    """
    :param rank: The rank of a restaurant, returned by a Yelp API query (ie, the first restaurant would be rank 0, the second rank 1)
    :param user_price: The price a user is willing to pay for the restaurant
    :param rest_price: The average price of mains at a restaurant
    :return: A score for how many points to give that restaurant. Similiar to rank_to_score(), but with a price deduction
    """
    deduction = 0
    if rest_price != None and (rest_price > user_price):
        deduction = (rest_price - user_price + 0.0) / user_price * 30
    return 40 - rank - deduction


def get_rest_score_dict(list_of_lists_of_restaurants, users, weights):
    """
    :param list_of_lists_of_restaurants: a list of lists of restaurant, where each list corresponds to the restaurant returned to a User by a Yelp query.
    :param users: A list of Users.
    :param weights: A list, where each number corresponds to how heavily to wait to corresponding user.
    :return: A dict mapping from Restaurant to its score, which represents how well it matches the users.
    """
    rest_to_score = {}
    for list, user, weight in zip(list_of_lists_of_restaurants, users, weights):
        for i, restaurant in enumerate(list):
            # If the restaurant is in the dictionary, increment its score. Otherwise, add the restaurant to the dictionary.
            if restaurant in rest_to_score:
                rest_to_score[restaurant] += rank_to_score_price(i, user.price_max, restaurant.price) * weight
            else:
                rest_to_score[restaurant] = rank_to_score_price(i, user.price_max, restaurant.price) * weight

    return rest_to_score

def get_cat_score_dict(list_of_lists_of_restaurants):
    """
    :param list_of_lists_of_restaurants: a list of lists of restaurant, where each list corresponds to the restaurant returned to a User by a Yelp query.
    :return: a dict mapping from a category to score.
    """
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
    """
    :param score_dict: a dict mapping from something to score
    :return: a list of tuples of (key, value) pairs of the dict sorted according to their values
    """
    scored_cats = [(k, v) for k, v in score_dict.iteritems()]
    sort = sorted(scored_cats, reverse=True, key=lambda x: x[1])

    return sort


def extract_from_list(sorted_cats):
    """
    :param sorted_cats: a list of tuples sorted according to values
    :return: the first values of the tuples
    """
    categories = []
    for cat, score in sorted_cats:
        categories.append(cat)
    return categories


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


if __name__ == '__main__':

    users = user.create_users()
    for rest in get_best_restaurants(users):
        pass
        print str(rest)
    
   