import Star

crawler = Star.Crawler()
crawler.run("https://www.google.de/", 5000)
print(crawler.getNodesEdges())
crawler.draw()