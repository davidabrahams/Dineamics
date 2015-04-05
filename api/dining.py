import pprint
import api

TERM = 'pizza'
LOCATION = 'Needham, MA'

def get_name(response):
    return response["name"]

def get_address(response):
    thing = []
    address = response["location"]["display_address"]
    for item in address:
        item = str(item)
        thing.append(item)
    return thing

def get_categories(response):
    thing = []
    categories = response["categories"]
    for item in response["categories"]:
            thing.append(item)

    return thing

def main(TERM,LOCATION):
    response = api.main(TERM,LOCATION)
    pprint.pprint(response)
    name = get_name(response)
    address = get_address(response)
    categories = get_categories(response)
    print " "
    print "Your generated restaurant is " + name + '!'
    print " "
    print "The address of " + name + " is:"
    for i in address:
        print i
    print " "
    print name + " is in the following categories:"
    for i in categories:
        print i[0]
    print " "

if __name__ == '__main__':
    main(TERM, LOCATION)