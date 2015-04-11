__author__ = 'davidabrahams'


class User:

    def __init__(self, term, location, price_max):
        self.term = term
        self.location = location
        self.price_max = price_max

    def __str__(self):
        return 'User looking for ' + self.term + ' in ' + self.location + ', paying up to $' + self.price_max + '.'


def create_user():

    term = raw_input("What would you like to eat? --> ")
    location = raw_input("Where are you? --> ")
    price_max = raw_input("How much are you willing to pay? --> ")

    return User(term, location, price_max)

def create_users():
    add_another = True
    users = []
    while add_another:
        user = create_user()
        users.append(user)
        input = raw_input("Would you like to add another user (Y/N)? --> ")
        add_another = input.upper() == 'Y'
        print

    return users

if __name__ == '__main__':
    create_users()