---
last_mapped_commit: ea9307c55fb09b359776c6efecfdc084ee10a6a9
last_mapped_at: 2026-09-25
---
# Technology Stack

**Analysis Date:** 2026-09-25

## Languages

**Primary:**

- **HTML5** — Complete markup for single-page website; all semantic structure in `index.html`
- **CSS 3** — Styling via Tailwind CSS utility classes; custom theme configuration inlined in `index.html`
- **JavaScript (ES6+)** — Vanilla JavaScript; all client-side functionality inlined in `index.html` (no transpilation)

## Runtime

**Environment:**

- **Node.js** v18+ — Required for local development and tooling

**Package Manager:**

- **npm** — Dependency management
- **Lockfile:** `package-lock.json` (present)

## Frameworks

**Core:**

- **Tailwind CSS** v3 (via CDN) — Utility-first CSS framework; loaded from `https://cdn.tailwindcss.com`
- **Custom Tailwind config** — Extended theme (custom colors: `ink`, `teal900`–`teal500`, `tealGlow`, `paper`, `mint`, `line`, `urgent`, `urgentDk`) and font families (`display`: Bricolage Grotesque, `body`: IBM Plex Sans) configured inline in `<script>` tag in `index.html` (lines 20–43)

**Testing:**

- None detected — no test framework, assertions, or test suites

**Build/Dev:**

- **serve.mjs** — Custom Node.js HTTP server for local development (uses built-in `http` module); serves project root at `http://localhost:3000` on port 3000
- **screenshot.mjs** — Puppeteer-based screenshot tool for desktop viewport (1440×900) — run with `node screenshot.mjs http://localhost:3000 [label]`
- **mobile_shot.mjs** — Puppeteer-based screenshot tool for mobile viewport — run with `node mobile_shot.mjs http://localhost:3000 [label]`

## Key Dependencies

**Critical:**

- **Puppeteer** v25.11.0 (`npm` production dependency) — Headless browser automation for taking full-page screenshots; Chrome binary cached at `~/.cache/puppeteer/` on macOS

**Infrastructure:**

- **Google Fonts CDN** — Bricolage Grotesque (weights 500, 600, 700, 800) and IBM Plex Sans (weights 400, 500, 600); preconnected in `index.html` (line 15–17) for performance
- **Tailwind CSS CDN** — Lazy-loaded style framework with custom theme overrides

## Configuration

**Environment:**

- **No .env file** — Project is static; no environment variables required for local development
- **Placeholder configuration in code:**
  - Google Analytics Measurement ID: `G-XXXXXXXXXX` (placeholder in `index.html` line 47) — must be replaced with real GA4 ID before production deployment
  - No secrets or credentials stored in version control

**Build:**

- **No build step** — Static HTML file served as-is
- **No bundler** — Tailwind CSS loaded via CDN; no PostCSS processing
- **No transpilation** — vanilla JavaScript compatible with all modern browsers (ES6 class syntax, IntersectionObserver, optional chaining used throughout `index.html`)

## Platform Requirements

**Development:**

- Node.js v18 or later (per `README.md` line 7)
- `npm` for dependency installation
- Modern browser with ES6+ support (all major browsers 2015+)
- For screenshots: Linux/macOS/Windows with X11 or compatible display server (Puppeteer requirement)

**Production:**

- **Deployment target:** Static file hosting (any HTTP server can serve this; no dynamic backend required)
- **Recommended:** CDN with automatic gzip/brotli compression for `index.html` (77KB uncompressed)
- **Browser compatibility:** All modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+); tested via Puppeteer screenshots

## Architecture Notes

- **Single-file static site** — all HTML, CSS (Tailwind config), and JavaScript coexist in `index.html` (~77KB)
- **No framework dependencies** — no React, Vue, Angular, or similar; pure DOM manipulation via `document` API
- **Inline styles** — no separate CSS files; Tailwind utilities and custom rules embedded in `<style>` tags
- **Client-side interactivity:** vanilla JS only (IntersectionObserver for reveal animations, mobile menu toggle, visit timeline stepper, open-status indicator based on Sydney timezone)
- **No API calls** — static content only; external links point to `https://www.swiftemergencycare.com.au` subdomain for appointment booking, services, and team info

---

*Stack analysis: 2026-09-25*
