import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from build_page import build, ROOT

CARD = 'bg-white rounded-2xl border border-line shadow-[0_2px_10px_-4px_rgba(30,69,63,0.15)]'
BULK = '<span class="inline-flex rounded-full bg-mint text-teal900 text-sm font-medium px-3 py-1">Bulk-billed</span>'
EXTRA = '<span class="text-[15px] text-ink/70">Extra charges</span>'

def price(amount, medicare=True):
    tail = ' <span class="block sm:inline text-sm font-normal text-ink/55">+ Medicare</span>' if medicare else ''
    return '<span class="font-display font-bold text-lg text-ink tabular-nums">' + amount + '</span>' + tail

def rows(items):
    out = []
    for i, (label, sub, cost) in enumerate(items):
        border = '' if i == len(items) - 1 else ' border-b border-line'
        subhtml = '<span class="block text-sm text-ink/55 mt-0.5">' + sub + '</span>' if sub else ''
        out.append('          <tr class="align-top' + border + '">\n'
                   '            <th scope="row" class="text-left font-normal py-4 pr-4"><span class="text-[15px] text-ink">' + label + '</span>' + subhtml + '</th>\n'
                   '            <td class="text-right py-4 whitespace-nowrap">' + cost + '</td>\n          </tr>')
    return '\n'.join(out)

def table(tid, heading, intro, items, caption):
    return '''
      <section id="%s" class="scroll-mt-[125px] sm:scroll-mt-[129px]">
        <h2 class="font-display font-bold text-xl sm:text-2xl tracking-tight text-ink">%s</h2>
        %s
        <div class="mt-4 %s px-5 sm:px-6">
          <table class="w-full">
            <caption class="sr-only">%s</caption>
            <thead><tr class="border-b border-line text-sm text-ink/50"><th scope="col" class="text-left font-normal py-3">Service</th><th scope="col" class="text-right font-normal py-3">Cost</th></tr></thead>
            <tbody>
%s
            </tbody>
          </table>
        </div>
      </section>''' % (tid, heading, ('<p class="text-ink/60 mt-1">' + intro + '</p>') if intro else '', CARD, caption, rows(items))

emergency = table('emergency', 'Emergency &amp; urgent care', 'Walk-in visits for illness and injury.', [
    ('First visit', 'SWIFT facility fee', price('$396')),
    ('Return visit for the same issue', 'Within 24 hours', BULK),
    ('Return visit for the same issue', '2 to 7 days later', price('$150')),
], 'Emergency and urgent care fees')

infusion = table('infusion', 'Infusion clinic', 'By appointment.', [
    ('Iron infusion', 'You bring your own Ferinject or iron medicine', price('$246')),
    ('Iron infusion', 'We supply Ferinject 1g for $77', price('$246 + $77')),
    ('IV antibiotics', 'After a SWIFT consultation, or prescribed by your GP', price('$150')),
    ('Other infusions', None, '<a href="tel:0288599099" class="focus-ring rounded text-[15px] font-medium text-teal700 hover:text-teal900 underline underline-offset-2 decoration-teal500/40 hover:decoration-teal700">Call us</a>'),
], 'Infusion clinic fees')

wound = table('wound', 'Wound care clinic', None, [
    ('Simple wound care or dressing', None, price('$80')),
    ('Complex wound care or dressing', None, price('$140')),
    ('Stitches removal', None, price('$80')),
], 'Wound care clinic fees')

radiology = '''
      <section id="radiology" class="scroll-mt-[125px] sm:scroll-mt-[129px]">
        <h2 class="font-display font-bold text-xl sm:text-2xl tracking-tight text-ink">Scans and imaging</h2>
        <p class="text-ink/60 mt-1">Provided on-site by Imaging Specialists, an independent practice. Questions about scans: <a href="tel:0286148400" class="focus-ring rounded font-medium text-teal700 hover:text-teal900">(02) 8614 8400</a>.</p>
        <div class="mt-4 %s px-5 sm:px-6">
          <table class="w-full">
            <caption class="sr-only">Radiology hours and fees for patients with Medicare</caption>
            <thead><tr class="border-b border-line text-sm text-ink/50"><th scope="col" class="text-left font-normal py-3">Scan and hours</th><th scope="col" class="text-right font-normal py-3">With Medicare</th></tr></thead>
            <tbody>
%s
            </tbody>
          </table>
        </div>
        <p class="mt-3 text-sm text-ink/60">Without Medicare, extra charges apply to all scans. These fees apply to patients seen at SWIFT.</p>
      </section>''' % (CARD, rows([
    ('X-ray and CT', 'Every day, 10am to 9pm', BULK),
    ('Ultrasound', 'Monday to Friday, 10am to 5pm', BULK),
    ('Ultrasound, after hours', 'Monday to Friday, 5pm to 8pm', EXTRA),
    ('Ultrasound, weekends', 'Saturday and Sunday, subject to availability', EXTRA),
    ('MRI', 'Subject to availability', EXTRA),
]))

main = '''
  <!-- Page intro -->
  <section class="bg-mint/60 border-b border-line">
    <div class="max-w-6xl mx-auto px-5 sm:px-8 pt-8 sm:pt-12 pb-10 sm:pb-14">
      <nav aria-label="Breadcrumb" class="hero-in text-sm text-ink/55 mb-5" style="animation-delay:.02s">
        <a href="index.html" class="hover:text-teal700 focus-ring rounded">Home</a>
        <span aria-hidden="true" class="mx-1.5">/</span>
        <span class="text-ink/80" aria-current="page">Fees</span>
      </nav>
      <div class="grid lg:grid-cols-[1fr_auto] gap-8 lg:gap-12 items-end">
        <div>
          <h1 class="hero-in font-display font-extrabold text-[2.25rem] leading-[1.05] sm:text-5xl sm:leading-[1.05] tracking-tight text-ink" style="animation-delay:.08s">Fees</h1>
          <p class="hero-in mt-4 text-lg text-ink/70 leading-relaxed max-w-xl" style="animation-delay:.2s">What you'll pay at SWIFT, with or without a Medicare card. No referral needed.</p>
        </div>
        <!-- Headline fee -->
        <div class="hero-in relative overflow-hidden %s p-6 sm:p-7 lg:w-[380px]" style="animation-delay:.3s">
          <svg class="absolute -right-5 -top-5 w-28 h-28 text-teal900/[0.07]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="0.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 2.5h10v19l-2.5-1.5-2 1.5-2-1.5-2.5 1.5V2.5Z"/><path d="M9.5 8h5M9.5 11.5h5M9.5 15h3"/></svg>
          <p class="relative text-sm text-ink/55">Walk-in visit, facility fee</p>
          <p class="relative font-display font-extrabold text-5xl tracking-tight text-ink mt-1">$396</p>
          <p class="relative text-sm text-ink/55 mt-1">plus standard Medicare charges</p>
        </div>
      </div>
    </div>
  </section>

  <section class="max-w-6xl mx-auto px-5 sm:px-8 py-10 sm:py-14">
    <div class="grid lg:grid-cols-[200px_1fr] gap-8 lg:gap-12 items-start">

      <!-- Jump menu -->
      <nav aria-label="On this page" class="lg:sticky lg:top-[132px] -mx-5 px-5 lg:mx-0 lg:px-0 overflow-x-auto">
        <ul class="flex lg:flex-col gap-2 lg:gap-1 text-[15px] whitespace-nowrap pb-1">
          <li><a href="#medicare" class="jump-link focus-ring block rounded-full lg:rounded-lg border border-line lg:border-0 bg-white lg:bg-transparent px-4 lg:px-3 py-1.5 lg:py-2 text-ink/70 hover:text-teal700 hover:bg-mint active:scale-[0.97] transition-[transform,background-color,color] duration-200">Medicare</a></li>
          <li><a href="#emergency" class="jump-link focus-ring block rounded-full lg:rounded-lg border border-line lg:border-0 bg-white lg:bg-transparent px-4 lg:px-3 py-1.5 lg:py-2 text-ink/70 hover:text-teal700 hover:bg-mint active:scale-[0.97] transition-[transform,background-color,color] duration-200">Urgent care</a></li>
          <li><a href="#infusion" class="jump-link focus-ring block rounded-full lg:rounded-lg border border-line lg:border-0 bg-white lg:bg-transparent px-4 lg:px-3 py-1.5 lg:py-2 text-ink/70 hover:text-teal700 hover:bg-mint active:scale-[0.97] transition-[transform,background-color,color] duration-200">Infusions</a></li>
          <li><a href="#wound" class="jump-link focus-ring block rounded-full lg:rounded-lg border border-line lg:border-0 bg-white lg:bg-transparent px-4 lg:px-3 py-1.5 lg:py-2 text-ink/70 hover:text-teal700 hover:bg-mint active:scale-[0.97] transition-[transform,background-color,color] duration-200">Wound care</a></li>
          <li><a href="#radiology" class="jump-link focus-ring block rounded-full lg:rounded-lg border border-line lg:border-0 bg-white lg:bg-transparent px-4 lg:px-3 py-1.5 lg:py-2 text-ink/70 hover:text-teal700 hover:bg-mint active:scale-[0.97] transition-[transform,background-color,color] duration-200">Scans</a></li>
          <li><a href="#extras" class="jump-link focus-ring block rounded-full lg:rounded-lg border border-line lg:border-0 bg-white lg:bg-transparent px-4 lg:px-3 py-1.5 lg:py-2 text-ink/70 hover:text-teal700 hover:bg-mint active:scale-[0.97] transition-[transform,background-color,color] duration-200">Other costs</a></li>
        </ul>
      </nav>

      <div class="space-y-12 max-w-3xl">

      <!-- Medicare -->
      <section id="medicare" class="scroll-mt-[125px] sm:scroll-mt-[129px]">
        <h2 class="font-display font-bold text-xl sm:text-2xl tracking-tight text-ink">How Medicare works at SWIFT</h2>
        <div class="mt-4 grid sm:grid-cols-2 gap-4">
          <div class="flex gap-3 %s p-5">
            <div class="w-9 h-9 rounded-lg bg-mint flex items-center justify-center shrink-0">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 12.5l5 5L20 7" stroke="#2C685E" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </div>
            <div>
              <p class="font-medium text-ink">With a valid Medicare card</p>
              <p class="text-sm text-ink/65 mt-1 leading-relaxed">You get the Medicare part of your fee back. The facility fee is not covered.</p>
            </div>
          </div>
          <div class="flex gap-3 %s p-5">
            <div class="w-9 h-9 rounded-lg bg-mint flex items-center justify-center shrink-0">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="8.5" stroke="#2C685E" stroke-width="1.6"/><path d="M9.5 9.5l5 5m0-5l-5 5" stroke="#2C685E" stroke-width="1.6" stroke-linecap="round"/></svg>
            </div>
            <div>
              <p class="font-medium text-ink">Without a Medicare card</p>
              <p class="text-sm text-ink/65 mt-1 leading-relaxed">You pay the full fee on the day: the SWIFT fee plus the Medicare-equivalent charges.</p>
            </div>
          </div>
        </div>
      </section>
%s
%s
%s
%s

      <!-- Other costs -->
      <section id="extras" class="scroll-mt-[125px] sm:scroll-mt-[129px]">
        <h2 class="font-display font-bold text-xl sm:text-2xl tracking-tight text-ink">Other costs</h2>
        <p class="text-ink/70 mt-2 leading-relaxed">Depending on your treatment, you may need items like crutches or a moon boot. These cost extra.</p>
      </section>

      <!-- Questions -->
      <div class="rounded-2xl bg-teal900 text-white p-6 sm:p-8 flex flex-col sm:flex-row sm:items-center gap-5 justify-between shadow-[0_24px_48px_-24px_rgba(30,69,63,0.6)]">
        <div>
          <p class="font-display font-bold text-xl">Questions about fees?</p>
          <p class="text-white/75 mt-1">Call us before you come in and we'll talk you through it.</p>
        </div>
        <a href="tel:0288599099" class="focus-ring spring shrink-0 inline-flex items-center justify-center rounded-full bg-white text-teal900 hover:bg-mint hover:scale-[1.03] font-medium px-6 py-3 transition-[transform,background-color] duration-300 active:scale-[0.97]">Call (02) 8859 9099</a>
      </div>

      </div>
    </div>
  </section>
''' % (CARD, CARD, CARD, emergency, infusion, wound, radiology)

build('fees.html',
      'Fees — SWIFT Emergency &amp; Urgent Care, Rouse Hill',
      'SWIFT fees for urgent care, infusions, wound care and on-site imaging, with and without Medicare. Walk-in facility fee $396 plus Medicare charges.',
      main, active='fees.html')
