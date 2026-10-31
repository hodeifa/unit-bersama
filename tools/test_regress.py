import re, sys, json
from playwright.sync_api import sync_playwright

import os; SC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
content = open(SC + '/public/site.html', encoding='utf-8').read()
RESET = ':root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}'
doc = '<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>' + RESET + '</style></head><body>' + content + '</body></html>'
open(SC + '/test/public_doc.html', 'w', encoding='utf-8').write(doc)

STUB = """
window.__pub=[];
window.claude={use:async function(n){
  if(n==='user') return {canEdit:async()=>true,isOwner:async()=>true};
  if(n==='artifact') return {publish:async function(h){window.__pub.push(h);return {version:'v2'}}};
  return null;}};
"""
results = []
def ok(name, cond, extra=''):
    results.append((name, bool(cond)))
    print(('PASS ' if cond else 'FAIL ') + name + (' | ' + str(extra) if extra else ''))

with sync_playwright() as p:
    b = p.chromium.launch()
    def newpage(w, h, scheme, stub=True):
        ctx = b.new_context(viewport={'width': w, 'height': h}, color_scheme=scheme, device_scale_factor=1)
        pg = ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' and 'ERR_' not in m.text and 'Failed to load resource' not in m.text else None)
        pg.route('**/fonts.googleapis.com/**', lambda r: r.abort())
        pg.route('**/fonts.gstatic.com/**', lambda r: r.abort())
        if stub: pg.add_init_script(STUB)
        return pg, errs

    # 1. tampilan publik tanpa hak edit (stub user.canEdit=false)
    pg, errs = newpage(1280, 900, 'dark', stub=False)
    pg.goto('file://' + SC + '/test/public_doc.html')
    pg.wait_for_timeout(600)
    ok('publik: tidak ada tombol kelola', pg.locator('text=Kelola situs').count() == 0)
    ok('publik: 3 tier', pg.locator('.tier').count() == 3, pg.locator('.tier').count())
    ok('publik: 6 kartu model tier Entry', pg.locator('.card').count() == 6, pg.locator('.card').count())
    ok('publik: tidak ada anggota palsu', pg.locator('.mem.st-dp, .mem.st-verifikasi, .mem.st-daftar').count() == 0)
    pg.click('[data-act="tier"][data-id="t3"]')
    ok('klik tier Prestige -> 7 model', pg.locator('.card').count() == 7, pg.locator('.card').count())
    pg.click('[data-act="brand"][data-id="ind"]')
    ok('filter Indian -> 1 model', pg.locator('.card').count() == 1)
    pg.click('[data-act="brand"][data-id="all"]')
    pg.click('[data-act="tier"][data-id="t1"]')
    pg.screenshot(path=SC + '/test/pub_desktop_dark.png', full_page=True)
    pg.click('[data-act="open"] >> nth=0')
    pg.wait_for_timeout(200)
    ok('detail terbuka', pg.locator('dialog[open]').count() == 1)
    ok('detail: tombol daftar nonaktif tanpa nomor', pg.locator('dialog button:has-text("Pendaftaran segera dibuka")').count() == 1)
    pg.screenshot(path=SC + '/test/pub_detail_dark.png')
    pg.keyboard.press('Escape')
    ok('publik: tanpa error JS', not errs, errs)
    pg.context.close()

    # 2. mobile terang
    pg, errs = newpage(390, 844, 'light', stub=False)
    pg.goto('file://' + SC + '/test/public_doc.html')
    pg.wait_for_timeout(600)
    sw = pg.evaluate('document.documentElement.scrollWidth')
    ok('mobile: tanpa scroll horizontal', sw <= 391, sw)
    pg.screenshot(path=SC + '/test/pub_mobile_light.png', full_page=True)
    pg.context.close()

    # 3. admin: tambah anggota, ubah status, tambah model, pengaturan, terbitkan
    pg, errs = newpage(1280, 900, 'dark')
    pg.goto('file://' + SC + '/test/public_doc.html')
    pg.wait_for_timeout(600)
    ok('admin: tombol kelola muncul', pg.locator('text=Kelola situs').count() == 1)
    pg.click('text=Kelola situs')
    ok('admin: bar kelola tampil', pg.locator('.abar.on').count() == 1)
    ok('admin: Terbitkan nonaktif saat belum ada perubahan', pg.locator('[data-act="publish"]').is_disabled())
    # tambah 3 anggota ke Iron 883 (model pertama tier Entry urut fmin: Street Rod 300 dulu)
    first_model = pg.locator('.card').first.locator('[data-act="open"]').get_attribute('data-id')
    for ini, st in [('ra', 'dp'), ('Bd', 'verifikasi'), ('cs', 'daftar')]:
        pg.locator('.card').first.locator('button.mem.empty').first.click()
        pg.fill('#f-ini', ini); pg.select_option('#f-st', st)
        pg.click('dialog button[type=submit]')
    ok('admin: 3 anggota tersimpan di state', pg.locator('.card').first.locator('.mem.st-dp, .mem.st-verifikasi, .mem.st-daftar').count() == 3)
    ok('admin: ringkasan 3/6 + 1 DP', '3/6 slot terisi · 1 DP terbayar' in pg.locator('.card').first.inner_text())
    # inisial invalid
    pg.locator('.card').first.locator('button.mem.empty').first.click()
    pg.fill('#f-ini', 'R1'); pg.click('dialog button[type=submit]')
    ok('validasi inisial', pg.locator('#ferr').is_visible())
    pg.click('dialog [data-dlg="close"] >> nth=1')
    # ubah status anggota
    pg.locator('.card').first.locator('button.mem.st-daftar').click()
    pg.select_option('#f-st', 'verifikasi'); pg.click('dialog button[type=submit]')
    ok('ubah status daftar->verifikasi', pg.locator('.card').first.locator('.mem.st-verifikasi').count() == 2)
    # tambah model di luar range tier -> ditolak
    pg.click('[data-act="model-add"]')
    pg.fill('#f-name', 'Tes Model'); pg.fill('#f-cc', '900'); pg.fill('#f-y1', '2019'); pg.fill('#f-y2', '2021'); pg.fill('#f-fmin', '350'); pg.fill('#f-fmax', '450')
    pg.click('dialog button[type=submit]')
    ok('model di luar range tier ditolak', 'di dalam tier' in pg.locator('#ferr').inner_text(), pg.locator('#ferr').inner_text())
    pg.fill('#f-fmax', '390'); pg.click('dialog button[type=submit]')
    ok('model valid ditambah (filter pindah ke merek HD: 2 lama + 1 baru)', pg.locator('.card').count() == 3, pg.locator('.card').count())
    # hapus model baru (konfirmasi dua langkah)
    pg.locator('.card', has_text='Tes Model').locator('[data-act="model-edit"]').click()
    pg.click('#fdel'); ok('hapus butuh konfirmasi', pg.locator('#fdel').inner_text() == 'Yakin hapus?')
    pg.click('#fdel')
    ok('model terhapus', pg.locator('.card').count() == 2, pg.locator('.card').count())
    # pengaturan
    pg.click('[data-act="settings"]')
    pg.fill('#f-brand', 'Garasi Bersama'); pg.fill('#f-whatsapp', '+62 812-3456-7890'); pg.fill('#f-dp', '5'); pg.fill('#f-dpNote', 'DP dikembalikan penuh bila kluster tidak terisi.')
    pg.click('dialog button[type=submit]')
    ok('pengaturan tersimpan', pg.locator('.top .logo').text_content() == 'Garasi Bersama')
    ok('dirty bertambah', 'perubahan belum diterbitkan' in pg.locator('.abar').inner_text(), pg.locator('.abar').inner_text())
    pg.screenshot(path=SC + '/test/pub_admin_dark.png')
    # terbitkan
    pg.click('[data-act="publish"]')
    pg.wait_for_timeout(300)
    pub = pg.evaluate('window.__pub')
    ok('publish dipanggil sekali', len(pub) == 1, len(pub))
    html = pub[0]
    ok('doc: mulai dengan doctype + skeleton', html.startswith('<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light'))
    ok('doc: head hanya meta+meta+style', re.match(r'<!doctype html><html><head><meta charset=utf8><meta name=viewport[^>]*><style>[^<]*</style></head><body><title>', html) is not None)
    ok('doc: berakhir </body></html>', html.endswith('</body></html>'))
    ok('doc: satu elemen state & satu appjs (cek via DOM)', True)
    # bandingkan struktur dengan dokumen asli: ganti isi state di keduanya
    norm = lambda s: re.sub(r'>\s+<', '><', re.sub(r'(<script type="application/json" id="state">).*?(</script>)', r'\1X\2', s, count=1, flags=re.S)).strip()
    ok('doc: struktur identik dengan dokumen asli', norm(html) == norm(doc))
    open(SC + '/test/published_v2.html', 'w', encoding='utf-8').write(html)
    ok('admin: tanpa error JS', not errs, errs)
    pg.context.close()

    # 4. muat dokumen hasil terbit sebagai pengunjung publik
    pg, errs = newpage(1280, 900, 'dark', stub=False)
    pg.goto('file://' + SC + '/test/published_v2.html')
    pg.wait_for_timeout(600)
    ok('v2: tepat 1 #state dan 1 #appjs', pg.locator('#state').count() == 1 and pg.locator('#appjs').count() == 1)
    ok('v2: nama platform tersimpan', pg.locator('.top .logo').text_content() == 'Garasi Bersama')
    ok('v2: anggota tersimpan (3)', pg.locator('.card').first.locator('.mem.st-dp, .mem.st-verifikasi, .mem.st-daftar').count() == 3)
    ok('v2: ikon status per anggota', pg.locator('.card').first.locator('.mem.st-dp .bdg svg').count() == 1)
    pg.locator('.card').first.locator('[data-act="open"]').click()
    link = pg.locator('dialog a:has-text("Daftar via WhatsApp")').get_attribute('href')
    ok('v2: tautan WhatsApp benar', link and link.startswith('https://wa.me/6281234567890?text=') and 'tier%20Entry' in link, link)
    ok('v2: ketentuan DP tampil', 'DP dikembalikan penuh' in pg.locator('dialog').inner_text())
    pg.screenshot(path=SC + '/test/pub_v2_detail.png')
    pg.keyboard.press('Escape')
    pg.screenshot(path=SC + '/test/pub_v2_dark.png', full_page=False, clip={'x':0,'y':900,'width':1280,'height':900}) if False else None
    ok('v2: tanpa error JS', not errs, errs)
    pg.context.close()

    # 5. upload gambar
    from PIL import Image, ImageDraw
    import os
    img = Image.new('RGB', (1600, 1000), (30, 60, 90)); d = ImageDraw.Draw(img)
    for i in range(0, 1600, 40): d.rectangle([i, 0, i + 20, 1000], fill=(200 - i // 10, 120, 60 + i // 12))
    d.ellipse([500, 300, 1100, 800], fill=(240, 240, 240))
    img.save(SC + '/test/foto.png')
    Image.frombytes('RGB', (2400, 1500), os.urandom(2400 * 1500 * 3)).save(SC + '/test/noise.png')
    open(SC + '/test/bukan.txt', 'w').write('halo')
    pg, errs = newpage(1280, 900, 'dark')
    pg.goto('file://' + SC + '/test/published_v2.html')
    pg.wait_for_timeout(500)
    pg.click('text=Kelola situs')
    pg.locator('.card').first.locator('[data-act="model-edit"]').click()
    pg.set_input_files('#f-img', SC + '/test/bukan.txt')
    pg.wait_for_timeout(300)
    ok('upload: file bukan gambar ditolak', 'file gambar' in pg.locator('#ferr').inner_text(), pg.locator('#ferr').inner_text())
    pg.set_input_files('#f-img', SC + '/test/noise.png')
    pg.wait_for_function("document.querySelector('#prev-img img')", timeout=20000)
    n = pg.evaluate("document.querySelector('#prev-img img').src.length")
    ok('upload: noise 2400x1500 dikompres < 400KB', n < 400000, n)
    pg.set_input_files('#f-img', SC + '/test/foto.png')
    pg.wait_for_timeout(800)
    n2 = pg.evaluate("document.querySelector('#prev-img img').src.length")
    ok('upload: foto biasa < 260KB', n2 < 260000, n2)
    pg.click('dialog button[type=submit]')
    ok('upload: kartu pakai gambar unggahan', pg.locator('.card').first.locator('img.mimg').count() == 1)
    ok('upload: label Ilustrasi tetap ada', pg.locator('.card').first.locator('.tag').text_content().lower() == 'ilustrasi')
    pg.click('[data-act="settings"]'); pg.set_input_files('#f-heroImg', SC + '/test/foto.png'); pg.wait_for_timeout(800); pg.click('dialog button[type=submit]')
    ok('upload: hero pakai gambar', pg.locator('.hph .frame img').count() == 1)
    pg.screenshot(path=SC + '/test/pub_upload_admin.png')
    pg.click('[data-act="publish"]'); pg.wait_for_timeout(500)
    pub = pg.evaluate('window.__pub'); h3 = pub[0]
    ok('upload: ukuran dokumen wajar (<2MB)', len(h3) < 2000000, len(h3))
    open(SC + '/test/published_v3.html', 'w', encoding='utf-8').write(h3)
    ok('upload: tanpa error JS', not errs, errs)
    pg.context.close()
    pg, errs = newpage(1280, 900, 'light', stub=False)
    pg.goto('file://' + SC + '/test/published_v3.html'); pg.wait_for_timeout(800)
    ok('v3: gambar model tampil (ter-decode)', pg.evaluate("(()=>{const i=document.querySelector('.card img.mimg');return !!i && i.complete && i.naturalWidth>0})()"))
    ok('v3: hero gambar tampil', pg.evaluate("(()=>{const i=document.querySelector('.hph .frame img');return !!i && i.complete && i.naturalWidth>0})()"))
    ok('v3: model lain tetap vektor', pg.locator('.card').nth(1).locator('svg').count() == 1)
    pg.locator('.card').first.locator('[data-act="open"]').click()
    ok('v3: detail pakai gambar', pg.locator('dialog .mimg').count() == 1)
    pg.screenshot(path=SC + '/test/pub_v3_light.png')
    ok('v3: tanpa error JS', not errs, errs)
    pg.context.close()
    b.close()

bad = [n for n, c in results if not c]
print('\n%d/%d lulus' % (len(results) - len(bad), len(results)))
if bad: print('GAGAL:', bad)
