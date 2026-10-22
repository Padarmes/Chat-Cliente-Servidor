**DOCUMENTACIÓN  
TÉCNICA DEL PROYECTO**

Sistema de chat TCP para red local

Arquitectura • Funcionamiento • Componentes • Código fuente

| **Proyecto**            | Chat de comunicación entre equipos en una red local |
|-------------------------|-----------------------------------------------------|
| **Tecnologías**         | Python, sockets TCP, hilos, Tkinter y SQLite        |
| **Versión documentada** | Código proporcionado para análisis                  |
| **Autor / equipo**      | \[Completar\]                                       |

*Documento base editable. Completar los campos institucionales y validar los detalles de despliegue antes de entregar.*



> **Elementos repetidos del documento original:** encabezado: DOCUMENTACIÓN TÉCNICA  |  SISTEMA DE CHAT LOCAL. Pie de página: Proyecto de comunicación en red local • Documento técnico   |   Página 1–18.

# Control del documento

| **Campo**            | **Descripción**                                                                | **Estado**    |
|----------------------|--------------------------------------------------------------------------------|---------------|
| Objetivo             | Describir la arquitectura, operación y estructura del código del chat.         | Preparado     |
| Alcance              | Cliente gráfico, servidor TCP y persistencia local de mensajes.                | Incluido      |
| Pendiente de validar | Pruebas reales, sistema operativo, topología de red y requisitos de seguridad. | Por completar |

Nota: esta documentación describe el comportamiento que se observa en el código entregado. No afirma que se hayan ejecutado pruebas ni que existan funciones que todavía no están implementadas.

# 1. Resumen ejecutivo

El proyecto implementa un chat de texto cliente-servidor mediante sockets TCP. El servidor recibe conexiones, asigna un color a cada conexión, distribuye los mensajes a los clientes conectados y guarda el historial en una base de datos SQLite. El cliente presenta una interfaz gráfica creada con Tkinter, permite indicar la dirección IP y el puerto del servidor, elegir un nombre al conectarse, enviar mensajes y consultar los mensajes recibidos.

La solución puede operar sin acceso a Internet siempre que los equipos tengan conectividad entre sí por una red local (por ejemplo, una LAN o un punto de acceso local) y que la dirección IP y el puerto sean accesibles. El código no implementa una conexión a Internet ni depende de un servicio externo.

# 2. Objetivo y alcance

## 2.1 Objetivo general

Documentar cómo se estructura y funciona el sistema de chat, justificando la separación entre cliente y servidor y explicando los componentes principales del código.

## 2.2 Funcionalidades presentes en el código

- Comunicación entre varios equipos mediante TCP/IP.

- Interfaz gráfica para conectar, leer y enviar mensajes.

- Elección del nombre al iniciar la conexión.

- Asignación de colores a los usuarios conectados y visualización del nombre en ese color.

- Distribución de mensajes a todos los clientes conectados.

- Registro persistente de mensajes, fecha, usuario y color en SQLite.

- Envío del historial almacenado cuando se conecta un cliente nuevo.

- Avisos de conexión y desconexión, y límite configurado de diez clientes.

- Recepción de mensajes en un hilo separado para no bloquear la interfaz gráfica.

## 2.3 Límites identificados

- El cambio de nombre después de conectarse no está implementado. El nombre se solicita al conectar y se mantiene durante esa sesión.

- No hay autenticación, cifrado TLS, administración de permisos ni protección contra suplantación de nombres.

- El límite de clientes es 10. La lista de colores también tiene 10 valores; si todos están ocupados, la función vuelve al primer color, por lo que podría repetirse.

- El protocolo separa campos mediante el carácter \|. Aunque el cliente recompone partes del texto, los mensajes que contienen ese carácter pueden volver ambiguo el formato.

- El servidor guarda la base de datos en el archivo relativo chat.db, en el directorio desde el que se ejecuta el proceso.

- La gestión de errores es básica: algunas excepciones se silencian y la desconexión por fallo de envío no siempre elimina todas las estructuras asociadas al cliente.

# 3. Arquitectura del sistema

Se adopta una arquitectura cliente-servidor centralizada. Los clientes no se envían mensajes directamente entre sí: cada cliente mantiene una conexión con el servidor, y este actúa como intermediario. Esta decisión simplifica la distribución de mensajes, la asignación de colores y la conservación de un historial común.

## 3.1 Vista lógica

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>CLIENTE A<br />
Tkinter + socket TCP</strong></th>
<th><strong>SERVIDOR<br />
socket TCP + hilos</strong></th>
<th><strong>CLIENTE B<br />
Tkinter + socket TCP</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Envía mensajes<br />
Recibe y muestra</td>
<td>Gestiona conexiones<br />
Reenvía mensajes<br />
Asigna colores</td>
<td>Envía mensajes<br />
Recibe y muestra</td>
</tr>
<tr class="even">
<td>↘</td>
<td><strong>SQLite: chat.db<br />
mensajes persistentes</strong></td>
<td>↙</td>
</tr>
</tbody>
</table>

Flujo general: los clientes envían solicitudes al servidor por TCP; el servidor procesa cada conexión en un hilo, registra los mensajes y los retransmite a los clientes conectados. Al entrar, un cliente recibe el historial almacenado.

## 3.2 Componentes y responsabilidades

| **Componente** | **Responsabilidad**                                                  | **Tecnología / elementos**                                          |
|----------------|----------------------------------------------------------------------|---------------------------------------------------------------------|
| Cliente        | Interfaz, validación básica, envío y presentación de mensajes.       | Tkinter, socket, threading, after()                                 |
| Servidor       | Aceptación de conexiones, control de clientes, difusión y protocolo. | socket TCP, threading, Lock                                         |
| Persistencia   | Guardar mensajes y recuperar el historial.                           | SQLite, tabla mensajes                                              |
| Protocolo      | Identificar el tipo de evento y separar sus campos.                  | Texto UTF-8 delimitado por \| y líneas terminadas en salto de línea |

## 3.3 Justificación de las decisiones

**TCP.** Se usa SOCK_STREAM porque proporciona un flujo de bytes fiable y ordenado. La aplicación debe definir cómo delimitar cada mensaje; en este código se usa el salto de línea como terminador.

**Modelo cliente-servidor.** Centraliza el envío, la asignación de colores y el historial. Los clientes solo necesitan conocer la IP y el puerto del servidor.

**Hilos.** El servidor crea un hilo por conexión para atender varios clientes concurrentemente. El cliente también usa un hilo para recibir mensajes mientras la ventana permanece interactiva.

**Tkinter.** Permite construir la ventana de escritorio sin incorporar un framework gráfico externo.

**SQLite.** Almacena el historial en un archivo local, sin requerir un servidor de base de datos independiente ni Internet.

# 4. Flujo de funcionamiento

**1. Inicio del servidor:** Se crea o actualiza la tabla mensajes, se abre el socket TCP, se enlaza al puerto 5000 y se empieza a escuchar conexiones.

**2. Conexión del cliente:** El usuario introduce IP y puerto; la aplicación solicita un nombre, abre el socket y envía el nombre al servidor.

**3. Validación del servidor:** El servidor verifica que el nombre recibido no esté vacío y que no se haya alcanzado el límite MAX_CLIENTS. Después registra el socket y asigna un color.

**4. Carga del historial:** El servidor consulta SQLite y envía los mensajes guardados al cliente recién conectado.

**5. Envío de un mensaje:** El cliente envía el texto con el prefijo MENSAJE\|. El servidor identifica el texto, guarda el mensaje con usuario, fecha y color y lo difunde.

**6. Recepción y presentación:** El cliente interpreta el tipo de mensaje. Para los mensajes de chat muestra la fecha, el nombre en color y el texto en color normal.

**7. Desconexión:** Al cerrar la ventana se cierra el socket del cliente. El servidor detecta el cierre, elimina al cliente de las estructuras y notifica a los demás.

# 5. Protocolo de mensajes

El protocolo es un formato textual sencillo. Los mensajes se codifican en UTF-8 y el servidor añade un salto de línea al enviarlos. En el cliente, recibir_mensajes acumula bytes decodificados en un búfer hasta encontrar una línea completa.

| **Tipo**          | **Formato ilustrativo**                 | **Uso**                                                    |
|-------------------|-----------------------------------------|------------------------------------------------------------|
| Identificación    | nombre\n                                | El cliente comunica su nombre al conectarse.               |
| Mensaje           | MENSAJE\|texto\n                        | El cliente solicita publicar un mensaje.                   |
| Mensaje difundido | MENSAJE\|usuario\|texto\|fecha\|color   | El servidor envía el mensaje enriquecido a los clientes.   |
| Historial         | HISTORIAL\|usuario\|texto\|fecha\|color | El servidor entrega mensajes previamente almacenados.      |
| Sistema           | SISTEMA\|texto                          | Notifica conexión, desconexión o estado del sistema.       |
| Error             | ERROR\|texto                            | Comunica un problema, por ejemplo, que el chat está lleno. |

Importante: TCP es un flujo y no garantiza que cada llamada recv() corresponda exactamente a un mensaje completo. El cliente procesa líneas mediante un búfer; en el servidor, en cambio, la lectura de nombre y la lectura posterior de mensajes asumen que los datos llegan en bloques adecuados. Para robustecer el protocolo se recomienda implementar lectura por líneas también en el servidor y definir un escape para el carácter \|.

# 6. Base de datos

La base de datos se llama chat.db y contiene la tabla mensajes. El identificador id es autoincremental y permite recuperar el historial en el orden de inserción.

| **Campo** | **Tipo / restricción**            | **Finalidad**                                |
|-----------|-----------------------------------|----------------------------------------------|
| id        | INTEGER PRIMARY KEY AUTOINCREMENT | Identificador y orden de inserción.          |
| usuario   | TEXT NOT NULL                     | Nombre del remitente.                        |
| mensaje   | TEXT NOT NULL                     | Contenido del mensaje.                       |
| fecha     | TEXT NOT NULL                     | Fecha y hora en formato YYYY-MM-DD HH:MM:SS. |
| color     | TEXT NOT NULL DEFAULT '#333333'   | Color asociado al remitente en ese mensaje.  |

crear_base_datos() crea la tabla si no existe y comprueba si falta la columna color para agregarla a una base de datos anterior. guardar_mensaje() inserta cada mensaje usando parámetros SQL, y obtener_historial() recupera los registros en orden ascendente.

# 7. Funciones importantes del cliente

**\_\_init\_\_(ventana) —** Inicializa el estado de la aplicación, configura el título y tamaño de ventana, crea la interfaz y conecta el cierre de la ventana con cerrar_conexion().

**crear_interfaz() —** Construye los campos de IP y puerto, el botón de conexión, el área desplazable del chat, la entrada de mensajes y el botón Enviar. Enter también ejecuta el envío.

**mostrar_mensaje(texto) —** Añade una línea de texto general al área del chat y desplaza la vista al final.

**mostrar_mensaje_usuario(fecha, usuario, texto_mensaje, color) —** Presenta fecha, nombre coloreado y mensaje. Utiliza etiquetas de formato de Tkinter para colorear solo el nombre.

**conectar() —** Valida IP y puerto, solicita el nombre, abre el socket TCP, envía el nombre, cambia el estado de los controles y crea el hilo receptor.

**recibir_mensajes() —** Lee los datos recibidos, recompone líneas completas usando un búfer y delega cada línea a procesar_mensaje().

**procesar_mensaje(mensaje) —** Interpreta los prefijos SISTEMA, HISTORIAL, MENSAJE y ERROR; programa las actualizaciones de interfaz con ventana.after() para ejecutarlas en el hilo de Tkinter.

**enviar_mensaje() —** Comprueba conexión y contenido no vacío, transmite el texto con el prefijo MENSAJE\| y limpia la entrada.

**conexion_perdida() —** Deshabilita el envío e informa que se perdió la conexión.

**cerrar_conexion() —** Marca la conexión como cerrada, intenta cerrar el socket y destruye la ventana.

# 8. Funciones importantes del servidor

**crear_base_datos() —** Crea la tabla mensajes si hace falta y adapta una base antigua si no contiene la columna color.

**guardar_mensaje(usuario, mensaje, color) —** Genera la fecha y almacena el mensaje y sus metadatos en SQLite.

**obtener_historial() —** Consulta los mensajes persistidos ordenados por id.

**obtener_color_disponible() —** Busca el primer color de la lista que no esté asignado a un cliente conectado.

**enviar_mensaje(cliente, mensaje) —** Codifica el mensaje en UTF-8, añade el salto de línea y lo transmite. Devuelve True si no se produjo excepción.

**enviar_a_todos(mensaje, cliente_excluido=None) —** Recorre las conexiones activas y retransmite el mensaje, con opción de excluir una conexión.

**desconectar_cliente(cliente) —** Elimina el cliente y su color de los diccionarios, cierra el socket y anuncia la desconexión si había un usuario registrado.

**atender_cliente(cliente, direccion) —** Gestiona el ciclo de vida de una conexión: recibe el nombre, valida capacidad, asigna color, envía historial, recibe mensajes, los guarda y los difunde.

**iniciar_servidor() —** Inicializa la base de datos, crea el socket de escucha, habilita reutilizar el puerto, enlaza HOST y PORT y crea un hilo por cliente aceptado.

# 9. Variables y estructuras relevantes

| **Elemento**     | **Valor / estructura**       | **Significado**                                                                 |
|------------------|------------------------------|---------------------------------------------------------------------------------|
| HOST             | '0.0.0.0'                    | Escucha en todas las interfaces de red IPv4 del equipo servidor.                |
| PORT             | 5000                         | Puerto TCP utilizado por el servidor.                                           |
| MAX_CLIENTS      | 10                           | Máximo de clientes conectados según el control de admisión.                     |
| clientes         | diccionario socket → usuario | Mantiene sockets de clientes activos y sus nombres.                             |
| colores_clientes | diccionario socket → color   | Relaciona cada conexión con su color de sesión.                                 |
| lock_clientes    | threading.Lock()             | Protege operaciones concurrentes sobre las estructuras compartidas de clientes. |
| self.conectado   | booleano                     | Indica si el cliente considera activa la conexión.                              |
| self.socket      | socket o None                | Socket TCP utilizado por el cliente.                                            |

# 10. Instalación y ejecución

Requisitos: Python 3 con los módulos estándar socket, threading, sqlite3, datetime y tkinter. En algunas distribuciones Linux, Tkinter puede requerir la instalación del paquete del sistema correspondiente.

## 10.1 En el equipo servidor

- Guardar el código del servidor en un archivo, por ejemplo servidor.py.

- Ejecutar desde una terminal: python servidor.py

- Confirmar que aparezca el mensaje de espera de conexiones y que el puerto 5000 esté permitido por el firewall para la red local.

- Mantener el programa activo mientras los clientes estén utilizando el chat.

## 10.2 En cada equipo cliente

- Guardar el código del cliente en un archivo, por ejemplo cliente.py.

- Asegurar que el equipo cliente pueda alcanzar la IP local del servidor.

- Ejecutar: python cliente.py

- Escribir la IP del servidor y el puerto 5000, pulsar Conectar e introducir un nombre.

La IP predeterminada del cliente es 192.168.137.1, pero debe reemplazarse por la dirección IPv4 real del equipo que ejecuta el servidor si la topología de red es diferente. HOST='0.0.0.0' no es la dirección que se escribe en el cliente: significa que el servidor escucha en todas las interfaces IPv4 locales.

## 10.3 Operación sin Internet

No se necesita Internet ni un servidor externo. Sí se necesita una red local funcional que permita el tráfico entre los equipos. Si se utiliza un punto de acceso o una red compartida, debe evitarse el aislamiento de clientes y debe permitirse el puerto TCP 5000. Si el firewall bloquea ese puerto, la conexión fallará aunque los equipos estén conectados a la misma red.

# 11. Pruebas recomendadas

La siguiente matriz sirve para registrar pruebas de aceptación. Los resultados deben completarse después de ejecutar el programa; no se consideran pruebas ya realizadas.

| **ID** | **Prueba**                         | **Resultado esperado**                                                     | **Resultado real** |
|--------|------------------------------------|----------------------------------------------------------------------------|--------------------|
| P-01   | Conectar un cliente                | El cliente se conecta y muestra el aviso de sistema.                       | \[Completar\]      |
| P-02   | Conectar dos clientes              | Ambos clientes pueden intercambiar mensajes.                               | \[Completar\]      |
| P-03   | Enviar mensaje con tildes/emoji    | El texto UTF-8 se presenta correctamente.                                  | \[Completar\]      |
| P-04   | Reiniciar el servidor y reconectar | Los mensajes guardados aparecen en el historial, si la base persiste.      | \[Completar\]      |
| P-05   | Intentar un puerto no numérico     | El cliente muestra un error de validación.                                 | \[Completar\]      |
| P-06   | Conectar más de diez clientes      | El servidor rechaza conexiones que superen el límite configurado.          | \[Completar\]      |
| P-07   | Desconectar un cliente             | Los demás reciben un aviso de desconexión.                                 | \[Completar\]      |
| P-08   | Operar sin Internet en LAN         | Los clientes se comunican si la red local y el firewall permiten TCP 5000. | \[Completar\]      |

# 12. Riesgos y mejoras recomendadas

**Lectura TCP robusta.** Implementar en el servidor un búfer de líneas como el del cliente; una llamada recv() puede contener parte de un mensaje o varios mensajes.

**Control de concurrencia.** Revisar el uso del lock durante la difusión. Evitar mantener el bloqueo global mientras se realizan operaciones de red potencialmente lentas.

**Limpieza de clientes.** Cuando falla un envío, asegurar que se eliminen el socket, el nombre y el color, y que se cierre la conexión.

**Manejo de errores.** Registrar excepciones específicas en lugar de ignorarlas y distinguir un cierre esperado de un error de red.

**Validación de nombres.** Limitar longitud y caracteres, y definir si se permiten nombres duplicados.

**Cambio de nombre.** Si es requisito, diseñar un comando de protocolo específico para cambiar el nombre y actualizar de forma sincronizada los diccionarios y avisos.

**Protocolo seguro.** Definir escape de delimitadores o usar JSON por línea; validar tamaño de mensajes y campos.

**Seguridad.** Si se necesita confidencialidad o autenticación, añadir un mecanismo de identidad y cifrado. El código actual transmite texto sin cifrar y no verifica identidades.

**Colores.** Asegurar que los colores sean distinguibles y definir comportamiento cuando no haya colores libres.

**Historial.** Definir una política de retención, límite de tamaño y opción de limpiar/exportar el historial.

# 13. Guía de lectura del código fuente

El código completo se incluye en los anexos, separado en cliente y servidor. Se conserva la lógica del código recibido; los títulos y la explicación de las secciones sirven para facilitar la revisión y no representan una reescritura del programa.

# Anexo A. Código fuente del cliente

Archivo sugerido: cliente.py. Implementa la interfaz gráfica, la conexión TCP y el procesamiento de los mensajes recibidos.

~~~python
import socket
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext


class ClienteChat:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Chat TCP")
        self.ventana.geometry("600x500")

        self.socket = None
        self.usuario = None
        self.conectado = False

        self.crear_interfaz()

        self.ventana.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar_conexion
        )

    def crear_interfaz(self):
        marco_superior = tk.Frame(self.ventana)
        marco_superior.pack(pady=10)

        tk.Label(
            marco_superior,
            text="IP del servidor:"
        ).grid(row=0, column=0, padx=5)

        self.entrada_ip = tk.Entry(marco_superior, width=18)
        self.entrada_ip.insert(0, "192.168.137.1")
        self.entrada_ip.grid(row=0, column=1, padx=5)

        tk.Label(
            marco_superior,
            text="Puerto:"
        ).grid(row=0, column=2, padx=5)

        self.entrada_puerto = tk.Entry(marco_superior, width=8)
        self.entrada_puerto.insert(0, "5000")
        self.entrada_puerto.grid(row=0, column=3, padx=5)

        self.boton_conectar = tk.Button(
            marco_superior,
            text="Conectar",
            command=self.conectar
        )
        self.boton_conectar.grid(row=0, column=4, padx=5)

        self.area_chat = scrolledtext.ScrolledText(
            self.ventana,
            width=70,
            height=22,
            state="disabled",
            wrap=tk.WORD
        )
        self.area_chat.pack(padx=10, pady=10)

        marco_mensaje = tk.Frame(self.ventana)
        marco_mensaje.pack(fill=tk.X, padx=10, pady=10)

        self.entrada_mensaje = tk.Entry(marco_mensaje)
        self.entrada_mensaje.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            padx=(0, 10)
        )

        self.entrada_mensaje.bind(
            "<Return>",
            lambda evento: self.enviar_mensaje()
        )

        self.boton_enviar = tk.Button(
            marco_mensaje,
            text="Enviar",
            command=self.enviar_mensaje,
            state="disabled"
        )
        self.boton_enviar.pack(side=tk.RIGHT)

    def mostrar_mensaje(self, texto):
        self.area_chat.config(state="normal")
        self.area_chat.insert(tk.END, texto + "\n")
        self.area_chat.see(tk.END)
        self.area_chat.config(state="disabled")


    def mostrar_mensaje_usuario(self, fecha, usuario, texto_mensaje, color):
        self.area_chat.config(state="normal")

        # Mostrar la fecha normalmente
        self.area_chat.insert(
            tk.END,
            f"[{fecha}] "
        )

        # Crear un tag para el color del usuario
        nombre_tag = "color_" + color.replace("#", "")

        self.area_chat.tag_configure(
            nombre_tag,
            foreground=color
        )

        # Mostrar solamente el nombre con color
        self.area_chat.insert(
            tk.END,
            usuario,
            nombre_tag
        )

        # Mostrar el mensaje con el color normal
        self.area_chat.insert(
            tk.END,
            f": {texto_mensaje}\n"
        )

        self.area_chat.see(tk.END)
        self.area_chat.config(state="disabled")


    def conectar(self):
        if self.conectado:
            return

        ip = self.entrada_ip.get().strip()
        puerto_texto = self.entrada_puerto.get().strip()

        if not ip:
            messagebox.showerror(
                "Error",
                "Escribe la IP del servidor"
            )
            return

        try:
            puerto = int(puerto_texto)
        except ValueError:
            messagebox.showerror(
                "Error",
                "El puerto debe ser un número"
            )
            return

        nombre = simpledialog.askstring(
            "Nombre",
            "Escribe tu nombre:",
            parent=self.ventana
        )

        if not nombre:
            return

        try:
            self.socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            self.socket.connect((ip, puerto))

            # Enviar el nombre al servidor
            self.socket.sendall(
                (nombre + "\n").encode("utf-8")
            )

            self.usuario = nombre
            self.conectado = True

            self.boton_conectar.config(
                state="disabled"
            )

            self.boton_enviar.config(
                state="normal"
            )

            self.entrada_ip.config(
                state="disabled"
            )

            self.entrada_puerto.config(
                state="disabled"
            )

            self.mostrar_mensaje(
                "[SISTEMA] Conectado al servidor"
            )

            hilo = threading.Thread(
                target=self.recibir_mensajes,
                daemon=True
            )

            hilo.start()

        except Exception as error:
            messagebox.showerror(
                "Error de conexión",
                f"No se pudo conectar:\n{error}"
            )

            self.socket = None

    def recibir_mensajes(self):
        buffer = ""

        try:
            while self.conectado:
                datos = self.socket.recv(4096)

                if not datos:
                    break

                buffer += datos.decode("utf-8")

                while "\n" in buffer:
                    linea, buffer = buffer.split("\n", 1)

                    if linea:
                        self.procesar_mensaje(linea)

        except Exception:
            pass

        self.conectado = False

        self.ventana.after(
            0,
            self.conexion_perdida
        )

    def procesar_mensaje(self, mensaje):
        partes = mensaje.split("|")

        if partes[0] == "SISTEMA":
            texto = "[SISTEMA] " + "|".join(partes[1:])

            self.ventana.after(
                0,
                self.mostrar_mensaje,
                texto
            )

        elif partes[0] == "HISTORIAL":
            if len(partes) >= 5:
                usuario = partes[1]

                # El color y la fecha son los dos ultimos datos
                color = partes[-1]
                fecha = partes[-2]

                # Todo lo que exista entre usuario y fecha es el mensaje
                texto_mensaje = "|".join(partes[2:-2])

                self.ventana.after(
                    0,
                    self.mostrar_mensaje_usuario,
                    fecha,
                    usuario,
                    texto_mensaje,
                    color
                )

        elif partes[0] == "MENSAJE":
            if len(partes) >= 5:
                usuario = partes[1]

                color = partes[-1]
                fecha = partes[-2]

                texto_mensaje = "|".join(partes[2:-2])

                self.ventana.after(
                    0,
                    self.mostrar_mensaje_usuario,
                    fecha,
                    usuario,
                    texto_mensaje,
                    color
                )

        elif partes[0] == "ERROR":
            texto = "[ERROR] " + "|".join(partes[1:])

            self.ventana.after(
                0,
                self.mostrar_mensaje,
                texto
            )

        else:
            self.ventana.after(
                0,
                self.mostrar_mensaje,
                mensaje
            )

    def enviar_mensaje(self):
        if not self.conectado:
            return

        texto = self.entrada_mensaje.get().strip()

        if not texto:
            return

        try:
            mensaje = f"MENSAJE|{texto}\n"

            self.socket.sendall(
                mensaje.encode("utf-8")
            )

            self.entrada_mensaje.delete(
                0,
                tk.END
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo enviar el mensaje:\n{error}"
            )

    def conexion_perdida(self):
        self.boton_enviar.config(
            state="disabled"
        )

        self.mostrar_mensaje(
            "[SISTEMA] Se perdió la conexión con el servidor"
        )

    def cerrar_conexion(self):
        self.conectado = False

        try:
            if self.socket:
                self.socket.close()
        except:
            pass

        self.ventana.destroy()


if __name__ == "__main__":
    ventana = tk.Tk()

    aplicacion = ClienteChat(ventana)

    ventana.mainloop()
~~~

# Anexo B. Código fuente del servidor

Archivo sugerido: servidor.py. Implementa el socket de escucha, la concurrencia por hilos, la difusión de mensajes y la persistencia SQLite.

~~~python
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
~~~

# 14. Resumen

La solución está organizada en dos programas: un cliente gráfico y un servidor central. El cliente se ocupa de la interacción con el usuario y el servidor coordina la comunicación, asigna colores y conserva el historial en SQLite. La arquitectura es adecuada para una demostración o uso controlado en una red local sin Internet, siempre que exista conectividad entre equipos. Antes de considerarlo listo para un entorno más exigente, conviene reforzar el protocolo TCP, el tratamiento de desconexiones, la validación de datos y la seguridad.
