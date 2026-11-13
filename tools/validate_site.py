"""Dependency-free checks for generated pages and their local navigation."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote, parse_qs
import json

ROOT = Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.links, self.meta = path, set(), [], {}
        self.h1, self.canonical, self.lang, self.alts = 0, None, None, []
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, (self.path, 'duplicate id', a['id'])
            self.ids.add(a['id'])
        if tag == 'html': self.lang = a.get('lang')
        if tag == 'h1': self.h1 += 1
        if tag == 'meta': self.meta[a.get('name', a.get('property'))] = a.get('content')
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical = a['href']
        if tag == 'img':
            assert 'alt' in a and 'width' in a and 'height' in a, (self.path, a)
        if tag in ('a', 'link', 'img', 'source', 'video'):
            self.links.extend(a[k] for k in ('href', 'src', 'poster') if k in a)

pages = {p: Page(p) for p in ROOT.rglob('*.html') if '.git' not in p.parts}
for path, page in pages.items():
    assert page.h1 == 1 and page.lang in ('en', 'es'), path
    assert all(page.meta.get(k) for k in ('description','viewport','og:title','og:description','og:image','og:url','twitter:card')), path
    expected = 'https://jnregames.github.io/' + str(path.relative_to(ROOT).parent).replace('.', '').strip('/')
    expected = expected.rstrip('/') + '/'
    assert page.canonical == expected == page.meta['og:url'], (path, expected)
    for link in page.links:
        u = urlsplit(link)
        if u.netloc == 'play.google.com':
            assert u.path == '/store/apps/details' and parse_qs(u.query).get('id') == ['com.jnr.galaxiga'], link
        if u.scheme or u.netloc: continue
        target = ROOT / unquote(u.path).lstrip('/') if u.path.startswith('/') else path.parent / unquote(u.path)
        if not u.path: target = path
        if target.is_dir(): target /= 'index.html'
        assert target.exists(), (path, link)
        if u.fragment and target in pages: assert u.fragment in pages[target].ids, (path, link)
config = json.loads((ROOT/'content/release.json').read_text())
assert config['status'] in ('coming_soon', 'available_now')
if config['status'] == 'coming_soon':
    for path in pages:
        text = path.read_text()
        assert ('PRÓXIMAMENTE' if pages[path].lang == 'es' else 'COMING SOON') in text
        assert 'AVAILABLE NOW' not in text and 'YA DISPONIBLE' not in text
print(f'PASS: {len(pages)} pages; routes/anchors/assets, metadata/canonicals, language, H1, release status and official Google Play targets')
