from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date
from .models import Profesor, Clase

@login_required
def home_view(request):
    """Vista simple de bienvenida - redirige al dashboard"""
    return redirect('dashboard')

@login_required
def dashboard_view(request):
    """Vista principal del dashboard con estadísticas y guardias"""
    try:
        # Obtener el profesor basado en el email del usuario autenticado
        profesor = Profesor.objects.get(email=request.user.email)
        
        # Obtener todas las clases del profesor con relaciones
        datos = Clase.objects.filter(
            profesor=profesor
        ).select_related(
            'asignatura', 'aula', 'hora'
        ).order_by('fecha', 'hora__hora_inicio')
        
        # Estadísticas generales
        total_guardias = datos.count()
        guardias_pendientes = datos.filter(fecha__gte=date.today()).count()
        guardias_aceptadas = datos.filter(fecha__lt=date.today()).count()
        guardias_hoy = datos.filter(fecha=date.today()).count()
        
        context = {
            'datos': datos,
            'profesor': profesor,
            'total_guardias': total_guardias,
            'guardias_pendientes': guardias_pendientes,
            'guardias_aceptadas': guardias_aceptadas,
            'guardias_hoy': guardias_hoy,
        }
        
    except Profesor.DoesNotExist:
        # Si el usuario no está asociado a un profesor
        context = {
            'datos': [],
            'profesor': None,
            'total_guardias': 0,
            'guardias_pendientes': 0,
            'guardias_aceptadas': 0,
            'guardias_hoy': 0,
        }
    
    return render(request, 'dashboard/dashboard.html', context)