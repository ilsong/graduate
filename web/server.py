from flask import Flask, render_template, request
from graph_func import get_subgraph
import json
import pickle
import networkx as nx
app = Flask(__name__)

# nx_digraph = nx.read_gpickle(path="data/graph.bin")
# pagerank = pickle.load(open("data/pagerank.bin", "rb"))

@app.route('/')
def home():
    return render_template("/index.html")

@app.route('/query', methods = ['POST'])
def get_graph():
    search_str = request.form.get('query_str')
    # result = get_subgraph(nx_digraph, search_str, pagerank, 6)

    # sample result:
    result = nx.path_graph(8)

    return json.dumps(result)

if __name__ == '__main__':
   app.run(debug = True)
