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

    # test graph
    test_pred = nx.path_graph(6)
    test_succ = nx.star_graph(6)
    result = {'predgraph': test_pred, 'succgraph': test_succ}

    # real subgraph
    # result = get_subgraph(nx_digraph, search_str, pagerank, 6)

    # type cast: NodeView -> list
    result_pred = list(result['predgraph'].nodes())
    result_pred.append('/nodes_edges/')
    result_pred += list(result['predgraph'].edges())
    result_succ = list(result['succgraph'].nodes())
    result_succ.append('/nodes_edges/')
    result_succ += list(result['succgraph'].edges())

    print(result_pred)
    print(result_succ)

    result_pred.append('/pred_succ/')
    result = result_pred + result_succ
    '''
    ex) ["a","b","c", "/nodes_edges/" ,["a","b"],["b","c"], "/pred_succ/",
            "d","e","f", "/nodes_edges/" ,["d","e"],["f","d"],  ]
    '''

    return json.dumps(result,ensure_ascii = False ).encode('utf-8')

if __name__ == '__main__':
   app.run(debug = True)
