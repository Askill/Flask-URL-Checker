import os
from Star import Crawler
import json
import argparse


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


def graph(url, limit):
    obj = Crawler()
    obj.run(url, limit)

    current = os.path.dirname(__file__)
    n, e = obj.getNodesEdges()
    with open(os.path.join(current, './cached/' + url.rsplit('/')[2] + '.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps({"nodes": n, "edges": e}))

    nodes, edges = transformForDrawing(n, e)
    return nodes, edges


def load(url):
    print("Loaded from cache: " + url)
    current = os.path.dirname(__file__)
    with open(os.path.join(current, './cached/{}.json'.format(url)),  'r', encoding='utf-8') as f:
        content = f.read()
        jsonContent = json.loads(content)
        return transformForDrawing(jsonContent["nodes"], jsonContent["edges"])


def main(url, pathToCached):
    withoutProtocol = url.split("/")[2]

    if pathToCached is not None:
        nodes, edges = graph(url, limit)
    else:
        nodes, edges = load(withoutProtocol)

    pathToTemplate = os.path.join(os.path.dirname(
        __file__), "templates", "graph.html")
    with open(pathToTemplate, "rt") as fin:
        with open(withoutProtocol + ".html", "wt") as fout:
            fout.write(fin.read().replace('{{nodes}}', json.dumps(
                nodes)).replace('{{edges}}', json.dumps(edges)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Map any website. Only map websites you own, as this tool will open any link on a given website, which can potentially incure high costs for the owner and be interpreted as a small scale DOS attack.')
    parser.add_argument('-url', type=str, help='url to map', required=True)
    parser.add_argument('--plot-cached', type=str,
                        help='path to cached file', required=False)
    parser.add_argument(
        '-limit', type=str, help='maximum number of nodes on original site', required=False, default=5000)

    args = parser.parse_args()
    url = args.url
    pathToCached = args.plot_cached
    limit = args.limit

    main(url, pathToCached, limit)
