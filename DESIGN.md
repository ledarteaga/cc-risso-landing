# Design

<!-- impeccable:design-schema 1 -->

## Status of this document

This file is the **living design contract** for the Risso re-design. It records:

1. The **durable brand system** already established by real assets (colors from the official logo — verified, not approximated).
2. The **client's redesign directives** (post-client-meeting corrections) that any working session must honor.

The visual world is treated as a **replace/redesign**: the incumbent one-page look is *evidence/anti-reference*, not authority. The working session builds a new committed world that satisfies the constraints below and then ships DESIGN.md's final tokens + DESIGN.json at finish (per new-work flow). This file is the starting contract, not the final token bank.

---

## Mode

The public marketing site is a **Persuade** surface (landing/marketing: the visitor decides and acts — understands Risso, then visits or contacts). One idea should land per section, one page at a time.

---

## Client redesign directives (binding)

These come from the post-meeting corrections and take precedence over the old design:

1. **Storytelling section order on the HOME page (Inicio only):** `Sobre Risso → Descuentos → Tiendas → Contacto`.
   The home page presents each topic as a section in this exact order (brand story first, then converts to visit), linking out to the dedicated pages. This is the **Inicio flow**, not a nav mandate.
2. **Multi-page, not one-page:** split into separate pages/routes instead of the current long one-pager. Pages: Inicio / Sobre Risso / Descuentos / Tiendas / Contacto, with a consistent shared nav + footer. The storytelling order (directive 1) is how the **Inicio** page sequences its sections; the dedicated pages hold the depth.
3. **Fewer cards:** reduce the card-heavy pattern of the incumbent build. Favor editorial/storytelling layout, lists, and focused sections over a grid of equal-weight cards.
4. **Use brand colors:** lean on the brand **green** and **blue** as the visual identity across sections.
5. **Black footer:** the footer stays **black** (brand-anchor).
6. **Remove lateral padding on `xl` screens:** at large viewports the content widens — no generous side gutters on xl.
7. **UX/copy reference (positive):** `https://jockeyplaza.com.pe/` — mirror its **information architecture, per-section page model and copywriting tone** (see "IA modeled on Jockey Plaza" below).
8. **Brand/reference:** current `https://ccrisso.com` — source of the real brand story, tone and tenants (see PRODUCT.md "Evidence on Hand").
9. **Hero = video, modeled on Jockey Plaza.** The home hero should **attract the eye with a full-bleed autoplay (muted, looping) background video** of the center, with the brand line/claim overlaid — like Jockey's "Te vas a querer quedar" over its video. **The client does not have the video yet**, so design must be video-ready with a graceful fallback: use a real photo poster (`assets/img/cc/*.jpeg`) as the poster/first-frame and a `<video>` element with `poster` + a photographic fallback so it ships now and renders the video the moment the asset arrives. Do not block the build on the missing asset.

---

## IA modeled on Jockey Plaza (reference for structure, not a clone)

Jockey Plaza's strength is **one focused topic per page** with a clear shared nav + rich black footer — the exact posture the client asked for. Map its proven blocks to Risso's content (adapted, branded, not copied):

| Jockey Plaza pattern | Risso application |
|---|---|
| Storytelling hero + positioning ("Te vas a querer quedar" → brand line), **full-bleed background video** | Inicio hero: **video full-bleed (autoplay/muted/loop)** + brand line in Risso's own words. Video not available yet → rhythmic photo poster (`assets/img/cc/*.jpeg`) with a `<video poster>` element, video-ready |
| Directorio (Tiendas / Gastronomía / Centro Financiero) | **Tiendas** page grouped by Risso's real taxonomy (Supermercados, Bancos y Financieras, Restaurantes, Entretenimiento, Ropa y Accesorios, etc.) |
| "Descuentos del mes" → dedicated page | **Descuentos** page |
| "Disfruta los eventos" | optional event/agenda block (Risso: eventos, promos) |
| "¿Quieres visitarnos?" (location, hours, transport) | **Contacto** page: dirección, horarios, transporte, estacionamiento, contacto |
| "¿Tienes alguna duda? Contáctanos" contact blocks | Contact form + channels |
| Rich black footer (Explora / Información / legal) | **Black footer**: nav, legal (libro de reclamaciones si aplica), redes, horario |
| Copy tone: clear, warm, benefit-led, "para ti y tu familia" | Risso's own voice (see Content section) |

**Client-ordered order of the main nav: Inicio → Sobre Risso → Descuentos → Tiendas → Contacto** (Jockey orders by department; Risso's client explicitly set storytelling-first ordering — honor the client order over Jockey's).

---

## Content section

**Real content, from ccrisso.com / Risso (do not invent):**
- Story (real history): Casa Hacienda de Don Manuel Risso Diggione, Fundo Lobatón, project from the 1950s, construction 1966, opened 1968 (anchors Todos & Monterrey; brands Yompián, Labrousse, Marcantonio).
- Taglines: "Un centro comercial con historia", "Más de 50 años contigo", "Ven y disfruta en familia", "nos renovamos pensando en ti".
- Tenant taxonomy: Supermercados, Bancos y Financieras, Restaurantes, Entretenimiento, Peluquería y Belleza, Ropa y Accesorios, Tecnología, Deportes, Regalos, Varios.
- Known trademarks shown on the site: Platanitos, Wester, Plaza Vea, BCP, McDonald's, Casino.
- No fabricated tenants, stats, testimonials or commercial claims. Mark anything synthetic explicitly.
- Spanish (es-PE).

---

## Brand tokens (verified from official logo assets)

Sampled from `assets/img/logo.png` and `assets/img/logo-white.png` (RGBA, opaque pixels). These are **verified**, not approximated.

### Color

| Role | Token | Hex | Notes |
|---|---|---|---|
| Brand green (primary) | `--brand-green` | **`#02AF5B`** | Dominant green in the logo mark |
| Brand green (light) | `--brand-green-light` | `#41C384` | Secondary/illustrative green |
| Brand blue (primary) | `--brand-blue` | **`#2B58A8`** | Dominant blue in the logo mark |
| Brand blue (light) | `--brand-blue-light` | `#5F81BD` | Lighter blue for tints/surfaces |
| Ink / footer | `--ink` / `--footer` | **`#000000`** | Black footer per directive 5 |
| Background (light) | `--bg` | `#FFFFFF` (or near-white neutral) | Clean light ground for brand surfaces |

Contrast: verify text on green (`#02AF5B`) and blue (`#2B58A8`) and on black footer meets WCAG AA (white text on these needs checking; the blue is dark enough for white text, treat green as accent/fill with dark or white text verified for AA).

### Typography

**Brand typeface: Futura** (verified — the whole family is in `/Users/ledarteaga/Developer/risso/fonts/`). It is the center's brand font and should drive the display/headline voice.

Available weights/styles in `fonts/` (desktop TTF/OTF):
- Light, Light Italic (+ `Futura-CondensedLight.otf`)
- Book, Book Italic
- Medium, Medium Italic (+ `futura medium condensed bt.ttf`)
- Heavy, Heavy Italic
- Bold, Bold Italic
- Extra Black (`Futura Extra Black font.ttf`, `Futura XBlk BT.ttf`)
- `futur.ttf`, `futura light bt.ttf`, `unicode.futurab/bb.ttf`, `tt0205m_.ttf`

Usage direction: Futura for display/headlines (geometric, confident — very on-brand for the storytelling home). Body can stay Futura for full brand cohesion or pair with a clean body face if readability suffers at small sizes — decide during build.
**Web note:** the files are desktop TTF/OTF. Convert the needed weights to **self-hosted WOFF2** (e.g. via `fonttools pyftsubset`/`woff2_compress`) and serve from the project's files per the handoff hero rule — **no hosted font stylesheet** (no fonts.googleapis.com). Keep the number of weights low (e.g. Book/Medium + Heavy or Extra Black for display).

### Spacing / radius / motion

Re-defined by the working session under the new world; keep the rule "more space above a heading than below it" and one spacing rhythm throughout.

---

## Content rules

- **Real content only:** preserve real store names, photos (`assets/img/cc/`, `assets/img/tenants/`), copy and data from ccrisso/Risso.
- No fabricated tenants, stats, testimonials or commercial claims. Mark anything synthetic explicitly.
- Spanish (es-PE).

---

## Working-skills contract (how skills apply to this project)

When working this project, load these skills and use them as described:

- **`impeccable`** — the driver: run `impeccable context` (loads this PRODUCT.md + DESIGN.md), then the applicable verb (`critique` for UX review of the incumbent, `shape` to plan IA/wireframe before code, `distill` for fewer-cards, `colorize`/`typeset`/`layout` for brand alignment, `adapt` for the xl padding-responsive rule, `audit` for a11y/perf). Finish with the finish-review + documenter so DESIGN.md + DESIGN.json land.
- **`claude-design`** — process & taste for committing to the surface (Decide/Persuade), anti-slop, building each page as self-contained HTML, verifying in browser.
- **`design-md`** — final token spec (green/blue/black tokens above) as a machine-readable DESIGN.md/DTCG export.
- **`sketch`** — 2–3 structural variants of the multi-page IA (order, nav, per-page composition) to align before committing.
- **`taste`** — calibrate iterations against the human's aesthetic feedback.

---

## Open / unresolved

- Exact button treatment, nav style, hero composition and per-page visual world → decided by the working session (new-work), then committed to DESIGN.md at finish.
- Whether the green accent reads best dark-text or white-text on fills → verify contrast during build.
