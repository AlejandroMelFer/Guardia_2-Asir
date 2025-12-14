#!/bin/bash
set -e

# Configuración
NETWORK_NAME="red_kronoleon"
MYSQL_CONTAINER_NAME="mysqlserver"
WEB_CONTAINER_NAME="webapp"
MYSQL_ROOT="#kr0n0L30N*"
MYSQL_DB="kronoleondb"
MYSQL_USER="usuario"
MYSQL_PASS="usuario"
WEB_DIR="$HOME/webapp"
mkdir -p "$WEB_DIR"

# Comprobar Docker instalado
command -v docker >/dev/null 2>&1 || { echo "ERROR: Docker no está instalado."; exit 1; }

# Crear red Docker
docker network create "$NETWORK_NAME"
echo "Red $NETWORK_NAME creada"

# Crear volumen para MySQL
docker volume create mysql_data || true
echo "Volumen mysql_data creado"

# Descargar imágenes Docker
docker pull nginx:alpine
docker pull mysql:8.0
echo "Imágenes Docker descargadas"

# Lanzar contenedor Nginx
docker run -d --name "$WEB_CONTAINER_NAME" \
  --network "$NETWORK_NAME" \
  -p 8080:80 \
  -v "$WEB_DIR":/usr/share/nginx/html \
  nginx:alpine

# Lanzar contenedor MySQL
docker run -d --name "$MYSQL_CONTAINER_NAME" \
  --network "$NETWORK_NAME" \
  -e MYSQL_ROOT_PASSWORD="$MYSQL_ROOT" \
  -e MYSQL_DATABASE="$MYSQL_DB" \
  -e MYSQL_USER="$MYSQL_USER" \
  -e MYSQL_PASSWORD="$MYSQL_PASS" \
  -v mysql_data:/var/lib/mysql \
  -p 3306:3306 \
  mysql:8.0
sleep 20

# Actualizar contenedor Nginx
docker exec -d "$WEB_CONTAINER_NAME" sh -c "apk update && apk upgrade -y"

# Actualizar contenedor MySQL
docker exec -d "$MYSQL_CONTAINER_NAME" sh -c "apt-get update && apt-get upgrade -y -q"

# Informe final
docker ps
echo "Web: http://localhost:8080"
echo "Directorio de trabajo para la web: $WEB_DIR"
echo "MySQL: puerto (3306), usuario ($MYSQL_USER), contraseña ($MYSQL_PASS), contraseña root ($MYSQL_ROOT)"
