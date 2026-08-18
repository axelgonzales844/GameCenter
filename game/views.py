from datetime import datetime

from functools import wraps
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Producto, Opinión, Usuario, Orden, OrdenItem, Direccion, Carrito, ElementoCarrito
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Sum, Count, F
from django.utils import timezone


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('is_admin', False):
            messages.error(request, 'Acceso denegado. Se requieren permisos de administrador.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def login_required_custom(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            messages.error(request, 'Debes iniciar sesión para acceder a esta sección.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def _obtener_o_crear_carrito_db(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        usuario = Usuario.objects.filter(id=usuario_id).first()
        if usuario:
            carrito_db, _ = Carrito.objects.get_or_create(usuario=usuario)
            return carrito_db
    return None


@admin_required
def altaproducto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        clasificacion = request.POST.get('clasificacion', 'SIM_AVANZADA')
        costo_comercial = request.POST.get('costo_comercial', 0)
        descuento = request.POST.get('descuento', 0)
        descuento_inicio = request.POST.get('descuento_inicio')
        descuento_fin = request.POST.get('descuento_fin')
        descuento_minimo_unidades = request.POST.get('descuento_minimo_unidades', 0)
        especificaciones_tecnicas = request.POST.get('especificaciones_tecnicas', '').strip()
        existencia_inicial = request.POST.get('existencia_inicial', 0)
        imagen = request.FILES.get('imagen') 
        
        if not nombre or not costo_comercial or not existencia_inicial:
            messages.error(request, 'Por favor completa todos los campos requeridos.')
        else:
            try:
                descuento_int = int(descuento)
                if descuento_int < 0 or descuento_int > 100:
                    raise ValueError('El descuento debe estar entre 0 y 100.')

                descuento_inicio_dt = timezone.make_aware(datetime.fromisoformat(descuento_inicio)) if descuento_inicio else None
                descuento_fin_dt = timezone.make_aware(datetime.fromisoformat(descuento_fin)) if descuento_fin else None
                if descuento_inicio_dt and descuento_fin_dt and descuento_fin_dt < descuento_inicio_dt:
                    raise ValueError('La fecha final del descuento no puede ser anterior a la fecha inicial.')

                Producto.objects.create(
                    nombre=nombre,
                    clasificacion=clasificacion,
                    costo_comercial=costo_comercial,
                    descuento=descuento_int,
                    descuento_inicio=descuento_inicio_dt,
                    descuento_fin=descuento_fin_dt,
                    descuento_minimo_unidades=int(descuento_minimo_unidades or 0),
                    especificaciones_tecnicas=especificaciones_tecnicas,
                    existencia_inicial=int(existencia_inicial),
                    imagen=imagen 
                )
                messages.success(request, f'Producto "{nombre}" creado exitosamente.')
                return redirect('control')
            except Exception as e:
                messages.error(request, f'Error al crear el producto: {str(e)}')
    
    return render(request, 'game/altaproducto.html', {
        'clasificaciones': Producto.CLASIFICACION_CHOICES,
    })


@admin_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, pk=id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        clasificacion = request.POST.get('clasificacion', 'SIM_AVANZADA')
        costo_comercial = request.POST.get('costo_comercial', 0)
        descuento = request.POST.get('descuento', 0)
        descuento_inicio = request.POST.get('descuento_inicio')
        descuento_fin = request.POST.get('descuento_fin')
        descuento_minimo_unidades = request.POST.get('descuento_minimo_unidades', 0)
        especificaciones_tecnicas = request.POST.get('especificaciones_tecnicas', '').strip()
        existencia_inicial = request.POST.get('existencia_inicial', 0)
        imagen = request.FILES.get('imagen')

        if not nombre or not costo_comercial or not existencia_inicial:
            messages.error(request, 'Por favor completa todos los campos requeridos.')
        else:
            try:
                descuento_int = int(descuento)
                if descuento_int < 0 or descuento_int > 100:
                    raise ValueError('El descuento debe estar entre 0 y 100.')

                descuento_inicio_dt = timezone.make_aware(datetime.fromisoformat(descuento_inicio)) if descuento_inicio else None
                descuento_fin_dt = timezone.make_aware(datetime.fromisoformat(descuento_fin)) if descuento_fin else None
                if descuento_inicio_dt and descuento_fin_dt and descuento_fin_dt < descuento_inicio_dt:
                    raise ValueError('La fecha final del descuento no puede ser anterior a la fecha inicial.')

                producto.nombre = nombre
                producto.clasificacion = clasificacion
                producto.costo_comercial = costo_comercial
                producto.descuento = descuento_int
                producto.descuento_inicio = descuento_inicio_dt
                producto.descuento_fin = descuento_fin_dt
                producto.descuento_minimo_unidades = int(descuento_minimo_unidades or 0)
                producto.especificaciones_tecnicas = especificaciones_tecnicas
                producto.existencia_inicial = int(existencia_inicial)
                if imagen:
                    producto.imagen = imagen
                producto.save()
                messages.success(request, f'Producto "{nombre}" actualizado correctamente.')
                return redirect('control')
            except Exception as e:
                messages.error(request, f'Error al actualizar el producto: {str(e)}')

    return render(request, 'game/editarproducto.html', {
        'producto': producto,
        'clasificaciones': Producto.CLASIFICACION_CHOICES,
    })
@admin_required
def eliminar_producto(request, id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, pk=id)
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado correctamente.')
    return redirect('control')

def catalogo(request):
    clasificacion_filter = request.GET.get('clasificacion', None)
    query = request.GET.get('q', '').strip()

    productos = Producto.objects.all()

    if clasificacion_filter:
        productos = productos.filter(clasificacion=clasificacion_filter)

    if query:
        productos = productos.filter(nombre__icontains=query)

    return render(request, 'game/catalogo.html', {
        'productos': productos,
        'clasificaciones': Producto.CLASIFICACION_CHOICES,
        'clasificacion_actual': clasificacion_filter,
        'query_actual': query,
    })


def detallesproducto(request, producto_id): 
    producto = get_object_or_404(Producto, pk=producto_id) 
    return render(request, 'game/detallesproducto.html', {'producto': producto})


@admin_required
def control(request):
    # Traemos todos los productos registrados en la BD
    productos = Producto.objects.all()
    
    # Se los enviamos al HTML
    return render(request, 'game/control.html', {
        'productos': productos
    })


@admin_required
def lista_usuarios(request):
    usuarios = Usuario.objects.all().order_by('-id')
    return render(request, 'game/usuarios.html', {'usuarios': usuarios})


@login_required_custom
def perfil(request):
    usuario_id = request.session.get('usuario_id')
    usuario_obj = get_object_or_404(Usuario, pk=usuario_id)
    
    direcciones = Direccion.objects.filter(usuario=usuario_obj)
    ordenes = Orden.objects.filter(usuario=usuario_obj).order_by('-created')

    return render(request, 'game/perfil.html', {
        'usuario': usuario_obj,
        'direcciones': direcciones,
        'ordenes': ordenes
    })


@login_required_custom
def agregar_direccion(request):
    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')
        usuario = get_object_or_404(Usuario, pk=usuario_id)

        calle = request.POST.get('calle', '').strip()
        numero_exterior = request.POST.get('numero_exterior', '').strip()
        numero_interior = request.POST.get('numero_interior', '').strip()
        colonia = request.POST.get('colonia', '').strip()
        codigo_postal = request.POST.get('codigo_postal', '').strip()
        ciudad = request.POST.get('ciudad', '').strip()
        pais = request.POST.get('pais', 'México').strip()
        numero_telefonico = request.POST.get('numero_telefonico', '').strip()
        referencias = request.POST.get('referencias', '').strip()

        if not calle or not numero_exterior or not colonia or not codigo_postal or not ciudad or not numero_telefonico:
            messages.error(request, 'Por favor llena todos los campos obligatorios de la dirección.')
            return redirect('perfil')

        Direccion.objects.create(
            usuario=usuario,
            calle=calle,
            numero_exterior=numero_exterior,
            numero_interior=numero_interior if numero_interior else None,
            colonia=colonia,
            codigo_postal=codigo_postal,
            ciudad=ciudad,
            pais=pais,
            numero_telefonico=numero_telefonico,
            referencias=referencias if referencias else None
        )

        messages.success(request, '¡Dirección agregada correctamente!')
        return redirect('perfil')

    return redirect('perfil')


def opiniones(request):
    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, 'Debes iniciar sesión para publicar una opinión.')
            return redirect('login')

        usuario_obj = get_object_or_404(Usuario, pk=usuario_id)
        mensaje_form = request.POST.get('opinion', '').strip()

        if mensaje_form:
            Opinión.objects.create(
                user=usuario_obj.username,  
                message=mensaje_form
            )
            messages.success(request, '¡Tu opinión ha sido enviada!')
        else:
            messages.error(request, 'El comentario no puede estar vacío.')

        return redirect('opiniones')

    opiniones_aprobadas = Opinión.objects.filter(status='APROBADO', is_hidden=False)
    return render(request, 'game/opiniones.html', {'opiniones': opiniones_aprobadas})


def carrito(request):
    carrito_items = []
    subtotal = 0
    carrito_db = _obtener_o_crear_carrito_db(request)

    if carrito_db:
        elementos = ElementoCarrito.objects.filter(carrito=carrito_db).select_related('producto')
        for item in elementos:
            precio_unitario = float(item.producto.precio_con_descuento())
            subtotal_item = precio_unitario * item.cantidad
            subtotal += subtotal_item
            carrito_items.append({
                'producto_id': item.producto.id,
                'nombre': item.producto.nombre,
                'precio': precio_unitario,
                'cantidad': item.cantidad,
                'imagen': item.producto.imagen.url if item.producto.imagen else '',
                'subtotal': subtotal_item
            })
    else:
        carrito_session = request.session.get('carrito', {})
        for prod_id, item in carrito_session.items():
            subtotal_item = float(item['precio']) * int(item['cantidad'])
            subtotal += subtotal_item
            carrito_items.append({
                'producto_id': prod_id,
                'nombre': item['nombre'],
                'precio': item['precio'],
                'cantidad': item['cantidad'],
                'imagen': item.get('imagen', ''),
                'subtotal': subtotal_item
            })

    usuario_id = request.session.get('usuario_id')
    usuario_obj = Usuario.objects.filter(id=usuario_id).first() if usuario_id else None
    direcciones_usuario = Direccion.objects.filter(usuario=usuario_obj) if usuario_obj else []

    return render(request, 'game/carrito.html', {
        'carrito_items': carrito_items,
        'subtotal': subtotal,
        'total': subtotal,
        'direcciones': direcciones_usuario
    })


def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    carrito_db = _obtener_o_crear_carrito_db(request)

    if carrito_db:
        elemento, created = ElementoCarrito.objects.get_or_create(
            carrito=carrito_db,
            producto=producto,
            defaults={'cantidad': 1}
        )
        if not created:
            elemento.cantidad += 1
            elemento.save()
    else:
        carrito_session = request.session.get('carrito', {})
        str_id = str(producto_id)
        if str_id in carrito_session:
            carrito_session[str_id]['cantidad'] += 1
        else:
            carrito_session[str_id] = {
                'nombre': producto.nombre,
                'precio': float(producto.precio_con_descuento()),
                'cantidad': 1,
                'imagen': producto.imagen.url if producto.imagen else ''
            }
        request.session['carrito'] = carrito_session

    messages.success(request, f'"{producto.nombre}" se agregó al carrito.')
    next_url = request.META.get('HTTP_REFERER', 'catalogo')
    return redirect(next_url)


def cambiar_cantidad_carrito(request, producto_id, accion):
    carrito_db = _obtener_o_crear_carrito_db(request)

    if carrito_db:
        elemento = ElementoCarrito.objects.filter(carrito=carrito_db, producto_id=producto_id).first()
        if elemento:
            if accion == 'sumar':
                elemento.cantidad += 1
                elemento.save()
            elif accion == 'restar':
                elemento.cantidad -= 1
                if elemento.cantidad <= 0:
                    elemento.delete()
                else:
                    elemento.save()
            elif accion == 'eliminar':
                elemento.delete()
    else:
        carrito_session = request.session.get('carrito', {})
        str_id = str(producto_id)
        if str_id in carrito_session:
            if accion == 'sumar':
                carrito_session[str_id]['cantidad'] += 1
            elif accion == 'restar':
                carrito_session[str_id]['cantidad'] -= 1
                if carrito_session[str_id]['cantidad'] <= 0:
                    del carrito_session[str_id]
            elif accion == 'eliminar':
                del carrito_session[str_id]
        request.session['carrito'] = carrito_session

    return redirect('carrito')


@login_required_custom
def procesar_pago(request):
    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')
        usuario_obj = get_object_or_404(Usuario, pk=usuario_id)
        carrito_db = _obtener_o_crear_carrito_db(request)

        items_a_comprar = []
        subtotal = 0

        if carrito_db:
            elementos = ElementoCarrito.objects.filter(carrito=carrito_db).select_related('producto')
            for el in elementos:
                costo = float(el.producto.precio_con_descuento())
                items_a_comprar.append({
                    'producto_obj': el.producto,
                    'cantidad': el.cantidad,
                    'precio': costo
                })
                subtotal += costo * el.cantidad
        else:
            carrito_session = request.session.get('carrito', {})
            for prod_id, item in carrito_session.items():
                p_obj = Producto.objects.filter(id=prod_id).first()
                if p_obj:
                    costo = float(item['precio'])
                    cant = int(item['cantidad'])
                    items_a_comprar.append({
                        'producto_obj': p_obj,
                        'cantidad': cant,
                        'precio': costo
                    })
                    subtotal += costo * cant

        if not items_a_comprar:
            messages.error(request, 'Tu carrito está vacío.')
            return redirect('carrito')

        metodo_pago = request.POST.get('metodo_pago', 'TARJETA')
        if metodo_pago == 'TARJETA':
            num_tarjeta = request.POST.get('numero_tarjeta', '').replace(' ', '')
            cvv = request.POST.get('cvv', '')
            if len(num_tarjeta) != 16 or not num_tarjeta.isdigit():
                messages.error(request, 'Error en el pago: Ingresa un número de tarjeta válido de 16 dígitos.')
                return redirect('carrito')
            if len(cvv) < 3 or not cvv.isdigit():
                messages.error(request, 'Error en el pago: El código CVV es incorrecto.')
                return redirect('carrito')

        direccion_id = request.POST.get('direccion_id')
        if direccion_id:
            dir_obj = Direccion.objects.filter(id=direccion_id, usuario=usuario_obj).first()
            if dir_obj:
                direccion_postal = f"{dir_obj.calle} #{dir_obj.numero_exterior}, Col. {dir_obj.colonia}"
                estado_ciudad = dir_obj.ciudad
                codigo_postal = dir_obj.codigo_postal
            else:
                direccion_postal = "Entrega Digital / Descarga"
                estado_ciudad = "Digital"
                codigo_postal = "00000"
        else:
            direccion_postal = "Entrega Digital / Descarga"
            estado_ciudad = "Digital"
            codigo_postal = "00000"

        nueva_orden = Orden.objects.create(
            usuario=usuario_obj,
            nombre_completo=usuario_obj.username,
            direccion_postal=direccion_postal,
            estado_ciudad=estado_ciudad,
            codigo_postal=codigo_postal,
            metodo_pago=metodo_pago,
            total_neto=subtotal
        )

        for item in items_a_comprar:
            prod = item['producto_obj']
            cant = item['cantidad']
            if prod.existencia_inicial >= cant:
                prod.existencia_inicial -= cant
            else:
                prod.existencia_inicial = 0
            prod.save()

            OrdenItem.objects.create(
                orden=nueva_orden,
                producto=prod,
                cantidad=cant,
                precio_unitario=item['precio']
            )

        if carrito_db:
            ElementoCarrito.objects.filter(carrito=carrito_db).delete()
        request.session['carrito'] = {}
        request.session.modified = True

        messages.success(request, f'¡Pago aprobado con éxito! Tu Orden #{nueva_orden.id} fue registrada.')
        return redirect('carrito')

    return redirect('carrito')


def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not username or not email or not password:
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'game/registro.html')

        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener mínimo 8 caracteres.')
            return render(request, 'game/registro.html')

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'Ese nombre de usuario ya existe.')
            return render(request, 'game/registro.html')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Ese correo ya está registrado.')
            return render(request, 'game/registro.html')

        Usuario.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            is_admin=False,
        )
        messages.success(request, 'Cuenta creada. Ya puedes iniciar sesión.')
        return redirect('login')

    return render(request, 'game/registro.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        try:
            usuario = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return render(request, 'game/login.html')

        if not check_password(password, usuario.password):
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return render(request, 'game/login.html')

        request.session['usuario_id'] = usuario.id
        request.session['username'] = usuario.username
        request.session['is_admin'] = usuario.is_admin

        carrito_session = request.session.get('carrito', {})
        if carrito_session:
            carrito_db, _ = Carrito.objects.get_or_create(usuario=usuario)
            for prod_id, item in carrito_session.items():
                producto = Producto.objects.filter(id=prod_id).first()
                if producto:
                    el, created = ElementoCarrito.objects.get_or_create(
                        carrito=carrito_db,
                        producto=producto,
                        defaults={'cantidad': item['cantidad']}
                    )
                    if not created:
                        el.cantidad += item['cantidad']
                        el.save()
            request.session['carrito'] = {}

        if usuario.is_admin:
            return redirect('control')
        return redirect('catalogo')

    return render(request, 'game/login.html')


def logout_view(request):
    request.session.flush()
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')

# --- ADMINISTRACIÓN DE OPINIONES ---
@admin_required
def admin_opiniones(request):
    opiniones_lista = Opinión.objects.all().order_by('-id')
    return render(request, 'game/admin_opiniones.html', {'opiniones': opiniones_lista})


@admin_required
def eliminar_opinion(request, id):
    if request.method == 'POST':
        opinion = get_object_or_404(Opinión, pk=id)
        opinion.delete()
        messages.success(request, 'La opinión fue eliminada correctamente.')
    return redirect('admin_opiniones')


# --- PERFIL DE USUARIO (ACTUALIZADO) ---
@login_required_custom
def perfil(request):
    usuario_id = request.session.get('usuario_id')
    usuario_obj = get_object_or_404(Usuario, pk=usuario_id)
    
    direcciones = Direccion.objects.filter(usuario=usuario_obj)
    ordenes = Orden.objects.filter(usuario=usuario_obj).order_by('-created')
    mis_opiniones = Opinión.objects.filter(user=usuario_obj.username).order_by('-id')

    return render(request, 'game/perfil.html', {
        'usuario': usuario_obj,
        'direcciones': direcciones,
        'ordenes': ordenes,
        'opiniones': mis_opiniones
    })


# --- ESTADÍSTICAS DE PRODUCTOS ---
@admin_required
def admin_estadisticas(request):
    total_productos = Producto.objects.count()
    productos_bajo_stock = Producto.objects.filter(existencia_inicial__lt=3).count()
    total_ingresos = Orden.objects.aggregate(Sum('total_neto'))['total_neto__sum'] or 0
    total_pedidos = Orden.objects.count()

    # Cálculo de unidades vendidas e ingresos por cada producto
    productos_stats = Producto.objects.annotate(
        unidades_vendidas=Sum('ordenitem__cantidad'),
        ingresos_generados=Sum(F('ordenitem__cantidad') * F('ordenitem__precio_unitario'))
    ).order_by('-unidades_vendidas')

    return render(request, 'game/admin_estadisticas.html', {
        'total_productos': total_productos,
        'productos_bajo_stock': productos_bajo_stock,
        'total_ingresos': total_ingresos,
        'total_pedidos': total_pedidos,
        'productos_stats': productos_stats,
    })


# --- LISTADO GENERAL DE PEDIDOS (ADMIN) ---
@admin_required
def admin_pedidos(request):
    pedidos = Orden.objects.all().order_by('-created')
    return render(request, 'game/admin_pedidos.html', {'pedidos': pedidos})