from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Producto, Opinión

# Create your views here.

def altaproducto(request):
    # Procesar formulario POST para crear nuevo producto
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        clasificacion = request.POST.get('clasificacion', 'SIM_AVANZADA')
        costo_comercial = request.POST.get('costo_comercial', 0)
        especificaciones_tecnicas = request.POST.get('especificaciones_tecnicas', '').strip()
        existencia_inicial = request.POST.get('existencia_inicial', 0)
        
        # Validar campos requeridos
        if not nombre or not costo_comercial or not existencia_inicial:
            messages.error(request, 'Por favor completa todos los campos requeridos')
        else:
            try:
                Producto.objects.create(
                    nombre=nombre,
                    clasificacion=clasificacion,
                    costo_comercial=costo_comercial,
                    especificaciones_tecnicas=especificaciones_tecnicas,
                    existencia_inicial=int(existencia_inicial)
                )
                messages.success(request, f'Producto "{nombre}" creado exitosamente')
                return redirect('catalogo2')
            except Exception as e:
                messages.error(request, f'Error al crear el producto: {str(e)}')
    
    # Obtener clasificación seleccionada desde query parameters
    clasificacion_filter = request.GET.get('clasificacion', None)
    
    # Obtener todos los productos o filtrar por clasificación
    if clasificacion_filter:
        productos = Producto.objects.filter(clasificacion=clasificacion_filter)
    else:
        productos = Producto.objects.all()
    
    # Obtener todas las clasificaciones disponibles
    clasificaciones = Producto.CLASIFICACION_CHOICES
    
    context = {
        'productos': productos,
        'clasificaciones': clasificaciones,
        'clasificacion_actual': clasificacion_filter,
    }
    
    return render(request, 'game/altaproducto.html', context)


def catalogo2(request):
    # Obtener clasificación seleccionada desde query parameters
    clasificacion_filter = request.GET.get('clasificacion', None)
    
    # Obtener todos los productos o filtrar por clasificación
    if clasificacion_filter:
        productos = Producto.objects.filter(clasificacion=clasificacion_filter)
    else:
        productos = Producto.objects.all()
    
    # Obtener todas las clasificaciones disponibles
    clasificaciones = Producto.CLASIFICACION_CHOICES
    
    context = {
        'productos': productos,
        'clasificaciones': clasificaciones,
        'clasificacion_actual': clasificacion_filter,
    }
    
    return render(request, 'game/catalogo2.html', context)


def opiniones(request):
    # Procesar formulario POST para crear nueva opinión
    if request.method == 'POST':
        usuario = request.POST.get('usuario', '').strip()
        opinion = request.POST.get('opinion', '').strip()
        
        if usuario and opinion:
            try:
                Opinión.objects.create(
                    user=usuario,
                    message=opinion,
                    status='APROBADO'
                )
                messages.success(request, '¡Tu opinión ha sido compartida exitosamente!')
            except Exception as e:
                messages.error(request, f'Error al registrar la opinión: {str(e)}')
        else:
            messages.error(request, 'Por favor completa todos los campos')
        
        return redirect('opiniones')
    
    # Obtener opiniones aprobadas
    opiniones_list = Opinión.objects.filter(status='APROBADO', is_hidden=False).order_by('-created')
    
    context = {
        'opiniones': opiniones_list,
    }
    
    return render(request, 'game/opiniones.html', context)
