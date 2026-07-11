document.addEventListener("DOMContentLoaded", function() {
    let totalStock = 0;
    let valorInventario = 0;

    // Selecciona todos los botones para extraer sus atributos de datos
    const botones = document.querySelectorAll('.view-details-btn');

    botones.forEach(boton => {
        const precio = parseFloat(boton.getAttribute('data-precio')) || 0;
        const stock = parseInt(boton.getAttribute('data-stock')) || 0;

        totalStock += stock;
        valorInventario += (precio * stock);
    });

    // Actualiza los elementos de las tarjetas de estadísticas
    const txtStock = document.getElementById('totalStock');
    const txtInventario = document.getElementById('valorInventario');

    if (txtStock) txtStock.innerText = totalStock;
    if (txtInventario) {
        txtInventario.innerText = '$' + valorInventario.toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }
});

// Funciones del Modal
function abrirDetalles(boton) {
    document.getElementById('modalProductName').innerText = boton.getAttribute('data-nombre');
    document.getElementById('modalPrecio').innerText = '$' + boton.getAttribute('data-precio');
    document.getElementById('modalClasificacion').innerText = boton.getAttribute('data-clasificacion');
    document.getElementById('modalStock').innerText = boton.getAttribute('data-stock') + ' piezas';
    document.getElementById('modalEspecificaciones').innerText = boton.getAttribute('data-especificaciones') || 'Sin especificaciones';
    
    document.getElementById('detallesModal').style.display = 'block';
}

function cerrarModal() {
    document.getElementById('detallesModal').style.display = 'none';
}

// Cerrar modal al hacer clic fuera del recuadro
window.onclick = function(event) {
    const modal = document.getElementById('detallesModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}