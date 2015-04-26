__author__ = 'davidabrahams'
from app.api import user


def rank_to_score(rank, user_price, rest_price):
    deduction = 0
    if rest_price != None and (rest_price > user_price):
        deduction = (rest_price - user_price + 0.0) / (user_price) * 20
    return 40 - rank - deduction

def get_rest_score_dict(users, list_of_lists_of_restaurants):
    rest_to_score = {}
    for user, lst in zip(users, list_of_lists_of_restaurants):
        for i, restaurant in enumerate(lst):
            if restaurant in rest_to_score:
                rest_to_score[restaurant] = rest_to_score[restaurant] + rank_to_score(i, user.price_max, restaurant.price)
            else:
                rest_to_score[restaurant] = rank_to_score(i, user.price_max, restaurant.price)

    return rest_to_score

def get_best_rests(score_dict):
    scored_rests = [(k,v) for k,v in score_dict.iteritems()]
    sort = sorted(scored_rests, reverse=True, key=lambda x: x[1])
    return sort

def get_top_rest(best_rests):
    top_rest = best_rests[0][0]
    return top_rest

if __name__ == '__main__':
    users = user.create_users()
    user_rests = user.get_users_restaurants(users)
    score_dict = get_rest_score_dict(users, user_rests)
    sorted_rests = get_best_rests(score_dict)
    for tup in sorted_rests:
        price_str = "No price"
        if tup[0].price != None:
            price_str = str(tup[0].price)
        print tup[0].name + ", Score: " + str(tup[1]) + ", Price: " + price_str