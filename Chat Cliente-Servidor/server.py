import socket
import threading
import sqlite3
from datetime import datetime


# ---------------- CONFIGURACIÓN ----------------

HOST = "0.0.0.0"
PORT = 5000
MAX_CLIENTS = 10

# Colores disponibles para los usuarios
COLORES_USUARIOS = [
    "#D32F2F",  # Rojo
    "#1976D2",  # Azul
    "#388E3C",  # Verde
    "#7B1FA2",  # Morado
    "#F57C00",  # Naranja
    "#00796B",  # Verde azulado
    "#C2185B",  # Rosado
    "#455A64",  # Gris azulado
    "#512DA8",  # Violeta
    "#5D4037"   # Cafe
]

clientes = {}
colores_clientes = {}

lock_clientes = threading.Lock()
# ---------------- BASE DE DATOS ----------------

def crear_base_datos():
    conexion = sqlite3.connect("chat.db")

    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            mensaje TEXT NOT NULL,
            fecha TEXT NOT NULL,
            color TEXT NOT NULL DEFAULT '#333333'
        )
    """)

    # Si la base de datos ya existia antes de agregar colores,
    # agregamos la nueva columna automaticamente.
    cursor.execute("PRAGMA table_info(mensajes)")
    columnas = [fila[1] for fila in cursor.fetchall()]

    if "color" not in columnas:
        cursor.execute("""
            ALTER TABLE mensajes
            ADD COLUMN color TEXT NOT NULL DEFAULT '#333333'
        """)

    conexion.commit()
    conexion.close()


def guardar_mensaje(usuario, mensaje, color):
    conexion = sqlite3.connect("chat.db")

    cursor = conexion.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO mensajes (usuario, mensaje, fecha, color)
        VALUES (?, ?, ?, ?)
    """, (usuario, mensaje, fecha, color))

    conexion.commit()
    conexion.close()


def obtener_historial():
    conexion = sqlite3.connect("chat.db")

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT usuario, mensaje, fecha, color
        FROM mensajes
        ORDER BY id ASC
    """)

    mensajes = cursor.fetchall()

    conexion.close()

    return mensajes


def obtener_color_disponible():
    colores_usados = set(colores_clientes.values())

    for color in COLORES_USUARIOS:
        if color not in colores_usados:
            return color

    return COLORES_USUARIOS[0]



# ---------------- COMUNICACIÓN ----------------

def enviar_mensaje(cliente, mensaje):
    try:
        cliente.sendall((mensaje + "\n").encode("utf-8"))
        return True
    except:
        return False


def enviar_a_todos(mensaje, cliente_excluido=None):
    clientes_eliminados = []

    with lock_clientes:
        for cliente, usuario in clientes.items():

            if cliente == cliente_excluido:
                continue

            if not enviar_mensaje(cliente, mensaje):
                clientes_eliminados.append(cliente)

        for cliente in clientes_eliminados:
            clientes.pop(cliente, None)


def desconectar_cliente(cliente):
    with lock_clientes:
        usuario = clientes.pop(cliente, None)
        colores_clientes.pop(cliente, None)

    try:
        cliente.close()
    except:
        pass

    if usuario:
        print(f"[DESCONEXIÓN] {usuario}")
        enviar_a_todos(f"SISTEMA|{usuario} se ha desconectado")


# ---------------- MANEJO DE CLIENTES ----------------

def atender_cliente(cliente, direccion):
    usuario = None
    color = None

    try:
        # El cliente primero envía su nombre
        datos = cliente.recv(1024).decode("utf-8").strip()

        if not datos:
            cliente.close()
            return

        usuario = datos

        with lock_clientes:
            if len(clientes) >= MAX_CLIENTS:
                enviar_mensaje(cliente, "ERROR|El chat está lleno")
                cliente.close()
                return

            color = obtener_color_disponible()

            clientes[cliente] = usuario
            colores_clientes[cliente] = color

        print(f"[CONEXIÓN] {usuario} - {direccion}")

        enviar_mensaje(cliente, "SISTEMA|Conectado correctamente al servidor")

        # Enviar historial anterior al nuevo cliente
        historial = obtener_historial()

        for usuario_historial, mensaje_historial, fecha, color_historial in historial:
            enviar_mensaje(
                cliente,
                f"HISTORIAL|{usuario_historial}|{mensaje_historial}|{fecha}|{color_historial}"
            )

        enviar_a_todos(
            f"SISTEMA|{usuario} se ha conectado",
            cliente_excluido=cliente
        )

        # Recibir mensajes continuamente
        while True:
            datos = cliente.recv(4096)

            if not datos:
                break

            mensaje = datos.decode("utf-8").strip()

            if not mensaje:
                continue

            if mensaje.startswith("MENSAJE|"):
                texto = mensaje.split("|", 1)[1]

                guardar_mensaje(usuario, texto, color)

                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                mensaje_completo = f"MENSAJE|{usuario}|{texto}|{fecha}|{color}"

                # Enviar a todos los clientes, incluido quien envio
                enviar_a_todos(mensaje_completo)

    except Exception as error:
        print(f"[ERROR] {error}")

    finally:
        desconectar_cliente(cliente)


# ---------------- INICIO DEL SERVIDOR ----------------

def iniciar_servidor():
    crear_base_datos()

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Permite reutilizar el puerto
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    servidor.bind((HOST, PORT))
    servidor.listen(MAX_CLIENTS)

    print("======================================")
    print("       SERVIDOR TCP DE CHAT")
    print("======================================")
    print(f"Puerto: {PORT}")
    print(f"Máximo de clientes: {MAX_CLIENTS}")
    print("Esperando conexiones...")
    print("Presiona Ctrl + C para detener el servidor")
    print("======================================")

    while True:
        cliente, direccion = servidor.accept()

        hilo = threading.Thread(
            target=atender_cliente,
            args=(cliente, direccion),
            daemon=True
        )

        hilo.start()


if __name__ == "__main__":
    iniciar_servidor()