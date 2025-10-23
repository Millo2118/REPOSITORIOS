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

    # Crear tabla de productos de ejemplo (corregido)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Producto (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria REAL NOT NULL,
            marca TEXT,
            presentacion TEXT,
            precio INTEGER NOT NULL DEFAULT 0
        );
    ''')
    
    # Crear tabla Pedido de ejemplo (fecha_entrega puede ser NULL)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pedido (
            id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE NOT NULL,
            total INTEGER NOT NULL,
            estado TEXT NOT NULL,
            metodo_pago TEXT NOT NULL,
            observaciones TEXT,
            direccion TEXT NOT NULL,
            fecha_entrega DATE
        );
    ''')

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
        cursor.executemany('INSERT INTO Cliente (nombre, tipo_cliente, direccion, telefono) VALUES (?, ?, ?, ?)', usuarios_ejemplo)
        
        productos_ejemplo = [
             ("Aguila","Cerveza","Bavaria","Botella",4500),
             ("Aguila Light","Cerveza","Bavaria","Lata",4700),
             ("Club Colombia","Cerveza","Bavaria","Botella",5200),
             ("Club Colombia Roja","Cerveza","Bavaria","Lata",5400),
             ("Club Colombia Negra","Cerveza","Bavaria","Botella",5500),
             ("Poker","Cerveza","Bavaria","Botella",4300),
             ("Poker","Cerveza","Bavaria","Lata",4500),
             ("Costeña","Cerveza","Bavaria","Botella",4200),
             ("Costeña","Cerveza","Bavaria","Lata",4400),
             ("Pilsen","Cerveza","Bavaria","Botella",4100),
             ("Pilsen","Cerveza","Bavaria","Lata",4300),
             ("Redd's","Cerveza","Bavaria","Botella",4800),
             ("Redd's","Cerveza","Bavaria","Lata",5000),
             ("Aguila Cero","Cerveza","Bavaria","Botella",4600),
             ("Aguila Cero","Cerveza","Bavaria","Lata",4800),
             ("Club Colombia Dorada","Cerveza","Bavaria","Botella",5300),
             ("Club Colombia Dorada","Cerveza","Bavaria","Lata",5500),
             ("Poker Radler","Cerveza","Bavaria","Botella",4700),
             ("Poker Radler","Cerveza","Bavaria","Lata",4900),
             ("Costeña Bacana","Cerveza","Bavaria","Botella",4400),
             ("Costeña Bacana","Cerveza","Bavaria","Lata",4600),
             ("Aguila Original","Cerveza","Bavaria","Botella",4500),
             ("Aguila Original","Cerveza","Bavaria","Lata",4700),
             ("Club Colombia Trigo","Cerveza","Bavaria","Botella",5600),
             ("Club Colombia Trigo","Cerveza","Bavaria","Lata",5800)
        ]
        cursor.executemany('INSERT INTO Producto (nombre, categoria, marca, presentacion, precio) VALUES (?, ?, ?, ?, ?)', productos_ejemplo)
        
        pedidos_ejemplo = [
             ("2025-10-01", 125000, "Pendiente", "Efectivo", "Sin observaciones", "Cra 10 #23-45", "2025-10-03"),
             ("2025-09-28", 76000, "Enviado", "Tarjeta", "Dejar en recepción", "Calle 5 #12-34", "2025-09-30"),
             ("2025-09-30", 43000, "Entregado", "Contra entrega", "Recibido por Juan Pérez", "Av. 7 #45-67", "2025-10-01"),
             ("2025-10-02", 98000, "Pendiente", "Transferencia", "Pago en proceso", "Cra 15 #67-89", "2025-10-06"),
             ("2025-10-03", 54000, "En preparación", "Efectivo", "Agregar bolsa extra", "Calle 8 #56-78", "2025-10-05"),
             ("2025-09-25", 210000, "Cancelado", "Tarjeta", "Pedido cancelado por cliente", "Cra 20 #34-56", "2025-11-23"),
             ("2025-10-05", 67000, "En reparto", "Contra entrega", "Contactar antes de llegar", "Calle 3 #21-43", "2025-10-06"),
             ("2025-10-06", 45000, "Pendiente", "Efectivo", "Horario de entrega 9-12", "Av. 9 #12-34", "2025-10-08"),
             ("2025-09-29", 125000, "Entregado", "Transferencia", "Entrega a cuarto piso", "Cra 18 #23-45", "2025-09-30"),
             ("2025-10-04", 82000, "Enviado", "Tarjeta", "Verificar existencia", "Calle 6 #78-90", "2025-10-06"),
             ("2025-10-01", 138000, "Pendiente", "Efectivo", "Incluir factura impresa", "Cra 22 #45-67", "2025-10-04"),
             ("2025-09-27", 39000, "Entregado", "Contra entrega", "Cliente satisfecho", "Calle 12 #34-56", "2025-09-28"),
             ("2025-10-07", 157000, "En preparación", "Transferencia", "Preparar con cuidado", "Av. 5 #67-89", "2025-10-09"),
             ("2025-10-08", 47000, "Pendiente", "Tarjeta", "Llamar al llegar", "Cra 30 #12-34", "2025-10-10"),
             ("2025-09-26", 92000, "Cancelado", "Efectivo", "Sin stock", "Calle 9 #45-67", "2025-11-20"),
             ("2025-10-09", 30000, "En reparto", "Contra entrega", "Dejar con portería", "Av. 11 #23-45", "2025-10-09"),
             ("2025-10-02", 115000, "Enviado", "Transferencia", "Revisar productos frágiles", "Cra 25 #67-89", "2025-10-04"),
             ("2025-09-24", 68000, "Entregado", "Tarjeta", "Recibido por administrador", "Calle 14 #56-78", "2025-09-25"),
             ("2025-10-10", 255000, "Pendiente", "Transferencia", "Pedido grande, coordinar transporte", "Av. 13 #78-90", "2025-10-15"),
             ("2025-10-11", 54000, "En preparación", "Efectivo", "Incluir manual de uso", "Cra 17 #23-45", "2025-10-13"),
             ("2025-09-23", 47000, "Entregado", "Contra entrega", "Cliente no contestó llamada", "Calle 15 #67-89", "2025-09-24"),
             ("2025-10-12", 99000, "Enviado", "Tarjeta", "Entregar en horario nocturno", "Cra 28 #45-67", "2025-10-14"),
             ("2025-10-13", 61000, "Pendiente", "Efectivo", "Confirmar dirección", "Av. 16 #12-34", "2025-12-19"),
             ("2025-10-14", 73000, "En reparto", "Transferencia", "Evitar entregar fines de semana", "Calle 17 #34-56", "2025-10-15"),
             ("2025-10-01", 125000, "Pendiente", "Efectivo", "Sin observaciones", "Cra 10 #23-45", "2025-10-03"),
             ("2025-09-28", 76000, "Enviado", "Tarjeta", "Dejar en recepción", "Calle 5 #12-34", "2025-09-30"),
             ("2025-09-30", 43000, "Entregado", "Contra entrega", "Recibido por Juan Pérez", "Av. 7 #45-67", "2025-10-01"),
             ("2025-10-02", 98000, "Pendiente", "Transferencia", "Pago en proceso", "Cra 15 #67-89", "2025-09-14"),
             ("2025-10-03", 54000, "En preparación", "Efectivo", "Agregar bolsa extra", "Calle 8 #56-78", "2025-10-05"),
             ("2025-09-25", 210000, "Cancelado", "Tarjeta", "Pedido cancelado por cliente", "Cra 20 #34-56", "2026-03-20"),
             ("2025-10-05", 67000, "En reparto", "Contra entrega", "Contactar antes de llegar", "Calle 3 #21-43", "2025-10-06"),
             ("2025-10-06", 45000, "Pendiente", "Efectivo", "Horario de entrega 9-12", "Av. 9 #12-34", "2025-10-08"),
             ("2025-09-29", 125000, "Entregado", "Transferencia", "Entrega a cuarto piso", "Cra 18 #23-45", "2025-09-30"),
             ("2025-10-04", 82000, "Enviado", "Tarjeta", "Verificar existencia", "Calle 6 #78-90", "2025-10-06"),
             ("2025-10-01", 138000, "Pendiente", "Efectivo", "Incluir factura impresa", "Cra 22 #45-67", "2025-10-04"),
             ("2025-09-27", 39000, "Entregado", "Contra entrega", "Cliente satisfecho", "Calle 12 #34-56", "2025-09-28"),
             ("2025-10-07", 157000, "En preparación", "Transferencia", "Preparar con cuidado", "Av. 5 #67-89", "2025-10-09"),
             ("2025-10-08", 47000, "Pendiente", "Tarjeta", "Llamar al llegar", "Cra 30 #12-34", "2025-10-10"),
             ("2025-09-26", 92000, "Cancelado", "Efectivo", "Sin stock", "Calle 9 #45-67", "2026-06-23"),
             ("2025-10-09", 30000, "En reparto", "Contra entrega", "Dejar con portería", "Av. 11 #23-45", "2025-10-09"),
             ("2025-10-02", 115000, "Enviado", "Transferencia", "Revisar productos frágiles", "Cra 25 #67-89", "2025-10-04"),
             ("2025-09-24", 68000, "Entregado", "Tarjeta", "Recibido por administrador", "Calle 14 #56-78", "2025-09-25"),
             ("2025-10-10", 255000, "Pendiente", "Transferencia", "Pedido grande, coordinar transporte", "Av. 13 #78-90", "2025-10-15"),
             ("2025-10-11", 54000, "En preparación", "Efectivo", "Incluir manual de uso", "Cra 17 #23-45", "2025-10-13"),
             ("2025-09-23", 47000, "Entregado", "Contra entrega", "Cliente no contestó llamada", "Calle 15 #67-89", "2025-09-24"),
             ("2025-10-12", 99000, "Enviado", "Tarjeta", "Entregar en horario nocturno", "Cra 28 #45-67", "2025-10-14"),
             ("2025-10-13", 61000, "Pendiente", "Efectivo", "Confirmar dirección", "Av. 16 #12-34", "2026-06-13"),
             ("2025-10-14", 73000, "En reparto", "Transferencia", "Evitar entregar fines de semana", "Calle 17 #34-56", "2025-10-15")
        ]
        cursor.executemany('INSERT INTO Pedido (fecha, total, estado, metodo_pago, observaciones, direccion, fecha_entrega) VALUES (?, ?, ?, ?, ?, ?, ?)', pedidos_ejemplo)
        
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
    """Endpoint que retorna consultas SQL de ejemplo (renombrar columnas, filtrar y más)"""
    examples = [
        # Renombrar columna en la tabla (SQLite >= 3.25.0)
        {
            "title": "Renombrar columna (tabla)",
            "query": "ALTER TABLE Pedido RENAME COLUMN direccion TO direccion_entrega;"
        },

        # Renombrar columna solo en el resultado (alias)
        {
            "title": "Alias: renombrar columna en SELECT",
            "query": "SELECT id_pedido AS pedido, fecha AS fecha_pedido, direccion AS direccion_entrega, total FROM Pedido;"
        },

        # Ordenar resultados (ORDER BY) - ejemplos
        {
            "title": "Ordenar por precio ascendente",
            "query": "SELECT id_producto, nombre, precio FROM Producto ORDER BY precio ASC;"
        },
        {
            "title": "Ordenar por precio desc y nombre asc",
            "query": "SELECT id_producto, nombre, precio FROM Producto ORDER BY precio DESC, nombre ASC;"
        },

        # Filtrar (WHERE) - ejemplos
        {
            "title": "Filtrar pedidos por estado y rango de total",
            "query": "SELECT id_pedido, fecha, total, estado FROM Pedido WHERE estado = 'Pendiente' AND total BETWEEN 50000 AND 200000;"
        },
        {
            "title": "Filtrar clientes por tipo y nombre parcial (LIKE)",
            "query": "SELECT id_cliente, nombre, telefono FROM Cliente WHERE tipo_cliente IN ('Mayorista','Licorera') AND nombre LIKE '%Supermercado%';"
        },

        # NULL checks y actualización
        {
            "title": "Buscar pedidos sin fecha_entrega y actualizar",
            "query": "SELECT id_pedido, fecha, fecha_entrega FROM Pedido WHERE fecha_entrega IS NULL;\n-- Para rellenar: UPDATE Pedido SET fecha_entrega = fecha WHERE fecha_entrega IS NULL;"
        },

        # Aliases en WHERE usando CTE
        {
            "title": "Usar alias en WHERE (CTE)",
            "query": "WITH cte AS (SELECT id_pedido, total AS total_pesos FROM Pedido) SELECT * FROM cte WHERE total_pesos > 100000;"
        },

        # PRAGMA para ver esquema/columnas
        {
            "title": "Ver columnas de una tabla",
            "query": "PRAGMA table_info(Pedido);"
        }
    ]
    return jsonify({"examples": examples})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)