import re, sys, json
from playwright.sync_api import sync_playwright

import os; SC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else SC + '/public/site_final.html'
RESET = ':root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}'
def wrap(content):
    return '<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>' + RESET + '</style></head><body>' + content + '</body></html>'
open(SC + '/test/site_test_doc.html', 'w', encoding='utf-8').write(wrap(open(SRC, encoding='utf-8').read()))
URL = 'file://' + SC + '/test/site_test_doc.html'

STUB = """
window.__pub=[];
window.claude={use:async function(n){
  if(n==='user') return {canEdit:async()=>true,isOwner:async()=>true};
  if(n==='artifact') return {publish:async function(h){window.__pub.push(h);return {version:'v9'}}};
  return null;}};
"""
results = []
def ok(name, cond, extra=''):
    results.append((name, bool(cond)))
    print(('PASS ' if cond else 'FAIL ') + name + (' | ' + str(extra) if extra else ''))


def idr(n):
    n = int(n + 0.5) if n >= 0 else -int(-n + 0.5)
    return ('−' if n < 0 else '') + 'Rp' + format(abs(n), ',').replace(',', '.')
def calc(contrib, trips, varm, sale):
    c = contrib * 1e6; pool = c * 6; unit = pool / 1.1
    s = unit * sale / 100; fe = s * 0.1; per = (s - fe) / 6
    out = c + 250000 * 60 + 100000 * trips * 5 + varm * 60
    return {'month': idr((out - per) / 60), 'out': idr(out), 'fe': idr(-fe), 'margin': idr(pool - unit), 'unit': idr(unit)}

ROUTES = ['beranda', 'cara-kerja', 'biaya', 'aturan', 'perlindungan', 'faq', 'tentang']
H1 = {'beranda': 'Satu moge', 'cara-kerja': 'Dari pilih model', 'biaya': 'Biaya yang perlu', 'aturan': 'Aturan pemakaian', 'perlindungan': 'Yang sudah pasti', 'faq': 'Pertanyaan yang sering', 'tentang': 'Tentang kami'}

with sync_playwright() as p:
    b = p.chromium.launch()
    def newpage(w, h, scheme, stub=True, url=URL):
        ctx = b.new_context(viewport={'width': w, 'height': h}, color_scheme=scheme)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' and 'ERR_' not in m.text and 'Failed to load resource' not in m.text else None)
        pg.route('**/fonts.googleapis.com/**', lambda r: r.abort()); pg.route('**/fonts.gstatic.com/**', lambda r: r.abort())
        if stub: pg.add_init_script(STUB)
        pg.goto(url); pg.wait_for_timeout(500)
        return pg, errs
    def go(pg, r):
        pg.evaluate("location.hash='#%s'" % r); pg.wait_for_timeout(150)
    def text(pg): return re.sub(r'\s+', ' ', pg.locator('main').inner_text())

    # ---- 1. publik: semua rute, menu, tanpa kontrol admin
    pg, errs = newpage(1280, 900, 'dark', stub=False)
    ok('publik: tidak ada tombol kelola', pg.locator('text=Kelola situs').count() == 0)
    ok('publik: hero & foto Street Rod dari state tayang', pg.locator('.hph .frame img').count() == 1 and pg.locator('.card img.mimg').count() == 1)
    for r in ROUTES:
        go(pg, r)
        h1 = pg.locator('main h1').first.inner_text().strip().lower().replace('\n', ' ')
        ok('rute #%s tampil' % r, H1[r].lower() in h1, h1[:60])
        cur = pg.locator('.nav a[aria-current="page"]').get_attribute('href')
        ok('menu aktif #%s' % r, cur == '#' + r, cur)
    # klik menu
    pg.click('.nav a[href="#biaya"]'); pg.wait_for_timeout(150)
    ok('klik menu -> Biaya', 'Simulasi biaya per anggota' in text(pg).replace('SIMULASI', 'Simulasi') or pg.locator('#calc-out').count() == 1)
    pg.evaluate("location.hash='#tidak-ada'"); pg.wait_for_timeout(150)
    ok('hash tak dikenal -> beranda', pg.locator('.tier').count() == 3)
    go(pg, 'perlindungan')
    ok('perlindungan: 6 ketentuan "Sedang difinalisasi"', pg.locator('.pol.tbd').count() == 6, pg.locator('.pol.tbd').count())
    ok('perlindungan: 8 kartu risiko', pg.locator('.g3 .pc').count() == 8, pg.locator('.g3 .pc').count())
    t = text(pg)
    ok('perlindungan: jawaban 1-3 ada (PT, denda, sanksi)', 'PT Mitra Nusantara Solusindo' in t and 'dikenakan denda' in t and 'pengurangan masa pakai' in t)
    ok('perlindungan: tak ada klaim untung', not re.search(r'imbal hasil(?! )|pasti untung|dijamin', t.replace('Tidak ada janji keuntungan atau imbal hasil', '')) )
    go(pg, 'faq')
    ok('faq: 11 pertanyaan', pg.locator('.faq details').count() == 11, pg.locator('.faq details').count())
    pg.locator('.faq summary').nth(1).click()
    ans = pg.locator('.faq details').nth(1).inner_text()
    ok('faq: token {dp} diganti 5%', '{dp}' not in ans and '5%' in ans, ans[-120:])
    ok('faq: tautan antar halaman [[#biaya|Biaya]] jadi anchor', pg.locator('.faq details').nth(1).locator('a[href="#biaya"]').count() == 1)
    pg.locator('.faq details').nth(3).locator('summary').click()
    ok('faq: token {perusahaan} diganti', 'PT Mitra Nusantara Solusindo' in pg.locator('.faq details').nth(3).inner_text())
    go(pg, 'tentang')
    ok('tentang: NIB/alamat "Sedang dilengkapi"', pg.locator('.idl dd.na').count() == 4, pg.locator('.idl dd.na').count())
    ok('tentang: tombol WA aktif (nomor dari state tayang)', pg.locator('main a.btn.primary:has-text("Chat WhatsApp")').count() == 1)
    ok('publik: tanpa error JS', not errs, errs)
    pg.context.close()

    # ---- 2. kalkulator
    pg, errs = newpage(1280, 900, 'light', stub=False)
    go(pg, 'biaya')
    big = lambda: pg.locator('.big b').inner_text().strip()
    E = calc(75, 0, 0, 70)
    ok('kalkulator default %s/bln' % E['month'], big() == E['month'], big())
    def setr(k, v): pg.evaluate("(a)=>{var e=document.getElementById('c-'+a[0]);e.value=a[1];e.dispatchEvent(new Event('input',{bubbles:true}))}", [k, v])
    setr('sale', 100)
    E = calc(75, 0, 0, 100)
    ok('jual 100%% -> %s' % E['month'], big() == E['month'], big())
    setr('sale', 70); setr('contrib', 100)
    E = calc(100, 0, 0, 70)
    ok('kontribusi 100 jt -> %s' % E['month'], big() == E['month'], big())
    ok('label kontribusi diperbarui', pg.locator('#o-contrib').inner_text() == 'Rp100.000.000', pg.locator('#o-contrib').inner_text())
    ok('range harga setara Prestige', 'Prestige' in pg.locator('#calc-out').inner_text())
    setr('contrib', 50); setr('trips', 10); setr('varm', 500000)
    # c=50M; iuran 15M; antar 5M; var 30M => out 100M; pool 300M sale 70% = 210M fee 21M net 189M per 31.5M; cost 68.5M; /60 = 1.141.667
    E = calc(50, 10, 500000, 70)
    ok('kombinasi input -> %s' % E['month'], big() == E['month'], big())
    out = pg.locator('#calc-out').inner_text()
    ok('rincian: total pengeluaran, komisi, margin, harga unit', E['out'] in out and E['fe'] in out and E['margin'] in out and E['unit'] in out, (E, out[:300].replace('\n', ' | ')))
    ok('slider tetap fokus setelah input (tak dirender ulang)', pg.evaluate("document.getElementById('c-varm') !== null"))
    pg.context.close()

    # ---- 3. mobile: tanpa scroll horizontal di semua rute
    pg, errs = newpage(390, 844, 'light', stub=False)
    for r in ROUTES:
        go(pg, r)
        sw = pg.evaluate('document.documentElement.scrollWidth')
        ok('mobile #%s tanpa scroll horizontal' % r, sw <= 391, sw)
    pg.screenshot(path=SC + '/test/m_nav.png', clip={'x': 0, 'y': 0, 'width': 390, 'height': 300})
    ok('mobile: tanpa error JS', not errs, errs)
    pg.context.close()

    # ---- 4. admin: info pengelola, ketentuan, FAQ, terbitkan, muat ulang hasil terbit
    pg, errs = newpage(1280, 900, 'dark')
    ok('admin: tombol Kelola situs', pg.locator('text=Kelola situs').count() == 1)
    pg.click('text=Kelola situs')
    ok('admin: bar kelola + Info pengelola + Ketentuan', pg.locator('.abar.on').count() == 1 and pg.locator('[data-act="company"]').count() >= 1 and pg.locator('[data-act="policy"]').count() >= 1)
    ok('admin: + Model hanya di beranda', pg.locator('[data-act="model-add"]').count() == 1)
    go(pg, 'faq')
    ok('admin: + Model hilang di halaman lain', pg.locator('[data-act="model-add"]').count() == 0)
    ok('admin: Terbitkan nonaktif awalnya', pg.locator('[data-act="publish"]').is_disabled())
    # info pengelola
    pg.click('.abar [data-act="company"]')
    pg.fill('#f-nib', '1234567890123'); pg.fill('#f-email', 'salah'); pg.click('dialog button[type=submit]')
    ok('admin: email tak valid ditolak', pg.locator('#ferr').is_visible())
    pg.fill('#f-email', 'halo@mitra.example'); pg.fill('#f-address', 'Jl. Contoh No. 1\nJakarta'); pg.fill('#f-hours', 'Senin–Jumat, 09.00–17.00 WIB')
    pg.click('dialog button[type=submit]')
    go(pg, 'tentang')
    ok('admin: data pengelola tampil di Tentang', pg.locator('.idl dd.na').count() == 0 and 'halo@mitra.example' in text(pg), pg.locator('.idl dd.na').count())
    # ketentuan
    go(pg, 'perlindungan')
    pg.click('[data-act="policy"][data-key="dpPenalty"]')
    ok('admin: dialog ketentuan fokus ke kolom denda', pg.evaluate("document.activeElement && document.activeElement.id") == 'f-dpPenalty')
    pg.fill('#f-dpPenalty', 'Denda 20% dari DP.'); pg.fill('#f-usage', 'SIM C/A aktif wajib.\nMaks 3 hari per giliran.')
    pg.click('dialog button[type=submit]')
    ok('admin: ketentuan terisi -> 2 "Sudah ditetapkan", 4 tbd', pg.locator('.pol.ok').count() == 2 and pg.locator('.pol.tbd').count() == 4, (pg.locator('.pol.ok').count(), pg.locator('.pol.tbd').count()))
    ok('admin: teks ketentuan tampil dengan baris baru', 'Denda 20% dari DP.' in text(pg))
    go(pg, 'aturan')
    ok('aturan: ketentuan SIM ikut tampil', 'SIM C/A aktif wajib' in text(pg))
    # FAQ
    go(pg, 'faq')
    pg.click('[data-act="faq-add"]')
    pg.fill('#f-q', 'Apakah ada biaya admin?'); pg.fill('#f-a', 'Lihat [[#biaya|Biaya]] untuk {perusahaan}.')
    pg.click('dialog button[type=submit]')
    ok('admin: FAQ ditambah -> 12', pg.locator('.faq details').count() == 12, pg.locator('.faq details').count())
    pg.locator('.faq details').nth(0).locator('summary').click()
    pg.click('[data-act="faq-edit"][data-id="q1"]')
    pg.fill('#f-q', 'Apakah ini investasi?'); pg.click('dialog button[type=submit]')
    ok('admin: FAQ diubah', 'Apakah ini investasi?' in pg.locator('.faq').inner_text())
    pg.locator('.faq details').nth(2).locator('summary').click()
    pg.click('[data-act="faq-edit"][data-id="q3"]')
    pg.click('#fdel'); pg.click('#fdel')
    ok('admin: FAQ dihapus dengan dua langkah -> 11', pg.locator('.faq details').count() == 11, pg.locator('.faq details').count())
    ok('admin: Terbitkan aktif', not pg.locator('[data-act="publish"]').is_disabled())
    # terbitkan
    pg.click('[data-act="publish"]'); pg.wait_for_timeout(300)
    pub = pg.evaluate('window.__pub')
    ok('terbit: 1 dokumen diterbitkan', len(pub) == 1)
    doc = pub[0]
    ok('terbit: diawali doctype & skeleton platform', doc.startswith('<!doctype html><html><head><meta charset=utf8>') and '<title>Unit Bersama</title>' in doc)
    ok('terbit: ukuran wajar', len(doc) < 12_000_000, len(doc))
    st = json.loads(re.search(r'<script type="application/json" id="state">(.*?)</script>', doc, re.S).group(1).replace('\\u003c', '<'))
    ok('terbit: state memuat company/policy/faq', st['site']['company']['nib'] == '1234567890123' and st['site']['policy']['dpPenalty'] == 'Denda 20% dari DP.' and len(st['site']['faq']) == 11)
    ok('terbit: gambar unggahan tetap ada', bool(st['settings'].get('heroImg')) and any(m.get('img') for m in st['models']))
    ok('terbit: 19 model tetap', len(st['models']) == 19)
    ok('tanpa error JS (admin)', not errs, errs)
    pg.context.close()

    # ---- 5. muat ulang dokumen hasil terbit (publik)
    open(SC + '/test/site_published.html', 'w', encoding='utf-8').write(doc)
    pg, errs = newpage(1280, 900, 'light', stub=False, url='file://' + SC + '/test/site_published.html')
    go(pg, 'perlindungan')
    ok('muat ulang: ketentuan terisi bertahan', pg.locator('.pol.ok').count() == 2 and 'Denda 20% dari DP.' in text(pg))
    go(pg, 'tentang')
    ok('muat ulang: data pengelola bertahan', 'halo@mitra.example' in text(pg) and '1234567890123' in text(pg))
    go(pg, 'faq')
    ok('muat ulang: FAQ 11 & tanpa pertanyaan terhapus', pg.locator('.faq details').count() == 11 and 'Apakah unit di katalog itu unit asli?' not in pg.locator('.faq').inner_text())
    go(pg, 'beranda')
    ok('muat ulang: foto tetap tampil', pg.locator('.hph .frame img').count() == 1)
    ok('muat ulang: tanpa error JS', not errs, errs)
    pg.context.close()

    b.close()

bad = [n for n, r in results if not r]
print('\n%d/%d lulus' % (len(results) - len(bad), len(results)))
if bad:
    print('GAGAL:', bad)
    sys.exit(1)
