from flask import Flask, request, render_template
import os
from Star import Crawler
import json
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

def transformForDrawing(n, e):
    nodes = []
    drawn = []
    edges = []
    for nn in n:
        if "web.archive.org" in nn:
            continue
        label = nn.rsplit('/')[-1]
        if label == "":
            label = nn.rsplit('/')[-2]
        nodes.append({"id": nn, "label":  label, "group": 0})
        drawn.append(nn)

    for e0, e1 in e:
        if "web.archive.org" in e1:
            continue
        if e1 not in drawn and e1 not in n:
            nodes.append({"id": e1, "label": e1, "group": 1})
            drawn.append(e1)

        edges.append({"from": e0, "to": e1})

    return nodes, edges

def graph(url):
    obj = Crawler()
    obj.run(url, 5000)
    
    current = os.path.dirname(__file__)
    n, e = obj.getNodesEdges()
    with open(os.path.join(current, './cached/' + url.rsplit('/')[2] + '.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps({"nodes": n,"edges": e}))

    nodes, edges = transformForDrawing(n, e)
    return nodes, edges


def load(url):
    print("Loaded from cache: " + url)
    current = os.path.dirname(__file__)
    with open(os.path.join(current,'./cached/{}.json'.format(url)),  'r', encoding='utf-8') as f:
        content = f.read()
        jsonContent = json.loads(content)
        return transformForDrawing(jsonContent["nodes"], jsonContent["edges"])

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
# input for urls over url

@app.route('/')
def index():
    url = request.args.get("url")
    cached = os.listdir(os.path.join(os.path.dirname(__file__), "./cached"))
    withoutProtocol = url.split("/")[2]
    if withoutProtocol + '.json' not in cached:
        nodes, edges = graph(url)
    else:
        nodes, edges = load(withoutProtocol)
    

    print(url)
    return render_template('graph.html', nodes = json.dumps(nodes), edges = json.dumps(edges))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)


    



