import sys, html, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from build_page import build, ROOT

# Names and roles from the current live site. Bios there are placeholder text, so
# 'bio' is left empty until SWIFT supplies real ones; the profile shows a neutral note meanwhile.
TEAM = [
  ('Leadership', 'Founders and clinical leads', [
    ('vijay-manivel', 'Dr Vijay Manivel', 'Co-Founder and Director', ''),
    ('gopinath-betarayappa', 'Dr Gopinath Betarayappa', 'Co-Founder and Director', ''),
    ('berinder-shahpuri', 'Dr Berinder Shahpuri', 'Deputy Clinical Director, Emergency Physician', ''),
  ]),
  ('Emergency doctors', 'Emergency physicians who see every walk-in patient', [
    ('nina-dhaliwal', 'Dr Nina Dhaliwal', 'Emergency Physician and Toxicologist', ''),
    ('pramod-chandru', 'Dr Pramod Chandru', 'Emergency Physician and Toxicologist', ''),
    ('earl-butler', 'Dr Earl Butler', 'Emergency Physician and Toxicologist', ''),
    ('stephen-madden', 'Dr Stephen Madden', 'Senior Emergency Doctor', ''),
    ('athar-khan', 'Dr Athar Khan', 'Senior Emergency Doctor', ''),
    ('mahesh-jagada-gangadharaiah', 'Dr Mahesh Jagada Gangadharaiah', 'Emergency Physician', ''),
    ('behzad-mirmiran', 'Dr Behzad Mirmiran', 'Emergency Physician', ''),
    ('nasim-erfani', 'Dr Nasim Erfani', 'Emergency Physician', ''),
  ]),
  ('Nursing team', 'Emergency nurses and nurse practitioners', [
    ('gisha-george', 'Gisha George', 'Nurse Unit Manager', ''),
    ('farai-mupedzi', 'Farai Mupedzi', 'Transitional Nurse Practitioner', ''),
    ('natalie-weitenberg', 'Natalie Weitenberg', 'Transitional Nurse Practitioner', ''),
    ('geetha-ganesan', 'Geetha Ganesan', 'Emergency Registered Nurse', ''),
    ('stuart-dawkins', 'Stuart Dawkins', 'Emergency Registered Nurse', ''),
    ('edsel-de-mesa', 'Edsel de Mesa', 'Registered Nurse', ''),
  ]),
]
NO_PHOTO = {'earl-butler'}

def initials(name):
    parts = [p for p in name.replace('Dr ', '').split() if p[0].isupper()]
    return (parts[0][0] + parts[-1][0]).upper()

def photo(slug, name, cls):
    if slug in NO_PHOTO:
        return ('<div class="%s bg-mint flex items-center justify-center"><span class="font-display font-bold text-4xl text-teal700">%s</span></div>' % (cls, initials(name)))
    return ('<div class="%s relative overflow-hidden bg-mint">'
            '<img src="brand_assets/team/%s.jpg" alt="Portrait of %s" loading="lazy" width="480" height="480" class="team-img w-full h-full object-cover object-top">'
            '<div class="absolute inset-0 bg-teal900 mix-blend-multiply opacity-[0.06]" aria-hidden="true"></div>'
            '<div class="absolute inset-x-0 bottom-0 h-1/3 bg-gradient-to-t from-ink/25 to-transparent" aria-hidden="true"></div></div>') % (cls, slug, html.escape(name))

def card(slug, name, role, bio):
    return ('''        <li class="flex">
          <button type="button" id="%s" class="team-card group w-full h-full flex flex-col text-left focus-ring rounded-2xl bg-white border border-line overflow-hidden shadow-[0_2px_10px_-4px_rgba(30,69,63,0.15)] hover:shadow-[0_14px_28px_-10px_rgba(30,69,63,0.25)] hover:-translate-y-0.5 active:scale-[0.98] transition-[transform,box-shadow] duration-300 scroll-mt-[140px]"
            data-slug="%s" data-name="%s" data-role="%s" data-bio="%s" data-photo="%s" data-initials="%s" aria-haspopup="dialog">
            %s
            <span class="flex-1 flex flex-col p-4 sm:p-5">
              <span class="block font-display font-semibold text-[17px] leading-snug text-ink">%s</span>
              <span class="block text-sm text-ink/60 mt-1">%s</span>
              <span class="mt-auto pt-3 inline-flex items-center gap-1 text-sm font-medium text-teal700 group-hover:text-teal900">View profile
                <svg class="transition-transform duration-300 group-hover:translate-x-0.5" width="13" height="13" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </span>
            </span>
          </button>
        </li>''' % (slug, slug, html.escape(name), html.escape(role), html.escape(bio),
                     '' if slug in NO_PHOTO else 'brand_assets/team/%s.jpg' % slug, initials(name),
                     photo(slug, name, 'aspect-square'), html.escape(name), html.escape(role)))

groups = []
for i, (title, sub, people) in enumerate(TEAM):
    cols = 'sm:grid-cols-2 lg:grid-cols-3' if i == 0 else 'grid-cols-2 lg:grid-cols-4'
    groups.append('''
    <section class="%s" aria-labelledby="grp%d">
      <div class="flex items-baseline justify-between flex-wrap gap-x-4 gap-y-1 mb-5">
        <h2 id="grp%d" class="font-display font-bold text-xl sm:text-2xl tracking-tight text-ink">%s</h2>
        <p class="text-sm text-ink/55">%s</p>
      </div>
      <ul class="grid %s gap-3 sm:gap-5">
%s
      </ul>
    </section>''' % ('' if i == 0 else 'mt-14', i, i, title, sub, cols, '\n'.join(card(*p) for p in people)))

main = '''
  <!-- Page intro -->
  <section class="bg-mint/60 border-b border-line">
    <div class="max-w-6xl mx-auto px-5 sm:px-8 pt-8 sm:pt-12 pb-10 sm:pb-14">
      <nav aria-label="Breadcrumb" class="hero-in text-sm text-ink/55 mb-5" style="animation-delay:.02s">
        <a href="index.html" class="hover:text-teal700 focus-ring rounded">Home</a>
        <span aria-hidden="true" class="mx-1.5">/</span>
        <span class="text-ink/80" aria-current="page">Our team</span>
      </nav>
      <h1 class="hero-in font-display font-extrabold text-[2.25rem] leading-[1.05] sm:text-5xl sm:leading-[1.05] tracking-tight text-ink" style="animation-delay:.08s">Meet the team</h1>
      <p class="hero-in mt-4 text-lg text-ink/70 leading-relaxed max-w-2xl" style="animation-delay:.2s">Experienced emergency physicians and nurses, working with specialists in orthopaedics, cardiology, paediatrics and more.</p>
    </div>
  </section>

  <div class="max-w-6xl mx-auto px-5 sm:px-8 py-10 sm:py-14">
%s
  </div>

  <!-- Profile dialog -->
  <dialog id="profile" class="team-dialog p-0 m-auto w-[calc(100%%-2rem)] max-w-3xl rounded-2xl bg-white text-ink shadow-[0_30px_80px_-20px_rgba(24,37,36,0.55)] backdrop:bg-ink/55 backdrop:backdrop-blur-sm" aria-labelledby="profileName">
    <div class="grid sm:grid-cols-[260px_1fr]">
      <div id="profilePhoto" class="aspect-square sm:aspect-auto sm:h-full bg-mint"></div>
      <div class="relative p-6 sm:p-8">
        <button type="button" id="profileClose" class="focus-ring absolute top-3 right-3 w-10 h-10 flex items-center justify-center rounded-full text-ink/55 hover:text-ink hover:bg-mint active:scale-95 transition-[transform,background-color,color] duration-200" aria-label="Close profile">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
        </button>
        <h2 id="profileName" class="font-display font-bold text-2xl sm:text-3xl tracking-tight text-ink pr-10"></h2>
        <p id="profileRole" class="text-teal700 font-medium mt-1"></p>
        <p id="profileBio" class="mt-5 text-ink/75 leading-relaxed"></p>
        <div class="mt-7 pt-5 border-t border-line flex flex-wrap gap-3">
          <a href="request-appointment.html" class="focus-ring spring inline-flex items-center rounded-full bg-teal700 hover:bg-teal600 hover:scale-[1.03] text-white font-medium text-[15px] px-5 py-2.5 transition-[transform,background-color] duration-300 active:scale-[0.97]">Request appointment</a>
          <a href="tel:0288599099" class="focus-ring spring inline-flex items-center rounded-full border border-teal700 text-teal900 hover:bg-mint hover:scale-[1.03] font-medium text-[15px] px-5 py-2.5 transition-[transform,background-color] duration-300 active:scale-[0.97]">Call (02) 8859 9099</a>
        </div>
      </div>
    </div>
  </dialog>
''' % '\n'.join(groups)

css = '''
  /* Team */
  .team-img { transition: transform .6s cubic-bezier(.22,1,.36,1); }
  .team-card:hover .team-img { transform: scale(1.04); }
  .team-dialog[open] { animation: dialogIn .35s cubic-bezier(.22,1,.36,1); }
  .team-dialog[open]::backdrop { animation: fadeIn .25s ease; }
  @keyframes dialogIn { from { opacity: 0; transform: translateY(14px) scale(.98); } to { opacity: 1; transform: none; } }
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
'''

js = '''  (function () {
    var dialog = document.getElementById('profile');
    if (!dialog || typeof dialog.showModal !== 'function') return;
    var photoEl = document.getElementById('profilePhoto');
    var lastCard = null;

    function open(card, push) {
      var d = card.dataset;
      document.getElementById('profileName').textContent = d.name;
      document.getElementById('profileRole').textContent = d.role;
      document.getElementById('profileBio').textContent = d.bio ||
        'A full profile for ' + d.name + ' is coming soon.';
      photoEl.innerHTML = '';
      if (d.photo) {
        var img = document.createElement('img');
        img.src = d.photo; img.alt = 'Portrait of ' + d.name;
        img.className = 'w-full h-full object-cover object-top';
        photoEl.appendChild(img);
        photoEl.className = 'aspect-square sm:aspect-auto sm:h-full bg-mint';
      } else {
        photoEl.className = 'aspect-square sm:aspect-auto sm:h-full bg-mint flex items-center justify-center';
        photoEl.innerHTML = '<span class="font-display font-bold text-6xl text-teal700">' + d.initials + '</span>';
      }
      lastCard = card;
      dialog.showModal();
      if (push && history.replaceState) history.replaceState(null, '', '#' + d.slug);
    }
    function close() { dialog.close(); }

    document.querySelectorAll('.team-card').forEach(function (card) {
      card.addEventListener('click', function () { open(card, true); });
    });
    document.getElementById('profileClose').addEventListener('click', close);
    // Click on the backdrop closes the dialog
    dialog.addEventListener('click', function (e) { if (e.target === dialog) close(); });
    dialog.addEventListener('close', function () {
      if (history.replaceState) history.replaceState(null, '', location.pathname);
      if (lastCard) lastCard.focus();
    });

    // Deep link: team.html#vijay-manivel opens that profile
    var hash = location.hash.slice(1);
    if (hash) {
      var target = document.getElementById(hash);
      if (target && target.classList.contains('team-card')) open(target, false);
    }
  })();
'''

build('team.html',
      'Our team — SWIFT Emergency &amp; Urgent Care, Rouse Hill',
      'Meet the emergency physicians and nurses at SWIFT Emergency &amp; Urgent Care in Rouse Hill, NSW.',
      main, active=None, css=css, js=js)
