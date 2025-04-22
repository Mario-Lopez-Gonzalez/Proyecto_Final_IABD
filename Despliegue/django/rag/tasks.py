from celery import shared_task

@shared_task
def run_rag_task():
    return "Tarea RAG ejecutada"
