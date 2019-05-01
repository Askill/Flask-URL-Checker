from flask import Flask, request
import os
import urlchecker
import sitemapper
import _pickle as cPickle
import json
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/test/')
def index():
    url = request.args.get("url")
    #print(url)
    obj = sitemapper.url(url)
    obj.run_check(url)
    
    nodes = ""
    drawn = []
    for key, values in obj.sites.items():
        label = key.rsplit('/')[-1]
        if label == "":
            label = key.rsplit('/')[-2]
        nodes += '{' + 'id: "{}", label: "{}", group: {}'.format(key, label, 0) + '},\n'
        drawn.append(key)

    for key, values in obj.sites.items():
        for value in values:
            if value not in drawn and value not in obj.sites:
                nodes += '{' + 'id: "{}", label: "{}", group: {}'.format(value, value, 1) + '},\n'
                drawn.append(value)

    nodes = nodes[:-2] + "\n"

    edges = ""
    for key, values in obj.sites.items():
        for value in values:
            edges += '{' + 'from: "{}", to: "{}"'.format(key, value) + '},\n'
    edges = edges[:-2] + "\n"

    with open('./cached/' + url.rsplit('/')[2] + '.txt', 'w') as f:
        f.write(nodes)
        f.write(edges)

    results = '''
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css">
    <div id="mynetwork" style = "background-color: grey;"></div>
        <script type="text/javascript">
            var color = 'gray';
        
            var nodes = [
    ''' + nodes + '''
            ];
            var edges = [
    ''' + edges + '''
            ];
        
            // create a network
            var container = document.getElementById('mynetwork');
            var data = {
                nodes: nodes,
                edges: edges
            };
            var options = {
                autoResize: true,
                layout: {
                    improvedLayout:true,
                    randomSeed: 10,
                    
                },
                height: '100%',
                width: '100%',
                nodes: {
                    shape: 'dot',
                    size: 8,
                    font: {
                        size: 5,
                        color: '#ffffff'
                    },
                    borderWidth: 1
                },
                edges: {
                    width: 1,
                    color: {
                    color:'#356b6b',
                    highlight:'#4286f4',
                    hover: '#41f4f4',
                    inherit: 'from',
                    opacity:1.0
                    },
                },
                interaction: {
                    hoverConnectedEdges: true,
                    tooltipDelay: 200
                }
            };
            network = new vis.Network(container, data, options);
            network.on("stabilizationIterationsDone", function () {
                network.setOptions( { physics: false } );
            });
        </script>
        '''
    return results


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    sys.setrecursionlimit(2000)
    app.run(host='0.0.0.0', port=port)


    



