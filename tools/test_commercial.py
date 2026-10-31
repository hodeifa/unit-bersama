import re, sys
from playwright.sync_api import sync_playwright
import os; SC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else SC + '/public/site_final.html'
FD = SC + '/fonts/node_modules/@fontsource'
FONTCSS = ''.join("@font-face{font-family:'Barlow Condensed';font-weight:%d;font-display:block;src:url('file://%s/barlow-condensed/files/barlow-condensed-latin-%d-normal.woff2') format('woff2')}" % (w, FD, w) for w in (500, 600, 700, 800)) + ''.join("@font-face{font-family:'Barlow';font-weight:%d;font-display:block;src:url('file://%s/barlow/files/barlow-latin-%d-normal.woff2') format('woff2')}" % (w, FD, w) for w in (400, 500, 600, 700))
RESET = FONTCSS + ':root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}'
open(SC + '/test/com_doc.html', 'w', encoding='utf-8').write('<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>' + RESET + '</style></head><body>' + open(SRC, encoding='utf-8').read() + '</body></html>')
URL = 'file://' + SC + '/test/com_doc.html'
STUB = "window.__pub=[];window.claude={use:async function(n){if(n==='user')return{canEdit:async()=>true,isOwner:async()=>true};if(n==='artifact')return{publish:async function(h){window.__pub.push(h);return{version:'v9'}}};return null;}};"
res = []
def ok(n, c, x=''):
    res.append(bool(c)); print(('PASS ' if c else 'FAIL ') + n + (' | ' + str(x) if x else ''))
ROUTES = ['beranda', 'cara-kerja', 'biaya', 'aturan', 'perlindungan', 'faq', 'tentang']
with sync_playwright() as p:
    b = p.chromium.launch()
    def page(w, h, scheme='light', stub=False):
        ctx = b.new_context(viewport={'width': w, 'height': h}, color_scheme=scheme)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.route('**/fonts.googleapis.com/**', lambda r: r.abort()); pg.route('**/fonts.gstatic.com/**', lambda r: r.abort())
        if stub: pg.add_init_script(STUB)
        pg.goto(URL); pg.wait_for_timeout(300)
        return pg, errs
    def go(pg, r): pg.evaluate("location.hash='#%s'" % r); pg.wait_for_timeout(150)

    # desktop
    pg, errs = page(1280, 900)
    wa = pg.locator('header.top a.hdcta').get_attribute('href')
    ok('header: tombol WhatsApp ke nomor tayang', wa and wa.startswith('https://wa.me/6285708090100?text='), wa)
    ok('header: lengket untuk pengunjung', pg.evaluate("getComputedStyle(document.querySelector('header.top')).position") == 'sticky')
    ok('promo: bar atas ada', pg.locator('.promo').count() == 1)
    ok('hero: h1 dua baris + foto', pg.locator('.hero2 h1 span').count() == 2 and pg.locator('.hph .frame img').count() == 1)
    ok('hero: tombol utama tidak menyempit', pg.locator('.hero2 .btn.primary').bounding_box()['width'] > 150, pg.locator('.hero2 .btn.primary').bounding_box())
    ok('mobile bar: tersembunyi di desktop', not pg.locator('.mcta').is_visible())
    ok('menu seluler: tersembunyi di desktop', not pg.locator('.mnav').is_visible() and pg.locator('.nav').is_visible())
    h0 = pg.evaluate('location.hash')
    pg.locator('.hero2 button[data-act="scroll"]').click(); pg.wait_for_timeout(900)
    top = pg.evaluate("document.getElementById('katalog').getBoundingClientRect().top")
    ok('hero: "Pilih motor impian" menggulir ke katalog', abs(top - 72) < 120 and pg.evaluate('location.hash') == h0, top)
    ok('beranda: 4 manfaat, tabel banding 6 baris, 4 langkah',
       pg.locator('.ben .bc').count() == 4 and pg.locator('.cmp .row:not(.h)').count() == 6 and pg.locator('.stp li').count() == 4)
    ok('katalog: satu grid, 6 kartu entry', pg.locator('#katalog .cards').count() == 1 and pg.locator('#katalog .card').count() == 6 and pg.locator('.gh').count() == 0)
    lnk = pg.locator('.card .btn.primary').first.get_attribute('href')
    ok('kartu: WA berisi nama model', 'Street%20Rod' in lnk, lnk[:140])
    ok('kartu: bar slot 6 segmen', pg.locator('.card').first.locator('.seg i').count() == 6)
    # teaser kalkulator
    before = pg.locator('#tz-out .big b').inner_text()
    pg.evaluate("var e=document.getElementById('c-contrib'); e.value=100; e.dispatchEvent(new Event('input',{bubbles:true}))"); pg.wait_for_timeout(100)
    after = pg.locator('#tz-out .big b').inner_text()
    ok('teaser kalkulator: geser kontribusi mengubah total', before == 'Rp90.000.000' and after == 'Rp115.000.000', (before, after))
    ok('teaser kalkulator: label kontribusi ikut', pg.locator('#o-contrib').inner_text() == 'Rp100.000.000')
    ok('pendiri: teaser tampil dengan nama', 'Hodeifa' in pg.locator('.fte').inner_text())
    ok('faq ringkas: 5 butir + tautan semua', pg.locator('.sect .faq details').count() == 5 and pg.locator('a[href="#faq"]').count() >= 1)
    ok('pita CTA akhir + footer WA', pg.locator('.cband a.btn.ink').count() == 1 and '+6285708090100' in pg.locator('footer').inner_text())
    ok('desktop: tanpa error JS', not errs, errs)
    for r in ROUTES:
        go(pg, r)
        ok('rute %s: pita judul/hero, CTA akhir, tanpa overflow' % r, (pg.locator('.phd').count() + pg.locator('.hero2').count()) == 1 and pg.locator('.cband').count() == 1 and pg.evaluate('document.documentElement.scrollWidth') <= 1281)
    pg.context.close()

    # ponsel
    for w in (360, 390, 768):
        pg, errs = page(w, 800)
        for r in ROUTES:
            go(pg, r)
            sw = pg.evaluate('document.documentElement.scrollWidth')
            ok('overflow %dpx rute %s' % (w, r), sw <= w + 1, sw)
        ok('%dpx: tanpa error JS' % w, not errs, errs)
        pg.context.close()
    pg, errs = page(390, 800)
    ok('ponsel: bilah WhatsApp bawah tampil', pg.locator('.mcta').is_visible() and pg.locator('.mcta a').get_attribute('href').startswith('https://wa.me/'))
    ok('ponsel: tombol menu tampil, nav sebaris disembunyikan', pg.locator('.mnav summary').is_visible() and not pg.locator('.nav').is_visible())
    pg.locator('.mnav summary').click(); pg.wait_for_timeout(100)
    ok('ponsel: menu terbuka berisi 7 tautan', pg.locator('.mnav nav a').count() == 7 and pg.locator('.mnav nav a').first.is_visible())
    pg.locator('.mnav nav a', has_text='Biaya').click(); pg.wait_for_timeout(250)
    ok('ponsel: pilih menu -> rute biaya & menu menutup', pg.evaluate('location.hash') == '#biaya' and pg.locator('.mnav[open]').count() == 0 and 'BIAYA YANG PERLU' in pg.locator('h1').inner_text().upper())
    lg = pg.evaluate("(()=>{const r=document.querySelector('.logo').getBoundingClientRect();return [r.width, document.querySelector('.logo span').scrollWidth > document.querySelector('.logo span').clientWidth]})()")
    ok('ponsel: nama merek tidak terpotong', lg[1] is False, lg)
    pg.context.close()

    # admin (pemilik)
    pg, errs = page(1280, 900, stub=True)
    ok('admin: header tidak lengket, bar kelola tampil', pg.evaluate("getComputedStyle(document.querySelector('header.top')).position") == 'static' and pg.locator('.abar').count() == 1)
    pg.locator('.abar [data-act="admin"]').click(); pg.wait_for_timeout(150)
    ok('admin: mode kelola, bar bawah ponsel tidak ada', pg.locator('.abar.on').count() == 1 and pg.locator('.mcta').count() == 0)
    ok('admin: tombol Ubah di kartu + slot admin', pg.locator('.card [data-act="model-edit"]').count() == 6)
    pg.locator('.abar [data-act="settings"]').click(); pg.wait_for_timeout(150)
    ok('admin: dialog pengaturan terbuka', pg.locator('dialog[open]').count() == 1)
    ok('admin: tanpa error JS', not errs, errs)
    pg.context.close()

    # tema gelap
    pg, errs = page(1280, 900, 'dark')
    bg = pg.evaluate("getComputedStyle(document.body).backgroundColor")
    cb = pg.evaluate("getComputedStyle(document.querySelector('.sect.alt')).backgroundColor")
    ok('tema gelap: latar gelap dan bagian alt berbeda', bg == 'rgb(15, 17, 20)' and cb != bg, (bg, cb))
    pg.screenshot(path=SC + '/test/dark_home.png', full_page=False)
    pg.context.close()
print('\n%d/%d lulus' % (sum(res), len(res)))
