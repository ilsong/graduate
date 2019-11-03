from flask import Flask, render_template
from graph_func import get_subgraph
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("/index.html")

@app.route('/get_graph', methods = ['GET'])
def get_graph():
    if request.method == 'GET':
        search_str = requst.form.get('input_str')
        search_str = search_str.split('/w/')[1].replace("%20"," ")
        if '?from=' in search_str:
            search_str = search_str.split('?from=')[0]
        result = get_subgraph(search_str)
        return result

if __name__ == '__main__':
   app.run(debug = True)
