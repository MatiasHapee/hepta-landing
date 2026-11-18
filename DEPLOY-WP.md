# Publicar la landing como portada de heptachile.cl

Esto no toca el sitio en vivo por sí solo. Hay que hacerlo en WordPress (Hostinger) cuando se decida el corte. La tienda WooCommerce sigue en `https://heptachile.cl/tienda/`.

## Qué archivo se publica

| Archivo | Para qué |
| --- | --- |
| `hepta-home-v9.html` | Vista previa estática. Rutas `Imagenes/` y `Public/`. Se abre directo o con `python3 -m http.server`. No se pega en WordPress. |
| `hepta-home-wp.html` | Fragmento listo para pegar en una página. CSS acotado a `#hepta-landing` y fotos en `/wp-content/uploads/hepta-landing/`. |
| `scripts/build-wp-landing.py` | Regenera el fragmento. Si cambia el HTML de diseño, edita `hepta-home-v*.html` y corre `python3 scripts/build-wp-landing.py`. No edites `hepta-home-wp.html` a mano. |

El fragmento no es un documento (`doctype`, `<head>`, `<body>`). Una página de WordPress ya tiene ese esqueleto; pegar otro lo rompe o el editor lo descarta. `<title>`, meta description, canonical y Open Graph van en el plugin SEO, no dentro del widget: en el `<body>` el navegador los ignora.

## Por qué está armado así

- Los estilos van con el prefijo `#hepta-landing#hepta-landing` (dos ids). Astra y Elementor cargan CSS sin capa y a veces después del contenido; un `@layer` perdería contra ese CSS, y un `@scope` solo dejaría la portada sin estilos en un navegador que no lo entienda. El doble id gana a reglas como `#content .entry-content a` sin pintar el resto del sitio.
- El reset (`margin`, `padding`, `box-sizing`, botones, listas) vive dentro de `#hepta-landing`. No hay un `*` suelto sobre `html` o `body`.
- En la página que contiene `#hepta-landing` se ocultan el header y el footer del tema (Astra `#masthead` / `#colophon` y el header/footer de Elementor Theme Builder) y se anula el padding del contenedor. `/tienda/`, el carrito y el checkout no llevan ese bloque, así que conservan el menú, el carrito y el footer de la tienda.
- `overflow-x` queda en `html`, no en el bloque: en el bloque rompería el header sticky y el botón de WhatsApp.
- Las fotos no pasan por Medios → Añadir. La mediateca aplana carpetas, cambia nombres y mete el archivo en `uploads/2026/11/`. El HTML pide la ruta fija de abajo.

Si la instalación no está en la raíz del dominio, reemplaza en el fragmento la cadena `/wp-content/uploads/hepta-landing` por la ruta real y vuelve a probar.

## 1. Subir las imágenes

En hPanel → Sitios web → Administrar → Administrador de archivos (o por SFTP), entra a `public_html`.

Crea la carpeta y copia **manteniendo los nombres**, espacios incluidos:

```text
public_html/wp-content/uploads/hepta-landing/Imagenes/
public_html/wp-content/uploads/hepta-landing/Public/
```

Desde este repo, sube las carpetas `Imagenes/` y `Public/` tal cual. El HTML solo pide los `.webp`; los PNG y JPG originales no se muestran, pero la copia completa evita dejar fuera un archivo o renombrar `Fotos Categoria` y `Terciados`.

Comprueba en el navegador, antes de armar la página, que esta URL responde 200:

`https://heptachile.cl/wp-content/uploads/hepta-landing/Imagenes/Banners/banner-asesoria-terreno.webp`

Icono del sitio: en Apariencia → Personalizar → Identidad del sitio (o Ajustes → Generales → Icono del sitio) sube `Public/favicon-192.png`. WordPress no usa el `favicon.svg` como icono del sitio.

## 2. Crear la página

1. Páginas → Añadir nueva. Título interno: `Inicio`. Si ya existe una página con el slug `inicio`, renombra la portada vieja (por ejemplo a `Portada anterior`) antes, para no pisar el slug. Como portada, la URL pública igual va a ser `/`.
2. Editar con Elementor. Engranaje (abajo a la izquierda) → Ajustes de página → Diseño de página → **Elementor Canvas**. Canvas saca el header, el footer y el título de Astra. El CSS del fragmento también los oculta por si el diseño de página queda en Default.
3. Un solo contenedor, ancho completo, hueco 0, padding 0 en el contenedor y en la columna. Sin fondo de sección.
4. Widget **HTML**. Pega **todo** el contenido de `hepta-home-wp.html`, desde el comentario inicial hasta el `</div>` final. Tiene que pegarlo un administrador: un rol sin `unfiltered_html` pierde `<style>` y `<script>`, y la página queda sin diseño ni sliders.
5. No uses el editor visual ni el bloque de párrafo. Si Elementor avisa que el widget HTML quitó el script, pega el mismo fragmento en Elementor → Código personalizado, ubicación Body, solo en esta página, o con el plugin WPCode en el contenido de la página.
6. Actualizar / Publicar.

El formulario de cotización sigue siendo el embed de Hapee (`data-zentru-form="774691286/solicitud-de-cotizaci-n-landing-hepta"` y `https://beta.hapee.ai/static/form-embed.js`). Campos y colores se editan en Hapee, no en este HTML.

## 3. Dejarla como portada

Ajustes → Lectura:

- La página de inicio muestra: **Una página estática**.
- Portada: `Inicio` (la página nueva).
- Página de entradas: la que ya apunta al blog, si existe. No elijas la portada nueva.

No borres la portada vieja de Elementor en el primer corte. Solo deja de ser la portada. Si algo falla, Ajustes → Lectura vuelve a apuntar a esa página.

WooCommerce → Ajustes → Productos → General → **Página de la tienda** tiene que seguir siendo la página cuya URL es `/tienda/`, no la portada nueva.

## 4. Menú Inicio / Tienda

Hay dos menús distintos.

**El de la landing** (solo se ve en `/`) ya va en el HTML:

- Logo del header, logo del footer e **Inicio** → `/` (la propia portada).
- **Tienda E-Commerce** (header) y **Tienda** (footer) → `https://heptachile.cl/tienda/`, en la misma pestaña.
- Bajo 860 px el header esconde Productos, Blog, Tienda E-Commerce y Contacto, igual que la maqueta. En el celular la entrada a la tienda es el enlace **Tienda** del footer y las tarjetas de categoría.

**El del tema** (el que sigue en `/tienda/`, ficha de producto, carrito y checkout):

- Apariencia → Menús, o el header de Elementor si la tienda usa Theme Builder.
- Inicio debe ir a `/` (la portada nueva), no a la página vieja de Elementor ni a `/tienda/`.
- Tienda / Tienda E-Commerce debe ir a `https://heptachile.cl/tienda/`.
- No cambies Blog, Contacto, categorías, catálogos ni WhatsApp.

## 5. SEO de la portada

En Yoast, Rank Math o el plugin que esté activo, en la página Inicio:

- Título: `Hepta Chile | Materiales de construcción y andamios en Chile`
- Meta description: `Hepta Chile: venta de andamios, terciados, impermeabilizantes, geosintéticos y productos para asfalto. Despacho a todo Chile. Cotiza y compra online.`
- Canonical y URL de Open Graph: `https://www.heptachile.cl/`
- Indexable.

El JSON-LD `HardwareStore` va dentro del fragmento (dirección, teléfonos, horario y categorías). La `url` del negocio sigue siendo `https://www.heptachile.cl/` porque esa URL ahora es esta portada, no la tienda. Si el plugin SEO imprime otro schema del mismo negocio y Search Console marca duplicado, deja el del fragmento y apaga el del plugin en la portada.

## 6. Caché de Hostinger y LiteSpeed

Después de publicar, en este orden:

1. Elementor → Herramientas → Regenerar archivos CSS y datos → Guardar cambios.
2. Si está el plugin LiteSpeed Cache: LiteSpeed Cache → Caja de herramientas → Vaciar todo. Si la portada no anima el hero o el carrusel, en LiteSpeed Cache → Optimizar página excluye `/` de la combinación y del aplazamiento de JS y vuelve a vaciar.
3. hPanel → Sitios web → Administrar → Rendimiento o Avanzado → Borrar caché (la caché de Hostinger / LiteSpeed del servidor). Si hay CDN de Hostinger activo, bórrala también.
4. Prueba en una ventana privada. Un refresco normal puede seguir mostrando la portada vieja.

## 7. Pruebas después del corte

Portada (`/`):

- Se ve la landing a ancho completo, sin el header naranja de Astra encima ni un `<h1>` “Inicio” del tema.
- Hero, contadores, carrusel de categorías y banda de líneas destacadas se mueven.
- **Tienda E-Commerce** y el **Tienda** del footer abren `https://heptachile.cl/tienda/` en la misma pestaña.
- Logo e **Inicio** vuelven a `/`.
- Una tarjeta (Andamios, Terciados, etc.) abre su categoría de WooCommerce. Blog abre `/blog/`. WhatsApp abre `https://wa.me/56987690593`.
- El formulario de Hapee carga dentro de la tarjeta (iframe), sin fondo doble.
- En un celular (~360 px) no hay scroll horizontal. El footer muestra Tienda. Los títulos grandes siguen en `vw` / `clamp`, no en px fijos.

Tienda, carrito y checkout (con la caché ya vaciada):

- `/tienda/` responde y muestra el catálogo con el header del tema, para que el carrito siga accesible.
- Agrega un producto, ábrelo en el carrito, cambia la cantidad y quítalo.
- Entra a finalizar compra. El formulario carga y Webpay aparece como medio de pago. No completes un pago real.
- WooCommerce → Ajustes → Avanzado confirma que las páginas de carrito y de finalizar compra siguen siendo las de siempre.

## Enlaces que cambiaron

| Dónde | Antes | Ahora | Por qué |
| --- | --- | --- | --- |
| Header, botón Tienda E-Commerce | `https://heptachile.cl/` en pestaña nueva | `https://heptachile.cl/tienda/` en la misma pestaña | Era el acceso a la tienda y apuntaba a la home, que pasa a ser esta landing. |
| Footer, Navegación, enlace nuevo Tienda | no existía | `https://heptachile.cl/tienda/` | Bajo 860 px el header esconde el botón. El footer queda como entrada explícita a la tienda. |
| Footer, Inicio | `https://heptachile.cl/` en pestaña nueva | `/` | Inicio es la portada (esta landing), no la tienda. |
| Logo del header | `#` | `/` | Volver al inicio del sitio. |
| Logo del footer | `https://heptachile.cl/` en pestaña nueva | `/` | La marca vuelve a la portada. |

Sin cambio a propósito: canonical, `og:url` y `url` del JSON-LD siguen en `https://www.heptachile.cl/` (la portada). Categorías, blog, nosotros, contacto del sitio, catálogos, ferretería, WhatsApp, teléfonos, correo y el embed de Hapee quedan como estaban.

## Si hay que volver atrás

Ajustes → Lectura → Portada: la página anterior. Vacía de nuevo la caché de Elementor, LiteSpeed y Hostinger. Las imágenes en `uploads/hepta-landing/` pueden quedarse.
