# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML/CSS/JS — several `.html` pages (one route per user-facing screen), no build step. Chosen to keep the deliverable self-contained and directly openable, and because the client explicitly wants to move from a one-page scroll to a **multi-page** site. This is a user recommendation recorded here so later work does not re-litigate the stack.

## Users

- **Primary:** local visitors of Centro Comercial Risso (Lince, Lima) and prospective shoppers looking for stores, discounts, food and practical info (location, parking, hours). They arrive to *understand who Risso is*, *see what to buy / where*, and *come visit*.
- **Secondary:** prospective tenants / commercial prospects (existing "Alquila un local" / investment CTA) and local media / community.

## Product Purpose

A public-facing marketing site for Centro Comercial Risso — a neighborhood shopping center on Av. Arequipa 2201, Lince — with more than 50 years of history. It must convey brand identity, tell the center's story, surface discounts and stores, and drive visits (location, hours, transport, parking). Success = the visitor understands what Risso is and why it matters, then chooses to visit or contact.

## Positioning

Risso is a **centro comercial con historia** in the heart of Lince ("más de 50 años contigo", "un espacio de reencuentro"). Its differentiating claim a nearby competitor could not copy: decades of local roots embedded in Lince, plus everyday convenience (supermarket, banks, gastronomy, cinemas, parking) in one compact commercial strip.

## Operating Context

- Spanish (Peru) content; `lang="es-PE"`.
- Real photos of the center and its tenants available under `assets/img/cc/` and `assets/img/tenants/` (use these; do not invent imagery).
- Target modern 2025–2026 viewports (360 → 1920 wide), must avoid horizontal scroll.
- Client references for UX / section order / copywriting: `https://jockeyplaza.com.pe/` (positive reference). Brand/tone reference: current `https://ccrisso.com`.

## Capabilities and Constraints

- Multi-page structure required by the client: **Sobre Risso → Descuentos → Tiendas → Contacto** (storytelling order).
- **One page per section** — client rejected the current one-page long-scroll approach; do not rebuild as a single long scroll.
- **Fewer cards** than the incumbent design — reduce card-heavy patterning.
- **Brand colors** green + blue (see DESIGN.md tokens), keep **black footer**.
- Remove lateral padding on **xl** screens (content can breathe wider at large viewports).
- Preserve real copy, labels, store names and data (do not replace with generic filler); only use synthetic material clearly marked as such.

## Brand Commitments

- Name: **Centro Comercial Risso** (logotipo: "R" mark).
- Brand colors derived from the official logo assets (verified RGB, see DESIGN.md): green and blue primaries, black footer.
- Tone: familiar, welcoming, local, but polished and trustworthy (reference the UX/copy of Jockey Plaza, not a cold corporate tone).
- Use the real logo files: `assets/img/logo.png` (dark) and `assets/img/logo-white.png` (light/on-dark).

## Evidence on Hand

- Official logo assets: `assets/img/logo.png`, `assets/img/logo-white.png` (color-sampled for brand tokens).
- Photography of the center: `assets/img/cc/*.jpeg`.
- Photography of tenants/stores: `assets/img/tenants/*.jpeg`.
- Incumbent implementation: `index.html` (one-page, to be replaced/reorganized per the redesign directives).
- Current public site `https://ccrisso.com` — includes the real brand story and tenant taxonomy below.

### Real brand story (from ccrisso.com/quienes-somos) — use, do not invent

- Risso sits on what was the **Casa Hacienda de Don Manuel Risso Diggione**, which with his brother Roberto belonged to **Fundo Lobatón**.
- The shopping-center project was commissioned by Sr. Manuel Risso at the end of the **1950s** (architect: Granadino); construction began **1966** with anchors **Todos** and **Monterrey**.
- Officially opened **1968**, with brands **Yompián, Labrousse, Marcantonio** among others.
- Theme from the current site: **"Un centro comercial con historia"**, "Más de 50 años contigo", "Ven y disfruta en familia", "nos renovamos pensando en ti".

### Real tenant taxonomy (from ccrisso.com/tiendas)

Supermercados · Bancos y Financieras · Restaurantes · Entretenimiento · Peluquería y Belleza · Ropa y Accesorios · Tecnología · Deportes · Regalos · Varios.
Known anchors/logos on the homepage: Platanitos, Wester, Plaza Vea, BCP, McDonald's, Casino.

## Product Principles

1. **Tell the story, then sell the visit** — lead with who Risso is (history, neighborhood) before discounts/stores/contact.
2. **Divide, don't scroll** — one clear page per section instead of a marathon one-pager.
3. **Brand is the signal** — green and blue carry the identity; black footer anchors; cards are the exception, not the default.
4. **Give visitors the decision they came to make** — directions, hours, parking, and contact must be easy to reach.
5. **Real assets over invention** — use the actual photos, store names and copy; never fabricate tenants, data or claims.

## Accessibility & Inclusion

- Spanish-first content with a clear reading order; ensure contrast for text on green/blue surfaces and on the black footer (WCAG AA as the working bar).
- Keyboard-focusable nav/controls and visible focus states across every page.
