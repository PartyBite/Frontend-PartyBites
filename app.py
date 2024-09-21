from flask import Flask, render_template
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'contrasena'  

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin123' 
app.config['MYSQL_DB'] = 'PARTYBITE'

mysql = MySQL(app)

# Ruta para el registro
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        user_type = request.form['userType']

        # Mapeamos el tipo de usuario a su valor correspondiente en la base de datos
        user_type_id = 1 if user_type == 'Comprador' else 2

        # Guardar datos del usuario en la base de datos
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO Usuario(idTipo, nombre, correo, contrasena, telefono, fecha_registro) 
                           VALUES(%s, %s, %s, %s, %s, CURDATE())''', (user_type_id, name, email, password, phone))
        mysql.connection.commit()

        # Si es un repartidor, insertamos en la tabla de repartidores
        if user_type_id == 2:
            user_id = cursor.lastrowid
            cursor.execute(''' INSERT INTO Repartidores(idUsuario) VALUES (%s)''', (user_id,))
            mysql.connection.commit()

        cursor.close()

        # Mostrar un mensaje de éxito y redirigir al login
        flash('Registro exitoso. Por favor, inicia sesión.')
        return redirect(url_for('home'))  # Cambia a la página principal donde está el modal de login

    return render_template('index.html')


@app.route('/')
def home():
    return render_template('index.html')


# Ruta para el inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute(''' SELECT * FROM Usuario WHERE correo = %s AND contrasena = %s ''', (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Guardar la sesión del usuario
            session['loggedin'] = True
            session['id'] = user[0]
            session['nombre'] = user[2]  # El nombre está en la tercera columna
            return redirect(url_for('welcome'))
        else:
            flash('Correo o contraseña incorrectos. Inténtalo de nuevo.')
            return redirect(url_for('home'))  # Redirige al home si hay error

    return redirect(url_for('home'))


# Ruta para mostrar la página de bienvenida después de iniciar sesión
@app.route('/welcome')
def welcome():
    if 'loggedin' in session:
        return render_template('DespuesInicioSesion.html', nombre=session['nombre'])
    else:
        return redirect(url_for('home'))  # Redirige al home si no está logueado

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('nombre', None)
    flash('Sesión cerrada con éxito.')
    return redirect(url_for('home'))


@app.route('/bebidas')
def bebidas():
    if 'loggedin' in session:
        nombre = session['nombre']  # Obtenemos el nombre del usuario logueado

        # Consulta para obtener las bebidas alcohólicas
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT nombre, precio, stock, image_url, descripcion FROM Producto WHERE idCategoria = 1")
        bebidas = cursor.fetchall()
        cursor.close()

        # Renderiza la página de bebidas con los datos obtenidos y el nombre del usuario
        return render_template('bebidas.html', bebidas=bebidas, nombre=nombre)
    else:
        return redirect(url_for('home'))  # Redirige al home si no está logueado



@app.route('/agregar_carrito', methods=['POST'])
def agregar_carrito():
    nombre_bebida = request.form['nombre']

    # Aquí puedes manejar la lógica de agregar al carrito (sesión, base de datos, etc.)
    # Ejemplo simple usando la sesión para almacenar los productos en el carrito
    if 'carrito' not in session:
        session['carrito'] = []

    session['carrito'].append(nombre_bebida)
    flash(f'{nombre_bebida} ha sido agregado al carrito.')
    
    return redirect(url_for('bebidas'))


if __name__ == '__main__':
    app.run(debug=True)
