from urllib.parse import urljoin
from lxml import html
import requests


class URL:

    url = ""                # the url of the website to be checked
    sites = dict()          # dic. with all sites and urls on those sites
    header_values = {
                'Connection:' : 'Keep-alive',
                'name' : 'Michael Foord',
                'location' : 'Northampton',
                'language' : 'English',
                'User-Agent': 'Mozilla 4/0'}

    exclude = [
        "title=Spezial",
        "doodles",
        "#",
        "&"
    ]
        
    

    def __init__(self, url):
        self.url = url
  

    def run_check(self, root=None):      # root is the url of the current Site
        
        if root in self.sites or self.url.rsplit('/')[2] not in root:
            #print(self.url.rsplit('/')[2])
            return
        if "https" not in root:
            return
        for element in self.exclude:
            if element in root:
                return
        print(root)
        try:
            site = requests.get(root)
            tree = html.fromstring(site.content)
            links = tree.xpath('//a/@href')
            #print(links)
        except:
            return
                
        nlinks = []
        for link in links:
            if link not in nlinks:
                if link.startswith("http"):
                    nlinks.append(link)
                else:
                    nlinks.append(urljoin(site.url, link))

        self.sites[root] = nlinks

        for each_link in nlinks:         
            self.run_check(each_link)
     