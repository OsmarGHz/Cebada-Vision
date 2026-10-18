# Despliegue de CebadaVision (agrocebada-pagina)

Guía para quien administre el hosting o el VPS. La aplicación es un **sitio estático**: HTML, JS,
CSS y cuatro archivos de datos. No tiene backend, base de datos ni variables de entorno. El
modelo ya viene precalculado en `public/data/`; el navegador solo lee esos archivos.

Repositorio: https://github.com/David54s/agrocebada-pagina (rama `main`).

## 1. Generar el build

Requisitos: Node.js 20 o superior (probado con 22 y 24).

```bash
git clone https://github.com/David54s/agrocebada-pagina.git
cd agrocebada-pagina
npm ci
npm run validate   # revisa los datos; debe terminar sin "✗"
npm run build      # genera la carpeta dist/
```

`dist/` pesa unos 5 MB (el archivo grande es `data/series.json`, ~4 MB; se carga solo al abrir
la ficha de una parcela). Las rutas son relativas y usan `#/` (HashRouter), así que funciona en
cualquier subcarpeta y no necesita reglas de reescritura.

## 2. Opción A — Hosting estático gratuito (lo más rápido)

**Netlify** o **Vercel**: conectar el repo, comando de build `npm run build`, carpeta de
publicación `dist`. Cada push a `main` redespliega solo.

**GitHub Pages**: en el repo, Settings → Pages → "Deploy from a branch". Subir el contenido de
`dist/` a una rama `gh-pages` (por ejemplo con `npx gh-pages -d dist`) o usar GitHub Actions. La
URL queda como `https://david54s.github.io/agrocebada-pagina/`.

## 3. Opción B — VPS propio con Nginx

```bash
# en el servidor (Ubuntu/Debian)
sudo apt update && sudo apt install -y nginx
sudo mkdir -p /var/www/cebadavision
# copiar el contenido de dist/ (desde la máquina donde se hizo el build):
#   scp -r dist/* usuario@servidor:/var/www/cebadavision/
sudo chown -R www-data:www-data /var/www/cebadavision
```

`/etc/nginx/sites-available/cebadavision`:

```nginx
server {
    listen 80;
    server_name cebadavision.ejemplo.mx;   # o la IP del servidor

    root /var/www/cebadavision;
    index index.html;

    # compresión: series.json pasa de ~4 MB a ~0.6 MB
    gzip on;
    gzip_types application/json application/javascript text/css application/geo+json;
    gzip_min_length 1024;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # los datos del modelo cambian poco; cache de 1 hora
    location /data/ {
        add_header Cache-Control "public, max-age=3600";
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/cebadavision /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
# HTTPS (recomendado; el jurado abrirá el enlace desde cualquier red):
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d cebadavision.ejemplo.mx
```

Si no hay dominio, sirve con la IP por HTTP; funciona igual, solo sin candado.

## 4. Opción C — Docker (si el VPS ya usa contenedores)

```dockerfile
# Dockerfile en la raíz del repo de la app
FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
```

```bash
docker build -t cebadavision .
docker run -d --name cebadavision -p 80:80 --restart unless-stopped cebadavision
```

## 5. Verificación después de desplegar

1. Abrir la URL en una **ventana de incógnito** y desde un **celular con datos** (no la red de la
   oficina): debe cargar sin pedir usuario.
2. Buscar la parcela `AGC_003` en la caja "Consultar por ID_POLIGONO": debe mostrar la ficha con
   estimación, rango, semáforo y la tarjeta "¿Cómo se llegó a este número?".
3. Entrar a "Modelo" y descargar el CSV: debe tener 59 filas.
4. Si el navegador muestra "Datos de demostración" en una franja amarilla, se subió un build viejo:
   volver a copiar `public/data/` del repo y reconstruir.
5. Dejar la página en línea **al menos hasta el 20 de noviembre de 2026**.

## 6. Actualizar los datos del modelo (si cambia)

En el repo de modelación (`Cebada-Vision`): `python src/modelo_final.py` y `python src/exportar_app.py`
generan `data/app/`. Copiar esos cuatro archivos a `public/data/` de la app, `npm run validate`,
`npm run build` y volver a publicar `dist/`. No hay que tocar código de la app.
