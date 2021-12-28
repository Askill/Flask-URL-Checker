from flask import Flask, request, render_template
import os
from Star import Crawler
import json
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)


def graph(url):
    obj = Crawler(url)
    obj.run_check(url)
    
    current = os.path.dirname(__file__)

    nodes = []
    drawn = []
    edges = []
    for key, values in obj.sites.items():
        label = key.rsplit('/')[-1]
        if label == "":
            label = key.rsplit('/')[-2]
        nodes.append('{' + "id: '{}', label: '{}', group: {}".format(key, label, 0) + '}')
        drawn.append(key)

        for value in values:
            if value not in drawn and value not in obj.sites:
                nodes.append('{' + "id: '{}', label: '{}', group: {}".format(value, value, 1) + '}')
                drawn.append(value)

        for value in values:
            edges.append('{' + "from: '{}', to: '{}'".format(key, value) + '}')
    
    with open(os.path.join(current, './cached/' + url.rsplit('/')[2] + '.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps({"nodes": nodes,"edges": edges}))

    return nodes, edges


def load(url):
    print("Loaded from cache: " + url)
    current = os.path.dirname(__file__)
    with open(os.path.join(current,'./cached/{}.json'.format(url)),  'r', encoding='utf-8') as f:
        content = f.read()
        jsonContent = json.loads(content)
        nodes =  jsonContent["nodes"]
        edges =  jsonContent["edges"]
        return nodes, edges

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
# input for urls over url

@app.route('/')
def index():
    url = "beauty"

    cached = os.listdir(os.path.join(os.path.dirname(__file__), "./cached"))
    withoutProtocol = url
    if withoutProtocol + '.json' not in cached:
        nodes, edges = graph(url)
    else:
        nodes, edges = load(withoutProtocol)
    
    str1 = "," 
    nodes = str1.join(nodes)
    edges = str1.join(edges)
    with open("./templates/data.js", "w") as f:
        f.write(f"var nodes={nodes}\nvar=edges={edges}")
    return render_template('graph.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    sys.setrecursionlimit(5000)
    app.run(host='0.0.0.0', port=port)


    



