from flask import Flask, render_template, request, jsonify
from graph_func import get_subgraph
import json
import pickle
import networkx as nx
app = Flask(__name__)

nx_digraph = nx.read_gpickle(path="data/graph.bin")
pagerank = pickle.load(open("data/pagerank.bin", "rb"))

@app.route('/')
def home():
    return render_template("/index.html")

@app.route('/query', methods = ['POST'])
def get_graph():
    search_str = request.form.get('query_str')

    # real subgraph
    subgraph = get_subgraph(nx_digraph, search_str, pagerank, 3)

    # type cast: NodeView -> list
    result = {}
    result['predgraph'] = {'nodes': list(subgraph['predgraph'].nodes()), 'edges': list(subgraph['predgraph'].edges())}
    result['succgraph'] = {'nodes': list(subgraph['succgraph'].nodes()), 'edges': list(subgraph['succgraph'].edges())}

    return jsonify(**result)

if __name__ == '__main__':
   app.run(debug = True)
