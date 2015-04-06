from locu import MenuItemApiClient
import urllib2
from urllib import urlencode
import pprint
import json

from httplib2 import Http

def get_ID(name,locality):
    name = name.replace(" ","%20")
    name = name.replace("'","%27")

    url = 'http://api.locu.com/v1_0/venue/search/?name='+name+'&locality='+locality+'&api_key=f60f052cf5d0473b25022a62a73b107cf0db0aad'

    f = urllib2.urlopen(url)

    try:
        response_text = f.read()
        response_data = json.loads(response_text)


        return response_data["objects"][0]["resource_uri"]

    except:
        return "We're sorry! Price data isn't available. Check the website!"

def get_menu(name,locality):
    ID = get_ID(name,locality)
    #print ID

    url = 'http://api.locu.com'+ID+'?api_key=f60f052cf5d0473b25022a62a73b107cf0db0aad'
    #print url
    try: 
        f = urllib2.urlopen(url)
        response_text = f.read()
        response_data = json.loads(response_text)

        return response_data

    except:
        return "We're sorry! Price data isn't available. Check the website!"


def filter_data(name,locality):
    try:
        response_data = get_menu(name,locality)["objects"][0]["menus"]
        
    except:
        return "We're sorry! Price data isn't available. Check the website!"

    prices = []  
    key = 'price'

    for entry in response_data:
        sections = entry['sections']
        
        for i in range(len(sections)):
            temp = sections[i]
            dict1 = temp['subsections']
            
            for j in range(len(dict1)):
                temp1 = dict1[j]
                dict2 = temp1['contents']

                for k in range(len(dict2)):
                    temp2 = dict2[k]
                   
                    try:
                        money = (temp2['price'].encode('utf-8'))

                        try:
                            money = float(money)
                            prices.append(money)
                            
                        except:
                            pass

                    except:
                        pass

    return prices

def get_topthirty(name,locality):
    
    prices = filter_data(name,locality)
    
    if prices != "We're sorry! Price data isn't available. Check the website!":
        sorted_prices = sorted(prices,reverse=True)
        
        num = int(.25*len(sorted_prices))
        num1 = int(.5*len(sorted_prices))
        return int(sum(sorted_prices[num:num1])/(num1-num))
    
    else:
        return "We're sorry! Price data isn't available. Check the website!"

if __name__ == '__main__':
    get_topthirty(name,locality)

