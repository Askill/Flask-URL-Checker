from flask import Flask, request
import os
import urlchecker
import sitemapper
import _pickle as cPickle
import json
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

    with open('your_file.txt', 'w') as f:
        for item in obj.sites:
            f.write("%s\n" % item)

    nodes = ""
    for link in obj.sites:
        nodes += '{' + 'id: "{}", label: "{}", group: {}'.format(link, link.rsplit('/')[-1], 0) + '},'
    nodes = nodes[:-1]

    edges = ""
    for key, values in obj.sites.items():
        for value in values:
            edges += '{' + 'from: "{}", to: "{}"'.format(key, value) + '},'
    edges = edges[:-1]


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
                    improvedLayout:false,
                    randomSeed: undefined,
                    hierarchical: {
                        enabled:false,
                        levelSeparation: 150,
                        nodeSpacing: 100,
                        treeSpacing: 200,
                        blockShifting: true,
                        edgeMinimization: true,
                        parentCentralization: true,
                        direction: 'UD',        // UD, DU, LR, RL
                        sortMethod: 'hubsize'   // hubsize, directed
                    }
                },
                height: '100%',
                width: '100%',
                nodes: {
                    shape: 'dot',
                    size: 30,
                    font: {
                        size: 32,
                        color: '#ffffff'
                    },
                    borderWidth: 2
                },
                edges: {
                    width: 2
                }
            };
            network = new vis.Network(container, data, options);
        </script>
        '''
    return results


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)


    



