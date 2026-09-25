---
last_mapped_commit: ea9307c55fb09b359776c6efecfdc084ee10a6a9
last_mapped_at: 2026-09-25
---
# Codebase Concerns

**Analysis Date:** 2026-09-25

## Tech Debt

**Monolithic HTML File:**

- Issue: All markup, styles, and JavaScript embedded in a single 1156-line `index.html` file with no build process or modularity
- Files: `index.html`
- Impact: Impossible to version, test, or reuse components; maintenance and scaling become exponentially harder as features are added; testing requires full page context
- Fix approach: Break into separate component files with a build system (Vite/Webpack), separate CSS/JS files, and a templating/build step

**Inline Tailwind CDN:**

- Issue: Tailwind CSS loaded from CDN on every page load instead of pre-built CSS; configuration defined in inline `<script>` tag
- Files: `index.html` (lines 19-44)
- Impact: Extra network request per page load; unused CSS classes still compiled on the client; custom color palette baked into HTML instead of CSS layer
- Fix approach: Use a build process to compile Tailwind at build time; eliminate the CDN dependency for production

**Inline JavaScript in HTML:**

- Issue: All JavaScript logic (scroll reveal, menu toggle, stepper, campaign switcher, viewport preview) embedded as IIFE functions inside `<script>` tags (lines 849-1153)
- Files: `index.html`
- Impact: No ability to minify, tree-shake, or code-split; difficult to debug and test in isolation; script dependencies hidden and fragile
- Fix approach: Extract to separate `.js` files; use module imports; set up a bundler

**Scattered Inline Styles:**

- Issue: 8 occurrences of inline `style=` attributes throughout `index.html` for animations, safe-area insets, and CSS Grid width calculations
- Files: `index.html` (lines 230, 300, 301, 318, 321, 324, 334, 979)
- Impact: Duplicated styling logic; difficult to maintain consistent design system; breaks CSS separation of concerns
- Fix approach: Move all styles to `<style>` block or external CSS; use Tailwind utility classes instead of inline styles

**No Testing Infrastructure:**

- Issue: `package.json` defines a test script that exits with error; no test files (`.test.ts`, `.spec.js`) found
- Files: `package.json` (line 7)
- Impact: No way to verify functionality, regressions, or edge cases; manual testing only; high risk for breaking changes
- Fix approach: Add testing framework (Vitest/Jest); write unit tests for JavaScript functions; add E2E tests for critical user flows

**Hard-Coded URLs to Old Site:**

- Issue: All navigation links point to `https://www.swiftemergencycare.com.au/` instead of local paths or the new site domain
- Files: `index.html` (lines 201, 222, 403, 489, 501, 509, 517, 525, 533, 541, 549, 569, 621, 692, 714)
- Impact: New site cannot function independently; all CTAs send users away to old site until URLs are manually updated before launch
- Fix approach: Replace all URLs with relative paths or environment-based configuration; use a config file or build-time substitution

**Data Hardcoded in JavaScript:**

- Issue: Visit stepper steps (line 921-936), campaign configurations (line 1008-1045), and viewport sizes (line 1111-1114) hardcoded as arrays in script
- Files: `index.html`
- Impact: Cannot update content without editing HTML; no CMS integration possible; dynamic content requires code changes
- Fix approach: Move to JSON config files or API endpoints; load data at runtime

## Known Bugs

**Scroll-to-Top Anchor Issue (FIXED - commit dd3a4c0):**

- Symptoms: Smooth scroll to `#top` may be affected by sticky headers
- Files: `index.html` (line 170 `<div id="top"></div>`)
- Trigger: Clicking header logo to return to top
- Status: Addressed in commit dd3a4c0, but monitor for regression

**Mobile Menu Overflow Handling:**

- Problem: `document.body.style.overflow = 'hidden'` is applied to prevent scroll when mobile menu or modal is open, but this is cleared without tracking state
- Files: `index.html` (lines 1085, 1089, 1130, 1136)
- Trigger: Open mobile menu, then open modal, close menu — scroll state may be incorrectly restored
- Workaround: Users can manually scroll; not critical UX issue
- Fix approach: Implement a stack-based overflow state manager (increment/decrement counter instead of toggle)

**Viewport Preview Self-Check Fragile:**

- Problem: Code checks `window.top !== window.self` to detect if running inside an iframe and disable the viewport switcher
- Files: `index.html` (line 1102)
- Cause: Unreliable cross-origin iframe detection; can break if viewport preview iframe uses `sandbox` attribute
- Risk: Preview tool may not work correctly in all hosting scenarios
- Improvement path: Use feature detection or explicit parent-child messaging instead of frame detection

**Campaign Modal Missing Keyboard Trap:**

- Problem: Modal doesn't trap focus (Escape key closes it, but no focus management on open/close)
- Files: `index.html` (lines 1083-1097)
- Cause: JavaScript only manages visibility, not focus cycling
- Risk: Keyboard-only users can tab outside modal to background content
- Improvement path: Implement FocusTrap library or manual focus management

## Security Considerations

**Google Analytics Placeholder Not Configured:**

- Risk: `G-XXXXXXXXXX` placeholder left in production code; analytics will not work on launch
- Files: `index.html` (lines 46-52)
- Current mitigation: None — this is a pre-launch blocker
- Recommendations: Replace placeholder before deploying; automate via environment variable or build-time substitution to prevent re-occurrence

**External CDN Dependencies:**

- Risk: Dependency on `https://cdn.tailwindcss.com` and Google Fonts CDN; if CDN is unavailable, site styling breaks; CDN compromise could inject malicious CSS
- Files: `index.html` (lines 15-17, 19)
- Current mitigation: None
- Recommendations: 
  - For production: self-host Tailwind pre-built CSS and fonts
  - Add fallback fonts in `font-family` stack
  - Consider using `integrity` attributes or CSP (Content Security Policy) headers to pin dependencies

**Missing Open Graph Image:**

- Risk: Social sharing will not display preview image; no `og:image` meta tag defined
- Files: `index.html` (lines 10-13)
- Current mitigation: None
- Recommendations: Add `og:image` with absolute URL to social preview image

**Embedded gtag Script Allows Arbitrary Config:**

- Risk: If someone modifies the config object, tracking data could be sent to wrong account
- Files: `index.html` (lines 48-52)
- Current mitigation: Hardcoded config, but placeholder makes this moot
- Recommendations: Once GA4 ID is configured, consider separating gtag initialization into a separate config file

## Performance Bottlenecks

**Tailwind CDN On Every Page Load:**

- Problem: CSS is compiled on every request, not cached; ~50KB+ of unused Tailwind utilities sent to browser
- Files: `index.html` (line 19)
- Cause: CDN-based approach compiles full Tailwind framework including all variants
- Metrics: Adds ~200-400ms to initial page load; blocks rendering until script executes
- Improvement path:
  1. Build Tailwind CSS offline using `tailwindcss` CLI
  2. Use purge/content config to remove unused classes (should reduce to ~10-15KB)
  3. Minify and gzip
  4. Serve as static asset with long cache headers
  5. Measure: aim for <50ms CSS parse time

**Large Image Assets Without Optimization:**

- Problem: JPEG images in `brand_assets/` are not optimized; some exceed 160KB
- Files: `brand_assets/*.jpeg`, `brand_assets/*.jpg` (e.g., `clinic-reception.jpg` 165KB, `Arrive.jpeg` 91KB)
- Cause: Original uncompressed exports from design tool
- Metrics: Total image payload ~1.3MB; uncompressed
- Improvement path:
  1. Compress using ImageOptim or similar (target 60% reduction)
  2. Generate WebP variants for modern browsers
  3. Implement lazy loading with `loading="lazy"` on below-fold images
  4. Consider responsive image variants for mobile (smaller dimensions)
  5. Use CDN with automatic image optimization (Cloudflare, Imgix)

**No Asset Versioning / Cache Busting:**

- Problem: Images and assets loaded with no version querystring; browsers cache indefinitely, updates won't reflect without hard refresh
- Files: All `brand_assets/` references in `index.html`
- Cause: Static file server doesn't set cache headers; no build process to add hashes
- Impact: Users may see stale images for days after updates
- Improvement path: Add hash-based versioning in build step (e.g., `Arrive-a3c5f2.jpeg`) and update references

**Blocking Google Fonts Request:**

- Problem: Google Fonts CSS loaded synchronously in `<head>`; blocks page render
- Files: `index.html` (line 17)
- Cause: Synchronous stylesheet link without `async` or resource hints
- Impact: Adds ~50-100ms to First Contentful Paint (FCP) on slower networks
- Improvement path: Use `rel="preload"` with async loading; or self-host fonts

## Fragile Areas

**Mobile Menu State Management:**

- Files: `index.html` (lines 888-918)
- Why fragile: Menu state tracked only via class names and `aria-expanded` attributes; no internal state object; multiple buttons (`#menuBtn` and `#bottomMenuBtn`) must stay synchronized
- Safe modification: Refactor into a stateful class or useReducer-style pattern; test that opening from one button and closing from another stays in sync
- Test coverage: No unit tests; manual verification only

**Visit Stepper Data Binding:**

- Files: `index.html` (lines 920-1005)
- Why fragile: Steps array is tightly coupled to DOM structure; changing step count requires updating HTML node selectors and array length; no schema validation
- Safe modification: 
  1. Create a test that verifies number of `.visit-node` elements matches steps array
  2. Add data attributes to link DOM to data (`data-step-id`)
  3. Refactor step rendering to be data-driven rather than DOM-driven
- Test coverage: No validation that steps array length matches DOM nodes

**Campaign Preview Modal:**

- Files: `index.html` (lines 1007-1098)
- Why fragile: Dynamically creates buttons in JavaScript from hardcoded campaigns array; HTML selectors must match exact IDs; no validation
- Safe modification: Add `data-campaign-id` attributes to generated buttons; test that modal title/description updates match selected campaign
- Test coverage: None

**Viewport Size Constants:**

- Files: `index.html` (lines 1111-1114)
- Why fragile: Hardcoded viewport sizes (768px tablet, 390px mobile) don't match actual device breakpoints or Tailwind config; if design changes, these must be updated in three places (here, Tailwind config in line 21-44, and CSS media queries)
- Safe modification: Define breakpoints in a single source of truth (JSON config or CSS custom properties)
- Test coverage: No automated tests verify breakpoints work correctly

**Intl.DateTimeFormat Timezone Lookup:**

- Files: `index.html` (lines 856-859)
- Why fragile: Uses unsupported features fallback with try/catch; if timezone lookup fails silently, status shows "Closed" even when open
- Safe modification: Add logging to detect fallback; consider server-side rendering of open/closed status
- Test coverage: No tests for timezone edge cases (e.g., DST transitions)

## Scaling Limits

**Single HTML File Approach:**

- Current capacity: ~1200 lines works for a single homepage
- Limit: Adding new sections/features makes file unmanageable at ~2000+ lines; performance degrades with inline scripts
- Scaling path: Migrate to component-based architecture with build system before adding more features

**No Database or CMS Integration:**

- Current capacity: All content hardcoded in HTML/JS; works for static sites
- Limit: Cannot scale to multi-page site, user-generated content, or dynamic data
- Scaling path: Add headless CMS (Contentful, Sanity) or backend API if patient booking, testimonials, or dynamic content needed

**Inline JavaScript Performance:**

- Current capacity: ~300 lines of JavaScript acceptable for homepage
- Limit: Adding more interactivity (real-time booking, live chat, dynamic forms) will bloat single file and increase parse time
- Scaling path: Extract to separate modules; implement code splitting; lazy-load non-critical features

## Dependencies at Risk

**Tailwind CDN (Production Risk):**

- Risk: External dependency; if CDN unreachable, site is unstyled
- Impact: Site unusable without CDN or fallback CSS
- Migration plan: Build Tailwind locally; serve as static CSS file; remove CDN dependency

**Google Fonts (Non-Critical):**

- Risk: External dependency; fallback fonts available (sans-serif)
- Impact: Typography changes if Google Fonts unavailable; FOUT (flash of unstyled text)
- Migration plan: Self-host fonts or use system fonts; preload in `<head>`

**Puppeteer Dependency in Package.json:**

- Risk: Puppeteer installs full Chromium binary (~150MB) on `npm install`; may fail in CI/CD without proper setup
- Impact: Slow installs; large node_modules; unnecessary for production deployment
- Migration plan: Move to dev-only dependency; separate screenshot tooling from app deployment

## Missing Critical Features

**Build/Deployment Process:**

- Problem: No `npm run build` command; no minification, bundling, or asset pipeline
- Blocks: Cannot deploy to production; no version control of assets; no CI/CD pipeline possible
- Solution: Set up build tool (Vite, Parcel, or custom Node script)

**Analytics Configuration:**

- Problem: GA4 Measurement ID is placeholder `G-XXXXXXXXXX`
- Blocks: No usage analytics; cannot measure traffic, user behavior, or conversion
- Solution: Replace with real GA4 ID before launch; set up GA4 property

**Live ED Wait Time Data Source:**

- Problem: "Weighing up where to go?" section shows sample data; no real NSW Health API integration
- Blocks: Feature is misleading until real data is connected
- Solution: Identify data source (NSW Health API or manual updates); build API integration; test data freshness

**Dynamic Booking System:**

- Problem: "Request appointment" links point to old site's booking system
- Blocks: Cannot accept appointments through new site
- Solution: Integrate real appointment system (own or third-party like HubSpot, Calendly); or direct to new booking page once built

## Test Coverage Gaps

**No Unit Tests:**

- What's not tested: All JavaScript functions (scroll reveal, menu toggle, stepper navigation, modal handling, timezone detection)
- Files: `index.html` (lines 849-1153)
- Risk: Refactoring or bug fixes may introduce regressions; no regression suite to catch edge cases
- Priority: High — at least 50% code coverage required before major updates

**No E2E Tests:**

- What's not tested: Full user flows (navigate menu, open triage, view services, request appointment, view location)
- Files: `index.html` (full page)
- Risk: UI bugs may go unnoticed until reported by users; responsive design not validated
- Priority: High — add critical path E2E tests (booking flow, emergency info prominence)

**No Accessibility Tests:**

- What's not tested: Screen reader support, keyboard navigation, color contrast, ARIA labels
- Files: `index.html`
- Risk: Clinic may violate accessibility laws (AODA, ADA, WCAG); patients with disabilities cannot access services
- Priority: Critical — add axe-core accessibility audits; test with screen readers

**No Visual Regression Tests:**

- What's not tested: Responsive design, cross-browser rendering, animation smoothness
- Files: Screenshot tools (`screenshot.mjs`, `mobile_shot.mjs`) are manual-only
- Risk: Visual bugs introduced silently; no automated detection of layout shifts, color changes, or spacing regressions
- Priority: Medium — set up Percy or similar visual testing service

**No Performance Tests:**

- What's not tested: Load time, Core Web Vitals, Lighthouse scores
- Files: All
- Risk: Performance degrades silently; users on slow connections have poor experience
- Priority: Medium — add Lighthouse CI; set performance budgets (CLS <0.1, LCP <2.5s)

**No Mobile/Tablet Testing:**

- What's not tested: Actual device testing; only viewport preview tool
- Files: `index.html` (viewport switcher); `mobile_shot.mjs`
- Risk: Layout breaks on specific device sizes; touch interactions untested
- Priority: Medium — add device lab testing or BrowserStack integration

## Additional Concerns

**Inconsistent Screenshot Tool Scripts:**

- Problem: `screenshot.mjs` and `mobile_shot.mjs` have different code styles and path handling
- Files: `screenshot.mjs` (uses `path.join`, proper error handling) vs `mobile_shot.mjs` (hardcoded string paths, no error handling)
- Impact: Inconsistent developer experience; `mobile_shot.mjs` may fail silently
- Fix: Unify both scripts; add proper error handling and logging to both

**Missing Error Boundaries:**

- Problem: JavaScript has try/catch only in timezone detection (line 855-869); other functions will throw uncaught errors
- Files: `index.html` (lines 888-1152)
- Impact: One JavaScript error can break the entire page
- Fix approach: Wrap IIFE functions with error logging; add global error handler

**No Environment Configuration:**

- Problem: All configuration hardcoded (GA4 ID, URLs, data); no way to use different values for staging/production
- Files: `index.html`
- Impact: Cannot deploy same build to multiple environments; risks pushing wrong IDs/URLs to production
- Fix approach: Use environment variables and build-time substitution

**No README for Demo/Debug Features:**

- Problem: Campaign preview and viewport switcher are "demo-only" but not documented; hidden in comments
- Files: `index.html` (lines 251, 275)
- Impact: Developers don't know these exist; they may be forgotten before launch and left in production
- Fix approach: Add launch checklist to CLAUDE.md and README; mark demo features with `data-demo="true"` for easy removal

---

*Concerns audit: 2026-09-25*
