#import os
#import time
#from watchdog.observers import Observer
#from watchdog.events import FileSystemEventHandler
#from pyspark.sql import SparkSession
#from hdfs import InsecureClient  # Importamos el cliente HDFS
#
## Configuración
#LOCAL_FOLDER = '/app/local_images'  # Carpeta local a monitorear
#HDFS_FOLDER = '/ondaakin/imagenes'  # Carpeta en HDFS
#HDFS_FOLDER_PREP = '/ondaakin/imagenes_preprocesadas'  # Carpeta en HDFS
#HDFS_URL = 'http://g3-namenode:50070'  # URL del NameNode (WebHDFS)
#
## Crear una sesión de Spark
#def create_spark_session():
#    return SparkSession.builder.appName("UploadImagesToHDFS").getOrCreate()
#
## Crear cliente HDFS
#def create_hdfs_client():
#    return InsecureClient(HDFS_URL, user='hadoop')  # Cambia 'hadoop' por tu usuario HDFS
#
## Subir archivo a HDFS usando el cliente Python
#def upload_to_hdfs(hdfs_client, file_path):
#    try:
#        hdfs_path = os.path.join(HDFS_FOLDER, os.path.basename(file_path))
#        
#        # Subir el archivo
#        with open(file_path, 'rb') as local_file:
#            hdfs_client.write(hdfs_path, local_file, overwrite=True)
#            
#        print(f"Archivo {file_path} subido a HDFS en {hdfs_path}")
#        return True
#    except Exception as e:
#        print(f"Error al subir {file_path} a HDFS: {e}")
#        return False
#
## Clase para manejar eventos de archivo
#class ImageEventHandler(FileSystemEventHandler):
#    def __init__(self, hdfs_client):
#        self.hdfs_client = hdfs_client
#
#    def on_created(self, event):
#        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
#            print(f"Nueva imagen detectada: {event.src_path}")
#            # Esperar a que el archivo esté completamente escrito
#            time.sleep(1)
#            upload_to_hdfs(self.hdfs_client, event.src_path)
#
## Monitoreo de la carpeta local
#def monitor_folder():
#    spark = create_spark_session()  # Aunque no lo usamos directamente, lo mantenemos por si acaso
#    hdfs_client = create_hdfs_client()
#    
#    # Verificar si existe la carpeta HDFS, si no, crearla
#    if not hdfs_client.status(HDFS_FOLDER, strict=False):
#        hdfs_client.makedirs(HDFS_FOLDER)
#    
#    event_handler = ImageEventHandler(hdfs_client)
#    observer = Observer()
#    observer.schedule(event_handler, path=LOCAL_FOLDER, recursive=False)
#    observer.start()
#    print(f"Monitoreando la carpeta: {LOCAL_FOLDER}")
#    
#    try:
#        while True:
#            time.sleep(1)
#    except KeyboardInterrupt:
#        observer.stop()
#    observer.join()
#
#if __name__ == "__main__":
#    monitor_folder()

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pyspark.sql import SparkSession
from hdfs import InsecureClient
from PIL import Image
import matplotlib.pyplot as plt
from ultralytics import YOLO
import numpy as np

# Configuración
LOCAL_FOLDER = '/app/local_images'
HDFS_FOLDER = '/ondaakin/imagenes'
HDFS_FOLDER_PREP = '/ondaakin/imagenes_preprocesadas'
HDFS_URL = 'http://g3-namenode:50070'
MODEL_PATH = "/app/yolo11l-seg_batch8/best.pt"

# Crear una sesión de Spark
def create_spark_session():
    return SparkSession.builder.appName("UploadImagesToHDFS").getOrCreate()

# Crear cliente HDFS
def create_hdfs_client():
    return InsecureClient(HDFS_URL, user='hadoop')

# Subir archivo a HDFS
def upload_to_hdfs(hdfs_client, file_path, hdfs_target_folder):
    try:
        hdfs_path = os.path.join(hdfs_target_folder, os.path.basename(file_path))
        
        with open(file_path, 'rb') as local_file:
            hdfs_client.write(hdfs_path, local_file, overwrite=True)
            
        print(f"Archivo {file_path} subido a HDFS en {hdfs_path}")
        return True
    except Exception as e:
        print(f"Error al subir {file_path} a HDFS: {e}")
        return False

# Procesar imagen con YOLO y guardar imagen con detecciones
def process_image_with_yolo(image_path, hdfs_client):
    try:
        # Cargar modelo YOLO
        model = YOLO(MODEL_PATH)
        
        # Cargar la imagen
        img = Image.open(image_path)
        
        # Realizar predicción
        resultados = model(img)
        
        # Generar imagen con anotaciones
        pred = resultados[0].plot()  # Esto devuelve un numpy array
        
        # Convertir numpy array a imagen PIL
        #pred_img = Image.fromarray(pred[..., ::-1])  # Convertir BGR (OpenCV) a RGB
        
        # Guardar imagen localmente temporalmente
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_image_path = f"/tmp/{base_name}_detections.jpg"
        pred.save(output_image_path)
        
        # Subir imagen con detecciones a HDFS
        upload_success = upload_to_hdfs(hdfs_client, output_image_path, HDFS_FOLDER_PREP)
        
        # Eliminar archivo temporal
        os.remove(output_image_path)
        
        return upload_success
    except Exception as e:
        print(f"Error al procesar imagen {image_path} con YOLO: {e}")
        return False

# Manejador de eventos
class ImageEventHandler(FileSystemEventHandler):
    def __init__(self, hdfs_client):
        self.hdfs_client = hdfs_client
        self.model = None  # Podrías cargar el modelo aquí si quieres reutilizarlo

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Nueva imagen detectada: {event.src_path}")
            time.sleep(1)  # Esperar a que el archivo esté completamente escrito
            
            # Subir imagen original a HDFS
            if upload_to_hdfs(self.hdfs_client, event.src_path, HDFS_FOLDER):
                # Procesar imagen y subir resultados
                process_image_with_yolo(event.src_path, self.hdfs_client)

# Monitoreo de carpeta
def monitor_folder():
    spark = create_spark_session()
    hdfs_client = create_hdfs_client()
    
    # Crear carpetas HDFS si no existen
    for folder in [HDFS_FOLDER, HDFS_FOLDER_PREP]:
        if not hdfs_client.status(folder, strict=False):
            hdfs_client.makedirs(folder)
    
    event_handler = ImageEventHandler(hdfs_client)
    observer = Observer()
    observer.schedule(event_handler, path=LOCAL_FOLDER, recursive=False)
    observer.start()
    print(f"Monitoreando la carpeta: {LOCAL_FOLDER}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    monitor_folder()