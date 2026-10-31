  /* ---------- situs: rute, konten, halaman info ---------- */
  var ROUTES = [['beranda', 'Beranda'], ['cara-kerja', 'Cara kerja'], ['biaya', 'Biaya'], ['aturan', 'Aturan pakai'], ['perlindungan', 'Perlindungan'], ['faq', 'FAQ'], ['tentang', 'Tentang']];
  function route() {
    var h = ''; try { h = (location.hash || '').replace(/^#/, ''); } catch (e) {}
    return ROUTES.some(function (r) { return r[0] === h; }) ? h : 'beranda';
  }
  var CHK = '<svg ' + ICON_ATTR + '><circle cx="8" cy="8" r="6.2" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M5.3 8.2l1.9 1.9 3.5-3.7" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var CLK = ico('daftar');
  var POL = [
    { k: 'dpPenalty', l: 'Denda mundur setelah anggota lain siap', h: 'Besaran atau rumus denda, misalnya persentase dari DP.' },
    { k: 'dpReady', l: 'Definisi “anggota lain sudah siap”', h: 'Kapan anggota lain dianggap siap sehingga denda mulai berlaku.' },
    { k: 'repairSanction', l: 'Sanksi pengurangan masa pakai', h: 'Berapa lama pengurangan, kapan berlaku, dan cara pemulihannya.' },
    { k: 'leave', l: 'Keluar sebelum tahun ke-5 dan tunggakan iuran', h: 'Syarat keluar lebih awal, biaya, dan penanganan anggota yang menunggak iuran rutin.' },
    { k: 'exitSale', l: 'Penentuan harga jual dan pembagian hasil (tahun ke-5)', h: 'Siapa yang menentukan harga jual dan bagaimana hasil bersih dibagi ke 6 anggota.' },
    { k: 'usage', l: 'Batas pemakaian dan syarat pengendara (SIM)', h: 'Batas durasi per giliran, wilayah pakai, dan kelengkapan SIM yang diwajibkan.' }
  ];
  var DEF_FAQ = [
    { id: 'q1', q: 'Apakah ini produk investasi?', a: 'Bukan. Tujuannya akses memakai moge dengan biaya awal lebih ringan lewat patungan 6 orang. Tidak ada janji keuntungan atau imbal hasil, dan nilai jual unit di tahun ke-5 bisa lebih rendah maupun lebih tinggi dari harga beli.' },
    { id: 'q2', q: 'Berapa yang harus saya bayar?', a: 'Kontribusi pembelian Rp50–100 juta per anggota (total Rp300–600 juta per unit, sudah termasuk margin beli pengelola 10%), iuran rutin Rp250.000 per bulan, serta biaya variabel seperti BBM, tol, dan perbaikan yang ditagih terpisah. Saat ini yang dikumpulkan di awal hanya DP sekitar {dp}%. Rinciannya ada di halaman [[#biaya|Biaya]].' },
    { id: 'q3', q: 'Apakah unit di katalog itu unit asli?', a: 'Bukan. Gambar hanya ilustrasi gaya motor. Unit sebenarnya dicarikan setelah dana 6 anggota terkumpul, sesuai model dan rentang tahun yang dipilih, sehingga warna, varian, dan tahun bisa sedikit berbeda.' },
    { id: 'q4', q: 'Unit terdaftar atas nama siapa?', a: 'Atas nama pengelola, {perusahaan}. Hak setiap anggota (1/6), termasuk hak pakai bergantian, diatur dalam perjanjian tertulis.' },
    { id: 'q5', q: 'Apakah DP bisa dikembalikan?', a: 'Ya, DP dikembalikan. Namun jika anggota mengundurkan diri saat anggota lain sudah siap, dikenakan denda. Rincian ada di halaman [[#perlindungan|Perlindungan & risiko]].' },
    { id: 'q6', q: 'Siapa yang menanggung biaya perawatan dan perbaikan?', a: 'Para anggota, dibagi bersama. Anggota yang tidak mau ikut membayar bagiannya dikenai sanksi pengurangan masa pakai.' },
    { id: 'q7', q: 'Bagaimana jadwal pemakaian dibagi?', a: 'Unit dipakai bergantian oleh 6 anggota. Pada tahap pilot, jadwal diatur manual oleh pengelola. Kalender otomatis dengan pembagian weekend dan weekday yang adil, serta tukar jadwal antaranggota, direncanakan di tahap berikutnya.' },
    { id: 'q8', q: 'Bisakah saya keluar sebelum kontrak 5 tahun berakhir?', a: 'Aturan keluar lebih awal dan penanganan tunggakan iuran sedang difinalisasi. Pengalihan atau penjualan kembali 1/6 hak kepada calon anggota baru direncanakan di tahap berikutnya.' },
    { id: 'q9', q: 'Apa yang terjadi di akhir kontrak?', a: 'Di tahun ke-5 unit dijual (likuidasi) dan komisi 10% dipotong dari harga jual. Cara penentuan harga jual dan pembagian hasilnya sedang difinalisasi.' },
    { id: 'q10', q: 'Siapa yang bisa melihat nama dan status saya?', a: 'Publik hanya melihat inisial dan ikon status (Mendaftar, Terverifikasi, DP terbayar), dan hanya atas persetujuan Anda. Data identitas dipakai untuk verifikasi dan tidak ditampilkan.' },
    { id: 'q11', q: 'Bagaimana cara mendaftar?', a: 'Pilih model di katalog, tekan “Daftar via WhatsApp”, lalu ikuti verifikasi manual oleh tim. Setelah terverifikasi, bayar DP sekitar {dp}% untuk mengamankan slot.' }
  ];
  var DEF_QUOTE = 'Mimpi memiliki moge tidak seharusnya menunggu kondisi finansial yang jarang datang.';
  var DEF_STORY = 'Banyak orang di sekitar kita punya mimpi yang sederhana: suatu hari memiliki moge. Mereka bekerja keras, hidup tertib, dan tetap merasa mimpi itu belum waktunya. Bukan karena kurang berusaha, tetapi karena memiliki satu unit sendirian menuntut modal besar, biaya perawatan, tempat menyimpan, dan ketentuan kepemilikan yang tidak ringan. Bagi kelas menengah, syarat itu sering baru terpenuhi setelah kondisi finansial tertentu yang jarang datang.\n\nSaya mendirikan usaha ini karena merasa mimpi tidak seharusnya menunggu selama itu. Ada cara yang lebih masuk akal: patungan enam orang, dengan aturan yang jelas, perjanjian tertulis, dan pengelola yang mengurus jadwal, garasi, serta pencatatan perawatan.\n\nAda satu hal lagi yang membuat saya yakin. Kendaraan rekreasional biasanya jarang dipakai, lebih sering diam di garasi daripada di jalan. Dengan berbagi, satu unit dipakai lebih sering dan biaya tetapnya terbagi, sehingga manfaatnya lebih terasa dibanding dimiliki sendirian.\n\nKami tidak menjanjikan jalan pintas. Kami menjanjikan keterbukaan: apa yang sudah pasti, apa yang masih disusun, dan risikonya, semuanya ada di situs ini. Silakan pelajari, lalu putuskan apakah cara ini cocok untuk Anda.';
  function ensureSite() {
    var s = S.site = S.site || {};
    s.founder = Object.assign({ name: '', role: 'Pendiri', photo: '', quote: DEF_QUOTE, story: DEF_STORY }, s.founder || {});
    s.company = Object.assign({ name: 'PT Mitra Nusantara Solusindo', nib: '', address: '', email: '', hours: '' }, s.company || {});
    s.policy = Object.assign({ dpPenalty: '', dpReady: '', repairSanction: '', leave: '', exitSale: '', usage: '' }, s.policy || {});
    if (!Array.isArray(s.faq)) s.faq = DEF_FAQ.map(function (f) { return { id: f.id, q: f.q, a: f.a }; });
  }
  function co() { return S.site.company.name || 'pengelola'; }
  function tok(s) {
    return esc(String(s == null ? '' : s).replace(/\{perusahaan\}/g, co()).replace(/\{dp\}/g, S.settings.dp))
      .replace(/\[\[#([a-z-]+)\|([^\]]+)\]\]/g, '<a href="#$1">$2</a>');
  }
  function idr(n) { n = Math.round(n); return (n < 0 ? '−' : '') + 'Rp' + String(Math.abs(n)).replace(/\B(?=(\d{3})+(?!\d))/g, '.'); }
  function pageHead(eyebrow, title, lead) {
    return '<section class="phd dark"><div class="wrap"><p class="eyebrow">' + esc(eyebrow) + '</p><h1 tabindex="-1">' + esc(title) + '</h1><p class="lead">' + tok(lead) + '</p></div></section>';
  }
  function blk(title, body) { return '<section class="wrap blk"><div class="sec"><h2>' + esc(title) + '</h2></div>' + body + '</section>'; }
  function waGeneral() {
    var n = (S.settings.whatsapp || '').replace(/\D/g, ''); if (!n) return '';
    return 'https://wa.me/' + n + '?text=' + encodeURIComponent('Halo, saya ingin bertanya tentang kepemilikan bersama moge.');
  }
  function rowsList(items) {
    return '<ul class="rows">' + items.map(function (t) { return '<li>' + CHK + '<span>' + tok(t) + '</span></li>'; }).join('') + '</ul>';
  }
  function pol(key, label, intro) {
    var v = (S.site.policy[key] || '').trim();
    var h = '<div class="pol ' + (v ? 'ok' : 'tbd') + '"><div class="polh"><span class="chip ' + (v ? 'ok' : 'tbd') + '">' + (v ? CHK + 'Sudah ditetapkan' : CLK + 'Sedang difinalisasi') + '</span><b>' + esc(label) + '</b></div>';
    if (intro) h += '<p class="pi muted">' + tok(intro) + '</p>';
    h += v ? '<p class="ut">' + tok(v) + '</p>' : '<p class="pi muted">Rincian ketentuan ini sedang difinalisasi dan akan dicantumkan di sini setelah final.</p>';
    if (UI.admin) h += '<button type="button" class="btn sm" data-act="policy" data-key="' + esc(key) + '" data-fk="pol-' + esc(key) + '">' + (v ? 'Ubah' : 'Isi') + ' ketentuan</button>';
    return h + '</div>';
  }
  function linkCard(href, title, text) { return '<a class="pc" href="#' + href + '"><h3>' + esc(title) + '</h3><p>' + esc(text) + '</p><span class="go">Buka halaman →</span></a>'; }

  /* ikon dan elemen bersama */
  function sv(inner, size) { return '<svg width="' + (size || 24) + '" height="' + (size || 24) + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + inner + '</svg>'; }
  var MARK = '<svg width="30" height="30" viewBox="0 0 28 28" aria-hidden="true" focusable="false"><path d="M14 14V2A12 12 0 0 1 24.39 8Z" fill="#F5B000"/><circle cx="14" cy="14" r="12" fill="none" stroke="currentColor" stroke-width="2"/><path d="M14 14V2M14 14l10.39-6M14 14l10.39 6M14 14v12M14 14L3.61 20M14 14L3.61 8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>';
  var WAI = sv('<path d="M20 11.5a8 8 0 0 1-11.9 7L4 20l1.5-3.9A8 8 0 1 1 20 11.5z"/><path d="M9.4 8.8c.2-.4.6-.4.8 0l.7 1.4c.1.3 0 .5-.2.7l-.4.4c.6 1.1 1.4 1.9 2.6 2.5l.5-.5c.2-.2.5-.2.7-.1l1.4.7c.4.2.3.6 0 1-.5.6-1.2.8-2 .6-2.2-.6-3.9-2.3-4.5-4.4-.1-.6.1-1.1.4-1.5z"/>', 20);
  var ARW = sv('<path d="M5 12h14M13 6l6 6-6 6"/>', 18);
  function minPer() { var m = Math.min.apply(null, S.tiers.map(function (t) { return t.min; })); return isFinite(m) ? Math.round(m / SLOTS) : 50; }
  function maxPer() { var m = Math.max.apply(null, S.tiers.map(function (t) { return t.max; })); return isFinite(m) ? Math.round(m / SLOTS) : 100; }
  function brandNames() {
    var n = S.brands.map(function (b) { return b.name; });
    return n.length < 2 ? n.join('') : n.slice(0, -1).join(', ') + ' dan ' + n[n.length - 1];
  }
  function promo() {
    var wa = waGeneral();
    return '<div class="promo"><div class="wrap"><span>DP hanya mengamankan slot, bukan pelunasan. Pendaftaran minat lewat WhatsApp.</span>' +
      (wa ? '<a href="' + esc(wa) + '" target="_blank" rel="noopener">Chat sekarang</a>' : '<a href="#tentang">Hubungi kami</a>') + '</div></div>';
  }
  function mobileBar() {
    var wa = waGeneral();
    if (!wa || UI.admin) return '';
    return '<div class="mcta"><a class="btn primary" href="' + esc(wa) + '" target="_blank" rel="noopener">' + WAI + '<span>Tanya atau daftar via WhatsApp</span></a></div>';
  }
  function ctaBand() {
    var wa = waGeneral();
    return '<section class="cband"><div class="wrap"><div><h2>Siap memilih unit Anda?</h2><p>Tanyakan model, tarif, atau langkah verifikasi lewat WhatsApp.</p></div><div class="cta">' +
      (wa ? '<a class="btn ink xl" href="' + esc(wa) + '" target="_blank" rel="noopener">' + WAI + '<span>Chat WhatsApp</span></a>' : '<a class="btn ink xl" href="#tentang">Hubungi kami</a>') +
      '<a class="btn xl" href="#aturan">Baca aturan pakai</a></div></div></section>';
  }

  /* beranda */
  function heroC() {
    var img = S.settings.heroImg;
    var photo = img ? '<img src="' + esc(img) + '" alt="Contoh unit moge" decoding="async">' : bike('cruiser', '#C8402F');
    return '<section class="hero2 dark"><div class="wrap h2in"><div class="hl">' +
      '<p class="eyebrow">Kepemilikan bersama moge</p>' +
      '<h1 tabindex="-1"><span>Satu moge,</span><span>enam pemilik.</span></h1>' +
      '<p class="sub">Pakai ' + esc(brandNames()) + ' mulai Rp' + minPer() + ' juta per anggota. Garasi dan jadwal diurus pengelola, hak Anda tertulis dalam perjanjian.</p>' +
      '<div class="cta"><button type="button" class="btn primary xl" data-act="scroll" data-to="katalog">Pilih motor impian</button><a class="btn xl" href="#biaya">Hitung biaya</a></div>' +
      '<ul class="checks"><li>' + CHK + 'Hak 1/6 tertulis di perjanjian</li><li>' + CHK + 'DP dikembalikan, ada ketentuan denda</li><li>' + CHK + 'Semua tarif terbuka di situs</li></ul></div>' +
      '<div class="hph"><div class="frame' + (img ? '' : ' art') + '"><span class="tag">Contoh unit</span>' + photo + '</div>' +
      '<div class="pcard"><b>Mulai Rp' + minPer() + ' jt</b><span>per anggota, 1 dari 6 slot</span></div></div></div>' +
      '<div class="wrap"><dl class="hstats">' +
      '<div><b>5 tahun</b><span>Durasi kontrak</span></div>' +
      '<div><b>Rp' + minPer() + '–' + maxPer() + ' jt</b><span>Kontribusi per anggota</span></div>' +
      '<div><b>1/6</b><span>Hak pakai bergantian</span></div>' +
      '<div><b>Rp250 rb</b><span>Iuran rutin per bulan</span></div></dl></div></section>';
  }
  function whyBlock() {
    var items = [
      [sv('<path d="M3 7h15a3 3 0 0 1 3 3v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7z"/><path d="M3 7l12-3v3"/><circle cx="17" cy="14" r="1.2"/>'), 'Mulai Rp' + minPer() + ' juta', 'Anda membayar 1/6 dari target dana unit. Satu unit berkisar Rp' + Math.min.apply(null, S.tiers.map(function (t) { return t.min; })) + '–' + Math.max.apply(null, S.tiers.map(function (t) { return t.max; })) + ' juta, jadi bagian Anda Rp' + minPer() + '–' + maxPer() + ' juta.'],
      [sv('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>'), 'Pakai bergantian', 'Unit dipakai 6 anggota secara bergantian. Pengelola mengatur jadwal agar pembagiannya adil.'],
      [sv('<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/><path d="M9 21v-6h6v6"/>'), 'Garasi dan catatan diurus', 'Iuran Rp250.000 per bulan sudah mencakup manajemen dan sewa garasi. Perawatan dan perbaikan dibagi antar anggota.'],
      [sv('<path d="M12 3l8 3v6c0 4.5-3.2 8-8 9-4.8-1-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/>'), 'Hak tertulis, tarif terbuka', 'Hak 1/6 Anda diatur dalam perjanjian tertulis. Tarif, ketentuan, dan risikonya ditulis terang di situs ini.']
    ];
    return '<section class="sect alt"><div class="wrap"><div class="shead"><h2>Kenapa patungan moge</h2><p>Mimpi memiliki moge tidak harus menunggu modal besar. Dengan berbagi enam orang, biaya awal dan biaya tetapnya terbagi.</p></div><div class="ben">' +
      items.map(function (x) { return '<div class="bc"><span class="ic">' + x[0] + '</span><h3>' + esc(x[1]) + '</h3><p>' + esc(x[2]) + '</p></div>'; }).join('') + '</div></div></section>';
  }
  function compareBlock() {
    var rows = [
      ['Dana awal', 'Rp300–600 juta untuk satu unit', 'Rp' + minPer() + '–' + maxPer() + ' juta per anggota'],
      ['Garasi dan pengelolaan', 'Dicari dan dibayar sendiri', 'Iuran Rp250.000 per bulan, sudah mencakup manajemen dan garasi'],
      ['Pemakaian', 'Kapan saja, sendirian', 'Bergantian dengan 6 anggota, jadwal diatur pengelola'],
      ['Kepemilikan', 'Atas nama sendiri', 'Hak 1/6 lewat perjanjian, unit atas nama ' + co()],
      ['Perawatan dan perbaikan', 'Ditanggung sendiri', 'Dibagi antar anggota'],
      ['Di akhir', 'Dijual sendiri kapan saja', 'Unit dijual di tahun ke-5, komisi jual 10%']
    ];
    var b = S.settings.brand || 'Patungan';
    return '<section class="sect alt"><div class="wrap"><div class="shead"><h2>Beli sendiri atau patungan</h2><p>Perbandingan jujur: Anda mengurangi modal dan beban tetap, dengan imbal balik berbagi pemakaian dan aturan kelompok.</p></div>' +
      '<div class="cmp" role="table" aria-label="Perbandingan beli sendiri dan patungan"><div class="row h" role="row"><div role="columnheader"><span class="sr">Aspek</span></div><div role="columnheader">Beli sendiri</div><div class="us" role="columnheader">' + esc(b) + '</div></div>' +
      rows.map(function (r) { return '<div class="row" role="row"><div role="rowheader">' + esc(r[0]) + '</div><div role="cell" data-l="Beli sendiri">' + esc(r[1]) + '</div><div class="us" role="cell" data-l="' + esc(b) + '">' + esc(r[2]) + '</div></div>'; }).join('') +
      '</div><p class="cmp-note">Perbandingan ringkas untuk gambaran umum. Ketentuan yang mengikat ada di perjanjian tertulis, dan beberapa ketentuan masih difinalisasi. Lihat <a class="lnk" href="#perlindungan">Perlindungan &amp; risiko</a>.</p></div></section>';
  }
  function stepsC() {
    var st = [
      ['Pilih model', 'Telusuri range harga, merek, lalu model dan rentang tahun yang Anda incar.'],
      ['Daftar dan verifikasi', 'Daftar lewat WhatsApp. Tim memverifikasi identitas dan kesiapan Anda secara manual.'],
      ['Bayar DP ' + S.settings.dp + '%', 'DP mengamankan satu dari 6 slot. DP bukan pelunasan dan dapat dikembalikan dengan ketentuan.'],
      ['Unit dicarikan', 'Setelah 6 anggota siap dan dana terkumpul, unit dicarikan dan dipakai bergantian selama 5 tahun.']
    ];
    return '<section class="sect"><div class="wrap"><div class="shead"><h2>Empat langkah sampai unit siap</h2></div><ol class="stp">' +
      st.map(function (s) { return '<li><h3>' + esc(s[0]) + '</h3><p>' + esc(s[1]) + '</p></li>'; }).join('') + '</ol>' +
      '<p class="more"><a href="#cara-kerja">Lihat cara kerja lengkap</a></p></div></section>';
  }
  function tzRows() {
    var r = calcCompute();
    return '<div class="big"><span>Total 5 tahun, di luar biaya variabel</span><b>' + idr(r.c + r.iuran) + '</b></div>' +
      rr('Kontribusi pembelian (termasuk DP)', idr(r.c)) +
      rr('Setara target dana unit' + (r.tier ? ', ' + esc(r.tier.name) : ''), idr(r.pool)) +
      rr('Iuran rutin, 60 × Rp250.000', idr(r.iuran));
  }
  function calcTeaser() {
    var wa = waGeneral();
    return '<section class="sect dark"><div class="wrap tz"><div class="shead"><h2>Hitung dulu sebelum daftar</h2><p>Geser kontribusi untuk melihat gambaran biaya Anda selama 5 tahun. Simulasi lengkap termasuk antar-jemput, biaya variabel, dan hasil jual ada di halaman Biaya.</p>' +
      '<div class="cta"><a class="btn primary xl" href="#biaya">Buka simulasi lengkap</a></div></div>' +
      '<div class="tzc"><div class="fld"><label for="c-contrib">Kontribusi per anggota<b id="o-contrib">' + idr(CALC.contrib * 1e6) + '</b></label><input id="c-contrib" data-calc="contrib" type="range" min="50" max="100" step="5" value="' + CALC.contrib + '" aria-valuetext="' + esc(idr(CALC.contrib * 1e6)) + '"><small>Sesuai skema: Rp50–100 juta per anggota.</small></div>' +
      '<div class="tzr res" id="tz-out">' + tzRows() + '</div>' +
      '<p class="fine" style="margin-top:12px">Belum termasuk BBM, tol, perbaikan, antar-jemput opsional, dan hasil jual unit di tahun ke-5. Bukan penawaran atau janji hasil.</p></div></div></section>';
  }
  function founderTeaser() {
    var f = S.site.founder; if (!f.quote && !f.photo) return '';
    var has = !!f.photo;
    return '<section class="sect"><div class="wrap fte' + (has ? '' : ' nophoto') + '">' +
      (has ? '<figure class="fph"><img src="' + esc(f.photo) + '" alt="' + esc(f.name ? 'Foto ' + f.name : 'Foto pendiri') + '" decoding="async"></figure>' : '') +
      '<div>' + (f.quote ? '<p class="fq">' + esc(f.quote) + '</p>' : '') +
      (f.name ? '<p class="who">' + esc(f.name) + (f.role ? '<span>' + esc(f.role) + ', ' + esc(co()) + '</span>' : '') + '</p>' : '') +
      '<div class="cta"><a class="btn" href="#tentang">Baca cerita kami</a></div></div></div></section>';
  }
  function faqTeaser() {
    var list = S.site.faq.slice(0, 5);
    if (!list.length) return '';
    return '<section class="sect alt"><div class="wrap"><div class="shead"><h2>Pertanyaan yang sering muncul</h2></div><div class="faq">' +
      list.map(function (f) { return '<details><summary>' + esc(f.q) + '</summary><div class="ans"><p class="ut">' + tok(f.a) + '</p></div></details>'; }).join('') + '</div>' +
      '<p class="more"><a href="#faq">Lihat semua pertanyaan</a></p></div></section>';
  }
  function pgBeranda() { return heroC() + whyBlock() + catalog() + compareBlock() + stepsC() + calcTeaser() + founderTeaser() + faqTeaser(); }

  /* cara kerja */
  function pgCara() {
    var steps = [
      ['Pilih model gambaran', 'Telusuri katalog menurut range harga, merek, lalu model dan rentang tahun pembuatan. Gambar hanya ilustrasi, karena unit sebenarnya belum dicarikan pada tahap ini.'],
      ['Daftar lewat WhatsApp', 'Tekan “Daftar via WhatsApp” pada model pilihan. Dengan persetujuan Anda, status tampil di katalog sebagai inisial dengan ikon “Mendaftar”.'],
      ['Verifikasi manual', 'Tim memeriksa identitas dan kesiapan Anda secara manual. Setelah lolos, ikon berubah menjadi “Terverifikasi”.'],
      ['Bayar DP', 'DP sekitar {dp}% dari kontribusi mengamankan satu dari 6 slot dan mengubah ikon menjadi “DP terbayar”. DP bukan pelunasan. Ketentuan pengembalian dan denda ada di [[#perlindungan|Perlindungan & risiko]].'],
      ['Dana terkumpul, unit dicarikan', 'Setelah 6 anggota siap dan dana terkumpul, pengelola mencarikan unit sesuai model dan rentang tahun yang dipilih, dan perjanjian disiapkan melalui notaris. Unit terdaftar atas nama {perusahaan}.'],
      ['Pakai bergantian selama 5 tahun', 'Jadwal dibagi di antara 6 anggota dengan iuran rutin Rp250.000 per anggota per bulan. Pengelola mengatur jadwal, garasi, dan pencatatan perawatan; biaya perawatan dan perbaikan dibagi antar anggota.'],
      ['Akhir kontrak: unit dijual', 'Di tahun ke-5 unit dijual (likuidasi) dan komisi jual 10% dipotong dari harga jual. Cara penentuan harga dan pembagian hasil dijelaskan di [[#perlindungan|Perlindungan & risiko]].']
    ];
    var stDesc = { daftar: 'Anggota sudah mendaftar dan menunggu verifikasi.', verifikasi: 'Identitas dan kesiapan sudah diperiksa tim secara manual.', dp: 'DP sudah diterima dan slot diamankan.' };
    var h = pageHead('Cara kerja', 'Dari pilih model sampai unit dijual', 'Urutan yang berlaku untuk setiap kelompok 6 anggota, dari pendaftaran sampai akhir kontrak 5 tahun.');
    h += '<section class="wrap blk" style="margin-top:28px"><ol class="tl">' + steps.map(function (s) { return '<li><div><h3>' + esc(s[0]) + '</h3><p>' + tok(s[1]) + '</p></div></li>'; }).join('') + '</ol></section>';
    h += blk('Arti ikon status', '<ul class="stlist">' + ['daftar', 'verifikasi', 'dp'].map(function (s) {
      return '<li><span class="lg st-' + s + '">' + ico(s) + '</span><div><b>' + STATUS[s] + '</b><span>' + stDesc[s] + '</span></div></li>';
    }).join('') + '</ul><p class="muted" style="margin-top:14px;font-size:14px;max-width:640px">Publik hanya melihat inisial dan ikon, dan hanya atas persetujuan anggota.</p>');
    h += blk('Siapa melakukan apa', '<div class="g3">' +
      '<div class="pc"><h3>Anggota</h3><p>Memakai unit sesuai jadwal, membayar iuran rutin, dan ikut menanggung biaya perawatan dan perbaikan.</p></div>' +
      '<div class="pc"><h3>Pengelola</h3><p>' + tok('{perusahaan}. Mencarikan unit, menjadi pemegang nama unit, mengatur jadwal dan garasi, mencatat perawatan, dan menyusun laporan keuangan.') + '</p></div>' +
      '<div class="pc"><h3>Mitra antar-jemput</h3><p>Opsional. Mengantar dan menjemput unit ke lokasi anggota dengan tarif Rp100.000 per trip.</p></div></div>');
    h += '<section class="wrap blk"><div class="cta"><a class="btn primary" href="#beranda">Lihat katalog</a><a class="btn" href="#biaya">Hitung biaya</a></div></section>';
    return h;
  }

  /* biaya & simulasi */
  var CALC = { contrib: 75, trips: 0, varm: 0, sale: 70 };
  function fee(name, val, note) { return '<div class="fee"><div class="fn">' + esc(name) + '</div><div class="fv">' + tok(val) + '</div>' + (note ? '<div class="fo">' + tok(note) + '</div>' : '') + '</div>'; }
  function calcCompute() {
    var c = CALC.contrib * 1e6, pool = c * SLOTS, dp = c * (Number(S.settings.dp) || 0) / 100;
    var iuran = 250000 * 60, antar = 100000 * CALC.trips * 5, vr = CALC.varm * 60;
    var out = c + iuran + antar + vr;
    var unit = pool / 1.1, margin = pool - unit;
    var sale = unit * CALC.sale / 100, fe = sale * 0.1, per = (sale - fe) / SLOTS, cost = out - per;
    var tier = S.tiers.filter(function (t) { return pool / 1e6 >= t.min && pool / 1e6 <= t.max; })[0];
    return { c: c, pool: pool, unit: unit, margin: margin, dp: dp, iuran: iuran, antar: antar, vr: vr, out: out, sale: sale, fe: fe, per: per, cost: cost, month: cost / 60, tier: tier };
  }
  function rr(a, b, cls) { return '<div class="rr' + (cls ? ' ' + cls : '') + '"><span>' + a + '</span><b>' + b + '</b></div>'; }
  function calcRows() {
    var r = calcCompute();
    return '<div class="big"><span>Perkiraan biaya bersih rata-rata per bulan</span><b>' + idr(r.month) + '</b><span>per anggota selama 60 bulan, setelah hasil jual asumsi</span></div>' +
      '<div class="res"><h4>Di awal</h4>' +
      rr('Total dana unit (6 anggota)', idr(r.pool)) +
      rr('Margin beli pengelola 10% (sudah termasuk)', idr(r.margin)) +
      rr('Harga unit setelah margin', idr(r.unit)) +
      rr('Setara range harga', r.tier ? esc(r.tier.name) : '–') +
      rr('DP sekitar ' + esc(S.settings.dp) + '% dari kontribusi', idr(r.dp)) +
      '<h4>Pengeluaran per anggota, 5 tahun</h4>' +
      rr('Kontribusi pembelian (termasuk DP)', idr(r.c)) +
      rr('Iuran rutin, 60 × Rp250.000', idr(r.iuran)) +
      rr('Antar-jemput, ' + (CALC.trips * 5) + ' trip × Rp100.000', idr(r.antar)) +
      rr('Biaya variabel (perkiraan Anda), 60 bulan', idr(r.vr)) +
      rr('Total pengeluaran', idr(r.out), 'tot') +
      '<h4>Di akhir kontrak (asumsi)</h4>' +
      rr('Harga jual asumsi, ' + CALC.sale + '% dari harga unit', idr(r.sale)) +
      rr('Komisi jual 10%', idr(-r.fe)) +
      rr('Hasil bersih dibagi 6, per anggota', idr(r.per)) +
      '<h4>Hasil</h4>' +
      rr('Biaya bersih per anggota', idr(r.cost), 'tot') + '</div>';
  }
  function calcVals() { return { contrib: idr(CALC.contrib * 1e6), trips: CALC.trips + ' trip', varm: idr(CALC.varm), sale: CALC.sale + '%' }; }
  function calcUpdate() {
    var o = document.getElementById('calc-out'); if (o) o.innerHTML = calcRows();
    var z = document.getElementById('tz-out'); if (z) z.innerHTML = tzRows();
    var v = calcVals();
    Object.keys(v).forEach(function (k) {
      var e = document.getElementById('o-' + k); if (e) e.textContent = v[k];
      var i = document.getElementById('c-' + k); if (i) i.setAttribute('aria-valuetext', v[k]);
    });
  }
  function slider(k, label, min, max, step, hint) {
    var v = calcVals();
    return '<div class="fld"><label for="c-' + k + '">' + label + '<b id="o-' + k + '">' + v[k] + '</b></label><input id="c-' + k + '" data-calc="' + k + '" type="range" min="' + min + '" max="' + max + '" step="' + step + '" value="' + CALC[k] + '" aria-valuetext="' + esc(v[k]) + '"><small>' + hint + '</small></div>';
  }
  function calcHtml() {
    return '<div class="calc"><div class="cin">' +
      slider('contrib', 'Kontribusi per anggota', 50, 100, 5, 'Sesuai skema: Rp50–100 juta per anggota.') +
      slider('trips', 'Antar-jemput per tahun', 0, 24, 1, 'Opsional, Rp100.000 per trip.') +
      slider('varm', 'Biaya variabel per bulan', 0, 2000000, 100000, 'BBM, tol, dan perbaikan. Belum ada tarif baku, isi perkiraan Anda sendiri.') +
      slider('sale', 'Asumsi harga jual di tahun ke-5', 40, 100, 5, 'Persentase dari harga unit (di luar margin beli). Hanya asumsi untuk simulasi, bukan prediksi.') +
      '</div><div class="cout" id="calc-out">' + calcRows() + '</div></div>' +
      '<p class="fine" style="margin-top:16px">Simulasi sederhana untuk gambaran biaya, bukan penawaran, prediksi, atau janji hasil. Nilai jual unit di tahun ke-5 bisa lebih rendah atau lebih tinggi dari asumsi. Asumsi: margin beli pengelola 10% sudah termasuk dalam kontribusi sehingga harga unit sama dengan total dana dibagi 1,1, dan hasil bersih dibagi rata untuk 6 anggota (ketentuan final soal harga jual dan pembagian sedang difinalisasi). Tidak memperhitungkan biaya yang belum ditetapkan, seperti pajak kendaraan dan asuransi.</p>';
  }
  function pgBiaya() {
    var h = pageHead('Biaya & simulasi', 'Biaya yang perlu Anda ketahui', 'Tarif di bawah berasal dari skema yang berlaku. Gunakan simulasi untuk melihat gambaran biaya per anggota selama 5 tahun.');
    function fc(title, inner) { return '<div class="fcard"><h3>' + esc(title) + '</h3><div class="fees">' + inner + '</div></div>'; }
    h += '<section class="wrap blk fgrid">' +
      fc('Di awal',
        fee('Kontribusi pembelian', 'Rp50–100 juta / anggota', 'Total dana Rp300–600 juta per unit dari 6 anggota, sudah termasuk margin beli pengelola.') +
        fee('Uang muka (DP)', 'sekitar {dp}% dari kontribusi', 'Saat ini hanya DP yang dikumpulkan untuk mengamankan slot, bukan pelunasan.') +
        fee('Margin beli pengelola', '10% dari harga unit', 'Sourcing dan markup fee. Sudah termasuk dalam kontribusi Anda, bukan biaya tambahan.')) +
      fc('Setiap bulan',
        fee('Biaya manajemen', 'Rp1.000.000 / unit', 'Rp166.667 per anggota per bulan.') +
        fee('Sewa garasi', 'Rp500.000 / unit', 'Rp83.333 per anggota per bulan.') +
        fee('Iuran rutin per anggota', 'Rp250.000 / bulan', 'Manajemen dan garasi, dibayar bulanan selama kontrak.')) +
      fc('Sesuai kebutuhan',
        fee('Antar-jemput unit', 'Rp100.000 / trip', 'Opsional, hanya saat dibutuhkan anggota.') +
        fee('BBM, tol, perbaikan khusus di luar garansi', 'Ditagih terpisah', 'Tagihan variabel sesuai pemakaian dan kondisi unit.') +
        fee('Perawatan dan perbaikan', 'Dibagi antar anggota', 'Menjadi tanggung jawab para anggota. Lihat [[#aturan|Aturan pakai]].')) +
      fc('Di akhir kontrak', fee('Komisi jual (exit fee)', '10%', 'Dipotong dari harga jual di tahun ke-5.')) + '</section>';
    h += blk('Simulasi biaya per anggota', calcHtml());
    return h;
  }

  /* aturan pakai */
  function pgAturan() {
    var h = pageHead('Aturan pakai', 'Aturan pemakaian unit', 'Aturan dasar agar 6 anggota bisa memakai unit dengan adil dan unit tetap terawat. Ketentuan lengkap yang mengikat ada di perjanjian tertulis.');
    h += blk('Kepemilikan unit', '<div class="prose"><p>' + tok('Unit didaftarkan atas nama pengelola, {perusahaan}. Hak setiap anggota (1/6), termasuk hak pakai bergantian, diatur dalam perjanjian tertulis, bukan lewat nama di dokumen kendaraan.') + '</p><p>' + tok('Konsekuensinya dijelaskan di [[#perlindungan|Perlindungan & risiko]].') + '</p></div>');
    h += blk('Jadwal pemakaian', '<div class="prose"><p>' + tok('Unit dipakai bergantian oleh 6 anggota. Pada tahap pilot, jadwal diatur manual oleh pengelola. Kalender otomatis dengan pembagian weekend dan weekday yang adil, serta fitur tukar jadwal antaranggota, direncanakan di tahap berikutnya.') + '</p></div>');
    h += blk('Biaya yang ditanggung anggota', rowsList([
      'Iuran rutin Rp250.000 per anggota per bulan (manajemen dan garasi).',
      'Biaya variabel seperti BBM, tol, dan perbaikan khusus di luar garansi, ditagih terpisah.',
      'Antar-jemput Rp100.000 per trip, bila memakai layanan ini.',
      'Perawatan dan perbaikan unit: tanggung jawab para anggota, dibagi bersama.'
    ]));
    h += blk('Perawatan dan perbaikan', '<div class="prose"><p>' + tok('Biaya perawatan dan perbaikan menjadi tanggung jawab para anggota dan dibagi bersama. Anggota yang tidak mau ikut membayar bagiannya dikenai sanksi berupa pengurangan masa pakai.') + '</p></div><div class="pols" style="margin-top:16px">' +
      pol('repairSanction', 'Rincian pengurangan masa pakai') + '</div>');
    h += blk('Batas pemakaian dan syarat pengendara', '<div class="pols">' + pol('usage', 'Batas pemakaian dan syarat SIM', 'Mencakup batas durasi per giliran, wilayah pakai, dan kelengkapan SIM pengendara.') + '</div>');
    return h;
  }

  /* perlindungan & risiko */
  function pgPerlindungan() {
    var h = pageHead('Perlindungan & risiko', 'Yang sudah pasti, yang masih disusun, dan risikonya', 'Skema ini punya manfaat sekaligus risiko. Halaman ini merangkum ketentuan yang sudah ditetapkan, yang masih difinalisasi, dan hal-hal yang perlu Anda pahami sebelum mendaftar.');
    h += blk('Sudah ditetapkan', rowsList([
      'Unit terdaftar atas nama pengelola, {perusahaan}. Hak anggota diatur dalam perjanjian tertulis.',
      'DP dikembalikan. Jika anggota mengundurkan diri saat anggota lain sudah siap, dikenakan denda.',
      'Perawatan dan perbaikan menjadi tanggung jawab para anggota. Anggota yang tidak mau ikut membayar bagiannya dikenai sanksi pengurangan masa pakai.',
      'Kontrak 5 tahun per unit. Iuran rutin Rp250.000 per anggota per bulan. Komisi jual 10% saat likuidasi di tahun ke-5.',
      'Verifikasi anggota dilakukan manual oleh tim sebelum status berubah menjadi Terverifikasi.',
      'Margin beli pengelola 10% sudah termasuk dalam kontribusi, bukan biaya tambahan.',
      'Saat ini hanya DP sekitar {dp}% yang dikumpulkan, bukan pelunasan.',
      'Publik hanya melihat inisial dan ikon status, atas persetujuan anggota.'
    ]));
    h += blk('Rincian yang disusun', '<div class="pols">' + POL.map(function (p) { return pol(p.k, p.l); }).join('') + '</div>');
    var risks = [
      ['Bukan produk investasi', 'Tidak ada janji keuntungan atau imbal hasil. Nilai jual unit di tahun ke-5 bisa lebih rendah atau lebih tinggi dari harga beli, dan komisi jual 10% dipotong dari harga jual. Anda bisa menerima kurang dari kontribusi.'],
      ['Unit atas nama pengelola', 'Hak Anda bersumber dari perjanjian, bukan dari nama di dokumen kendaraan. Risikonya bergantung pada kondisi dan kepatuhan pengelola serta kekuatan perjanjian. Baca perjanjian dengan teliti dan pertimbangkan berkonsultasi dengan notaris atau penasihat hukum.'],
      ['Bergantung pada anggota lain', 'Iuran dan biaya perbaikan dibagi di antara 6 anggota. Jika ada anggota yang tidak membayar, anggota lain bisa terdampak sementara ketentuan sanksi diberlakukan.'],
      ['Likuiditas terbatas', 'Kontrak berjalan 5 tahun. Aturan keluar lebih awal masih difinalisasi, dan pasar sekunder untuk pengalihan 1/6 hak direncanakan di tahap berikutnya, belum tersedia.'],
      ['Unit belum ditentukan', 'Gambar di katalog hanya ilustrasi. Unit sebenarnya dicarikan setelah dana terkumpul, sehingga warna, varian, dan tahun bisa berbeda dalam rentang yang tertera.'],
      ['Biaya variabel tidak pasti', 'BBM, tol, dan perbaikan di luar garansi ditagih sesuai pemakaian dan kondisi unit, sehingga nominalnya tidak bisa dipastikan di awal.'],
      ['Kerusakan, kehilangan, kecelakaan', 'Kejadian seperti ini dapat menimbulkan biaya. Cakupan perlindungan, misalnya asuransi, akan dijelaskan setelah ditetapkan.'],
      ['Jadwal bergantian', 'Unit dipakai 6 anggota sehingga ketersediaan pada hari tertentu bisa bersaing. Pembagian jadwal diatur agar adil, tetapi tidak semua permintaan hari bisa dipenuhi.']
    ];
    h += blk('Risiko yang perlu dipahami', '<div class="g3">' + risks.map(function (r) { return '<div class="pc"><h3>' + esc(r[0]) + '</h3><p>' + tok(r[1]) + '</p></div>'; }).join('') + '</div>' +
      '<p class="fine">Halaman ini berisi informasi umum, bukan nasihat hukum atau keuangan. Ketentuan yang mengikat adalah yang tercantum dalam perjanjian tertulis.</p>');
    return h;
  }

  /* FAQ */
  function pgFaq() {
    var h = pageHead('FAQ', 'Pertanyaan yang sering diajukan', 'Tidak menemukan jawabannya? Hubungi kami lewat halaman [[#tentang|Tentang & kontak]].');
    var list = S.site.faq.map(function (f) {
      return '<details><summary>' + esc(f.q) + '</summary><div class="ans"><p class="ut">' + tok(f.a) + '</p>' +
        (UI.admin ? '<button type="button" class="btn sm" data-act="faq-edit" data-id="' + esc(f.id) + '" data-fk="faq-' + esc(f.id) + '">Ubah pertanyaan</button>' : '') + '</div></details>';
    }).join('');
    h += '<section class="wrap blk" style="margin-top:28px">' + (list ? '<div class="faq">' + list + '</div>' : '<div class="empty-state">Belum ada pertanyaan.</div>') +
      (UI.admin ? '<div class="cta"><button type="button" class="btn" data-act="faq-add" data-fk="faqadd">+ Pertanyaan</button></div>' : '') + '</section>';
    return h;
  }

  /* tentang & kontak */
  function founderBlock() {
    var f = S.site.founder, has = !!f.photo, adm = UI.admin, showPhoto = has || adm;
    var cap = has && (f.name || f.role) ? '<figcaption>' + (f.name ? '<b>' + esc(f.name) + '</b>' : '') + esc(f.role) + '</figcaption>' : '';
    var photo = !showPhoto ? '' : '<figure class="fph">' +
      (has ? '<img src="' + esc(f.photo) + '" alt="' + esc(f.name ? 'Foto ' + f.name : 'Foto pendiri') + '" decoding="async">' : '<div class="ph0">Belum ada foto pendiri. Unggah lewat tombol Ubah profil pendiri.</div>') + cap + '</figure>';
    var body = '<div>' + (f.quote ? '<p class="fq">' + esc(f.quote) + '</p>' : '') +
      (f.story ? '<div class="prose ut">' + tok(f.story) + '</div>' : '') +
      (!has && f.name ? '<p class="sig">' + esc(f.name) + (f.role ? ', ' + esc(f.role) : '') + '</p>' : '') +
      (adm ? '<div class="cta"><button type="button" class="btn" data-act="founder" data-fk="founder">Ubah profil pendiri</button></div>' : '') + '</div>';
    return blk('Kenapa kami ada', '<div class="fnd' + (showPhoto ? '' : ' nophoto') + '">' + photo + body + '</div>');
  }
  function pgTentang() {
    var c = S.site.company, wa = waGeneral();
    function dd(v) { return v ? '<dd class="ut">' + esc(v) + '</dd>' : '<dd class="na">Sedang dilengkapi</dd>'; }
    var h = pageHead('Tentang & kontak', 'Tentang kami', (S.settings.brand || 'Platform ini') + ' memfasilitasi kepemilikan bersama moge: 1 unit dimiliki 6 anggota dengan hak pakai bergantian. Platform dikelola oleh ' + co() + '.');
    h += founderBlock();
    h += blk('Tiga hal yang kami lihat', '<div class="g3">' +
      '<div class="pc"><h3>Mimpi yang tertunda</h3><p>Bagi banyak profesional dan pengusaha kelas menengah, memiliki moge baru terasa mungkin setelah kondisi finansial tertentu yang jarang datang. Mimpinya tidak hilang, hanya menunggu terlalu lama.</p></div>' +
      '<div class="pc"><h3>Kepemilikan yang berat</h3><p>Harga beli, biaya perawatan, tempat menyimpan, dan ketentuan kepemilikan membuat satu unit terasa terlalu besar untuk dipikul sendirian.</p></div>' +
      '<div class="pc"><h3>Unit yang jarang dipakai</h3><p>Kendaraan rekreasional umumnya lebih banyak diam di garasi daripada dipakai. Dengan berbagi 6 orang, satu unit dipakai lebih sering dan biaya tetapnya terbagi.</p></div></div>');
    h += blk('Yang kami lakukan', rowsList([
      'Mengumpulkan 6 anggota untuk setiap unit dan memverifikasi anggota secara manual.',
      'Mencarikan unit sesuai model dan rentang tahun setelah dana terkumpul.',
      'Mengatur jadwal pemakaian, garasi, dan pencatatan perawatan unit.',
      'Menyusun laporan keuangan unit untuk para anggota.'
    ]));
    h += blk('Data pengelola', '<dl class="idl"><dt>Nama badan usaha</dt><dd>' + esc(c.name) + '</dd><dt>NIB</dt>' + dd(c.nib) + '<dt>Alamat</dt>' + dd(c.address) + '<dt>Email</dt>' + dd(c.email) + '<dt>Jam layanan</dt>' + dd(c.hours) + '</dl>' +
      (UI.admin ? '<div class="cta"><button type="button" class="btn" data-act="company" data-fk="company">Ubah data pengelola</button></div>' : ''));
    h += blk('Hubungi kami', '<div class="prose"><p>Pendaftaran dan pertanyaan dilayani lewat WhatsApp.</p></div><div class="cta">' +
      (wa ? '<a class="btn primary" href="' + esc(wa) + '" target="_blank" rel="noopener">Chat WhatsApp</a>' : '<button type="button" class="btn" disabled>Nomor WhatsApp segera tersedia</button>') + '</div>');
    h += blk('Privasi data', '<div class="prose"><p>Data identitas dikumpulkan hanya untuk verifikasi anggota. Di halaman publik hanya tampil inisial dan ikon status, dan hanya atas persetujuan anggota. Anggota dapat meminta inisialnya dihapus lewat WhatsApp.</p></div>' +
      '<p style="margin-top:14px"><span class="chip tbd">' + CLK + 'Kebijakan privasi lengkap sedang disusun</span></p>');
    return h;
  }

  function page(r) {
    switch (r) {
      case 'cara-kerja': return pgCara();
      case 'biaya': return pgBiaya();
      case 'aturan': return pgAturan();
      case 'perlindungan': return pgPerlindungan();
      case 'faq': return pgFaq();
      case 'tentang': return pgTentang();
    }
    return pgBeranda();
  }
  function siteFoot() {
    var n = (S.settings.whatsapp || '').replace(/\D/g, ''), c = S.site.company;
    var half = Math.ceil(ROUTES.length / 2);
    function col(list) { return list.map(function (x) { return '<a href="#' + x[0] + '">' + x[1] + '</a>'; }).join(''); }
    return '<footer class="gfoot dark"><div class="wrap"><div class="gf"><div><span class="logo">' + MARK + '<span>' + esc(S.settings.brand || '[NAMA PLATFORM]') + '</span></span><p>Kepemilikan bersama moge: 1 unit, 6 anggota, hak pakai bergantian. Dikelola oleh ' + esc(co()) + '. Unit terdaftar atas nama pengelola.</p></div>' +
      '<div><h4>Halaman</h4><nav aria-label="Tautan bawah">' + col(ROUTES) + '</nav></div>' +
      '<div><h4>Hubungi kami</h4><p style="margin-top:0">' + (n ? 'WhatsApp <span class="wan">+' + esc(n) + '</span>' : 'Nomor WhatsApp segera tersedia.') + '</p>' +
      (c.email ? '<p>' + esc(c.email) + '</p>' : '') + (c.hours ? '<p>' + esc(c.hours) + '</p>' : '') + (c.address ? '<p class="ut">' + esc(c.address) + '</p>' : '') + '</div></div>' +
      '<p class="fine">Bukan produk investasi. Tidak ada janji keuntungan atau imbal hasil. Gambar unit hanya contoh. Range dana dan tahun bersifat indikatif.</p></div></footer>';
  }
  function render() {
    fixUI();
    var r = route();
    app.innerHTML = adminBar(r) + header(r) + '<main>' + page(r) + ctaBand() + '</main>' + siteFoot() + mobileBar();
    if (UI.focus) { var el = app.querySelector('[data-fk="' + UI.focus + '"]'); if (el) el.focus(); UI.focus = null; }
  }
