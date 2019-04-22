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
    print(url)
    obj = sitemapper.url(url)
    obj.run_check()
    print(obj.sites)

    with open('your_file.txt', 'w') as f:
        for item in obj.sites:
            f.write("%s\n" % item)

    return obj.sites


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)


    



