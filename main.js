// Không có file này trang vẫn đọc được đủ: chữ hiện sẵn, nút web vẫn bấm được, cuộn bắt mục do CSS lo.
(function () {
  document.documentElement.classList.add('js');
  var links = window.THUMUA365_LINKS || {};
  var calm = matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('[data-link="web"]').forEach(function (a) {
    if (links.web) a.href = links.web;
  });

  // Nút APK: có apkUrl thì thành nút tải thật, không có thì giữ "Sắp có" viết sẵn trong HTML.
  // Không tự dò file: dò khi chưa có file là một lỗi 404 đỏ trong console.
  if (links.apkUrl) {
    var apks = document.querySelectorAll('[data-link="apk"]');
    var label = function (text) {
      apks.forEach(function (a) { var n = a.querySelector('.soon'); if (n) n.textContent = text; });
    };
    apks.forEach(function (a) {
      a.href = links.apkUrl;
      a.setAttribute('download', '');
      a.removeAttribute('title');
      a.classList.remove('is-soon');
    });
    label('Tải file APK');
    // File nằm cùng trang thì hỏi dung lượng để ghi lên nút (máy chủ khác thì CORS chặn, bỏ qua).
    if (!/^https?:/.test(links.apkUrl)) fetch(links.apkUrl, { method: 'HEAD' }).then(function (r) {
      var bytes = Number(r.ok && r.headers.get('content-length'));
      if (bytes) label('Tải file APK · ' + (bytes / 1048576).toFixed(bytes < 10485760 ? 1 : 0).replace('.', ',') + ' MB');
    }).catch(function () {});
  }

  // Đánh số thứ tự cho từng phần tử chuyển động trong mục, để chúng hiện lần lượt.
  var sections = Array.prototype.slice.call(document.querySelectorAll('main > section'));
  sections.forEach(function (s) {
    s.querySelectorAll('[data-a]').forEach(function (el, i) { el.style.setProperty('--i', i); });
  });

  // Hoạ tiết nông sản: rải hai bên mép mục, xen trái/phải cho cân. Số giả ngẫu nhiên có hạt giống
  // theo từng mục để lần nào tải trang cũng ra đúng một bố cục.
  var narrow = innerWidth < 768;
  sections.forEach(function (s, k) {
    var kind = s.dataset.crop;
    if (!kind) return;
    var seed = k * 7919 + 17;
    var rnd = function () { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; };
    var n = narrow ? 4 : 6;
    var html = '';
    for (var j = 0; j < n; j++) {
      var x = narrow ? (j % 2 ? 95 + rnd() * 5 : rnd() * 5) : (j % 2 ? 94 + rnd() * 3.5 : 1.5 + rnd() * 3.5); // tâm hình, tính theo % bề ngang
      var y = 6 + (j / n) * 84 + rnd() * 8;
      var size = (narrow ? 20 : 26) + rnd() * (narrow ? 12 : 22);
      html += '<svg class="crop' + (kind === 'tieu' ? ' tall' : '') + '" style="--x:' + x.toFixed(1) + '%;--y:' + y.toFixed(1) +
        '%;--s:' + size.toFixed(0) + 'px;--r:' + (rnd() * 360).toFixed(0) + 'deg;--d:' + (9 + rnd() * 8).toFixed(1) +
        's;--dl:-' + (rnd() * 8).toFixed(1) + 's"><use href="#c-' + kind + '"/></svg>';
    }
    var box = document.createElement('div');
    box.className = 'crops-bg';
    box.setAttribute('aria-hidden', 'true');
    box.innerHTML = html;
    s.prepend(box);
  });

  var dots = {};
  document.querySelectorAll('.dots a').forEach(function (a) { dots[a.hash.slice(1)] = a; });

  // Dải giữa màn hình: mục nào chạm dải này là mục đang xem. Dùng dải thay vì tỉ lệ
  // vì trên điện thoại có mục cao hơn màn hình, tỉ lệ hiện không bao giờ tới 50%.
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      // Chỉ mục đang xem mới cho hoạ tiết trôi, các mục khác đứng yên cho nhẹ máy.
      sections.forEach(function (s) { s.classList.toggle('on', s === e.target); });
      Object.keys(dots).forEach(function (id) {
        if (id === e.target.id) dots[id].setAttribute('aria-current', 'true');
        else dots[id].removeAttribute('aria-current');
      });
      e.target.querySelectorAll('[data-count]').forEach(function (el) { countUp(el, e.target.id === 'dau' ? 900 : 300); });
    });
  }, { rootMargin: '-45% 0px -45% 0px' });
  sections.forEach(function (s) { io.observe(s); });

  // Trả về mục sẽ tới, hoặc null khi nên để trình duyệt cuộn như thường:
  // mục đang xem cao hơn màn hình (hay gặp trên điện thoại) mà chưa đọc hết, hoặc đã ở mục đầu/cuối.
  function target(step) {
    var y = scrollY + innerHeight / 2;
    var cur = 0;
    sections.forEach(function (s, i) { if (s.offsetTop <= y) cur = i; });
    var box = sections[cur].getBoundingClientRect();
    if ((step === 1 && box.bottom > innerHeight + 2) || (step === -1 && box.top < -2)) return null;
    var next = Math.max(0, Math.min(sections.length - 1, cur + step));
    return next === cur ? null : sections[next];
  }
  function go(el) { el.scrollIntoView({ behavior: calm ? 'auto' : 'smooth' }); }

  // Phím ↑↓ / PageUp / PageDown / Home / End: nhảy đúng một mục.
  addEventListener('keydown', function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey || e.defaultPrevented) return;
    if (/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) return;
    var step = { ArrowDown: 1, PageDown: 1, ArrowUp: -1, PageUp: -1, Home: -99, End: 99 }[e.key];
    var el = step && target(step);
    if (!el) return;
    e.preventDefault();
    go(el);
  });

  // Lăn chuột: mỗi lần lăn sang đúng một mục. Chỉ bật khi CSS đang bắt mục chặt (màn rộng);
  // CSS thuần thì một nấc lăn nhỏ bị kéo về chỗ cũ. Khoá được gia hạn chừng nào còn sự kiện lăn,
  // để quán tính của touchpad không nhảy liền hai ba mục.
  var wide = matchMedia('(min-width: 768px) and (min-height: 600px)');
  var lockUntil = 0;
  addEventListener('wheel', function (e) {
    if (e.ctrlKey || !wide.matches || Math.abs(e.deltaY) < Math.abs(e.deltaX)) return;
    var el = target(e.deltaY > 0 ? 1 : -1);
    if (!el) return;
    e.preventDefault();
    var now = performance.now();
    if (now < lockUntil) { lockUntil = Math.max(lockUntil, now + 250); return; }
    if (Math.abs(e.deltaY) < 4) return;
    lockUntil = now + (calm ? 400 : 900);
    go(el);
  }, { passive: false });

  // Số chạy từ 0 lên như máy tính tiền. Mỗi số chỉ chạy một lần; HTML đã ghi sẵn số thật,
  // nên tắt JS hay bật giảm chuyển động vẫn thấy đúng số.
  var fmt = new Intl.NumberFormat('vi-VN');
  function countUp(el, wait) {
    if (calm || el.dataset.done) return;
    el.dataset.done = '1';
    var total = Number(el.dataset.count);
    var t0 = performance.now() + wait;
    requestAnimationFrame(function tick(now) {
      if (now < t0) return requestAnimationFrame(tick); // chưa tới lượt thì để nguyên số thật
      var p = Math.min(1, (now - t0) / 900);
      el.textContent = fmt.format(Math.round(total * (1 - Math.pow(1 - p, 3))));
      if (p < 1) requestAnimationFrame(tick);
    });
  }

  // Phiếu mẫu ở trang đầu: bấm thử "Trả đủ" / "Ghi nợ" thì đóng con dấu lên phiếu.
  var stamp = document.querySelector('.stamp');
  var icons = {
    paid: ['<path d="M5 12.5l4.5 4.5L19 7.5"/>', 'Phiếu đã chốt: trả đủ'],
    debt: ['<circle cx="12" cy="12" r="8"/><path d="M12 7.5V12l3 2"/>', 'Phiếu đã chốt: ghi nợ']
  };
  var stampTimer;
  document.querySelectorAll('[data-stamp]').forEach(function (b) {
    b.addEventListener('click', function () {
      var k = b.dataset.stamp;
      stamp.className = 'stamp ' + k;
      stamp.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true">' + icons[k][0] + '</svg><span class="sr-only">' + icons[k][1] + '</span>';
      void stamp.offsetWidth; // để lần bấm liền nhau vẫn thấy con dấu đóng lại từ đầu
      stamp.classList.add('show');
      clearTimeout(stampTimer);
      stampTimer = setTimeout(function () { stamp.classList.remove('show'); }, 1600);
    });
  });

  // Phiếu nghiêng nhẹ theo con chuột (chỉ máy có chuột, không bật khi giảm chuyển động).
  var card = document.querySelector('.phone-in');
  if (card && !calm && matchMedia('(hover: hover)').matches) {
    var hero = document.getElementById('dau');
    hero.addEventListener('pointermove', function (e) {
      var r = card.getBoundingClientRect();
      var x = Math.max(-1, Math.min(1, (e.clientX - r.left - r.width / 2) / r.width));
      var y = Math.max(-1, Math.min(1, (e.clientY - r.top - r.height / 2) / r.height));
      card.style.transform = 'perspective(900px) rotateY(' + (x * 8).toFixed(2) + 'deg) rotateX(' + (-y * 8).toFixed(2) + 'deg)';
    });
    hero.addEventListener('pointerleave', function () { card.style.transform = ''; });
  }
})();
