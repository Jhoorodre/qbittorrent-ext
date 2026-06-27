# VERSION: 1.00
# AUTHORS: Jhoorodre
# LICENSING INFORMATION: MIT

import html
import re
import urllib.parse
import urllib.request
from novaprinter import prettyPrinter

class darkmahou:
    # ponytail: minimal qbittorrent plugin structure
    url, name, supported_categories = 'https://darkmahou.io', 'Dark Mahou', {'all': '', 'anime': ''}

    def _get(self, url):
        # ponytail: one-line fetch
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=10).read().decode('utf-8', 'ignore')
        except Exception:
            return ""

    def search(self, what, cat='all'):
        page = self._get(f"{self.url}/?s={urllib.parse.quote(urllib.parse.unquote(what).replace('+', ' '))}")
        
        # ponytail: deduplicate order-preserving in one line and limit to 15
        links = list(dict.fromkeys(re.findall(r'<a href="(https://darkmahou\.io/[^"]+)"[^>]*class="tip"', page, re.I)))[:15]
        
        seen = set()
        for link in links:
            post = self._get(link)
            title = (re.search(r'<title>(.*?)</title>', post, re.I) or [None, "Dark Mahou Torrent"])[1].replace(' - Dark Animes', '').strip()
            
            for block in re.split(r'<div class="sorattl', post, flags=re.I):
                b_title = (re.search(r'<h3>(.*?)</h3>', block, re.I) or [None, ""])[1].strip()
                
                for mag, text in re.findall(r'<a[^>]*href="(magnet:\?[^"]+)"[^>]*>(.*?)</a>', block, re.I):
                    mag = html.unescape(mag.replace('&amp;', '&'))
                    hash_val = (re.search(r'xt=urn:btih:([a-zA-Z0-9]+)', mag, re.I) or [None, mag])[1].lower()
                    
                    if hash_val in seen:
                        continue
                    seen.add(hash_val)
                    
                    dn = re.search(r'[?&]dn=([^&]+)', mag, re.I)
                    name = urllib.parse.unquote(dn.group(1)).replace('+', ' ') if dn else f"{title} - {b_title} ({text.strip()})".replace(' -  ', ' ')
                    
                    # ponytail: direct dict construction
                    prettyPrinter({'link': mag, 'name': name, 'size': '-1', 'seeds': '-1', 'leech': '-1', 'engine_url': self.url, 'desc_link': link})
