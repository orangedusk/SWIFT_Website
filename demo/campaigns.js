/* Demo tool: campaign preview (demo branch only, loaded by demo/demo.js).
   Swaps the homepage hero for seasonal campaigns, like flu season or school holidays. */
(function () {
  var heroHeadline = document.getElementById('heroHeadline');
  if (!heroHeadline) return; // homepage only

  var campaigns = [
    {
      id: 'default',
      label: 'Everyday care',
      desc: 'The standard homepage hero (current)',
      swatch: '#2C685E',
      image: 'brand_assets/clinic-reception.jpg',
      imageAlt: "Reception at SWIFT's Rouse Hill clinic",
      headline: 'Is urgent care right for me?',
      subhead: 'Search a symptom to see where to go. SWIFT treats urgent illness and injury for ages 3 months and up, with no referral needed.',
      ctaText: 'Call (02) 8859 9099',
      ctaHref: 'tel:0288599099'
    },
    {
      id: 'flu',
      label: 'Flu shot season',
      desc: 'Seasonal vaccination campaign',
      swatch: '#4B9587',
      image: 'brand_assets/Flu_shot.jpeg',
      imageAlt: 'Flu vaccination campaign',
      headline: 'Flu shots, walk in today.',
      subhead: 'Protect yourself and your family this flu season. No appointment needed — just walk in during opening hours.',
      ctaText: 'Book your flu shot',
      ctaHref: 'request-appointment.html'
    },
    {
      id: 'kids',
      label: 'School holidays',
      desc: 'Paediatric-focused campaign',
      swatch: '#377E71',
      image: 'brand_assets/school_holidays.jpeg',
      imageAlt: 'School holidays campaign',
      headline: 'School holidays? We’ve got the kids covered.',
      subhead: 'From sprains to fevers, we treat children 3 months and up — every day of the holidays.',
      ctaText: 'Walk in today',
      ctaHref: '#right-care'
    }
  ];

  var wrap = document.createElement('div');
  wrap.innerHTML =
    '<button type="button" id="campaignDemoBtn" class="fixed z-30 bottom-5 left-4 focus-ring hidden lg:inline-flex items-center gap-1.5 rounded-full bg-white border border-dashed border-ink/25 text-ink/70 text-xs font-medium pl-3 pr-3.5 py-2 shadow-[0_4px_14px_-4px_rgba(0,0,0,0.2)] hover:border-ink/40 hover:text-ink/80 transition-colors">' +
    '  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 5h16M4 12h10M4 19h13" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>' +
    '  Preview campaigns' +
    '</button>' +
    '' +
    '<div id="campaignModal" class="fixed inset-0 z-50 hidden">' +
    '  <div id="campaignModalBackdrop" class="absolute inset-0 bg-ink/50 backdrop-blur-sm"></div>' +
    '  <div class="relative h-full flex items-end sm:items-center justify-center p-0 sm:p-6">' +
    '    <div class="relative bg-white w-full sm:max-w-md sm:rounded-2xl rounded-t-2xl shadow-[0_20px_50px_-12px_rgba(0,0,0,0.4)] max-h-[85vh] overflow-y-auto">' +
    '      <div class="flex items-center justify-between px-5 sm:px-6 pt-5 pb-3 sticky top-0 bg-white border-b border-line">' +
    '        <div>' +
    '          <p class="font-display font-semibold text-ink">Preview a campaign</p>' +
    '          <p class="text-xs text-ink/65 mt-0.5">Demo only — swaps the hero above</p>' +
    '        </div>' +
    '        <button type="button" id="campaignModalClose" class="focus-ring w-8 h-8 flex items-center justify-center rounded-full hover:bg-mint text-ink/65 hover:text-ink" aria-label="Close">' +
    '          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>' +
    '        </button>' +
    '      </div>' +
    '      <div id="campaignList" class="p-3 sm:p-3 space-y-1"></div>' +
    '    </div>' +
    '  </div>' +
    '</div>';
  while (wrap.firstChild) document.body.appendChild(wrap.firstChild);

  var demoBtn = document.getElementById('campaignDemoBtn');
  var modal = document.getElementById('campaignModal');
  var backdrop = document.getElementById('campaignModalBackdrop');
  var closeBtn = document.getElementById('campaignModalClose');
  var list = document.getElementById('campaignList');

  var heroImg = document.getElementById('heroImg');
  var heroSubhead = document.getElementById('heroSubhead');
  var heroCta = document.getElementById('heroPrimaryCta');

  function applyCampaign(c) {
    heroImg.src = c.image;
    heroImg.alt = c.imageAlt;
    heroHeadline.textContent = c.headline;
    heroSubhead.textContent = c.subhead;
    heroCta.textContent = c.ctaText;
    heroCta.setAttribute('href', c.ctaHref);
  }

  campaigns.forEach(function (c) {
    var item = document.createElement('button');
    item.type = 'button';
    item.className = 'w-full focus-ring flex items-center gap-3 text-left rounded-xl p-3 hover:bg-mint transition-colors';
    item.innerHTML =
      '<span class="shrink-0 w-10 h-10 rounded-lg" style="background:' + c.swatch + '"></span>' +
      '<span><span class="block font-medium text-ink text-sm">' + c.label + '</span>' +
      '<span class="block text-xs text-ink/65">' + c.desc + '</span></span>';
    item.addEventListener('click', function () {
      applyCampaign(c);
      closeModal();
    });
    list.appendChild(item);
  });

  function openModal() {
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }
  function closeModal() {
    modal.classList.add('hidden');
    document.body.style.overflow = '';
  }

  demoBtn.addEventListener('click', openModal);
  if (window.SwiftDemo) window.SwiftDemo.addMenuItem('Preview campaigns', openModal);
  closeBtn.addEventListener('click', closeModal);
  backdrop.addEventListener('click', closeModal);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeModal();
  });
})();
