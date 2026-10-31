# Tes mode kelola lokal: tanpa runtime Claude, Terbitkan menjadi Unduh HTML dan hasilnya bisa dipakai ulang.
import os, re, json, shutil, subprocess, sys, tempfile
from playwright.sync_api import sync_playwright
SC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RX = re.compile(r'<script type="application/json" id="state">(.*?)</script>', re.S)
bad = 0
def ok(c, m):
    global bad
    print(('PASS ' if c else 'FAIL ') + m)
    if not c: bad += 1
def state(path):
    return json.loads(RX.search(open(path, encoding='utf-8').read()).group(1))

IDX = SC + '/index.html'
DL = SC + '/test/dl_index.html'
os.makedirs(SC + '/test', exist_ok=True)
before = state(IDX)
NEWBRAND = 'Uji Lokal Moge'
ok(before['settings']['brand'] != NEWBRAND, 'awal: nama platform bukan nilai uji (%r)' % before['settings']['brand'])

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(accept_downloads=True, viewport={'width': 1280, 'height': 900})
    pg = ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route('**/fonts.googleapis.com/**', lambda r: r.abort())

    # pengunjung biasa: tidak ada tombol kelola
    pv = ctx.new_page(); pv.route('**/fonts.googleapis.com/**', lambda r: r.abort())
    pv.goto('file://' + IDX + '#beranda'); pv.wait_for_timeout(300)
    ok(pv.locator('[data-act="admin"],[data-act="publish"]').count() == 0, 'pengunjung: tidak ada tombol kelola atau unduh')

    # pengelola lokal (halaman baru: #kelola dibaca saat halaman dibuka)
    pg.goto('file://' + IDX + '#kelola'); pg.wait_for_timeout(300)
    ok(pg.locator('[data-act="admin"]').count() == 1, 'dengan #kelola: tombol Kelola situs muncul')
    pg.click('[data-act="admin"]'); pg.wait_for_timeout(200)
    btn = pg.locator('[data-act="publish"]')
    ok(btn.inner_text().strip() == 'Unduh HTML', 'tombol bernama Unduh HTML (%r)' % btn.inner_text())
    ok(btn.is_disabled(), 'tombol nonaktif sebelum ada perubahan')
    ok('Mode lokal' in pg.locator('.abar.on').inner_text(), 'bilah menjelaskan mode lokal')

    pg.click('[data-act="settings"]')
    pg.fill('#f-brand', NEWBRAND)
    pg.click('dialog button[type=submit]'); pg.wait_for_timeout(300)
    ok('belum diunduh' in pg.locator('.abar.on').inner_text(), 'setelah ubah: "perubahan belum diunduh"')
    ok(btn.is_enabled(), 'tombol aktif setelah ada perubahan')

    with pg.expect_download() as d:
        pg.click('[data-act="publish"]')
    dl = d.value
    ok(dl.suggested_filename == 'index.html', 'nama berkas unduhan index.html (%r)' % dl.suggested_filename)
    dl.save_as(DL)
    pg.wait_for_timeout(300)
    ok('Sudah diunduh' in pg.locator('.abar.on').inner_text(), 'setelah unduh: bilah "Sudah diunduh"')
    ok(pg.locator('#toast').is_visible() and 'diunduh' in pg.locator('#toast').inner_text(), 'toast konfirmasi tampil')
    ok(btn.is_disabled(), 'tombol kembali nonaktif setelah unduh')
    ok(not errs, 'tanpa error JS di sesi kelola: %s' % errs[:2])

    # batalkan: ubah lagi lalu Batalkan => kembali ke nilai file
    pg2 = ctx.new_page(); pg2.route('**/fonts.googleapis.com/**', lambda r: r.abort())
    pg2.goto('file://' + IDX + '#kelola'); pg2.wait_for_timeout(300)
    pg2.click('[data-act="admin"]'); pg2.click('[data-act="settings"]'); pg2.fill('#f-brand', 'Sementara'); pg2.click('dialog button[type=submit]'); pg2.wait_for_timeout(200)
    pg2.click('[data-act="discard"]'); pg2.wait_for_timeout(500)
    ok('Sementara' not in pg2.locator('body').inner_text(), 'batalkan: perubahan sementara hilang')

    # berkas hasil unduhan dibuka sebagai pengunjung
    pg3 = ctx.new_page(); errs3 = []
    pg3.on('pageerror', lambda e: errs3.append(str(e))); pg3.route('**/fonts.googleapis.com/**', lambda r: r.abort())
    pg3.goto('file://' + DL + '#beranda'); pg3.wait_for_timeout(400)
    ok(NEWBRAND.upper() in pg3.locator('.logo').first.inner_text().upper(), 'hasil unduhan: nama baru tampil di logo')
    ok(pg3.evaluate('document.documentElement.lang') == 'id', 'hasil unduhan: html lang=id')
    ok(pg3.locator('[data-act="admin"],[data-act="publish"]').count() == 0, 'hasil unduhan: pengunjung tidak melihat tombol kelola')
    ok(pg3.locator('h1').count() == 1, 'hasil unduhan: halaman beranda tampil')
    ok(not errs3, 'hasil unduhan: tanpa error JS %s' % errs3[:2])
    b.close()

# isi hasil unduhan = isi lama + satu perubahan
after = state(DL)
ok(after['settings']['brand'] == NEWBRAND, 'state unduhan: nama baru tersimpan')
a2 = json.loads(json.dumps(after)); a2['settings']['brand'] = before['settings']['brand']
ok(a2 == before, 'state unduhan: selain nama, semua data (teks, foto, kebijakan, anggota) sama persis')
ok(os.path.getsize(DL) > 0.95 * os.path.getsize(IDX), 'ukuran unduhan wajar (%d vs %d)' % (os.path.getsize(DL), os.path.getsize(IDX)))

# alur repo: timpa index.html dengan unduhan, lalu build ulang tidak menghapus perubahan
tmp = tempfile.mkdtemp()
try:
    R = tmp + '/r'
    shutil.copytree(SC, R, ignore=shutil.ignore_patterns('node_modules', 'test', '.git', '__pycache__'))
    shutil.copy(DL, R + '/index.html')
    for s in ('patch_site.py', 'build_final.py', 'build_index.py'):
        r = subprocess.run([sys.executable, R + '/tools/' + s], capture_output=True, text=True)
        ok(r.returncode == 0, 'build ulang %s berhasil' % s)
    rebuilt = state(R + '/index.html')
    ok(rebuilt == after, 'setelah build ulang dari unduhan: state identik (perubahan tidak hilang)')
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print('\nGAGAL: %d' % bad if bad else '\nSemua lulus')
sys.exit(1 if bad else 0)
