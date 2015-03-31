from flask import Flask, request, render_template
import urllib

app = Flask(__name__)

YELP_BASE_URL = 'http://api.yelp.com/v2/search?'

def get_yelp_api(food_type, distance, price):
	return YELP_BASE_URL + urllib.urlencode([('term', food_type), ('Location', 'Boston'), ('oauth_consumer_key', 'QLqsLHUp-w2f7KP4ylY_5A')])

@app.route('/')
def stuff():
	return render_template('search.html')

@app.route('/restaurant', methods=['POST'])
def submit_form():
	food_type = request.form['food_type']
	distance = request.form['distance']
	price = request.form['price']
	print food_type
	print distance
	print price
	print get_yelp_api(food_type, distance, price)
	return 'Swag'



if __name__ == '__main__':
	app.debug = True
	app.run()
