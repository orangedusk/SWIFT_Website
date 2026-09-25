---
last_mapped_commit: ea9307c55fb09b359776c6efecfdc084ee10a6a9
last_mapped_at: 2026-09-25
---
# External Integrations

**Analysis Date:** 2026-09-25

## APIs & External Services

**Google Analytics:**

- **Service:** Google Analytics 4 (GA4)
- **What it's used for:** Visitor tracking, event analytics, conversion measurement for website traffic analysis
  - **SDK/Client:** Google Tag Manager (`gtag.js`)
  - **Config location:** `index.html` (lines 46–52)
  - **Placeholder ID:** `G-XXXXXXXXXX` — must be replaced with client's real GA4 Measurement ID before launch
  - **Implementation:** Async script load from `https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX`; `gtag()` function configured with `gtag('config', 'G-XXXXXXXXXX')` on page load (line 51–52)

**Fonts (Web Fonts):**

- **Service:** Google Fonts CDN
- **What it's used for:** Serving custom typefaces for optimal typography across all viewports
  - **Fonts loaded:** Bricolage Grotesque (display font, weights 500–800) and IBM Plex Sans (body font, weights 400–600)
  - **Preconnect:** `https://fonts.googleapis.com` and `https://fonts.gstatic.com` (line 15–16) for DNS prefetching and early connection
  - **Stylesheet:** Loaded via `https://fonts.googleapis.com/css2?family=...&display=swap` (line 17)
  - **Fallback:** System fonts (sans-serif) if Google Fonts CDN unavailable

**Tailwind CSS CDN:**

- **Service:** Tailwind CSS CDN
- **What it's used for:** Utility-first CSS framework for responsive design
  - **URL:** `https://cdn.tailwindcss.com` (line 19)
  - **Configuration:** Inline Tailwind config in `<script>` tag (lines 20–43) extends default theme with custom colors (teal palette: `teal900` #1E453F through `tealGlow` #6FB3A3, critical colors: `urgent` #B23A3A) and font family mappings
  - **No build step:** Tailwind processes class list at runtime (lazy mode); slower on first load but eliminates need for build tooling

**Google Maps:**

- **Service:** Google Maps Embed API
- **What it's used for:** Display clinic location on website and provide navigation links
  - **Embedded map:** `https://maps.google.com/maps?q=32%20Civic%20Way%2C%20Rouse%20Hill%20NSW%202155&z=15&output=embed` (embedded iframe in location section)
  - **Directions link:** `https://www.google.com/maps/dir/?api=1&destination=G38%2C+32+Civic+Way%2C+Rouse+Hill+NSW+2155` (clickable link in footer/location CTA)
  - **No API key required:** Embedded map and directions links work without authentication

**Schema.org Structured Data:**

- **Service:** Schema.org ontology (JSON-LD)
- **What it's used for:** SEO and AI assistant indexing — helps search engines and AI systems (ChatGPT, Claude) understand clinic information
  - **Schemas used:**
    - `MedicalClinic` (lines 56–84) — clinic name, address, phone, email, hours, specialties, services
    - `FAQPage` (lines 86–110+) — frequently asked questions for rich snippet display
  - **No external API call:** Static JSON-LD embedded in `<head>`; processed by crawlers/indexers only

## Data Storage

**Databases:**

- None — static website; no backend or database connection

**File Storage:**

- **Local filesystem only** — all static assets (HTML, images) served from project directory via `serve.mjs`
- **Brand assets:** Stored in `brand_assets/` directory (logo marks, clinic photography)
  - Location: `/brand_assets/` (relative to project root)
  - Files: `swift-icon-dark.png`, `swift-icon-white.png`, clinic photos (`.jpg`), visit-timeline images (`.jpeg`)
  - Cached by browser via HTTP `Cache-Control` headers (set by `serve.mjs`)

**Caching:**

- **Browser caching:** `serve.mjs` returns 200 OK with appropriate `Content-Type` headers; relies on browser default caching heuristics (no explicit `Cache-Control` or `ETag` headers configured in `serve.mjs`)
- **No CDN** — assets not cached on a CDN in current setup; suitable for low-traffic static site or development

## Authentication & Identity

**Auth Provider:**

- None — static website with no user authentication

**Appointment Booking:**

- **External redirection:** Links to `https://www.swiftemergencycare.com.au/request-appointment` and `https://www.swiftemergencycare.com.au/team`
- **Current state:** These are stand-in links to the current live site; will be replaced with new site URLs when those pages are built
- **No embedded booking widget:** No calendar, form, or reservation system embedded in this site yet

## Monitoring & Observability

**Error Tracking:**

- None detected — no error monitoring service (Sentry, Rollbar, etc.) configured

**Logs:**

- **Server logs:** `serve.mjs` logs connection startup: `Serving {__dirname} at http://localhost:3000` (line 48–49)
- **Client logs:** Console logging via vanilla JavaScript functions (e.g., `console.log` in visit stepper logic, line 938+); no structured logging or log aggregation

**Analytics:**

- Google Analytics 4 (see "APIs & External Services" section above)

## CI/CD & Deployment

**Hosting:**

- Not configured — project is development-ready static HTML
- Recommended deployment targets: Netlify, Vercel, GitHub Pages, S3 + CloudFront, or any static file hosting
- No build step required; can deploy `index.html` and `brand_assets/` folder directly

**CI Pipeline:**

- None detected — no GitHub Actions, GitLab CI, Jenkins, or similar

## Environment Configuration

**Required env vars:**

- None — static site requires no environment variables for runtime
- **Pre-launch configuration (code change, not env var):**
  - Google Analytics ID: Replace `G-XXXXXXXXXX` in `index.html` line 47 and 52
  - Appointment redirect URLs: Update links to `https://www.swiftemergencycare.com.au/request-appointment`, `https://www.swiftemergencycare.com.au/team`, `https://www.swiftemergencycare.com.au/fees`, etc. (deployed in `index.html`)

**Secrets location:**

- No secrets stored — static website
- All links and data are public (phone, email, address, business info in structured data is intentionally public)

## Webhooks & Callbacks

**Incoming:**

- None — no server to receive webhooks

**Outgoing:**

- **External redirects only:**
  - Appointment request: `https://www.swiftemergencycare.com.au/request-appointment`
  - Phone calls: `tel:0288599099` (native phone app integration on mobile)
  - Navigation: `https://www.google.com/maps/dir/` (native Maps app or browser redirect)
  - Service detail pages: `https://www.swiftemergencycare.com.au/services/{cardiology,orthopaedics,paediatrics,etc.}`
  - Pricing: `https://www.swiftemergencycare.com.au/fees`
  - Team: `https://www.swiftemergencycare.com.au/team`
- No programmatic callbacks or event forwarding

## Placeholders & TODO Integrations

**From README.md (lines 43–49):**

1. **Google Analytics** — GA4 ID `G-XXXXXXXXXX` is a placeholder in `index.html`; must be replaced with real Measurement ID before launch

2. **Nearby ED wait times** — The "Weighing up where to go?" section displays sample data; no real-time NSW Health API identified yet; needs a data source decision and integration path

3. **Booking system** — "Request appointment" and "Meet the full team" / "See detailed pricing" links currently point to the live `swiftemergencycare.com.au` site as stand-ins; will be replaced with new site URLs when those pages are built

4. **Services list** — Current list reflects live site; final add/remove list from client is pending

5. **Gallery / News** — "From SWIFT" section has one article teaser with no real post behind it; needs editorial content

---

*Integration audit: 2026-09-25*
