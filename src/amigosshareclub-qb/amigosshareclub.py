# VERSION: 1.00
# AUTHORS: Jhoorodre
# LICENSING INFORMATION: MIT

import urllib.request, urllib.parse, re, tempfile, os
from novaprinter import prettyPrinter

class amigosshareclub:
    # ponytail: minimal qbittorrent plugin structure
    url, name, supported_categories = 'https://cliente.amigos-share.club', 'Amigos Share Club', {'all': '', 'movies': 'c119=1', 'tv': 'c118=1', 'anime': 'c69=1', 'music': 'c115=1', 'games': 'c47=1', 'software': 'c21=1', 'pictures': 'c70=1', 'books': 'c67=1'}
    
    # ponytail: externalize cookie (supports both raw string and Netscape HTTP format) to prevent github leaks
    try:
        _r = open(os.path.join(os.path.dirname(__file__), "amigos_cookie.txt")).read().strip()
        cookie = "; ".join(f"{p[5]}={p[6]}" for p in [l.split('\t') for l in _r.splitlines() if not l.startswith('#')] if len(p) >= 7) if "# Netscape" in _r else _r
    except: cookie = "COLE_SEU_COOKIE_AQUI"

    def _get(self, url):
        # ponytail: single fetch returning bytes (can be decoded or saved directly)
        try: return urllib.request.urlopen(urllib.request.Request(url, headers={'Cookie': self.cookie, 'User-Agent': 'Mozilla/5.0'})).read()
        except: return b""

    def download_torrent(self, info):
        # ponytail: concise tempfile write for private tracker .torrent
        try:
            fd, path = tempfile.mkstemp(suffix=".torrent")
            with os.fdopen(fd, 'wb') as f: f.write(self._get(info))
            print(f"{path} {info}")
        except: pass

    def search(self, what, cat='all'):
        # ponytail: cat query was unused, ignoring it and flattening loop
        q = urllib.parse.quote(urllib.parse.unquote(what).replace('+', ' '))
        for p in range(5):
            html = self._get(f"{self.url}/torrents-search.php?search={q}&page={p}" if p else f"{self.url}/torrents-search.php?search={q}").decode('utf-8', 'ignore')
            items = re.findall(r'<li class="list-group-item[^>]*>(.*?)</li>', html, re.S | re.I)
            if not items: break
            
            for item in items:
                title = (re.search(r'<a[^>]*href=["\']([^"\']*torrents-details\.php\?id=[^"\']+)["\'][^>]*>(.*?)</a>', item, re.I) or [None, None, None])
                dl = (re.search(r'<a[^>]*href=["\'](download\.php\?id=[^"\']+)["\']', item, re.I) or [None, None])[1]
                
                if title[1] and dl:
                    size = (re.search(r'([\d\.]+\s*[KMGTP]B)', item, re.I) or [None, '-1'])[1]
                    nums = re.findall(r'<br>\s*(\d+)\s*</a>', (re.search(r'class="list-group-item-controls"(.*?)</div>', item, re.S | re.I) or [None, ""])[1], re.I) or re.findall(r'>\s*(\d+)\s*<', item)
                    seeds, leech = (nums[0], nums[1]) if len(nums) >= 2 else (nums[-2], nums[-1]) if len(nums) >= 2 else ('-1', '-1')
                    
                    # ponytail: dictionary built inline
                    prettyPrinter({'link': urllib.parse.urljoin(self.url, dl), 'name': re.sub(r'<[^>]+>', '', title[2]).strip(), 'size': size, 'seeds': seeds, 'leech': leech, 'engine_url': self.url, 'desc_link': urllib.parse.urljoin(self.url, title[1])})
