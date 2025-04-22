<h1 align="center">Proyecto Ondaakin</h1>

<div align="center">
  <img src="https://github.com/user-attachments/assets/136496df-295a-460a-89ad-fc2f3096ec02" alt="ONDAAKIN LOGO" width="600"/>

</div>

## 📌 Descripción general del proyecto

**0ndAAkin** es una plataforma tecnológica diseñada para abordar el desperdicio alimentario mediante la inteligencia artificial. Utiliza modelos de detección y segmentación de imágenes para identificar y cuantificar los restos de comida en platos, con el objetivo de generar estadísticas útiles y concienciar sobre el impacto ambiental del desperdicio de alimentos.

Este sistema está pensado para entornos como comedores, restaurantes e instituciones, donde puede visualizar y analizar de forma automatizada la cantidad y tipo de comida desperdiciada.

## 🧠 Enfoque utilizado

- Se ha utilizado un modelo **YOLO11-seg** para llevar a cabo tanto la **segmentación** como la **clasificación** de los alimentos en imágenes.
- Para alimentar el modelo, se recopilaron y etiquetaron alrededor de **6.300 imágenes**, combinando **datasets públicos** y etiquetado manual con **Supervisely**.
- Se ha incorporado un componente **RAG** que permite a los usuarios hacer preguntas y obtener respuestas basadas en la documentación interna del proyecto.
- Se ha utilizado **Docker Compose** para desplegar los servicios del sistema de forma modular y portátil.

## 🚀 Instrucciones para ejecutar el proyecto

### 🔧 Requisitos previos

- Docker y Docker Compose
- Entorno con soporte GPU (opcional, para entrenar el modelo)

### 🛠️ Pasos para el despliegue

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/amaiaDi/7_Reto2_0ndAAkin_G3.git
   cd 7_Reto2_0ndAAkin_G3/Despliegue
   ```

2. Ejecutar el entorno completo desde la carpeta Despliegue:

   ```bash
   sudo sh start.sh
   ```



3. Acceder a los servicios:

   - Homepage (muestra los servicios): http://localhost:43000
   - Web: http://localhost:43001
   - Metabase: http://localhost:43003 (admin@admin.com | 12345@a)
   - HDFS: http://localhost:43007

## 🛠️ Herramientas utilizadas

| Categoría             | Herramienta / Tecnología              |
|-----------------------|---------------------------------------|
| **Backend**           | Django                                |
| **Frontend**          | Bootstrap                             |
| **Base de Datos**     | MongoDB, HDFS                         |
| **IA**                | YOLO11                                |
| **ETL**               | PySpark                               |
| **Dashboard**         | Metabase                              |
| **RAG**               | LangChain, Chroma, deepseek-v2 (Ollama) |
| **Infraestructura**   | Docker Compose, GitHub Actions (CI/CD) |
