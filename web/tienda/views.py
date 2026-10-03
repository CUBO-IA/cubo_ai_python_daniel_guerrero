from django.shortcuts import render

productos_lista = [
    {
        'id': 1,
        'nombre': 'Auriculares Bluetooth',
        'precio': 25.99,
        'descripcion': 'Auriculares inalámbricos con sonido de buena calidad.',
        'imagen': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800',
    },
    {
        'id': 2,
        'nombre': 'Reloj Inteligente',
        'precio': 39.99,
        'descripcion': 'Reloj inteligente moderno para el día a día.',
        'imagen': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800',
    },
    {
        'id': 3,
        'nombre': 'Cámara Fotográfica',
        'precio': 299.99,
        'descripcion': 'Cámara compacta para capturar tus mejores momentos.',
        'imagen': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800',
    },
    {
        'id': 4,
        'nombre': 'Zapatillas Deportivas',
        'precio': 59.99,
        'descripcion': 'Zapatillas cómodas para deporte y uso diario.',
        'imagen': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800',
    },
]


def inicio(request):
    return render(request, 'tienda/inicio.html', {
        'productos': productos_lista[:4]
    })


def productos(request):
    return render(request, 'tienda/productos.html', {
        'productos': productos_lista
    })


def detalle(request, id):
    producto = next(
        (p for p in productos_lista if p['id'] == id),
        None
    )

    return render(request, 'tienda/detalle.html', {
        'producto': producto
    })
