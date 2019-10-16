import json

data = {}

def parseLink(data):
    if "파일:" in data or "http://" in data or "https://" in data:
        return

    return data.split("|")[0].replace("\\", "").replace("\\", "").split("#s-")[0].split("#S-")[0]

with open("data.json", "r", encoding='utf-8-sig') as datafile:
    for line in datafile:
        temp = json.loads(line)
        data[temp['title']] = list(filter(None,list(map(parseLink, temp['link'][1:]))))
        if '#redirect ' in temp['link'][0]:
            redirect = temp['link'][0].split("#redirect ")[1][:-1].split("#s-")[0].replace("\\", "")
            data[temp['title']].append(redirect)

f = open("parsedData", "w", encoding='utf-8-sig')
keys = data.keys()
f.write("{\n")
for key in keys:
    f.write("\t"+key+":"+str(data[key])+",\n")
f.write("}")
f.close()
