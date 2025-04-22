
"""
from django.shortcuts import render
from django.http import JsonResponse
from .tasks import run_rag_task

def chat_view(request):
    return render(request, 'chat.html')

def execute_rag(request):
    query = request.GET.get("q", "¿Qué es Django?")
    task = run_rag_task.delay(query)
    return JsonResponse({"task_id": task.id, "status": "processing"})

"""
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .rag_system import rag_instance

def rag_chat(request):
    if request.method == 'GET':
        return render(request, 'chat_content.html')
"""
@csrf_exempt
def rag_send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        # Aquí puedes agregar la lógica para procesar el mensaje con RAG
        response_message = f"Gracias por tu mensaje: {message}"
        return JsonResponse({'message': response_message})
"""
@require_POST
def rag_send_message(request):
    question = request.POST.get('message', '').strip()
    
    if not question:
        return JsonResponse({'error': 'Pregunta vacía'}, status=400)
    
    try:
        answer = rag_instance.get_response(question)
        return JsonResponse({'message': answer})
    except Exception as e:
        return JsonResponse(
            {'error': f'Error en el sistema RAG: {str(e)}'},
            status=500
        )

"""
@csrf_exempt
def rag_send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        # Lógica RAG aquí (ej: generar respuesta)
        #respuesta_rag = generar_respuesta(message)  # Tu función RAG
       # return JsonResponse({'message': respuesta_rag})
    return JsonResponse({'error': 'Método no permitido'}, status=405)
    
"""