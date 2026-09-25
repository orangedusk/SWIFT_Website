# SWIFT Emergency & Urgent Care — Website Redesign

A from-scratch, patient-centric redesign of the SWIFT Emergency & Urgent Care homepage (Rouse Hill, NSW). Currently a single-page static build (`index.html`) — no framework or build step.

## Running locally

Requires [Node.js](https://nodejs.org) (v18+).

```
npm install
node serve.mjs
```

Then open **http://localhost:3000**.

## Screenshot tooling

Two Puppeteer scripts for visual review — always screenshot from `localhost`, never a `file://` URL:

```
node screenshot.mjs http://localhost:3000 [label]     # desktop, full page
node mobile_shot.mjs http://localhost:3000 [label]     # mobile viewport, full page
```

Screenshots save to `./temporary screenshots/` (git-ignored, auto-incremented filenames).

## Project structure

```
index.html          Single-page homepage — all markup, Tailwind (CDN), and JS inline
serve.mjs            Local static file server (port 3000)
screenshot.mjs        Desktop screenshot tool
mobile_shot.mjs       Mobile-viewport screenshot tool
brand_assets/         Logo marks and real clinic photography
```

## Brand assets

- `swift-icon-dark.png` / `swift-icon-white.png` — the SWIFT cross/arrow mark, cleanly cropped from the original logo export (the full wordmark export is clipped mid-text at the source and unusable — see `swift-original-logo-export-CLIPPED-reference-only.png`)
- `clinic-reception.jpg`, `clinic-waiting-area.jpg` — real architectural renders of the actual Rouse Hill clinic, sourced from the current live site
- `hero-doctor-patient.jpg` — supplied by the client, used in the hero and the featured services tile

## Known placeholders — needs real input before launch

- **Google Analytics**: `G-XXXXXXXXXX` in `index.html` is a placeholder — swap in the real GA4 Measurement ID
- **Nearby ED wait times**: the "Weighing up where to go?" section shows sample data. No public real-time NSW Health API was identified — needs a data source decision
- **Booking**: "Request appointment" now goes to `request-appointment.html`. The clinic uses Best Practice (Bp Premier), so live online booking should come from Best Health Booking: paste its embed code into `#bookingEmbedMount` and set `BOOKING_EMBED_ENABLED = true`. Until then the page shows a request form, which only shows a confirmation and sends nothing until `APPT_FORM_ENDPOINT` is set (the destination must be suitable for health information)
- **Other old-site links**: "Meet the full team" / "See detailed pricing" and the service tiles still point to the *current* live site (`swiftemergencycare.com.au`) as stand-ins
- **Services list**: reflects the current site's services, with radiology and dental separated out as co-located independent providers per the new brief. Final add/remove list from the client is still pending
- **Gallery**: two of three "From SWIFT" cards use real clinic photos; the third (an article teaser) has no real post behind it yet

## Design notes

Full brief and design rationale live in `CLAUDE.md` (frontend workflow rules) and the project conversation history — teal-driven custom palette (not Tailwind defaults), Bricolage Grotesque + IBM Plex Sans type pairing, mobile-first, symptom/need-based triage navigation in the hero.
