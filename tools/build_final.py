# Menggabungkan kode situs baru (site.html) dengan state di index.html yang sekarang (teks dan gambar unggahan Anda dipertahankan).
import re, json, sys
import os; SC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = SC + '/index.html'   # state (teks, gambar, kebijakan) dibaca dari index.html yang sekarang
RX = re.compile(r'(<script type="application/json" id="state">)(.*?)(</script>)', re.S)
live = json.loads(RX.search(open(LIVE, encoding='utf-8').read()).group(2))
site = open(SC + '/public/site.html', encoding='utf-8').read()
new = json.loads(RX.search(site).group(2))
merged = dict(live)           # state langsung = sumber kebenaran
for k, v in new.items():
    merged.setdefault(k, v)   # kunci baru dari template bila belum ada
js = json.dumps(merged, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
out = site[:RX.search(site).start(2)] + js + site[RX.search(site).end(2):]
open(SC + '/public/site_final.html', 'w', encoding='utf-8').write(out)
print('final', len(out), 'keys', list(merged.keys()), 'hero' , bool(merged['settings'].get('heroImg')), 'img models', [m['id'] for m in merged['models'] if m.get('img')])
