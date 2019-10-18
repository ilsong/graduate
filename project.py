import json
import sys
import io
import pickle
import networkx as nx

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8-sig')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8-sig')

def printf(arg):
    print(arg)
    sys.stdout.flush()

def parseLink(data):
    if "파일:" in data or "http://" in data or "https://" in data:
        return

    return data.split("|")[0].replace("\\", "").replace("\\", "").split("#s-")[0].split("#S-")[0].strip()

def parseRawData():
    parsedData = {}
    printf("Parse Raw Data Start...")
    with open("data.json", "r", encoding='utf-8-sig') as datafile:
        for line in datafile:
            temp = json.loads(line)
            parsedData[temp['title']] = list(filter(None,list(map(parseLink, temp['link'][1:]))))
            if '#redirect ' in temp['link'][0]:
                redirect = temp['link'][0].split("#redirect ")[1][:-1].split("#s-")[0].replace("\\", "").strip()
                parsedData[temp['title']].append(redirect)
    printf("Parse Raw Data Done...")
    return parsedData

def saveDict(filename, _dict, size=100000):
    if not isinstance(filename, str):
        raise ValueError("file name is not string")
    elif not isinstance(_dict, dict):
        raise ValueError("dict is not type of dict")
    elif not isinstance(size, int):
        raise ValueError("size is not type of int")
    elif size < 0:
        raise ValueError("size must be more then 0")

    printf("Save Parsed Data Start...")
    # size가 0보다 크면 size만큼 분할해서 저장하고 0이면 한번에 저장
    if size>0:
        splited_dict = splitDict(_dict, size)
        for idx, e in enumerate(splited_dict):
            pickle.dump(e, open(filename+str(idx)+".bin", "wb"))
    elif size==0:
        pickle.dump(_dict, open(filename+".bin", "wb"))

    printf("Save Parsed Data Done...")

def loadDict(filename, total):
    if not isinstance(filename, str):
        raise ValueError("file name is not string")
    elif not isinstance(total, int):
        raise ValueError("total count is not int")
    elif total < 0:
        raise ValueError("total count must be more than 0")

    printf("Load Parsed Data Start...")
    data = {}
    if total > 0:
        for idx in range(total):
            data.update(pickle.load(open(filename+str(idx)+".bin", "rb")))
    elif total==0:
        data.update(pickle.load(open(filename+".bin", "rb")))
    printf("Load Parsed Data Done...")
    return data

def splitDict(_dict, size=100000):
    ret = []
    temp = {}
    for idx, key in enumerate(_dict.keys()):
        temp[key] = _dict[key]
        if idx>0 and (idx%size)==0:
            ret.append(temp)
            temp = {}
    ret.append(temp)
    return ret

def removeDeadLinks(parsedData):
    printf("Remove Dead Links Start...")
    nodes = parsedData.keys()
    for node in nodes:
        for link in parsedData[node]:
            if not link in nodes:
                parsedData[node].remove(link)
    printf("Remove Dead Links Done...")
    return parsedData


if __name__ == '__main__':
    data = removeDeadLinks(loadDict("parsedData", 7))
    # idxToKey = loadDict("IdxToKey", 0)
    # keyToIdx = loadDict("KeyToIdx", 0)
    # graph = snap.TNGraph.New()
    # for idx, node in enumerate(data.keys()):
    #     graph.AddNode(keyToIdx[node])
    #     if idx%100000==0:
    #         printf(str(idx)+"nodes added")
    # printf("adding nodes done")
    # printf("Total nodes: "+str(graph.GetNodes()))
    graph = nx.Graph()
    nodes = data.keys()

    #graph.add_nodes_from(nodes)
    # for node in data.keys():
    #     graph.add_edges_from([(node, dst) for dst in data[node]])