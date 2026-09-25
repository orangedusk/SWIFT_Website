---
last_mapped_commit: ea9307c55fb09b359776c6efecfdc084ee10a6a9
last_mapped_at: 2026-09-25
---
# Coding Conventions

**Analysis Date:** 2026-09-25

## Naming Patterns

**Files:**

- Single file architecture: `index.html` contains all markup, styles, and scripts
- Utility scripts use camelCase with `.mjs` extension: `serve.mjs`, `screenshot.mjs`, `mobile_shot.mjs`
- Brand assets use descriptive kebab-case: `hero-doctor-patient.jpg`, `swift-icon-dark.png`

**HTML IDs & Variables:**

- Use camelCase: `menuBtn`, `openStatus`, `visitStepper`, `campaignModal`, `viewportSwitcher`
- Prefix with descriptive name: `heroImg`, `heroHeadline`, `heroPrimaryCta`
- Target elements directly: `visitTileContent`, `visitTileImg`, `openDot`, `openDotPing`

**Data Attributes:**

- Use kebab-case: `data-step`, `data-viewport`, `data-bar`
- Represent UI state or configuration: `data-step="0"` for stepper position, `data-viewport="mobile"` for responsive preview

**CSS Classes:**

- Tailwind utility classes for most styling
- Custom semantic classes for complex interactions: `.reveal`, `.hero-in`, `.hero-img-zoom`, `.spring`, `.focus-ring`, `.visit-node`, `.triage-row`, `.faq-item`
- Pseudo-class naming follows Tailwind patterns: `.is-visible`, `.is-open`, `.is-swapping`

**Functions:**

- camelCase throughout: `renderNodes()`, `renderTile()`, `goTo()`, `closeMenu()`, `openMenu()`, `applyCampaign()`, `showViewport()`, `setActive()`
- Descriptive verb-noun pattern: `closeModal()`, `openModal()`, `showDesktop()`, `renderTile()`

## Code Style

**Formatting:**

- Indentation: 2 spaces (inferred from HTML/JavaScript structure)
- Line length: no hard limit observed, but generally readable (max ~100 chars for readability)
- Semicolons: required (used consistently throughout)
- No trailing commas in arrays/objects

**Linting:**

- No linter configuration detected (no `.eslintrc`, `.prettierrc`, or `biome.json`)
- No automated code formatting tool (no Prettier or similar)
- Code follows manual consistency — review by eye

**JavaScript Style:**

- ES5-compatible syntax throughout (targets broader browser support)
- Uses `var` for variable declarations (not `let`/`const`)
- Uses `Array.prototype.slice.call()` for NodeList conversion instead of spread operator
- Uses `setAttribute()` / `getAttribute()` for dynamic attribute manipulation
- Uses `classList` API for class operations (add/remove/toggle)
- No use of template literals (backticks)

**HTML Structure:**

- Semantic HTML5 elements: `<header>`, `<main>`, `<footer>`, `<nav>`, `<section>`, `<article>`, `<details>`
- Accessibility attributes consistently applied: `aria-label`, `aria-expanded`, `aria-controls`, `aria-current`, `aria-pressed`, `aria-hidden`
- Alt text on images: descriptive when informative (`alt="A SWIFT doctor caring for a patient"`), empty when decorative (`alt=""` with `aria-hidden="true"`)
- Proper landmark structure with skip links (implicit via `#top` anchor)

## Import Organization

**Not applicable** — single-file architecture. No imports or module system.

**External dependencies loaded via CDN:**

1. Google Fonts (Bricolage Grotesque, IBM Plex Sans)
2. Tailwind CSS
3. Schema.org structured data (JSON-LD)
4. Google Analytics (placeholder)
5. Google Maps embed

## Error Handling

**Patterns observed:**

**Early returns for missing elements:**

```javascript
if (!statusEl) return;
if (!stepper) return;
if (!demoBtn || !modal || !list) return;
```

Silently exit functions if required DOM elements don't exist.

**Try-catch for non-critical features:**

```javascript
try {
  var sydneyHour = parseInt(
    new Intl.DateTimeFormat('en-AU', { ... }).format(new Date()),
    10
  );
  // ... set status
} catch (e) {
  /* Intl timezone lookup unsupported: leave static hours text as-is */
}
```

Graceful fallback if Intl API unavailable (browser support).

**No explicit error messages:** Errors are silent; fallbacks preserve basic functionality.

**Null check pattern:**

```javascript
if (!('IntersectionObserver' in window)) {
  // Fallback for older browsers
  document.querySelectorAll('.reveal').forEach(function (el) { 
    el.classList.add('is-visible'); 
  });
  return;
}
```

Check feature availability before use.

## Module/IIFE Pattern

**Immediately Invoked Function Expressions (IIFE) for scope isolation:**

All JavaScript is wrapped in IIFE blocks — each feature (open status, scroll reveal, mobile menu, stepper, campaign preview, viewport switcher) is self-contained:

```javascript
(function () {
  var statusEl = document.getElementById('openStatus');
  // ... logic
})();
```

**Benefits:**

- No global namespace pollution
- Variables scoped to IIFE (no accidental collisions)
- Clear feature boundaries

**Patterns:**

- Local variables declared with `var` at IIFE top
- DOM elements cached for reuse
- Event listeners attached only if required elements exist
- No return values; all state managed via DOM mutations

## Comments

**Sparse documentation:**

- Minimal inline comments
- HTML comments mark major sections: `<!-- Header -->`, `<!-- Hero -->`, `<!-- Triage directory -->`, `<!-- Mobile menu -->`, `<!-- FAQ -->`
- JavaScript comments used for clarification only:
  - `// Don't show the device switcher inside its own preview iframe`
  - `// Intl timezone lookup unsupported: leave static hours text as-is`
  - `/* Intl timezone lookup unsupported: leave static hours text as-is */`

**No JSDoc/TypeScript comments** — no types defined.

## Function Design

**Size:** Functions are compact, typically 10–50 lines. Stepper logic (renderNodes, renderTile, goTo) is largest at ~30 lines.

**Parameters:** Functions generally take no parameters; instead, they cache DOM elements and operate on local variables:

```javascript
function renderNodes() {
  nodes.forEach(function (node, i) {
    // ... logic using closure over 'nodes', 'current', 'ALL_NODE_CLASSES'
  });
}
```

**Return Values:** Most functions return nothing (`undefined`); they mutate DOM state directly:

```javascript
function closeMenu() {
  triggers.forEach(function (t) { t.setAttribute('aria-expanded', 'false'); });
  menu.classList.remove('is-open');
  // No return
}
```

**Exceptions:**

- Helper conditionals: `isOpen` derived from timezone check
- Event callbacks used inline: `addEventListener('click', function () { ... })`

## Tailwind Configuration

**Inline Tailwind config in `<script>` tag:**

```javascript
tailwind.config = {
  theme: {
    extend: {
      colors: {
        ink:      '#182524',
        teal900:  '#1E453F',
        teal700:  '#2C685E',
        teal600:  '#377E71',
        teal500:  '#4B9587',
        tealGlow: '#6FB3A3',
        paper:    '#F6F8F7',
        mint:     '#EAF1EF',
        line:     '#D9E3E0',
        urgent:   '#B23A3A',
        urgentDk: '#8C2C2C',
      },
      fontFamily: {
        display: ['"Bricolage Grotesque"', 'sans-serif'],
        body: ['"IBM Plex Sans"', 'sans-serif'],
      },
    },
  },
};
```

**Color naming convention:**

- Base colors named by intent: `ink` (text), `paper` (background), `mint` (light accent), `line` (borders)
- Teal palette: intensity-based naming (`teal900` darkest → `teal500` mid-tone → `tealGlow` brightest)
- Semantic colors: `urgent` (red for emergency banner)

## Global Styles

**In `<style>` block:**

- Root-level scroll behavior: `scroll-behavior: smooth`
- Body background: `#F6F8F7` (paper color)
- Selection colors: teal glow on dark background
- Focus ring: `.focus-ring:focus-visible` with 2px outline
- Prefers-reduced-motion: respected (animation duration set to 0.001ms)

**Custom animations defined:**

- `@keyframes heroIn` — entrance fade + slide
- `@keyframes heroImgZoom` — image zoom on load
- `@keyframes reveal` — scroll-triggered fade + slide
- Mobile menu transitions, FAQ animations

## Responsive Design

**Mobile-first approach (per CLAUDE.md):**

- Base styles apply to mobile (390px)
- `sm:` breakpoint for tablet/small desktop
- `lg:` breakpoint for full desktop
- `md:` breakpoint for intermediate layouts

**Example pattern:**

```html
<h1 class="text-2xl sm:text-3xl lg:text-4xl">...</h1>
<div class="grid grid-cols-2 md:grid-cols-4">...</div>
```

## Accessibility

**Consistent ARIA patterns:**

- `aria-expanded="true/false"` for toggles (menu, details)
- `aria-pressed="true/false"` for button state
- `aria-current="step"` for stepper position
- `aria-label` on icon-only buttons
- `aria-hidden="true"` on decorative SVGs and pseudo-elements
- `aria-controls` links buttons to controlled elements

**Keyboard support:**

- All interactive elements reachable via Tab
- Escape key closes modals and menus
- Enter/Space activates buttons (browser default)
- Focus styling via `.focus-ring` class

**Semantic HTML:** Proper use of `<button>`, `<a>`, `<details>` for interactive components (not divs).

---

*Convention analysis: 2026-09-25*
