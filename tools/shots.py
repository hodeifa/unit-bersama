import sys
from playwright.sync_api import sync_playwright
import os; SC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = sys.argv[1] if len(sys.argv) > 1 else SC + '/public/site.html'
content = open(src, encoding='utf-8').read()
FD = SC + '/fonts/node_modules/@fontsource'
FONTCSS = ''.join("@font-face{font-family:'Barlow Condensed';font-weight:%d;font-display:block;src:url('file://%s/barlow-condensed/files/barlow-condensed-latin-%d-normal.woff2') format('woff2')}" % (w, FD, w) for w in (500, 600, 700, 800)) + ''.join("@font-face{font-family:'Barlow';font-weight:%d;font-display:block;src:url('file://%s/barlow/files/barlow-latin-%d-normal.woff2') format('woff2')}" % (w, FD, w) for w in (400, 500, 600, 700))
RESET = FONTCSS + ':root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}'
doc = '<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>' + RESET + '</style></head><body>' + content + '</body></html>'
open(SC + '/test/site_doc.html', 'w', encoding='utf-8').write(doc)
routes = ['beranda', 'cara-kerja', 'biaya', 'aturan', 'perlindungan', 'faq', 'tentang']
with sync_playwright() as p:
    b = p.chromium.launch()
    for (w, h, scheme, tag) in [(1280, 900, 'light', 'd'), (390, 844, 'light', 'm')]:
        ctx = b.new_context(viewport={'width': w, 'height': h}, color_scheme=scheme)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.route('**/fonts.googleapis.com/**', lambda r: r.abort()); pg.route('**/fonts.gstatic.com/**', lambda r: r.abort())
        for r in routes:
            pg.goto('file://' + SC + '/test/site_doc.html#' + r)
            pg.reload(); pg.wait_for_timeout(300)
            sw = pg.evaluate('document.documentElement.scrollWidth')
            print(tag, r, 'scrollWidth', sw, 'ok' if sw <= w + 1 else 'OVERFLOW')
            pg.screenshot(path=SC + '/test/s_%s_%s.png' % (tag, r), full_page=True)
        print('errors', errs)
        ctx.close()
