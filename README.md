# Star-Mapper

Calls every link on a given website and produces an explorable graph visualization.

Please note that the graph layout can take a long time since it is JS based. Loading a graph with 3000 Nodes may take 5 minutes or more.

    Map any website. Only map websites you own, as this tool will open any link on a given
    website, which can potentially incure high costs for the owner and be interpreted 
    as a small scale DOS attack.

        optional arguments:
        -h, --help            show this help message and exit
        -url                  url to map
        --plot-cached         path to cached file
        -limit                maximum number of nodes on original site

## Examples:
### Google.de:
![google.de](./google.png)