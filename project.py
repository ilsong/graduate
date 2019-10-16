import json
import sys
import io
import pickle

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8-sig')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8-sig')

def printf(arg):
    print(arg)
    sys.stdout.flush()

def parseLink(data):
    if "파일:" in data or "http://" in data or "https://" in data:
        return

    return data.split("|")[0].replace("\\", "").replace("\\", "").split("#s-")[0].split("#S-")[0].strip()

def processRawData():
    parsedDataArray = []
    parsedData = {}
    printf("Parse Raw Data Start...")
    with open("data.json", "r", encoding='utf-8-sig') as datafile:
        for idx, line in enumerate(datafile):
            temp = json.loads(line)
            parsedData[temp['title']] = list(filter(None,list(map(parseLink, temp['link'][1:]))))
            if '#redirect ' in temp['link'][0]:
                redirect = temp['link'][0].split("#redirect ")[1][:-1].split("#s-")[0].replace("\\", "").strip()
                parsedData[temp['title']].append(redirect)
            if idx>0 and (idx%100000)==0:
                parsedDataArray.append(parsedData)
                parsedData = {}
        parsedDataArray.append(parsedData)
    printf("Parse Raw Data Done...")
    saveParsedData(parsedDataArray)

def saveParsedData(parsedDataArray):
    printf("Save Parsed Data Start...")
    for idx, parsedData in enumerate(parsedDataArray):
        pickle.dump(parsedData, open("parsedData"+str(idx)+".bin", "wb"), protocol=-1)
    printf("Save Parsed Data Done...")

def loadParsedData():
    printf("Load Parsed Data Start...")
    data = {}
    for idx in range(7):
        data.update(pickle.load(open("parsedData"+str(idx)+".bin", "rb")))
    printf("Load Parsed Data Done...")
    return data

if __name__ == '__main__':
    data = loadParsedData()
    links = data['공백']
    for link in links:
        printf(link)
