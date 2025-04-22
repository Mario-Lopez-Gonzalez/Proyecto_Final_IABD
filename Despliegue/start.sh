#!/bin/bash

# start.sh - Script para subir imágenes y las imágenes preprocesadas desde el volumen local a HDFS
# y restaurar un backup de PostgreSQL.

# Iniciar docker compose
echo "Iniciando docker compose..."
sudo docker compose up -d
echo "Espere un momento..."
sleep 5

# =============================================
# CONFIGURACIÓN HDFS
# =============================================

# Se monta en el contenedor: ./hdfs-upload:/hdfs-upload
# Se subirán:
#   - Los archivos de ./hdfs-upload/imagenes a /ondaakin/imagenes
#   - Los archivos de ./hdfs-upload/imagenes_preprocesadas a /ondaakin/imagenes_preprocesadas

NOMBRE_CONTENEDOR_HDFS="g3-namenode"

# Configuración para imágenes normales
DIRECTORIO_LOCAL_IMAGENES="./hdfs-upload/imagenes"
DIRECTORIO_HDFS_IMAGENES="/ondaakin/imagenes"

# Configuración para imágenes preprocesadas
DIRECTORIO_LOCAL_PREPROCESADAS="./hdfs-upload/imagenes_preprocesadas"
DIRECTORIO_HDFS_PREPROCESADAS="/ondaakin/imagenes_preprocesadas"

# Función para subir archivos desde un directorio local a un directorio en HDFS
subir_archivos_hdfs() {
    local directorio_local="$1"
    local directorio_hdfs="$2"
    
    if [ -d "$directorio_local" ] && [ -n "$(ls -A "$directorio_local")" ]; then
        echo "Subiendo archivos de $directorio_local a HDFS en $directorio_hdfs..."
        
        for archivo in "$directorio_local"/*; do
            nombre_archivo=$(basename "$archivo")
            echo "Procesando $nombre_archivo..."
            
            # Extraer la parte de la ruta a partir de "./hdfs-upload"
            subpath="${directorio_local#"./hdfs-upload"}"
            
            docker exec "$NOMBRE_CONTENEDOR_HDFS" bash -c \
                "su - hadoop -c 'cd /; hdfs dfs -test -e ${directorio_hdfs}/${nombre_archivo}' && \
                 echo 'El archivo ${nombre_archivo} ya existe en HDFS en ${directorio_hdfs}, omitiendo...' || \
                 su - hadoop -c 'cd /; hdfs dfs -put /hdfs-upload${subpath}/${nombre_archivo} ${directorio_hdfs}/'"
        done
        
        # Ajustar permisos en HDFS para la carpeta destino
        docker exec "$NOMBRE_CONTENEDOR_HDFS" bash -c \
            "su - hadoop -c 'hdfs dfs -chmod -R 777 ${directorio_hdfs}'"
    else
        echo "No se encontraron archivos en $directorio_local para subir a HDFS en ${directorio_hdfs}."
    fi
}

# Subir imágenes normales
subir_archivos_hdfs "$DIRECTORIO_LOCAL_IMAGENES" "$DIRECTORIO_HDFS_IMAGENES"

# Subir imágenes preprocesadas
subir_archivos_hdfs "$DIRECTORIO_LOCAL_PREPROCESADAS" "$DIRECTORIO_HDFS_PREPROCESADAS"

# =============================================
# CONFIGURACIÓN POSTGRESQL
# =============================================

# Variables de PostgreSQL
POSTGRES_CONTAINER="g3-postgres"
POSTGRES_USER="root"
POSTGRES_PASSWORD="example"
POSTGRES_DB="metabase"
BACKUP_DIR="./postgres-backup"
BACKUP_FILE="$BACKUP_DIR/metabase_backup.dump"

# Función para restaurar backup en PostgreSQL
restaurar_backup_postgres() {
    echo "Verificando contenedor PostgreSQL..."
    if ! docker ps --filter "name=$POSTGRES_CONTAINER" | grep -q "$POSTGRES_CONTAINER"; then
        echo "Error: Contenedor $POSTGRES_CONTAINER no está en ejecución."
        return 1
    fi

    echo "Buscando archivo de backup..."
    if [ ! -f "$BACKUP_FILE" ]; then
        echo "No se encontró el backup en $BACKUP_FILE"
        return 0
    fi

    echo "Restaurando backup..."
    # Terminar conexiones activas en la base de datos "metabase"
    docker exec -it "$POSTGRES_CONTAINER" psql -U root -d postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'metabase';"
    
    # Eliminar y recrear la base de datos
    docker exec -it "$POSTGRES_CONTAINER" dropdb -U root metabase
    docker exec -it "$POSTGRES_CONTAINER" createdb -U root metabase

    # Importar el backup
    docker exec -i "$POSTGRES_CONTAINER" pg_restore -U root -d metabase -F c < "$BACKUP_FILE"

    echo "Reiniciando PostgreSQL..."
    docker stop "$POSTGRES_CONTAINER"
    docker start "$POSTGRES_CONTAINER"

    # Esperar a que el servicio se estabilice
    sleep 5
    echo "Verificando restauración..."
    if docker exec "$POSTGRES_CONTAINER" psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT 1" &> /dev/null; then
        echo "Backup restaurado exitosamente en $POSTGRES_DB"
    else
        echo "Error en la restauración"
        return 1
    fi
}

# Llamar a la función para restaurar el backup
restaurar_backup_postgres
