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
        label = nn.rsplit('/')[-1]
        if label == "":
            label = nn.rsplit('/')[-2]
        nodes.append('{' + "id: '{}', label: '{}', group: {}".format(nn, label, 0) + '}\n')
        drawn.append(nn)

    for ee in e:
        if ee[1] not in drawn and ee[1] not in n:
            nodes.append('{' + "id: '{}', label: '{}', group: {}".format(ee[1], ee[1], 1) + '}\n')
            drawn.append(ee[1])

        edges.append('{' + "from: '{}', to: '{}'".format(ee[0], ee[1]) + '}\n')

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
        nodes =  jsonContent["nodes"]
        edges =  jsonContent["edges"]
        nodes, edges = transformForDrawing(nodes, edges)
        return nodes, edges

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
# input for urls over url

@app.route('/')
def index():
    url = request.args.get("url")
    cached = os.listdir(os.path.join(os.path.dirname(__file__), "./cached"))
    withoutProtocol = url
    if withoutProtocol + '.json' not in cached:
        nodes, edges = graph(url)
    else:
        nodes, edges = load(withoutProtocol)
    
    str1 = "," 
    nodes = str1.join(nodes)
    edges = str1.join(edges)

    return render_template('graph.html', nodes = nodes, edges = edges)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    sys.setrecursionlimit(5000)
    app.run(host='0.0.0.0', port=port)


    



