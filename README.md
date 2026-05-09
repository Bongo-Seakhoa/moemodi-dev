# MOEMODI &mdash; Manufacturer Website

The official manufacturer website for **MOEMODI (PTY) LTD**, a South African
natural products manufacturer producing Agave Herbal Lotion, Aloe Vera
Petroleum Jelly and Rosehip Petroleum Jelly.

The site is intentionally simple in function and high in finish: it
showcases the company, lists the product range, links each product to
Takealot for online purchase, and provides direct contact options for
single and bulk orders.

> **Stack:** Plain static HTML, CSS and vanilla JavaScript. No build step,
> no framework, no dependency manager. Works as-is on any static host.

---

## What's in the box

```
moemodi-dev/
├── index.html              # Main landing page (all sections)
├── 404.html                # Custom 404 page
├── robots.txt              # Search engine directives
├── sitemap.xml             # XML sitemap
├── site.webmanifest        # PWA manifest (icon + theme)
├── netlify.toml            # Netlify deploy config
├── vercel.json             # Vercel deploy config
├── .github/workflows/
│   └── pages.yml           # GitHub Pages deploy workflow
├── assets/
│   ├── css/styles.css      # Single production stylesheet
│   ├── js/main.js          # Vanilla JS (nav, reveal, contact form)
│   └── images/
│       ├── logos/          # Primary, icon, horizontal, watermark
│       ├── products/       # 5 SKUs + group hero image
│       └── backgrounds/    # Botanical decorative imagery
├── .gitignore
├── LICENSE                 # Proprietary brand, internal-use code
└── README.md
```

---

## Sections

1. **Sticky navigation** with branded mobile menu
2. **Hero** &mdash; bold typography, product trio composition, dual CTAs
3. **Trust strip** &mdash; "Made in SA", botanical, retail/bulk, heritage
4. **About** &mdash; brand story with stat cards
5. **Products** &mdash; five SKUs, each with a *Buy on Takealot* link and a
   "Order direct" CTA
6. **Where to buy** &mdash; primary Takealot card, direct order option,
   future retail partners placeholder
7. **Wholesale** &mdash; dark, premium block with phone + WhatsApp CTAs
8. **Contact** &mdash; details + a no-backend contact form that opens the
   user's email client *or* WhatsApp pre-filled with the message
9. **Footer** &mdash; links, social placeholders, trading info, legal note

---

## Running locally

No build step. Open `index.html` directly, or use any static server:

```sh
# Python 3
python -m http.server 8080

# Node (npx)
npx serve .

# PHP
php -S localhost:8080
```

Then open <http://localhost:8080>.

---

## Deploying to production

Pick whichever you prefer &mdash; the repo includes config for all three.

### GitHub Pages (zero config)

1. Push the repo to GitHub.
2. In the repository settings: **Settings &rarr; Pages &rarr; Source: GitHub Actions**.
3. The workflow at `.github/workflows/pages.yml` deploys on every push to `main`.
4. The `CNAME` file at the repo root is already set to `moemodi.co.za` &mdash;
   GitHub will pick it up automatically once DNS is configured (see below).

### Netlify

1. Connect the repo on Netlify.
2. Use defaults &mdash; build command empty, publish directory `.`.
3. `netlify.toml` configures security headers, asset caching and the 404 page.

### Vercel

1. Import the repo on Vercel.
2. Use defaults (Other / static).
3. `vercel.json` configures security headers, asset caching and the 404 page.

---

## Connecting your GoDaddy domain (`moemodi.co.za`)

The repo already includes a `CNAME` file with `moemodi.co.za`. Once your
host is live, point the domain at it from GoDaddy:

### Option A &mdash; GitHub Pages

1. Push the repo, enable **GitHub Pages** (Settings &rarr; Pages &rarr;
   Source: GitHub Actions). Your site will appear at
   `https://<username>.github.io/<repo>/`.
2. In **GoDaddy &rarr; My Products &rarr; Domains &rarr; moemodi.co.za &rarr; DNS**, set:

   | Type   | Name | Value                                 | TTL    |
   |--------|------|---------------------------------------|--------|
   | A      | @    | `185.199.108.153`                     | 1 hour |
   | A      | @    | `185.199.109.153`                     | 1 hour |
   | A      | @    | `185.199.110.153`                     | 1 hour |
   | A      | @    | `185.199.111.153`                     | 1 hour |
   | CNAME  | www  | `<username>.github.io`                | 1 hour |

   Delete any conflicting `A` or `CNAME` records on `@` and `www` (GoDaddy
   often pre-fills a parking record &mdash; remove it).
3. Back in GitHub: **Settings &rarr; Pages &rarr; Custom domain**, enter
   `moemodi.co.za` and tick **Enforce HTTPS** once it's available.

### Option B &mdash; Netlify

1. Deploy the repo to Netlify.
2. **Domain settings &rarr; Add custom domain &rarr; `moemodi.co.za`**.
3. In GoDaddy DNS, set:

   | Type   | Name | Value                                       | TTL    |
   |--------|------|---------------------------------------------|--------|
   | A      | @    | `75.2.60.5`                                 | 1 hour |
   | CNAME  | www  | `<your-site>.netlify.app`                   | 1 hour |

   Or follow Netlify's "External DNS" instructions (it will list the
   exact records). Netlify provisions HTTPS automatically.

### Option C &mdash; Vercel

1. Deploy on Vercel.
2. **Project &rarr; Settings &rarr; Domains &rarr; Add `moemodi.co.za`**.
3. In GoDaddy DNS, set:

   | Type   | Name | Value                | TTL    |
   |--------|------|----------------------|--------|
   | A      | @    | `76.76.21.21`        | 1 hour |
   | CNAME  | www  | `cname.vercel-dns.com` | 1 hour |

### Notes for any host

- DNS changes propagate in minutes to a few hours. Don't panic if
  `https://moemodi.co.za` isn't live within the first 10 minutes.
- Always set up both apex (`moemodi.co.za`) and `www` (`www.moemodi.co.za`).
  All three hosts above will redirect `www` &harr; apex automatically once
  configured.
- Disable any "Forwarding" GoDaddy may have enabled by default &mdash; it
  conflicts with custom DNS records.
- HTTPS (TLS) is provisioned by the host (Let's Encrypt) once DNS is
  pointing correctly. Allow up to an hour for the certificate.

---

## Customising

### Activate Takealot links (currently "coming soon")

While the Takealot listing is in progress, every retailer touchpoint on
the site reads **"Takealot &mdash; coming soon"**:

- Five disabled `<span class="btn btn-disabled">` placeholders below each
  product (the working CTA next to them is "Order direct" &rarr; #contact).
- One soft "Coming soon" card in the *Where to buy* section.
- One italic "Takealot &mdash; coming soon" entry in the footer.
- Hero copy reads *"Order direct from the manufacturer; Takealot listing
  coming soon."*

When your products go live on Takealot:

1. **Per-product cards** &mdash; in `index.html`, find each
   `<span class="btn btn-disabled" ...>Takealot &mdash; coming soon</span>`
   and swap it for an anchor:
   ```html
   <a class="btn btn-primary btn-sm"
      href="https://www.takealot.com/your-direct-product-url"
      target="_blank" rel="noopener noreferrer">
     Buy on Takealot
   </a>
   ```
   You may also flip the *Order direct* button back to `btn-ghost btn-sm`
   if you'd rather have Takealot as the primary CTA.
2. **Where to buy** card &mdash; replace the soft `<div class="retailer-card retailer-card-soft">`
   for Takealot with an `<a class="retailer-card primary" href="...">`.
3. **Footer** &mdash; swap the `<span class="footer-soft">` for an `<a>`.
4. **Hero copy** &mdash; remove the "Takealot listing coming soon" line.
5. **Meta description &amp; Open Graph** &mdash; in `<head>`, restore wording
   like "available on Takealot and direct from the manufacturer".

### Update contact details

In `index.html`:
- Phone number `+27 72 212 1348` &mdash; appears in nav, hero, wholesale,
  contact, footer, JSON-LD and the floating WhatsApp button.
- Email `hello@moemodi.co.za` is a placeholder &mdash; update wherever it
  appears (`mailto:` links and the JS `EMAIL_TO` constant in
  `assets/js/main.js`).
- Address is intentionally generic ("South Africa") until finalised.

### Brand colors / typography

Tokens live at the top of `assets/css/styles.css` under `:root`. Change a
single CSS variable to recolour the whole site.

### Add or edit products

Each product is an `<article class="product-card">` block in
`index.html`. Copy any block, swap the image src, name, copy and link.
The `data-accent` attribute (`green`, `aloe`, or `rose`) sets the top
border colour.

---

## Quality, accessibility and SEO

- Semantic HTML: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`,
  `<aside>`, `<footer>`.
- All decorative images use `aria-hidden`/empty alt; informative images
  have descriptive alt text.
- Skip-to-content link, keyboard-accessible nav, visible focus rings,
  `aria-expanded` on the mobile toggle.
- Respects `prefers-reduced-motion` &mdash; reveal animations and smooth
  scroll are disabled when the user opts out.
- JSON-LD `Organization` and product offers structured data.
- Open Graph and Twitter Card metadata.
- Canonical link, sitemap, robots, web manifest.
- Asset cache headers via Netlify/Vercel configs.
- Lazy loading on below-fold product imagery.

---

## Editorial guardrails

Per the brand brief, customer-facing copy avoids unverified medical
claims. Do not introduce wording like *cures*, *treats*, *heals* or
clinical claims unless independently verified and approved. Safe
language used throughout: *helps moisturise*, *supports daily skin care*,
*refreshing feel*, *suitable for everyday use*, *botanical-inspired*.

A short legal note in the footer reaffirms this.

---

## License

See `LICENSE`. Brand assets are proprietary; the non-brand source code is
provided for the operation of the official MOEMODI website.

&copy; 2026 MOEMODI (PTY) LTD.
