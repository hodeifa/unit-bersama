import re, sys, json
from playwright.sync_api import sync_playwright
import os; SC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESET = ':root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}'
def wrap(c): return '<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>' + RESET + '</style></head><body>' + c + '</body></html>'
open(SC + '/test/founder_doc.html', 'w', encoding='utf-8').write(wrap(open(sys.argv[1] if len(sys.argv) > 1 else SC + '/public/site_final.html', encoding='utf-8').read()))
URL = 'file://' + SC + '/test/founder_doc.html'
STUB = "window.__pub=[];window.claude={use:async function(n){if(n==='user')return{canEdit:async()=>true,isOwner:async()=>true};if(n==='artifact')return{publish:async function(h){window.__pub.push(h);return{version:'v9'}}};return null;}};"
res = []
def ok(n, c, e=''):
    res.append(bool(c)); print(('PASS ' if c else 'FAIL ') + n + (' | ' + str(e) if e else ''))
with sync_playwright() as p:
    b = p.chromium.launch()
    def np(w, h, scheme, stub, url=URL):
        ctx = b.new_context(viewport={'width': w, 'height': h}, color_scheme=scheme); pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.route('**/fonts.*/**', lambda r: r.abort())
        if stub: pg.add_init_script(STUB)
        pg.goto(url + '#tentang'); pg.wait_for_timeout(500); return pg, errs
    # publik tanpa foto
    pg, errs = np(1280, 900, 'dark', False)
    t = re.sub(r'\s+', ' ', pg.locator('main').inner_text())
    ok('publik: bagian Kenapa kami ada', 'KENAPA KAMI ADA' in t.upper())
    ok('publik: tanpa foto -> tata letak satu kolom, tanpa kotak kosong', pg.locator('.fnd.nophoto').count() == 1 and pg.locator('.ph0').count() == 0)
    ok('publik: kutipan & kisah tampil', 'tidak seharusnya menunggu kondisi finansial' in t and 'jarang dipakai' in t)
    ok('publik: 3 kartu alasan', pg.locator('.g3 .pc').count() == 3 and 'UNIT YANG JARANG DIPAKAI' in t.upper())
    ok('publik: tanpa tombol ubah', pg.locator('[data-act="founder"]').count() == 0)
    ok('publik: 4 paragraf kisah (baris kosong terjaga)', pg.locator('.fnd .ut').inner_text().count('\n\n') == 3, pg.locator('.fnd .ut').inner_text().count('\n\n'))
    ok('publik: tanpa error', not errs, errs); pg.context.close()
    # admin: unggah foto
    pg, errs = np(1280, 900, 'dark', True)
    pg.click('text=Kelola situs')
    ok('admin: kotak foto kosong tampil', pg.locator('.ph0').count() == 1)
    pg.click('[data-act="founder"]')
    ok('admin: kisah bawaan terisi di dialog', 'Banyak orang di sekitar kita' in pg.input_value('#f-story'))
    pg.set_input_files('#f-photo', SC + '/fixtures/potret.png'); pg.wait_for_timeout(800)
    ok('admin: pratinjau foto muncul', pg.locator('#prev-photo img').count() == 1)
    pg.fill('#f-name', 'Budi Santoso'); pg.fill('#f-role', 'Pendiri & Direktur')
    pg.click('dialog button[type=submit]'); pg.wait_for_timeout(200)
    ok('admin: foto tampil di halaman', pg.locator('.fph img').count() == 1 and pg.locator('.ph0').count() == 0)
    ok('admin: keterangan nama & jabatan di bawah foto', 'Budi Santoso' in pg.locator('.fph figcaption').inner_text() and 'Pendiri & Direktur' in pg.locator('.fph figcaption').inner_text())
    ok('admin: tanda tangan ganda tidak muncul saat ada foto', pg.locator('.sig').count() == 0)
    ratio = pg.evaluate("(()=>{var i=document.querySelector('.fph img').getBoundingClientRect();return i.width/i.height})()")
    ok('foto potret 4:5', abs(ratio - 0.8) < 0.02, ratio)
    pg.screenshot(path=SC + '/test/founder_desktop.png', full_page=False)
    pg.click('[data-act="publish"]'); pg.wait_for_timeout(300)
    doc = pg.evaluate('window.__pub[0]')
    st = json.loads(re.search(r'<script type="application/json" id="state">(.*?)</script>', doc, re.S).group(1).replace('\\u003c', '<'))
    f = st['site']['founder']
    ok('terbit: foto dan teks tersimpan', f['photo'].startswith('data:image/') and f['name'] == 'Budi Santoso' and len(f['photo']) < 400000, len(f['photo']))
    ok('terbit: gambar lain tetap ada', bool(st['settings'].get('heroImg')))
    ok('tanpa error (admin)', not errs, errs); pg.context.close()
    open(SC + '/test/founder_pub.html', 'w', encoding='utf-8').write(doc)
    # hasil terbit, publik, mobile
    pg, errs = np(390, 844, 'light', False, 'file://' + SC + '/test/founder_pub.html')
    ok('muat ulang mobile: foto tampil', pg.locator('.fph img').count() == 1)
    ok('mobile: tanpa scroll horizontal', pg.evaluate('document.documentElement.scrollWidth') <= 391)
    pg.screenshot(path=SC + '/test/founder_mobile.png', full_page=False)
    ok('mobile: tanpa error', not errs, errs); pg.context.close()
    b.close()
print('\n%d/%d lulus' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
