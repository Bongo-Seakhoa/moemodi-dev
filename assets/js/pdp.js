/* MOEMODI product detail page — size selector & WhatsApp deeplink update */
(function () {
  'use strict';

  var heroImg = document.getElementById('hero-img');
  var waLink = document.getElementById('wa-link');
  var sizeInputs = document.querySelectorAll('input[name="size"]');
  if (!heroImg || sizeInputs.length === 0) return;

  var productName = (document.title || '').split('|')[0].trim() || 'this product';
  var phoneNumber = '27722121348';

  function setActivePill(value) {
    document.querySelectorAll('.pdp-sizes .size-pill').forEach(function (pill) {
      var input = pill.querySelector('input[name="size"]');
      var on = input && input.value === value;
      pill.classList.toggle('is-active', !!on);
    });
  }

  function updateForSize(value) {
    var sizeNum = (value || '').replace(/\D/g, '');
    var src = heroImg.getAttribute('data-img-' + sizeNum);
    if (src) heroImg.setAttribute('src', src);
    var alt = heroImg.getAttribute('alt') || '';
    heroImg.setAttribute('alt', alt.replace(/\d+ml/, value));
    if (waLink) {
      var msg = "Hello MOEMODI, I'd like to order " + productName + " " + value + ".";
      waLink.href = 'https://wa.me/' + phoneNumber + '?text=' + encodeURIComponent(msg);
    }
    setActivePill(value);
    if (history.replaceState) history.replaceState(null, '', '#size-' + value);
  }

  sizeInputs.forEach(function (input) {
    input.addEventListener('change', function () { updateForSize(input.value); });
  });
  document.querySelectorAll('.pdp-sizes .size-pill').forEach(function (pill) {
    pill.addEventListener('click', function () {
      var input = pill.querySelector('input[name="size"]');
      if (input) { input.checked = true; updateForSize(input.value); }
    });
  });

  // If URL contains #size-250ml or #size-500ml, select that size
  var hash = (window.location.hash || '').replace('#size-', '');
  if (hash === '250ml' || hash === '500ml') {
    var target = document.querySelector('input[name="size"][value="' + hash + '"]');
    if (target) { target.checked = true; updateForSize(hash); }
  } else {
    // Initialise active pill state from current checked input
    var checked = document.querySelector('input[name="size"]:checked');
    if (checked) setActivePill(checked.value);
  }
})();
