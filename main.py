#main.py
from flask import Flask, request, render_template, jsonify, redirect, url_for
from random import sample
app = Flask(__name__)

#list of queries
queries = []

"""
Render index.html
"""
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

"""
query id to access URL for graph data
"""
@app.route('/search/<int:query_id>')
def searchId(query_id):
    if (query_id < len(queries)):
        query=queries[query_id]
        return render_template('index.html', query=query, query_id=query_id)
    else:
        return redirect(url_for('index'))

"""
Handle POST request from user submitting query
intialise tweet streaming and processing
query given unique id
"""
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        if (query in queries):
            query_id = queries.index(query)
        else:
            query_id = len(queries)
            queries.append(str(query))
        print('id: {}\nquery: {}'.format(query_id, query))
        return render_template('index.html', query=query, query_id=query_id)
    else:
        return redirect(url_for('index'))
    
"""
Collect data for graph
Requires query_id and timeline:frequency of graph updates
"""
@app.route('/search/<int:query_id>/data/<timeline>')
def data(query_id=0, timeline='sec'):
    try:
        if timeline == 'sec':
            print('Opening file')
            graph_data = open('../SentweetmentProject/{}_sec.txt'.format(query_id), 'r').read()
        elif timeline == 'min':
            graph_data = open('../SentweetmentProject/{}_min.txt'.format(query_id), 'r').read()
        elif timeline == 'hr':
            graph_data = open('../SentweetmentProject/{}_hr.txt'.format(query_id), 'r').read()
        elif timeline == 'day':
            graph_data = open('../SentweetmentProject/{}_day.txt'.format(query_id), 'r').read()
        else:
            print('Error: Invalid timeline')
    except(IOError):
        print('Error: No graph data found')
        return jsonify({'xs' : [], 'yi' : []})
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y, z = line.split(',')
            #xs.append(int(x))
            ys.append(int(y))
    return jsonify({'xs' : range(1,11), 'yi' : ys[-10:]})

"""
start server
"""
if __name__ == '__main__':
    #start the server
    app.run(debug=True)
