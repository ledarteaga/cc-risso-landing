# CC Risso — Landing

Landing de una sola página para el **Centro Comercial Risso** (Av. Arequipa 2201, Lince, Lima). Más de 50 años reuniendo a Lince (fundado 1972).

🔗 **Demo local:** abre [`index.html`](./index.html) en cualquier navegador moderno — no requiere build, ni servidor, ni dependencias.

---

## Stack

- **HTML5** semántico (un solo archivo: `index.html`)
- **CSS** vanilla con variables de diseño (sin preprocesador, sin Tailwind, sin frameworks)
- **JavaScript** vanilla (sin React, sin Vue, sin librerías de animación)
- **Tipografía:** Futura local (12 `@font-face` en `./fonts/`)
- **Imágenes:** WebP/JPEG locales en `./assets/`
- **Sin build step, sin npm install**

## Estructura

```
.
├── index.html              # Landing completa (HTML+CSS+JS inline, ~110 KB)
├── assets/
│   ├── img/                # Logos y assets auxiliares
│   └── img/cc/             # Fotos del CC (DSC08117…DSC08146)
���── fonts/                  # 19 archivos Futura (Light → Extra Black + italics)
├── DESIGN.md               # Design tokens (paleta, type scale, spacing)
├── DESIGN-HANDOFF.md       # Handoff técnico para implementación
├── DESIGN-MANIFEST.json    # Inventario de componentes y decisiones
└── PRODUCT.md              # Contexto de producto y audiencia
```

## Diseño

- **Estética:** cálida tipo Airbnb B (paleta warm con `--warm:#c66b3d` sobre fondo crema)
- **Tipografía:** Futura en 6 pesos (300/400/500/700/800/900) con jerarquía por peso y tamaño
- **Hero:** slideshow de 4 slides con headline a 3 líneas (última palabra en Bold Italic 700), motion interconectado de palabras, ken-burns en la imagen, dots de navegación
- **Navegación:** scrollspy, glass morphism al hacer scroll
- **CTAs:** text links uniformes con flecha animada (`Traducir →`)
- **Responsive:** mobile-first con breakpoints en 720px y 1080px

## Desarrollo local

```bash
# Solo abre el archivo — no necesita servidor
open index.html
```

O si prefieres servidor local (recomendado para desarrollo con DevTools):

```bash
python3 -m http.server 8000
# luego abre http://localhost:8000
```

## Despliegue

Es un sitio estático puro — basta con subir `index.html`, `assets/` y `fonts/` a cualquier hosting:

- **GitHub Pages:** Settings → Pages → Deploy from a branch → `main` / `(root)`
- **Netlify / Vercel:** drag & drop de la carpeta, listo
- **S3 + CloudFront:** `aws s3 sync . s3://bucket --exclude ".git/*" --exclude "*.md"`

## Créditos

- **Cliente:** Centro Comercial Risso
- **Diseño y desarrollo:** Luis Arteaga ([@ledarteaga](https://github.com/ledarteaga))
- **Tipografía:** Futura (Bitstream)
- **Año:** 2026

## Licencia

Código bajo MIT. Imágenes y tipografía son propiedad de sus respectivos titulares.
