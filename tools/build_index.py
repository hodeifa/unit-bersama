# Membuat index.html mandiri (siap deploy statis) dari public/site_final.html.
# Kerangka dokumen (doctype, meta, reset CSS) sama dengan yang dipakai Claude, supaya hasilnya identik dengan versi tayang.
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAD = '<meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}html{scroll-padding-top:env(safe-area-inset-top,0px)}body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#fff;color:#000}img{max-width:100%}[hidden]:not([hidden=until-found i]){display:none!important}</style>'
content = open(ROOT + '/public/site_final.html', encoding='utf-8').read()
doc = '<!doctype html><html lang="id"><head>' + HEAD + '</head><body>' + content + '</body></html>'
open(ROOT + '/index.html', 'w', encoding='utf-8').write(doc)
print('index.html', len(doc), 'byte')
