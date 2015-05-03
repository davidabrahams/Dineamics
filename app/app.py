from flask import Flask, render_template, request, redirect
from api import user, optimize_category

app = Flask(__name__)

foodtypes = []
locations = []
prices = []
rest_index = 0

@app.route('/')
def index():
    del foodtypes[:], locations[:], prices[:]
    rest_index = 0
    return render_template('index.html')

@app.route('/getstarted', methods = ['POST'])
def getstarted():
    return redirect('/search')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/nextperson', methods = ['POST'])
def nextperson():
    foodtypes.append(request.form['foodtype'])
    locations.append(request.form['location'])
    prices.append(request.form['price'])
    print(foodtypes)
    print(locations)
    print(prices)
    if request.form['submit'] == "Add another person!":
        return redirect('/search')
    elif request.form['submit'] == "Find me a restaurant!":
        return redirect('/results')
    elif request.form['submit'] == "Start Over":
        return redirect('/')

@app.route('/results')
def results():
    users = user.create_users(foodtypes, locations, prices)
    rests = optimize_category.get_best_restaurants(users)
    top_rest = rests[rest_index]
    rest_address = ""
    for piece in top_rest.address[0:-1]:
        rest_address += piece + ", "
    rest_address += top_rest.address[-1]
    return render_template('results.html', name=top_rest.display_name, image=top_rest.image, url=top_rest.url, price=top_rest.price, address=rest_address)

@app.route('/next', methods = ['POST'])
def next():
    global rest_index
    if request.form['submit'] == "Next restaurant!":
        rest_index = rest_index + 1
        return redirect('/results')
    elif request.form['submit'] == "Start Over":
        rest_index = 0
        return redirect('/')


if __name__=="__main__":
    app.debug = True
    app.run()