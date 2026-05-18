/* ============================================================
   MOEMODI — main.js
   Vanilla JS. No build step.
   - Sticky nav state
   - Mobile menu toggle
   - Scroll reveal (Intersection Observer)
   - Contact form (mailto + WhatsApp deeplink, no backend)
   - Footer year
   ============================================================ */
(function () {
  'use strict';

  // -------- Footer year --------
  var yearEl = document.getElementById('year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  // -------- Sticky nav scroll state --------
  var nav = document.querySelector('.site-nav');
  if (nav) {
    var lastScrolled = false;
    var onScroll = function () {
      var scrolled = window.scrollY > 8;
      if (scrolled !== lastScrolled) {
        nav.classList.toggle('scrolled', scrolled);
        lastScrolled = scrolled;
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // -------- Mobile menu --------
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.getElementById('mobile-menu');
  if (toggle && menu) {
    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.classList.toggle('is-open', open);
      menu.classList.toggle('is-open', open);
      if (open) {
        menu.removeAttribute('hidden');
      } else {
        menu.setAttribute('hidden', '');
      }
    };

    toggle.addEventListener('click', function () {
      var isOpen = toggle.classList.contains('is-open');
      setOpen(!isOpen);
    });

    // Close menu when a link inside is clicked
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { setOpen(false); });
    });

    // Close on escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.classList.contains('is-open')) {
        setOpen(false);
        toggle.focus();
      }
    });
  }

  // -------- Scroll reveal --------
  var revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length) {
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
      revealEls.forEach(function (el) { io.observe(el); });
    } else {
      // Fallback: just show
      revealEls.forEach(function (el) { el.classList.add('is-visible'); });
    }
  }

  // -------- Smooth scroll offset for sticky nav --------
  // (CSS scroll-behavior covers this; small JS guard for older browsers)
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (!id || id === '#' || id.length < 2) return;
      var target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      var navHeight = nav ? nav.offsetHeight : 0;
      var top = target.getBoundingClientRect().top + window.scrollY - navHeight - 8;
      window.scrollTo({ top: top, behavior: 'smooth' });
      // update hash without jumping
      if (history.replaceState) history.replaceState(null, '', id);
    });
  });

  // -------- Contact form --------
  var form = document.getElementById('contact-form');
  var waBtn = document.getElementById('send-whatsapp');
  var EMAIL_TO = 'Selina@gmail.com';
  var WA_NUMBER = '27722121348';

  function getFields() {
    if (!form) return null;
    var data = new FormData(form);
    return {
      name: (data.get('name') || '').toString().trim(),
      contact: (data.get('contact') || '').toString().trim(),
      topic: (data.get('topic') || '').toString().trim(),
      message: (data.get('message') || '').toString().trim()
    };
  }

  function isValid(fields) {
    return fields.name.length > 1 && fields.contact.length > 1 && fields.message.length > 1;
  }

  function flagInvalid() {
    if (!form) return;
    ['name', 'contact', 'message'].forEach(function (n) {
      var el = form.querySelector('[name="' + n + '"]');
      if (!el) return;
      var val = (el.value || '').trim();
      el.style.borderColor = val.length > 1 ? '' : '#C7453E';
      el.style.boxShadow = val.length > 1 ? '' : '0 0 0 4px rgba(199,69,62,0.10)';
    });
  }

  function buildMessageBody(fields) {
    return [
      'Hello MOEMODI,',
      '',
      'My name is ' + fields.name + '.',
      'You can reach me on: ' + fields.contact,
      'I\'m enquiring about: ' + fields.topic,
      '',
      'Message:',
      fields.message,
      '',
      '— Sent from moemodi.co.za'
    ].join('\n');
  }

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var fields = getFields();
      if (!fields || !isValid(fields)) { flagInvalid(); return; }
      var subject = 'Website enquiry — ' + fields.topic;
      var body = buildMessageBody(fields);
      var href = 'mailto:' + EMAIL_TO +
                 '?subject=' + encodeURIComponent(subject) +
                 '&body=' + encodeURIComponent(body);
      window.location.href = href;
    });
  }

  if (waBtn) {
    waBtn.addEventListener('click', function () {
      var fields = getFields();
      if (!fields || !isValid(fields)) { flagInvalid(); return; }
      var text = buildMessageBody(fields);
      var href = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(text);
      window.open(href, '_blank', 'noopener,noreferrer');
    });
  }

  // Clear validation styling on input
  if (form) {
    form.querySelectorAll('input, textarea, select').forEach(function (el) {
      el.addEventListener('input', function () {
        el.style.borderColor = '';
        el.style.boxShadow = '';
      });
    });
  }
})();
