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
        
        # 1. AJUSTE: Capturar el archivo de la imagen desde los archivos del request
        # Asegúrate de que el atributo name de tu input HTML sea "imagen" (<input name="imagen" type="file">)
        imagen = request.FILES.get('imagen') 
        
        # Validar campos requeridos
        if not nombre or not costo_comercial or not existencia_inicial:
            messages.error(request, 'Por favor completa todos los campos requeridos')
        else:
            try:
                # 2. AJUSTE: Añadir el campo imagen al create para que Django lo guarde en la base de datos
                Producto.objects.create(
                    nombre=nombre,
                    clasificacion=clasificacion,
                    costo_comercial=costo_comercial,
                    especificaciones_tecnicas=especificaciones_tecnicas,
                    existencia_inicial=int(existencia_inicial),
                    imagen=imagen  # <-- Línea agregada
                )
                messages.success(request, f'Producto "{nombre}" creado exitosamente')
                return redirect('catalogo')
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


def catalogo(request):
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
    
    return render(request, 'game/catalogo.html', context)


# En tu archivo views.py haz el query así para enviarlo al HTML:
def opiniones(request):
    if request.method == 'POST':
        usuario_form = request.POST.get('usuario')
        mensaje_form = request.POST.get('opinion')
        
        # Guarda en la base de datos usando los campos de tu modelo
        Opinión.objects.create(user=usuario_form, message=mensaje_form)
        messages.success(request, '¡Tu opinión ha sido enviada! Aparecerá cuando sea aprobada.')
        return redirect('opiniones')

    # Filtra las opiniones para mostrar en el HTML
    opiniones_aprobadas = Opinión.objects.filter(status='APROBADO', is_hidden=False)
    
    return render(request, 'game/opiniones.html', {'opiniones': opiniones_aprobadas})