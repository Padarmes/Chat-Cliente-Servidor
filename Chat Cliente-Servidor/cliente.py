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