"""Wrap a page's <main> content in the site chrome taken from request-appointment.html."""
import os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '')
src = open(ROOT + 'request-appointment.html').read()

def between(a, b, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

head = src[:src.index('  /* Service picker tiles */')]
chrome = between('<body', '<main>')
footer = between('<!-- Footer -->', '</footer>', incl_b=True)
menu_js = between('  (function () {\n    var btn = document.getElementById(\'menuBtn\');', '  })();', incl_b=True)

REQ_BTN = '''      <a href="request-appointment.html" class="hidden sm:inline-flex focus-ring items-center rounded-full bg-teal700 hover:bg-teal600 text-white text-sm font-medium px-4 py-2 sm:px-5 sm:py-2.5 transition-colors active:scale-[0.97]">
        Request appointment
      </a>
      <button id="menuBtn"'''
REQ_BTN_MOBILE = '''<a href="tel:0288599099" class="mobile-link font-medium text-teal900">(02) 8859 9099</a>
          <a href="request-appointment.html" class="mobile-link focus-ring inline-flex items-center justify-center rounded-full bg-teal700 hover:bg-teal600 text-white text-sm font-medium px-5 py-2.5 transition-colors active:scale-[0.97]">Request appointment</a>'''

def site_links(html):
    return (html.replace('index.html#services"', 'services.html"')
                .replace('index.html#fees"', 'fees.html"'))

def build(filename, title, desc, main, active=None, css='', js=''):
    h = head
    h = re.sub(r'<title>.*?</title>', '<title>' + title + '</title>', h)
    h = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="' + desc + '">', h)
    h = re.sub(r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="' + title.replace('&amp;', '&') + '">', h)
    h = re.sub(r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="' + desc + '">', h)
    c = chrome.replace('      <button id="menuBtn"', REQ_BTN, 1)
    c = c.replace('<a href="tel:0288599099" class="mobile-link font-medium text-teal900">(02) 8859 9099</a>', REQ_BTN_MOBILE, 1)
    c, f = site_links(c), site_links(footer)
    if 'team.html' not in f:
        f = f.replace('<li><a href="fees.html" class="hover:text-white focus-ring rounded">Fees</a></li>',
                  '<li><a href="fees.html" class="hover:text-white focus-ring rounded">Fees</a></li>\n        <li><a href="team.html" class="hover:text-white focus-ring rounded">Our team</a></li>')
    if active:
        # Mark the current page in the header and mobile menu
        c = c.replace('<a href="%s" class="hover:text-teal700' % active, '<a href="%s" aria-current="page" class="text-teal700 font-medium hover:text-teal900' % active)
        c = c.replace('<a href="%s" class="mobile-link py-2.5 hover:text-teal700' % active, '<a href="%s" aria-current="page" class="mobile-link py-2.5 text-teal700 font-medium hover:text-teal900' % active)
    out = (h + css + '</style>\n</head>\n\n' + c + '<main>\n' + main + '\n</main>\n\n' + f +
           '\n\n<script>\n' + menu_js + '\n' + js + '\n</script>\n</body>\n</html>\n')
    open(ROOT + filename, 'w').write(out)
    print('wrote', filename, len(out), 'bytes')
