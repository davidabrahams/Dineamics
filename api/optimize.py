__author__ = 'davidabrahams'
import user
import locu_setup


def rank_to_score(rank):
    return 40 - rank

def get_rest_score_dict(list_of_lists_of_restaurants):
    rest_to_score = {}
    for list in list_of_lists_of_restaurants:
        for i, restaurant in enumerate(list):
            key = restaurant.get_duplicate(rest_to_score.keys())
            if key == None:
                rest_to_score[restaurant] = rank_to_score(i)
            else:
                print 'Found match!'
                rest_to_score[key] = rest_to_score[key] + rank_to_score(i)

    return rest_to_score

def get_best_rests(score_dict):
    scored_rests = [(k,v) for k,v in score_dict.iteritems()]
    sort = sorted(scored_rests, reverse=True, key=lambda x: x[1])
    return sort

def get_top_rest(best_rests):
    top_rest = best_rests[0][0]
    top_rest.price = locu_setup.get_price_of_mains(top_rest.unencoded_name, top_rest.locality)
    return best_rests[0][0]

if __name__ == '__main__':
    users = user.create_users()
    user_rests = user.get_users_restaurants(users)
    score_dict = get_rest_score_dict(user_rests)
    sorted_rests = get_best_rests(score_dict)
    for tup in sorted_rests:
        print tup[0].name + ", Score: " + str(tup[1])