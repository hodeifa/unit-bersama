import re, sys
import os; SC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(SC + '/public/katalog.html', encoding='utf-8').read()
css = open(SC + '/tools/site_css.css', encoding='utf-8').read()
block = open(SC + '/tools/site_block.js', encoding='utf-8').read()
com = open(SC + '/tools/commercial.css', encoding='utf-8').read()
tokens = open(SC + '/tools/tokens.css', encoding='utf-8').read()
t = src

def rep(old, new, count=1):
    global t
    n = t.count(old)
    if n != count:
        print('PATCH FAIL (%d found, expected %d):' % (n, count), old[:90].replace('\n', ' '))
        sys.exit(1)
    t = t.replace(old, new)

# judul
rep('<title>Katalog Unit Bersama</title>', '<title>Unit Bersama</title>')
rep("var TITLE = 'Katalog Unit Bersama';", "var TITLE = 'Unit Bersama';")

# css
rep('@media (prefers-reduced-motion:reduce)', css + com + '@media (prefers-reduced-motion:reduce)')
_a = t.index('/* Konsep: katalog showroom'); _b = t.index('*{box-sizing:border-box}')
t = t[:_a] + tokens + t[_b:]
rep('family=Barlow+Condensed:wght@500;600;700&amp;family=Barlow:wght@400;500;600&amp;display=swap',
    'family=Barlow+Condensed:wght@500;600;700;800&amp;family=Barlow:wght@400;500;600;700&amp;display=swap', 2)

# header dengan menu
old_header = t[t.index('  function header() {'):t.index('  function hero() {')]
new_header = """  function header(r) {
    var wa = waGeneral();
    var links = ROUTES.map(function (x) { return '<a href="#' + x[0] + '"' + (x[0] === r ? ' aria-current="page"' : '') + '>' + x[1] + '</a>'; }).join('');
    return promo() + '<header class="top' + (UI.canEdit ? '' : ' stick') + '"><div class="wrap topin"><a class="logo" href="#beranda">' + MARK + '<span>' + esc(S.settings.brand || '[NAMA PLATFORM]') + '</span></a>' +
      '<nav class="nav" aria-label="Menu utama">' + links + '</nav>' +
      (wa ? '<a class="btn primary hdcta" href="' + esc(wa) + '" target="_blank" rel="noopener">' + WAI + '<span>Chat WhatsApp</span></a>' : '') +
      '<details class="mnav"><summary aria-label="Buka menu">' + sv('<path d="M4 7h16M4 12h16M4 17h16"/>', 20) + 'Menu</summary><nav aria-label="Menu seluler">' + links + '</nav></details></div></header>';
  }
"""
t = t.replace(old_header, new_header)

# rincian model: margin sudah termasuk kontribusi
rep("<dt>Margin pembelian (sourcing)</dt><dd>10% dari harga unit</dd>", "<dt>Margin pembelian, sudah termasuk kontribusi</dt><dd>10% dari harga unit</dd>")

# footer katalog
rep("""'<div class="foot"><p>Range dana, tahun pembuatan, dan segmen bersifat indikatif sebagai gambaran awal, bukan penawaran harga. Spesifikasi dan harga final dikonfirmasi saat unit dicarikan. Status anggota hanya menampilkan inisial atas persetujuan anggota.</p><span>' + esc(S.settings.brand || '[NAMA PLATFORM]') + '</span></div></section>';""",
    """'<p class="fine">Range dana, tahun pembuatan, dan segmen bersifat indikatif sebagai gambaran awal, bukan penawaran harga. Spesifikasi dan harga final dikonfirmasi saat unit dicarikan. Status anggota hanya menampilkan inisial atas persetujuan anggota.</p></div></section>';""")
rep("""'<section class="wrap" style="padding-top:clamp(36px,5vw,60px)">' +""",
    """'<section class="sect catalog" id="katalog"><div class="wrap"><div class="shead"><h2>Pilih motor impian</h2><p>Tentukan range harga, merek, lalu model. Harga di bawah adalah target dana per unit dan bagian per anggota (1/6).</p></div>' +""")

# kartu model komersial
_c0 = t.index('  function cardHtml(m) {'); _c1 = t.index('  function modelsHtml() {')
new_card = """  function segHtml(n) {
    var h = '<div class="seg" role="img" aria-label="' + n + ' dari ' + SLOTS + ' slot terisi">';
    for (var i = 0; i < SLOTS; i++) h += '<i' + (i < n ? ' class="on"' : '') + '></i>';
    return h + '</div>';
  }
  function cardHtml(m) {
    var ms = membersOf(m.id), full = ms.length >= SLOTS, link = waLink(m);
    var reg = !link ? '' : (full ? '<button type="button" class="btn" disabled>Semua slot terisi</button>' : '<a class="btn primary" href="' + esc(link) + '" target="_blank" rel="noopener" aria-label="Daftar via WhatsApp untuk ' + esc(m.name) + '">Daftar via WhatsApp</a>');
    return '<article class="card"><div class="stage' + (m.img ? ' ph' : '') + '"><span class="tag">Ilustrasi</span>' + pic(m) + '</div><div class="cb">' +
      '<div><div class="mt">' + esc(m.family) + ' · ' + esc(m.cc) + ' cc</div><h4>' + esc(m.name) + '</h4></div>' +
      '<div class="pr"><b>' + per(m.fmin, m.fmax) + '</b><span>per anggota (1/6)</span></div>' +
      '<dl class="kv"><dt>Tahun pembuatan</dt><dd>' + esc(m.y1) + '–' + esc(m.y2) + '</dd><dt>Target dana unit</dt><dd>' + rp(m.fmin, m.fmax) + '</dd></dl>' +
      '<div class="sl"><div class="lb"><span>Slot anggota</span><span>' + summary(m.id) + '</span></div>' + segHtml(ms.length) + ((ms.length || UI.admin) ? slotsHtml(m.id, UI.admin) : '') + '</div>' +
      '<div class="acts">' + reg + '<button type="button" class="btn" data-act="open" data-id="' + esc(m.id) + '" data-fk="open-' + esc(m.id) + '" aria-label="Lihat rincian ' + esc(m.name) + '">Lihat rincian</button>' +
      (UI.admin ? '<button type="button" class="btn" data-act="model-edit" data-id="' + esc(m.id) + '" data-fk="medit-' + esc(m.id) + '">Ubah</button>' : '') + '</div></div></article>';
  }
"""
t = t[:_c0] + new_card + t[_c1:]

# grid model tunggal, merek tampil di kartu
_m0 = t.index('  function modelsHtml() {'); _m1 = t.index('  function catalog() {')
new_models = """  function modelsHtml() {
    var order = S.brands.map(function (b) { return b.id; });
    var shown = S.models.filter(function (m) { return m.tier === UI.tier && (UI.brand === 'all' || m.brand === UI.brand); })
      .sort(function (x, y) { return (order.indexOf(x.brand) - order.indexOf(y.brand)) || (x.fmin - y.fmin); });
    if (!shown.length) return '<div class="empty-state">Belum ada model di pilihan ini.' + (UI.admin ? ' Gunakan “+ Model” untuk menambahkan.' : '') + '</div>';
    return '<div class="cards" style="margin-top:24px">' + shown.map(cardHtml).join('') + '</div>';
  }
"""
t = t[:_m0] + new_models + t[_m1:]
rep("""'<div><div class="mt">' + esc(m.family) + ' · ' + esc(m.cc) + ' cc</div><h4>'""", """'<div><div class="mt">' + esc(brandOf(m.brand).name) + ' · ' + esc(m.family) + ' · ' + esc(m.cc) + ' cc</div><h4>'""")

# render lama diganti blok situs
old_render = """  function render() {
    fixUI();
    app.innerHTML = adminBar() + header() + '<main>' + hero() + steps() + catalog() + '</main>';
    if (UI.focus) { var el = app.querySelector('[data-fk="' + UI.focus + '"]'); if (el) el.focus(); UI.focus = null; }
  }
"""
rep(old_render, block)

# admin bar
a0 = t.index('  function adminBar() {')
a1 = t.index('  function header(r) {')
new_admin = """  function adminBar(r) {
    if (!UI.canEdit) return '';
    if (!UI.admin) return '<div class="abar"><div class="wrap abin"><span>Anda masuk sebagai pengelola.</span><span class="sp"></span><button type="button" class="btn sm" data-act="admin" data-fk="admin">Kelola situs</button></div></div>';
    var st = UI.dirty ? '<span class="dirty">' + UI.dirty + (UI.local ? ' perubahan belum diunduh' : ' perubahan belum diterbitkan') + '</span>'
      : '<span class="muted">' + (UI.local ? (UI.saved ? 'Sudah diunduh. Timpa index.html lama dengan file ini.' : 'Mode lokal: simpan perubahan dengan Unduh HTML.') : 'Semua perubahan sudah terbit') + '</span>';
    return '<div class="abar on"><div class="wrap abin"><strong>Mode kelola</strong>' + st + '<span class="sp"></span>' +
      '<button type="button" class="btn sm" data-act="settings" data-fk="settings">Pengaturan</button>' +
      '<button type="button" class="btn sm" data-act="company" data-fk="company-bar">Info pengelola</button>' +
      '<button type="button" class="btn sm" data-act="policy" data-key="" data-fk="policy-bar">Ketentuan</button>' +
      (r === 'beranda' ? '<button type="button" class="btn sm" data-act="model-add" data-fk="madd">+ Model</button>' : '') +
      (UI.dirty ? '<button type="button" class="btn sm" data-act="discard">Batalkan</button>' : '') +
      '<button type="button" class="btn sm primary" data-act="publish" data-fk="publish"' + (UI.dirty && !UI.saving ? '' : ' disabled') + '>' + (UI.saving ? 'Menerbitkan…' : (UI.local ? 'Unduh HTML' : 'Terbitkan')) + '</button>' +
      '<button type="button" class="btn sm" data-act="admin" data-fk="admin">Selesai</button></div></div>';
  }
"""
t = t[:a0] + new_admin + t[a1:]

# mode kelola lokal: tanpa runtime Claude (hosting biasa atau file di laptop), Terbitkan mengunduh index.html baru
DOWNLOAD_FN = """  function downloadDoc() {
    try {
      var doc = buildDoc().replace('<html>', '<html lang="id">');
      var blob = new Blob([doc], { type: 'text/html;charset=utf-8' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url; a.download = 'index.html'; document.body.appendChild(a); a.click();
      setTimeout(function () { URL.revokeObjectURL(url); if (a.parentNode) a.parentNode.removeChild(a); }, 1500);
      UI.dirty = 0; UI.saved = true; render();
      toast('index.html diunduh. Timpa file lama di repo dengan file ini, lalu commit dan push.');
    } catch (e) { toast('Gagal mengunduh file. Coba lagi.'); }
  }
"""
rep("dirty: 0, saving: false, focus: null };", "dirty: 0, saving: false, focus: null, local: !(window.claude && window.claude.use), saved: false };")
rep("  function publish() {\n", DOWNLOAD_FN + "  function publish() {\n")
rep("if (!art) { toast('Penyimpanan tidak tersedia di tampilan ini. Buka halaman dari akun pengelola.'); return; }",
    "if (!art) { if (UI.local) downloadDoc(); else toast('Penyimpanan tidak tersedia di tampilan ini. Buka halaman dari akun pengelola.'); return; }")

# formDlg: baris textarea & fokus
rep("""'<textarea id="' + id + '" rows="3"'""", """'<textarea id="' + id + '" rows="' + (f.rows || 3) + '"'""")
rep("var first = dlg.querySelector('input,select,textarea'); if (first) first.focus();",
    "var first = (cfg.focus && dlg.querySelector('#f-' + cfg.focus)) || dlg.querySelector('input,select,textarea'); if (first) first.focus();")

# dialog baru
dialogs = """  function companyDlg() {
    formDlg({
      title: 'Info pengelola', values: S.site.company,
      fields: [
        { k: 'name', l: 'Nama badan usaha', max: 80, wide: true },
        { k: 'nib', l: 'NIB', max: 30, h: 'Kosongkan jika belum ingin ditampilkan.' },
        { k: 'email', l: 'Email', max: 80 },
        { k: 'address', l: 'Alamat', t: 'area', rows: 3, max: 300, wide: true },
        { k: 'hours', l: 'Jam layanan', max: 80, ph: 'Senin–Jumat, 09.00–17.00 WIB', wide: true }
      ],
      save: function (v) {
        if (!v.name) return 'Nama badan usaha wajib diisi.';
        if (v.email && !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(v.email)) return 'Format email tidak valid.';
        S.site.company = { name: v.name, nib: v.nib, address: v.address, email: v.email, hours: v.hours };
      }
    });
  }
  function founderDlg() {
    formDlg({
      title: 'Profil pendiri', values: S.site.founder,
      fields: [
        { k: 'name', l: 'Nama', max: 60, h: 'Kosongkan jika tidak ingin menampilkan nama.' },
        { k: 'role', l: 'Jabatan', max: 60, ph: 'Pendiri' },
        { k: 'photo', l: 'Foto', t: 'img', wide: true, h: 'Pakai foto Anda sendiri. Gambar dikecilkan otomatis dan paling pas berbentuk potret (4:5).' },
        { k: 'quote', l: 'Kutipan pembuka', t: 'area', rows: 2, max: 160, wide: true },
        { k: 'story', l: 'Kisah singkat', t: 'area', rows: 12, max: 1800, wide: true, h: 'Pisahkan paragraf dengan baris kosong.' }
      ],
      save: function (v) { S.site.founder = { name: v.name, role: v.role, photo: v.photo, quote: v.quote, story: v.story }; }
    });
  }
  function policyDlg(key) {
    formDlg({
      title: 'Ketentuan', values: S.site.policy, focus: key || '',
      fields: POL.map(function (p) { return { k: p.k, l: p.l, t: 'area', rows: 4, max: 900, wide: true, h: p.h + ' Kosongkan jika belum final.' }; }),
      save: function (v) { POL.forEach(function (p) { S.site.policy[p.k] = v[p.k]; }); }
    });
  }
  function faqDlg(id) {
    var f = id ? S.site.faq.filter(function (x) { return x.id === id; })[0] : { q: '', a: '' };
    if (!f) return;
    formDlg({
      title: id ? 'Ubah pertanyaan' : 'Tambah pertanyaan', values: f, del: id ? 'Hapus pertanyaan' : '',
      fields: [
        { k: 'q', l: 'Pertanyaan', max: 160, wide: true },
        { k: 'a', l: 'Jawaban', t: 'area', rows: 6, max: 900, wide: true, h: 'Boleh memakai {perusahaan} dan {dp}, diganti otomatis. Tautan antarhalaman: [[#biaya|Biaya]].' }
      ],
      save: function (v) {
        if (!v.q) return 'Pertanyaan wajib diisi.';
        if (!v.a) return 'Jawaban wajib diisi.';
        if (id) { f.q = v.q; f.a = v.a; } else { S.site.faq.push({ id: uid('q'), q: v.q, a: v.a }); }
      },
      onDel: function () { S.site.faq = S.site.faq.filter(function (x) { return x.id !== id; }); }
    });
  }

"""
rep('  /* ---------- rincian model ---------- */', dialogs + '  /* ---------- rincian model ---------- */')

# aksi
rep("      case 'slot': memberDlg(d.id, d.mid || null); break;",
    "      case 'slot': memberDlg(d.id, d.mid || null); break;\n      case 'scroll': { var tg = document.getElementById(d.to); if (tg) { var rm = false; try { rm = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {} tg.scrollIntoView({ behavior: rm ? 'auto' : 'smooth', block: 'start' }); } break; }\n      case 'company': companyDlg(); break;\n      case 'founder': founderDlg(); break;\n      case 'policy': policyDlg(d.key || ''); break;\n      case 'faq-add': faqDlg(null); break;\n      case 'faq-edit': faqDlg(d.id); break;")

# mulai
rep("  render();\n  use('user')", "  ensureSite();\n  render();\n  use('user')")
rep("  }).catch(function () {});\n})();",
    """  }).catch(function () {});
  window.addEventListener('hashchange', function () {
    if (dlg.open) closeDlg();
    render();
    try { window.scrollTo(0, 0); } catch (e) {}
    var h1 = app.querySelector('h1'); if (h1) { try { h1.focus({ preventScroll: true }); } catch (e) {} }
  });
  app.addEventListener('input', function (e) {
    var k = e.target && e.target.getAttribute && e.target.getAttribute('data-calc');
    if (!k) return;
    CALC[k] = Number(e.target.value); calcUpdate();
  });
})();""")

open(SC + '/public/site.html', 'w', encoding='utf-8').write(t)
print('ok', len(t))
