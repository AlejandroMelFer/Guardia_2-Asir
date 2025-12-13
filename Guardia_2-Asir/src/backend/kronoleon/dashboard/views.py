from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profesor, Clase

@login_required
def home_view(request):
    return render(request, 'dashboard/home.html')

@login_required
def dashboard_view(request):
    try:
        # Asumimos que el email del usuario coincide con el del Profesor
        profesor = Profesor.objects.get(email=request.user.email)
        datos = Clase.objects.filter(profesor=profesor).select_related('asignatura', 'aula', 'hora')
    except Profesor.DoesNotExist:
        datos = []
    
    return render(request, 'dashboard/dashboard.html', {'datos': datos})
