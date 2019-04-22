from urllib.parse import urljoin
import requests
import re
from requests_html import HTMLSession


class url:

    url = ""                # the url of the website to be checked
    sites = dict()          # dic. with all sites and urls on those sites
    does_work = []          # array with all prev. positiv tested urls
    does_not_work = dict()  # dic. with all not working urls and the site that linked there
    header_values = {
                'Connection:' : 'Keep-alive',
                'name' : 'Michael Foord',
                'location' : 'Northampton',
                'language' : 'English',
                'User-Agent': 'Mozilla 4/0'}

    def __init__(self, url):
        self.url = url
  

    def run_check(self, root=None):      # root is the url of the current Site
        
        if root == None:
            root = self.url

        root = requests.get(root).url
        if "Spezial" in root:
            return
        if root in self.sites or self.url.rsplit('/', 1)[1] not in root:
            return  

        session = HTMLSession()
        
        try:
            response = session.get(root)   
        except:
            return

        links = response.html.absolute_links
        nlinks = []
        for link in links:
            try:
                nlinks.append(requests.get(link).url.replace("/./", "/").replace("/../", "/"))
            except:
                return
        self.sites[root] = nlinks

        print(root)

        for each_link in nlinks:         
            self.run_check(each_link)
     