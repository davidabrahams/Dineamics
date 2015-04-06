import pprint
import api
import locu_setup

TERM = 'neptune oyster'
LOCATION = 'Boston, MA'

def get_name(response):
    return response["name"]

def get_address(response):
    thing = []
    address = response["location"]["display_address"]
    for item in address:
        item = str(item)
        thing.append(item)
    return thing

def get_locality(response):
    locality = response["location"]["city"]
    return locality.encode('utf-8')

def get_categories(response):
    thing = []
    categories = response["categories"]
    for item in response["categories"]:
            thing.append(item)

    return thing

def main(TERM,LOCATION):
    response = api.main(TERM,LOCATION)
    
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
    try:
        print "The average price per person at this restaurant is:"
        print locu_setup.filter_data(name,get_locality(response))
        
    except:
        print "We're sorry! Price isn't available for this location." 
        print "Check the website!" 

if __name__ == '__main__':
    main(TERM, LOCATION)