__author__ = 'davidabrahams'
import user
import locu_setup


def rank_to_score(rank):
    return 40 - rank

def get_rest_score_dict(list_of_lists_of_restaurants):
    rest_to_score = {}
    for list in list_of_lists_of_restaurants:
        for i, restaurant in enumerate(list):
            if restaurant in rest_to_score:
                rest_to_score[restaurant] = rest_to_score[restaurant] + rank_to_score(i)
            else:
                rest_to_score[restaurant] = rank_to_score(i)

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
    score_dict = get_rest_score_dict(user_rests)
    sorted_rests = get_best_rests(score_dict)
    for tup in sorted_rests:
        print tup[0].name + ", Score: " + str(tup[1])