---
last_mapped_commit: ea9307c55fb09b359776c6efecfdc084ee10a6a9
last_mapped_at: 2026-09-25
---
<!-- refreshed: 2026-09-25 -->

# Architecture

**Analysis Date:** 2026-09-25

## System Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                     Browser Context (HTML)                   │
├──────────────────┬──────────────────┬───────────────────────┤
│   Static Page    │  Tailwind (CDN)  │   Vanilla JavaScript  │
│  `index.html`    │   Theme Config   │   (Inline, 7 modules) │
└────────┬─────────┴────────┬─────────┴──────────┬────────────┘
         │                  │                     │
         └─────────────────┬┴─────────────────────┘
                           │
         ┌─────────────────┴─────────────────────┐
         │      Component Modules                 │
    ┌────┴─────┬──────────┬────────┬────────┬────┴────┐
    │ Status   │ Scroll   │ Mobile │ Visit  │Campaign │
    │Indicator │ Reveal   │ Menu   │Stepper │ Modal   │
    │ (IIFE)   │(IIFE)    │(IIFE)  │(IIFE)  │ (IIFE)  │
    └──────────┴──────────┴────────┴────────┴─────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│            DOM Elements (Structured Sections)                │
│  - Header/Nav  - Triage  - Services  - Location             │
│  - Hero        - Visit   - Fees      - Doctors               │
│  - Footer      - Media   - FAQs      - Modals                │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│              Static Assets & External Resources              │
│  - Brand assets (`brand_assets/`)                            │
│  - Google Fonts (CDN)                                        │
│  - Google Maps iframe                                        │
│  - Google Analytics (placeholder)                            │
└─────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| **Header/Nav** | Logo, desktop nav links, mobile toggle, contact CTA, emergency banner | `index.html` lines 172–227 |
| **Hero** | Eye-catching entry point with campaign-swappable image, headline, subhead, CTAs; live open status | `index.html` lines 308–342 |
| **Triage Directory** | Collapsible accordion for symptom/need-based routing; 4 conditions mapped to actions | `index.html` lines 356–408 |
| **Visit Stepper** | 7-step interactive journey through visit workflow; image + text tile updates per step | `index.html` lines 410–453 |
| **Services Grid** | 8 service cards (7 SWIFT + 1 featured large tile); featured imaging/dental co-located callout | `index.html` lines 482–585 |
| **Fees Section** | Pricing card + Medicare vs non-Medicare comparison | `index.html` lines 587–628 |
| **Wait Times** | ED comparison table (sample data, not live) | `index.html` lines 630–665 |
| **Location** | Address, hours, contact, embedded Google Map iframe | `index.html` lines 667–705 |
| **Doctors** | 3-card team snapshot (founders + 1 senior); link to full team site | `index.html` lines 707–740 |
| **Media** | 3-card gallery/news section (2 real photos + 1 placeholder) | `index.html` lines 742–770 |
| **FAQs** | Collapsible details-based Q&A (3 FAQs; LD+JSON schema version has more) | `index.html` lines 772–802 |
| **Footer** | Branding, explore/contact links, copyright | `index.html` lines 806–847 |

## Pattern Overview

**Overall:** Single-Page Static HTML + Vanilla JavaScript (Immediate Invoked Function Expressions)

**Key Characteristics:**

- **No framework** — pure DOM manipulation
- **No build step** — everything inline (CSS via Tailwind CDN, JS embedded)
- **No external JS libraries** — only Puppeteer for screenshot tooling (dev-only)
- **IIFE isolation** — 7 independent JavaScript modules wrap functionality to avoid global scope pollution
- **Progressive enhancement** — noscript fallback hides animations if JS disabled
- **Mobile-first responsive** — Tailwind breakpoints (sm:, md:, lg:)
- **Accessibility** — ARIA labels, focus-ring utility, semantic HTML, kbd navigation (Escape closes menus/modals)

## Layers

**HTML Structure (Semantic Markup):**

- Purpose: Markup all page sections, modals, component scaffolding
- Location: `index.html` (lines 1–1156)
- Contains: semantic sections, details/summary for collapsibles, button/link controls
- Depends on: none
- Used by: CSS + JavaScript

**CSS (Tailwind + Custom Theme):**

- Purpose: Styling + animations (hero entrance, scroll reveal, stepper transitions, menu toggle)
- Location: `index.html` lines 20–164 (Tailwind config + inline `<style>`)
- Contains: Tailwind classes in markup, custom @keyframes, interaction states (hover, focus-visible, active)
- Depends on: Tailwind CDN script
- Used by: Browser renderer

**JavaScript (7 Modules):**

- Purpose: Interactivity, state management, event listeners, DOM updates
- Location: `index.html` lines 849–1153 (inline `<script>`)
- Contains: 7 IIFEs + support functions
- Depends on: DOM elements (expects specific IDs and data attributes)
- Used by: Browser event loop

## Data Flow

### Primary Request Path

1. **Page Load** (`index.html` served by `serve.mjs` or static host)
   - Browser requests `http://localhost:3000/`
   - `serve.mjs` or static server returns `index.html` with 200 status
   - File: `serve.mjs` lines 26–46

2. **Head Processing** (lines 1–165 of `index.html`)
   - Meta tags parsed (charset, viewport, OG, structured data)
   - Google Fonts preconnected (performance optimization)
   - Tailwind CDN script injected; custom theme config applied
   - Google Analytics placeholder loaded (needs real GA4 ID)
   - Structured data (LD+JSON MedicalClinic, FAQPage schema) parsed by search engines/AI

3. **CSS Ready**
   - Tailwind processes classes in DOM
   - Custom `<style>` block applies animations, focus states, mobile menu transitions

4. **DOM Parse Complete** (lines 166–804 of `index.html`)
   - All sections, components, modals rendered
   - Noscript fallback hides animations for no-JS browsers
   - Scroll link anchors (`#top`, `#triage`, `#services`, etc.) ready

5. **JavaScript Execution** (lines 849–1153)
   - 7 IIFE modules run sequentially
   - Each module finds DOM elements by ID, attaches listeners, initializes state
   - Features activated:
     - **Status Indicator**: Sydney timezone check updates "Open now" text
     - **Scroll Reveal**: IntersectionObserver fires `.reveal` animations
     - **Mobile Menu**: Menu toggle + close-on-link-click + Escape handler
     - **Visit Stepper**: Initialize node styling + tile content
     - **Campaign Demo**: Modal builder from campaigns array
     - **Viewport Switcher**: Device preview tool (hidden on mobile)

6. **Ready for Interaction**
   - Page fully interactive
   - Scroll, click, keyboard (Escape) listeners active

### Secondary Flow: User Clicks Triage Option

1. User clicks `.triage-row` → `<details>` element toggles via browser native behavior
2. CSS `.triage-row[open] .chev { transform: rotate(90deg); }` rotates chevron
3. Answer content slides in via `@keyframes reveal` CSS animation
4. No JavaScript required (uses native `<details>`)

### Tertiary Flow: User Navigates Visit Stepper

1. User clicks `.visit-node` button (step 1–7)
2. JavaScript `goTo(index)` function called
3. DOM elements fetched from steps array: image src, title, description, tip
4. Content div adds `is-swapping` class (opacity fade) → waits 160ms → updates DOM → removes class (fade-in)
5. Node styling updated: active node gets teal background + shadow; past nodes stay teal; future nodes become white/bordered
6. Prev button disabled if on step 1

### Quaternary Flow: Hero Campaign Preview (Demo Feature)

1. User clicks "Preview campaigns" button
2. Campaign modal opens: backdrop + modal overlay fade in
3. JavaScript loops campaigns array → creates button for each
4. User clicks a campaign → `applyCampaign(c)` swaps hero image, headline, subhead, CTA href/text
5. Close button removes modal

### Scroll Reveal Animation

- Page loads with `.reveal` elements opacity: 0, transform: translateY(22px)
- IntersectionObserver created in IIFE (lines 873–886)
- When element enters viewport (15% threshold), `.is-visible` class added
- CSS transitions animate to opacity: 1, translateY(0) over 0.7s

**State Management:**

- **No centralized state** — each module manages its own:
  - Status module: Sydney timezone hour
  - Reveal module: IntersectionObserver registry
  - Menu module: `aria-expanded` attribute, `is-open` class
  - Stepper module: `current` variable (0–6), node array
  - Campaign module: campaigns array, active campaign context
  - Viewport module: sizes object, active viewport name

## Key Abstractions

**Collapsible Details Pattern:**

- Purpose: Expandable accordion sections (triage, FAQs)
- Examples: `index.html` lines 363–405 (triage), lines 777–799 (FAQ)
- Pattern: Native HTML `<details>/<summary>` elements; CSS handles chevron rotation + animations; no JS required (browser native)

**Interactive Stepper Component:**

- Purpose: Multi-step journey through visit workflow
- Example: `index.html` lines 415–452
- Pattern: Button array (7 step nodes) + single content tile; clicking node updates shared tile; node visual state tracks progression

**Modal Dialog Pattern:**

- Purpose: Overlayed content (campaign demo, viewport preview)
- Examples: `index.html` lines 257–273 (campaign), lines 291–304 (viewport)
- Pattern: Fixed overlay + positioned dialog; backdrop click or Escape closes; `hidden` class toggles visibility

**Scroll Reveal Animation:**

- Purpose: Stagger in headings/content as user scrolls
- Pattern: Mark elements with `.reveal` class; IntersectionObserver triggers `.is-visible` class addition; CSS transition handles animation

**Campaign Hero Pattern:**

- Purpose: Swap hero section imagery, headline, subhead, CTA based on campaign selection
- Data structure: Array of campaign objects (id, label, image, headline, subhead, ctaText, ctaHref)
- Logic: Apply campaign writes to DOM element properties/text content directly

## Entry Points

**Page Load Entry:**

- Location: `index.html` (served by `serve.mjs` lines 26–46 or static host)
- Triggers: HTTP GET request to `/`
- Responsibilities: Return HTML document, trigger browser parse → render → JS execution

**JavaScript Entry (7 IIFE Modules):**

- Lines 850–870: **Status Indicator** — Sydney timezone check, update open/closed display
- Lines 872–886: **Scroll Reveal** — IntersectionObserver setup
- Lines 888–918: **Mobile Menu** — toggle + close handlers
- Lines 920–1005: **Visit Stepper** — node click handlers, tile rendering
- Lines 1007–1098: **Campaign Modal** — modal show/close, campaign selection
- Lines 1100–1152: **Viewport Switcher** — device preview tool

**User Entry Points (Clickable Elements):**

- `.hero-in` links: call phone, get directions
- `.triage-row` details: click to expand
- `.visit-node` buttons: step navigation
- `#campaignDemoBtn`: open campaign preview
- Navigation `.mobile-link`: scroll to sections
- `#menuBtn`, `#bottomMenuBtn`: toggle mobile menu
- `#viewportSwitcher` buttons: device preview

## Architectural Constraints

- **Single File**: All markup, CSS, JS in `index.html` (1156 lines) — larger file size, but no HTTP round-trips for assets
- **No Node/Bundler**: No build step, no module system (CommonJS/ESM locally) — simpler deployment, harder to refactor large codebases
- **Inline Tailwind CDN**: Slower first paint than pre-compiled CSS; but enables quick style tweaks without build
- **Vanilla JavaScript only**: No DX helpers (React, Vue, etc.); state scattered across modules; harder to trace data flow
- **Synchronous script execution**: All JS runs in order; no async module loading
- **Browser timezone assumptions**: Status indicator uses `Intl.DateTimeFormat` with Sydney timezone; will show "Open/Closed" for all visitors regardless of location (intentional, but affects UX for international traffic)
- **Google Maps iframe**: Requires external network request; no fallback if Google Maps API unavailable
- **No service worker**: No offline capability; no caching strategy

## Anti-Patterns

### Single-Page HTML Monolith

**What happens:** All 1156 lines of markup, style, and logic bundled into one `index.html` file.

**Why it's wrong:** 

- Difficult to split responsibilities (content vs. behavior vs. styling)
- File is large for source control diff
- IDE autocomplete/navigation sluggish
- Team collaboration: merge conflicts likely on single file changes
- Testing: hard to unit test JS modules in isolation (all globals in one scope, even IIFEs)

**Do this instead:** 

- For a small marketing site (current state): acceptable trade-off; document component sections with comments
- For scaling: extract into templated HTML, separate CSS file, modular JS (even without bundler, use `<script type="module">` or build step)

### No State Container

**What happens:** Each JavaScript module maintains its own state (`current` variable in stepper, `triggers` array in menu, etc.). State mutations scattered across 7 IIFEs with no central source of truth.

**Why it's wrong:**

- Hard to debug — state changes not traceable to one place
- No time-travel debugging capability
- Risk of inconsistent state if two modules try to update related data
- Adding features (e.g., "persist stepper position to localStorage") requires touching multiple modules

**Do this instead:**

- For this site: state isolation via IIFE scoping is acceptable (each module is self-contained)
- If more interactivity needed: introduce a simple state object (even if not using Redux/Zustand) or split into ES modules

### Inline Script in HTML

**What happens:** All JavaScript written inside `<script>` tag in HTML; executed synchronously on page load.

**Why it's wrong:**

- Hard to debug (browser DevTools shows inline script as `index.html`)
- Caching: HTML file updates invalidate JS cache
- Not pre-parsed/compiled by browser until HTML fully loaded
- CDN/edge optimizations (minification, compression) applied to whole HTML file, not JS separately

**Do this instead:**

- For this site: acceptable (small JS footprint, no build overhead)
- If scaling: extract to external `app.js`, link with `<script src="app.js"></script>`, allows browser to parallelize load

### Direct DOM Manipulation Without Events

**What happens:** Event listeners attached inline in IIFE closures; no event delegation; each button/link gets its own listener. Campaigns array hardcoded in JS, no easy way to update campaigns without JS edit.

**Why it's wrong:**

- Harder to add/remove campaign options without touching JS
- Event listeners not delegated (one per element) — less memory-efficient at scale
- No clear data→view separation

**Do this instead:**

- Extract campaigns to data attribute or external JSON (even inline `<script type="application/json">`)
- Use event delegation (e.g., attach listener to `#campaignList`, check `event.target` for campaign button clicks)

## Error Handling

**Strategy:** Try-catch around timezone check only; silent failure on missing DOM elements (script checks `if (!element) return`); fallback noscript style hides animations

**Patterns:**

- **Timezone fetch** (lines 856–870): wrapped in try-catch; if `Intl.DateTimeFormat` unavailable, catch logs nothing, leaves static hours text unchanged
- **DOM queries** (lines 873–886, etc.): null-check pattern — `if (!element) return;` prevents errors on missing IDs
- **Browser feature detection** (line 873): checks `'IntersectionObserver' in window` before using; fallback adds `is-visible` to all `.reveal` elements immediately

**No explicit error logging:** Silent failures acceptable for a marketing site; no analytics for JS errors (placeholder GA config not filled in)

## Cross-Cutting Concerns

**Logging:** None (browser console available for debugging; no error reporting service configured)

**Validation:** Patient input validation not applicable (no form submission); external links rely on href validation (browser handles)

**Authentication:** Not applicable (public marketing site, no user accounts)

**Accessibility:**

- ARIA labels on all interactive elements (`aria-expanded`, `aria-controls`, `aria-label`, `aria-current`, `aria-pressed`)
- Focus visible ring utility (`.focus-ring` class) applied to all buttons/links
- Semantic HTML (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`, `<details>`)
- Keyboard navigation: Escape closes menus/modals, Tab moves through links/buttons (browser native)
- Structured data (LD+JSON) for search engine understanding

**Performance:**

- Single file (~77KB) transferred once; cached by browser
- Tailwind CDN: slightly slower than pre-compiled, but enables real-time editing in dev
- Images: lazy-loaded via default browser behavior (no explicit lazy-loading attributes)
- No analytics bloat (placeholder GA ID not active)
- Smooth scroll enabled via CSS (`:root { scroll-behavior: smooth; }`)

---

*Architecture analysis: 2026-09-25*
