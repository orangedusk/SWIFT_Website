---
last_mapped_commit: ea9307c55fb09b359776c6efecfdc084ee10a6a9
last_mapped_at: 2026-09-25
---
# Testing Patterns

**Analysis Date:** 2026-09-25

## Test Framework

**No automated test framework installed.**

`package.json` shows:

```json
"scripts": {
  "test": "echo \"Error: no test specified\" && exit 1"
}
```

**Testing is manual and visual only** — using Puppeteer for screenshot comparison against reference designs.

## Manual Testing Approach

**Screenshot-based verification workflow (defined in CLAUDE.md):**

1. **Start local server:**
   ```bash
   node serve.mjs
   ```
   Serves project root at `http://localhost:3000` on port 3000.

2. **Take screenshots:**
   ```bash
   node screenshot.mjs http://localhost:3000 [label]     # Desktop
   node mobile_shot.mjs http://localhost:3000 [label]     # Mobile
   ```

3. **Compare visually:**
   - Screenshots saved to `./temporary screenshots/` (git-ignored)
   - Files auto-numbered: `screenshot-1.png`, `screenshot-2.png`, etc.
   - Optional label suffix for organization: `screenshot-N-label.png`

4. **Verification checklist:**
   - Spacing/padding matches reference (pixel-perfect)
   - Font size/weight/line-height correct
   - Colors exact (hex values)
   - Alignment (flexbox/grid)
   - Border radius, shadows
   - Image sizing and positioning
   - Responsive breakpoints

## Screenshot Tooling

**`screenshot.mjs` — Desktop screenshots**

```javascript
const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });
await page.goto(url, { waitUntil: 'networkidle0' });
await page.screenshot({ path: outPath, fullPage: true });
```

- Viewport: 1440px × 900px (desktop)
- Waits for network idle before capture
- Full page screenshot (scrolls to capture entire page)
- Saves to `temporary screenshots/screenshot-N.png`

**`mobile_shot.mjs` — Mobile screenshots**

```javascript
await page.setViewport({ width: 390, height: 844, isMobile: true, deviceScaleFactor: 2 });
await page.goto(url, { waitUntil: 'networkidle0' });
await page.screenshot({ path: `${OUT_DIR}/mobile-${label}.png`, fullPage: true });
```

- Viewport: 390px × 844px (iPhone SE/13 mini size)
- Mobile user agent enabled
- Device pixel ratio 2 (retina)
- Full page screenshot
- Saves to `temporary screenshots/mobile-{label}.png`

**`serve.mjs` — Local static file server**

Handles MIME types for all assets:

- HTML, CSS, JavaScript
- Images (PNG, JPG, GIF, WebP, SVG)
- Fonts (WOFF, WOFF2)
- Redirects directories to `index.html`

## Comparison Workflow

**Per CLAUDE.md:**

1. **Screenshot existing state:**
   ```bash
   node screenshot.mjs http://localhost:3000 before
   ```

2. **Make changes to `index.html`**

3. **Screenshot new state:**
   ```bash
   node screenshot.mjs http://localhost:3000 after
   ```

4. **Read screenshots with Claude's image analysis tool:**
   - Opens `temporary screenshots/screenshot-N.png`
   - Compares layout, spacing, colors, typography

5. **Iterate until no visible differences remain:**
   - Re-screenshot after each fix
   - Minimum 2 comparison rounds required

**Key rule:** Always screenshot from `localhost` (never `file://` URLs) to ensure CSS/fonts load correctly.

## Interaction Testing

**Manual browser testing required for:**

**Mobile menu:**

- Click menu button → menu opens
- Click menu link → menu closes
- Press Escape → menu closes
- Verify `aria-expanded` toggles

**Stepper (visit timeline):**

- Click numbered step buttons → content updates
- Click prev/next buttons → step changes
- Previous button disabled on step 1
- Verify `aria-current="step"` on active step
- Content fades out/in during transition

**Triage details:**

- Click summary → details expand
- Chevron rotates 90°
- Click again → details collapse
- Answer text animates in/out

**FAQ accordion:**

- Click question → answer reveals
- Plus icon rotates 45° when open
- Click again → collapses

**Campaign preview (demo only):**

- Click "Preview campaigns" button → modal opens
- Click campaign → hero updates (image, headline, subhead, CTA)
- Modal backdrop click → closes
- Escape key → closes

**Viewport switcher (demo only, desktop only):**

- Click Desktop/Tablet/Mobile → viewport preview changes
- Tablet/Mobile opens iframe with correct dimensions
- Escape key returns to desktop view
- Inside iframe, switcher hidden (no infinite recursion)

**Open status indicator:**

- Updates based on Sydney timezone
- Green dot + "Open now" during 10am–10pm
- Gray dot + "Closed" outside hours
- Ping animation only when open

## Coverage Analysis

**Current state:** No automated coverage measurement.

**Manual coverage approach:**

- Visual testing: all interactive components tested in browser
- Responsive testing: desktop (1440px), tablet (768px), mobile (390px)
- Browser testing: assumed modern Chrome/Safari/Firefox
- Accessibility testing: keyboard navigation, screen reader compatibility (manual or via aXe DevTools)

**Untested areas (no automated tests):**

- User interactions in older browsers (IE11, etc.)
- Touch interactions on mobile devices (only viewport simulation)
- Offline functionality (service worker not implemented)
- Performance under network throttling
- Timezone edge cases (only Sydney timezone verified)

## Test Data

No test fixtures or factories used. All data hardcoded in JavaScript:

**Stepper steps:**

```javascript
var steps = [
  { title: 'Arrive', desc: "...", tip: "...", image: '...', pos: '75% 35%' },
  // ... 7 steps total
];
```

**Campaign previews:**

```javascript
var campaigns = [
  { id: 'default', label: 'Everyday care', desc: '...', swatch: '#2C685E', image: '...', ... },
  { id: 'flu', label: 'Flu shot season', ... },
  { id: 'kids', label: 'School holidays', ... },
];
```

**No database or API calls** — all data embedded in markup or JavaScript.

## Browser Support

Inferred from ES5 JavaScript patterns and feature detection:

**Required:**

- ES5 JavaScript support
- DOM API (querySelector, classList, addEventListener)
- CSS Flexbox and Grid
- Tailwind CSS (CDN)

**Feature detection used:**

- `IntersectionObserver` check — fallback to immediate reveal if unavailable
- `Intl.DateTimeFormat` check — fallback to static text if timezone lookup fails
- Frame detection (`window.top !== window.self`) — disable viewport switcher in iframe

**No transpilation** — code is ES5-compatible as-written.

## Known Testing Gaps

**Gaps identified during analysis:**

1. **No unit tests for JavaScript logic**
   - Stepper state transitions
   - Menu toggle logic
   - Campaign preview updates
   - Timezone calculations

2. **No integration tests**
   - Multi-step interactions (open menu, click link, verify content)
   - State persistence across interactions

3. **No accessibility automated testing**
   - aXe, WAVE, or Lighthouse not integrated
   - ARIA attributes verified manually only

4. **No performance testing**
   - Lighthouse scores not measured
   - Animation frame rates not verified
   - Image optimization not tested

5. **No cross-browser testing**
   - Only desktop viewport sizes tested
   - Mobile browser variations (iOS Safari, Android Chrome) not verified
   - Older browser fallbacks not tested (IE11, etc.)

6. **No end-to-end tests**
   - External links not verified (request-appointment, Google Maps, etc.)
   - Analytics tracking not tested
   - Schema.org structured data not validated

## Workflow Notes

**Setup for testing:**

1. **Install Node.js 18+**
2. **Install Puppeteer:**
   ```bash
   npm install
   ```
   Puppeteer binary cached at `~/.cache/puppeteer/` on macOS
3. **Start server in background:**
   ```bash
   node serve.mjs &
   ```
4. **Run screenshot comparison:**
   ```bash
   node screenshot.mjs http://localhost:3000 test-name
   ```

**Before committing:**

- Screenshot desktop version
- Screenshot mobile version
- Compare against reference design (via visual inspection or reference image overlay)
- Verify no visual regressions on any breakpoint

---

*Testing analysis: 2026-09-25*
