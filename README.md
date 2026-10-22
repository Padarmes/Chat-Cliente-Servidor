# Chat TCP

Aplicación de chat de texto cliente-servidor para redes locales, desarrollada en Python. Utiliza sockets TCP para la comunicación, Tkinter para la interfaz del cliente y SQLite para conservar el historial de mensajes. No requiere acceso a Internet ni paquetes externos.

## Contenido

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Arquitectura](#arquitectura)
- [Protocolo de comunicación](#protocolo-de-comunicación)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Limitaciones conocidas](#limitaciones-conocidas)
- [Documentación adicional](#documentación-adicional)

## Características

- Comunicación entre múltiples equipos mediante TCP, con un máximo de 10 clientes simultáneos.
- Cliente con interfaz gráfica para conectarse, enviar y leer mensajes.
- Un hilo por conexión en el servidor y un hilo de recepción en el cliente, de modo que la interfaz no se bloquea.
- Asignación de un color a cada conexión; el nombre del usuario se muestra en ese color.
- Persistencia de mensajes (usuario, texto, fecha y color) en una base de datos SQLite.
- Envío del historial completo a cada cliente al conectarse.
- Avisos de conexión y desconexión de usuarios.

## Requisitos

- Python 3.
- Módulos de la biblioteca estándar: `socket`, `threading`, `sqlite3`, `tkinter` y `datetime`.
- Tkinter viene incluido en la mayoría de las instalaciones de Python. En algunas distribuciones de Linux debe instalarse por separado (por ejemplo, `sudo apt install python3-tk`).
- Conectividad de red entre los equipos cliente y el equipo servidor, y el puerto 5000 accesible (verificar la configuración del firewall del servidor).

## Instalación y ejecución

Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
```

### Servidor

```bash
python server.py
```

El servidor escucha en `0.0.0.0:5000` y crea el archivo `chat.db` en el directorio desde el que se ejecuta.

### Cliente

```bash
python cliente.py
```

1. Ingresar la dirección IP del equipo servidor y el puerto (`5000`). El cliente trae por defecto la IP `192.168.137.1`, que debe modificarse según la red utilizada.
2. Pulsar **Conectar**.
3. Ingresar el nombre de usuario en el cuadro de diálogo.
4. Escribir el mensaje y enviarlo con el botón **Enviar** o con la tecla Enter.

## Arquitectura

El sistema sigue un modelo cliente-servidor centralizado. Los clientes no se comunican entre sí: cada uno mantiene una conexión TCP con el servidor, que guarda los mensajes y los retransmite a todos los clientes conectados, incluido el remitente.

```
Cliente A ----\                    /---- Cliente B
 (Tkinter)     \                  /      (Tkinter)
                +-- Servidor TCP -+
                |  (hilos + Lock) |
                +--------+--------+
                         |
                  SQLite (chat.db)
```

## Protocolo de comunicación

Formato lógico: texto codificado en UTF-8, un mensaje por línea (`\n`) y campos separados por el carácter `|`.

| Dirección | Formato | Descripción |
|---|---|---|
| Cliente a servidor | `nombre` | Identificación al conectar |
| Cliente a servidor | `MENSAJE\|texto` | Publicación de un mensaje |
| Servidor a cliente | `MENSAJE\|usuario\|texto\|fecha\|color` | Mensaje en tiempo real |
| Servidor a cliente | `HISTORIAL\|usuario\|texto\|fecha\|color` | Mensaje almacenado previamente |
| Servidor a cliente | `SISTEMA\|texto` | Avisos de conexión y desconexión |
| Servidor a cliente | `ERROR\|texto` | Errores, por ejemplo, chat lleno |

La base de datos contiene la tabla `mensajes` con los campos `id`, `usuario`, `mensaje`, `fecha` y `color`. El historial se recupera en orden de inserción.

## Estructura del proyecto

```
.
|-- server.py                       Servidor TCP
|-- cliente.py                      Cliente con interfaz gráfica
|-- Documentacion_Chat_TCP.md       Documento técnico
|-- README.md
`-- chat.db                         Generado al iniciar el servidor
```

## Limitaciones conocidas

- No incluye autenticación ni cifrado, y no valida que los nombres de usuario sean únicos.
- No permite cambiar el nombre una vez establecida la conexión.
- No ofrece reconexión desde la misma ventana: si se pierde la conexión, debe reiniciarse el cliente.
- No implementa mensajes privados, salas ni lista de usuarios conectados.
- El servidor procesa los datos de cada llamada a `recv()` sin acumular hasta el salto de línea; TCP no preserva los límites entre mensajes, por lo que en casos límite pueden agruparse o fragmentarse.
- El historial completo se envía a cada cliente nuevo, sin límite de tamaño.

## Documentación adicional

La descripción funcional, los casos de uso, las historias de usuario y los requerimientos se encuentran en [Documentacion_Chat_TCP.md](Documentacion_Chat_TCP.md).
