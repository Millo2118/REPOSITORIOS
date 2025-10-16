from flask import Flask, request, render_template, jsonify
import sqlite3
import os
import json
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_PATH = 'database/consultas.db'

def init_db():
    """Inicializa la base de datos con algunas tablas de ejemplo"""
    if not os.path.exists('database'):
        os.makedirs('database')
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Crear tabla de clientes de ejemplo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cliente (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo_cliente TEXT NOT NULL,
            direccion TEXT,
            telefono INTEGER
        )
    ''')


    
    # # Crear tabla de productos de ejemplo
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS productos (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         nombre TEXT NOT NULL,
    #         precio REAL NOT NULL,
    #         categoria TEXT,
    #         stock INTEGER DEFAULT 0
    #     )
    # ''')
    
    # # Crear tabla de ventas de ejemplo
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS ventas (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         usuario_id INTEGER,
    #         producto_id INTEGER,
    #         cantidad INTEGER,
    #         fecha_venta DATETIME DEFAULT CURRENT_TIMESTAMP,
    #         FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    #         FOREIGN KEY (producto_id) REFERENCES productos (id)
    #     )
    # ''')
    
    # Insertar datos de ejemplo si no existen
    cursor.execute('SELECT COUNT(*) FROM Cliente')
    if cursor.fetchone()[0] == 0:
        usuarios_ejemplo = [
            ("Supermercado Central","Mayorista","Cra 10 #23-45",3101234567),
            ("Tienda La Esquina","Minorista","Calle 5 #12-34",3209876543),
            ("Bar El Refugio","Bar","Av. 7 #45-67",3112345678),
            ("Restaurante Sazón","Restaurante","Cra 15 #67-89",3123456789),
            ("Licorera El Trago","Licorera","Calle 8 #56-78",3134567890),
            ("Minimercado Express","Minorista","Cra 20 #34-56",3145678901),
            ("Cafetería Aroma","Cafetería","Calle 3 #21-43",3156789012),
            ("Hotel Paraíso","Hotel","Av. 9 #12-34",3167890123),
            ("Panadería Dulce Pan","Panadería","Cra 18 #23-45",3178901234),
            ("Tienda El Ahorro","Minorista","Calle 6 #78-90",3189012345),
            ("Restaurante El Buen Sabor","Restaurante","Cra 22 #45-67",3190123456),
            ("Bar La Rumba","Bar","Calle 12 #34-56",3201234567),
            ("Supermercado La Oferta","Mayorista","Av. 5 #67-89",3212345678),
            ("Licorera La Cava","Licorera","Cra 30 #12-34",3223456789),
            ("Minimercado La Economía","Minorista","Calle 9 #45-67",3234567890),
            ("Cafetería El Grano","Cafetería","Av. 11 #23-45",3245678901),
            ("Hotel Sol y Luna","Hotel","Cra 25 #67-89",3256789012),
            ("Panadería La Espiga","Panadería","Calle 14 #56-78",3267890123),
            ("Tienda El Centro","Minorista","Av. 13 #78-90",3278901234),
            ("Restaurante Sabores","Restaurante","Cra 17 #23-45",3289012345),
            ("Bar El Encuentro","Bar","Calle 15 #67-89",3290123456),
            ("Supermercado El Progreso","Mayorista","Cra 28 #45-67",3301234567),
            ("Licorera El Barril","Licorera","Av. 16 #12-34",3312345678),
            ("Minimercado Familiar","Minorista","Calle 17 #34-56",3323456789),
            ("Cafetería La Taza","Cafetería","Cra 19 #56-78",3334567890)

        ]
        cursor.executemany('INSERT INTO usuarios (nombre, tipo_cliente, direccion, telefono) VALUES (?, ?, ?, ?)', usuarios_ejemplo)
        
        # productos_ejemplo = [
        #     ('Laptop', 999.99, 'Electrónicos', 15),
        #     ('Mouse', 25.50, 'Accesorios', 50),
        #     ('Teclado', 45.00, 'Accesorios', 30),
        #     ('Monitor', 299.99, 'Electrónicos', 20),
        #     ('Silla Gaming', 199.99, 'Muebles', 8)
        # ]
        # cursor.executemany('INSERT INTO productos (nombre, precio, categoria, stock) VALUES (?, ?, ?, ?)', productos_ejemplo)
        
        # ventas_ejemplo = [
        #     (1, 1, 1),
        #     (2, 2, 2),
        #     (1, 3, 1),
        #     (3, 1, 1),
        #     (4, 4, 1)
        # ]
        # cursor.executemany('INSERT INTO ventas (usuario_id, producto_id, cantidad) VALUES (?, ?, ?)', ventas_ejemplo)
    
    conn.commit()
    conn.close()

def execute_query(query, params=None):
    """Ejecuta una consulta SQL y retorna los resultados"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row  # Para obtener resultados como diccionarios
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Determinar si es una consulta SELECT o una operación de modificación
        if query.strip().upper().startswith('SELECT'):
            results = [dict(row) for row in cursor.fetchall()]
            columns = [description[0] for description in cursor.description]
        else:
            conn.commit()
            results = {"affected_rows": cursor.rowcount, "message": "Query executed successfully"}
            columns = []
        
        conn.close()
        return {"success": True, "data": results, "columns": columns}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.route('/')
def index():
    """Página principal con el formulario para consultas SQL"""
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_sql():
    """Endpoint para ejecutar consultas SQL"""
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({"success": False, "error": "Query cannot be empty"})
    
    result = execute_query(query)
    return jsonify(result)

@app.route('/schema')
def get_schema():
    """Endpoint para obtener el esquema de la base de datos"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Obtener información de las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()
        
        schema = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            schema[table_name] = [{"name": col[1], "type": col[2], "nullable": not col[3], "primary_key": bool(col[5])} for col in columns]
        
        conn.close()
        return jsonify({"success": True, "schema": schema})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/examples')
def get_examples():
    """Endpoint que retorna consultas SQL de ejemplo"""
    examples = [
        {
            "title": "Listar todos los usuarios",
            "query": "SELECT * FROM usuarios;"
        },
        {
            "title": "Productos con precio mayor a 100",
            "query": "SELECT * FROM productos WHERE precio > 100;"
        },
        {
            "title": "Contar usuarios por edad",
            "query": "SELECT edad, COUNT(*) as cantidad FROM usuarios GROUP BY edad ORDER BY edad;"
        },
        {
            "title": "Ventas con información de usuarios y productos",
            "query": """SELECT 
                v.id as venta_id,
                u.nombre as usuario,
                p.nombre as producto,
                v.cantidad,
                v.fecha_venta
            FROM ventas v
            JOIN usuarios u ON v.usuario_id = u.id
            JOIN productos p ON v.producto_id = p.id
            ORDER BY v.fecha_venta DESC;"""
        },
        {
            "title": "Insertar nuevo usuario",
            "query": "INSERT INTO usuarios (nombre, email, edad) VALUES ('Nuevo Usuario', 'nuevo@email.com', 25);"
        },
        {
            "title": "Actualizar precio de producto",
            "query": "UPDATE productos SET precio = 899.99 WHERE nombre = 'Laptop';"
        }
    ]
    return jsonify({"examples": examples})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)