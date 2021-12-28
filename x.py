import Star

crawler = Star.Crawler()
crawler.run("https://www.patricematz.de/", 5000)
print(crawler.getNodesEdges())
crawler.draw()