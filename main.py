from flask import Flask, request, render_template, jsonify
from random import sample
app = Flask(__name__)


#tell flask which URL will trigger following function
@app.route('/')
@app.route('/<query>')
def index(query=None):
    return render_template('index.html', query=query)

@app.route('/about')
def about():
    return '<h1>This is the about page</h1>'

#variables in URL
@app.route('/search/<query>')
def search(query):
    return 'This is your query: %s' % query

#requests, can handle GET or POST methods
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    if request.method == 'POST':
        return 'You are using POST\n The post ID is: %s' % post_id
    elif request.method == 'GET':
        return 'You are using GET\n The post ID is: %s' % post_id

#render templates
@app.route('/profile/<name>')
def profile(name):
    #look in '/templates/profile' for 'profile.html'
    return render_template('profile.html', name=name)

#passing objects to template
@app.route('/shopping')
def shopping():
    food = ["cheese", 'tuna', 'steak']
    return render_template("shopping.html", food=food)

#chart
@app.route('/chart')
def chart():
    return render_template("chart.html")

#data
@app.route('/data')
def data():
    graph_data = open('graph_data.txt', 'r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y, z = line.split(',')
            xs.append(x)
            ys.append(int(y))
#    return jsonify({'results':sample(range(1,10), 5)})
    return jsonify({'xs' : xs, 'yi' : ys})

#start webserver when 'main.py' is run directly i.e. it is the main file
if __name__ == '__main__':
    #start the server
    app.run(debug=True)
