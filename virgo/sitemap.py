import os
import json
import datetime


class SitemapGenerator:
    def __init__(self, root, domain):
        self.root = root
        self.json = {'domain': domain, 'pages': []}

    def get_sitemap(self):
        return json.dumps(self.json)

    def generate(self):
        for root, dirs, files in os.walk(self.root):
            for file in files:
                if not file.startswith('.'):
                    date = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(root, file)))
                    pages = {'page': os.path.join(root, file).replace(self.root, ''), 'lastmod': str(date.date())}
                    self.json['pages'].append(pages)
