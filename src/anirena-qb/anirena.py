# VERSION: 1.02
import re
import urllib.parse
import urllib.request
from novaprinter import prettyPrinter

class anirena:
    url = 'https://www.anirena.com'
    name = 'AniRena'
    supported_categories = {'all': ''}

    def search(self, what, cat='all'):
        query = urllib.parse.quote(urllib.parse.unquote(what))
        
        for page in range(1, 6):
            search_url = f"{self.url}/?q={query}&page={page}"
            try:
                req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
                html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', 'ignore')
            except Exception:
                break
                
            rows = re.findall(r'<tr[^>]*data-torrent-id=[^>]*>.*?</tr>', html, re.I | re.S)
            if not rows:
                break
                
            for row in rows:
                item = {}
                
                name_match = re.search(r'<a[^>]*class=["\']?tl-torrent-name[^>]*>([^<]+)</a>', row, re.I)
                if not name_match:
                    continue
                item['name'] = name_match.group(1).strip()
                
                dl_match = re.search(r'href=["\']?(/torrents/[^"\' >]+\.torrent)["\']?', row, re.I)
                if not dl_match:
                    continue
                item['link'] = self.url + dl_match.group(1)
                
                size_match = re.search(r'<td[^>]*class=["\']?col-size[^>]*>([^<]+)</td>', row, re.I)
                item['size'] = size_match.group(1).strip() if size_match else '-1'
                
                se_match = re.search(r'<td[^>]*class=["\']?col-se[^>]*>.*?<span[^>]*class=["\']?tl-se[^>]*>(\d+)</span>', row, re.I | re.S)
                item['seeds'] = se_match.group(1) if se_match else '-1'
                
                le_match = re.search(r'<td[^>]*class=["\']?col-le[^>]*>.*?<span[^>]*class=["\']?tl-le[^>]*>(\d+)</span>', row, re.I | re.S)
                item['leech'] = le_match.group(1) if le_match else '-1'
                
                date_match = re.search(r'data-created-ts=["\']?(\d+)["\']?', row, re.I)
                if date_match:
                    item['pub_date'] = date_match.group(1)
                
                item['engine_url'] = self.url
                item['desc_link'] = self.url
                
                prettyPrinter(item)
