from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Inicializar la sesión de productos
@app.before_request
def iniciar_sesion():
    if 'productos' not in session:
        session['productos'] = []

# Ruta principal - mostrar productos
@app.route('/')
def gestion_productos():
    return render_template('productos.html', productos=session['productos'])

# Agregar nuevo producto
@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        id = len(session['productos']) + 1
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        fecha_vencimiento = request.form['fecha_vencimiento']
        categoria = request.form['categoria']

        producto = {
            'id': id,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'fecha_vencimiento': fecha_vencimiento,
            'categoria': categoria
        }
        session['productos'].append(producto)
        session.modified = True
        return redirect(url_for('gestion_productos'))
    
    return render_template('nuevo_producto.html')

# Editar producto
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    productos = session['productos']
    producto = next((p for p in productos if p['id'] == id), None)
    
    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('gestion_productos'))
    
    return render_template('editar_producto.html', producto=producto)

# Eliminar producto y actualizar IDs
@app.route('/eliminar_producto/<int:id>', methods=['POST'])
def eliminar_producto(id):
    # Eliminar el producto por su ID
    productos = [p for p in session['productos'] if p['id'] != id]
    
    # Reindexar los IDs de los productos restantes
    for i, producto in enumerate(productos, start=1):
        producto['id'] = i
    
    # Guardar los productos actualizados en la sesión
    session['productos'] = productos
    session.modified = True
    return redirect(url_for('gestion_productos'))

if __name__ == '__main__':
    app.run(debug=True)
