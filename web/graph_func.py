import pickle
import networkx

# 상위 노드, 본인, 하위 노드 및 edge로 구성된 subgraph를 리턴
# pagerank를 이용하여 상/하위 노드 각각 점수 상위 n개씩 그래프에 포함
# param: 전체 graph, 현재 node, 전체 indegree dict, 전체 pagerank, 개수 n
def get_subgraph(graph, cur_node, pagerank, n):
    subgraph = {}

    predgraph_nodes = []
    # cur_node를 가리키고 있는 노드들 pagerank순 n개 구하기
    pred = graph.in_edges(cur_node, data=True)
    pr_local = {}
    for u,v,w in pred:
        pr_local[u] = pagerank[u]
    predgraph_nodes += sorted(pr_local.items(), key=lambda x:x[1], reverse=True)[:n]
    predgraph_nodes = [item[0] for item in predgraph_nodes]
    # 자신포함해야함
    predgraph_nodes.append(cur_node)
    subgraph['predgraph'] = graph.subgraph(predgraph_nodes)

    succgraph_nodes = []
    # cur_node가 가리키고 있는 노드들 pagerank순 n개 구하기
    pr_local.clear()
    succ = graph.out_edges(cur_node, data=True)
    for u,v,w in succ:
        pr_local[v] = pagerank[v]
    succgraph_nodes += sorted(pr_local.items(), key=lambda x:x[1], reverse=True)[:n]
    succgraph_nodes = [item[0] for item in succgraph_nodes]
    # 자신포함해야함
    succgraph_nodes.append(cur_node)
    subgraph['succgraph'] = graph.subgraph(succgraph_nodes)

    return subgraph
