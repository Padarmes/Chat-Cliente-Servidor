```
# ChatLocal — Sistema de chat TCP para red local
```

```
Sistema de mensajería en tiempo real desarrollado en Python mediante una
arquitectura cliente-servidor y el protocolo TCP. Permite que varios usuarios
conectados a una misma red local intercambien mensajes a través de una interfaz
gráfica de escritorio.
```

```
El proyecto utiliza sockets para la comunicación entre equipos, hilos para
atender múltiples conexiones y SQLite para almacenar el historial de mensajes de
forma persistente.
```

# `## Tabla de contenido` 

- `[1. Descripción del proyecto](#1-descripción-del-proyecto)` 

- `[2. Objetivos](#2-objetivos)` 

- `[3. Características principales](#3-características-principales)` 

- `[4. Tecnologías utilizadas](#4-tecnologías-utilizadas)` 

- `[5. Arquitectura del sistema](#5-arquitectura-del-sistema)` 

- `[6. Estructura del proyecto](#6-estructura-del-proyecto)` 

- `[7. Requisitos](#7-requisitos) - [8. Instalación](#8-instalación) - [9. Ejecución](#9-ejecución)` 

- `[10. Conexión entre equipos de una red local](#10-conexión-entre-equipos-deuna-red-local)` 

- `[11. Funcionamiento del sistema](#11-funcionamiento-del-sistema)` 

- `[12. Almacenamiento de mensajes](#12-almacenamiento-de-mensajes)` 

- `[13. Protocolo de comunicación](#13-protocolo-de-comunicación)` 

- `[14. Limitaciones conocidas](#14-limitaciones-conocidas)` 

- `[15. Pruebas recomendadas](#15-pruebas-recomendadas)` 

- `[16. Posibles mejoras](#16-posibles-mejoras)` 

- `[17. Documentación técnica](#17-documentación-técnica)` 

- `[18. Autoría y propósito académico](#18-autoría-y-propósito-académico)` 

# `## 1. Descripción del proyecto` 

```
ChatLocal es una aplicación de mensajería diseñada para funcionar dentro de una
red local, sin depender de servicios externos de mensajería ni de una conexión a
Internet.
```

```
El sistema sigue el modelo cliente-servidor. Un equipo ejecuta el servidor, que
permanece a la espera de conexiones entrantes, mientras que los demás equipos
ejecutan el cliente y se conectan a la dirección IP y al puerto del servidor.
```

```
Una vez establecida la conexión, los usuarios pueden enviar mensajes que se
distribuyen a los demás participantes conectados. El servidor también
proporciona el historial almacenado en la base de datos para que los usuarios
puedan consultar mensajes anteriores al conectarse.
```

```
La aplicación cuenta con una interfaz gráfica desarrollada con Tkinter y utiliza
SQLite para conservar los mensajes entre ejecuciones del servidor.
```

# `## 2. Objetivos` 

# `### Objetivo general` 

```
Desarrollar un sistema de chat para una red local mediante una arquitectura
cliente-servidor que permita la comunicación entre múltiples usuarios, la
distribución de mensajes en tiempo real y el almacenamiento persistente del
historial.
```

# `### Objetivos específicos` 

- `Implementar la comunicación entre equipos mediante sockets TCP.` 

- `Permitir la conexión simultánea de múltiples clientes.` 

- `Desarrollar una interfaz gráfica para enviar y recibir mensajes.` 

- `Distribuir los mensajes enviados a los usuarios conectados.` 

- `Registrar los mensajes en una base de datos SQLite.` 

- `Recuperar el historial de mensajes almacenados.` 

- `Mostrar información temporal y visual de los mensajes.` 

- `Facilitar la comunicación entre equipos conectados a una misma red local.` 

# `## 3. Características principales` 

# `### Comunicación en tiempo real` 

```
Los clientes envían sus mensajes al servidor mediante conexiones TCP. El
servidor procesa los mensajes recibidos y los distribuye a los demás clientes
conectados.
```

# `### Arquitectura cliente-servidor` 

```
La aplicación separa las responsabilidades de comunicación:
```

- `**Servidor:** administra las conexiones, procesa los mensajes y coordina su distribución.` 

```
- **Cliente:** proporciona la interfaz gráfica y permite al usuario participar
en la conversación.
```

# `### Interfaz gráfica` 

```
El cliente utiliza Tkinter para proporcionar una ventana de conversación con los
siguientes elementos:
```

- `Campo para introducir la dirección IP del servidor.` 

- `Campo para introducir el puerto.` 

- `Botón para establecer la conexión.` 

- `Área de visualización de mensajes.` 

- `Campo de entrada de texto.` 

- `Botón para enviar mensajes.` 

# `### Identificación de usuarios` 

```
El cliente solicita un nombre al usuario durante el proceso de conexión. Este
nombre se utiliza para identificar los mensajes enviados durante la sesión.
```

# `### Distribución de mensajes` 

```
Los mensajes recibidos por el servidor se retransmiten a los clientes
conectados, con excepción del cliente que originó el mensaje.
```

# `### Historial de conversación` 

```
El servidor consulta la base de datos y envía el historial almacenado cuando un
cliente se conecta.
```

# `### Persistencia de datos` 

```
Los mensajes se almacenan en una base de datos SQLite denominada `chat.db`. Al
estar guardados en un archivo, pueden conservarse después de cerrar el servidor
o reiniciar el equipo, siempre que el archivo permanezca disponible y no se
elimine.
```

# `### Identificación visual` 

```
El servidor asigna colores a los usuarios para facilitar la identificación
visual de los mensajes.
```

# `### Capacidad de conexión` 

```
El código establece un límite de diez clientes activos mediante una comprobación
del número de clientes registrados en el servidor.
```

```
> **Nota:** el comportamiento real de la conexión depende de la disponibilidad
de la red, la configuración del equipo servidor y las restricciones del sistema
operativo.
```

```
## 4. Tecnologías utilizadas
```

```
| Tecnología | Función |
```

- `|---|---|` 

- `| Python | Lenguaje de programación principal. |` 

- `| `socket` | Comunicación entre equipos mediante TCP. |` 

- `| `threading` | Atención concurrente de clientes y recepción de mensajes. |` 

- `| `tkinter` | Desarrollo de la interfaz gráfica del cliente. |` 

- `| `sqlite3` | Almacenamiento persistente de mensajes. |` 

- `| `datetime` | Generación de marcas temporales. |` 

- `| TCP/IP | Transporte de datos entre clientes y servidor. |` 

- `| SQLite | Sistema de base de datos embebido. |` 

```
Las bibliotecas indicadas pertenecen a la biblioteca estándar de Python. No se
requiere instalar un servidor de base de datos independiente.
```

- `## 5. Arquitectura del sistema` 

```
El proyecto utiliza una arquitectura cliente-servidor centralizada.
```

```
Todos los clientes se comunican con un único servidor, que recibe los mensajes y
se encarga de distribuirlos.
```

```
```text
```

# `RED LOCAL` 

```
     ┌─────────────────────────┐
     │                         │
     │     Cliente 1           │
     │     Python + Tkinter    │
     │          │              │
     │          │ TCP          │
     │          ▼              │
     │   ┌─────────────────┐   │
     │   │                 │   │
     │   │     SERVIDOR    │   │
     │   │                 │   │
     │   │ Gestión de      │   │
     │   │ conexiones      │   │
     │   │                 │   │
     │   │ Distribución    │   │
     │   │ de mensajes     │   │
     │   └────────┬────────┘   │
     │            │            │
     │            ▼            │
     │      ┌──────────┐       │
     │      │ SQLite   │       │
     │      │ chat.db  │       │
     │      └──────────┘       │
     │                         │
     │     Cliente 2           │
     │     Python + Tkinter    │
     │                         │
     └─────────────────────────┘
```

```
*El diagrama representa la arquitectura lógica del sistema. Las conexiones TCP
deben configurarse para que los clientes puedan alcanzar la dirección IP del
equipo que ejecuta el servidor.*
```

# `### 5.1. Servidor` 

```
El servidor es el componente central de la aplicación.
```

```
Sus responsabilidades son:
```

`1. Inicializar la base de datos.` 

`2. Crear el socket TCP.` 

`3. Escuchar conexiones entrantes.` 

`4. Aceptar clientes y administrar sus conexiones.` 

`5. Asignar identificadores visuales mediante colores.` 

`6. Consultar y enviar el historial almacenado.` 

`7. Recibir los mensajes de los clientes.` 

`8. Guardar los mensajes en SQLite.` 

`9. Distribuir los mensajes a los clientes conectados.` 

`10. Gestionar las desconexiones.` 

# `### 5.2. Cliente` 

```
El cliente es la aplicación que utiliza cada participante.
```

```
Sus responsabilidades son:
```

`1. Solicitar los datos necesarios para conectarse.` 

`2. Establecer una conexión TCP con el servidor.` 

`3. Enviar el nombre del usuario.` 

`4. Recibir mensajes y el historial de conversación.` 

`5. Interpretar los mensajes recibidos.` 

`6. Mostrar la conversación en la interfaz gráfica.` 

`7. Enviar los mensajes escritos por el usuario.` 

`8. Cerrar la conexión cuando el usuario sale.` 

```
### 5.3. Concurrencia
```

```
El servidor utiliza hilos para atender a los clientes de manera concurrente.
Esto permite que la recepción de mensajes de un cliente no dependa
exclusivamente de que otro termine su interacción.
```

```
El cliente también utiliza un hilo de recepción para mantener la comunicación
con el servidor sin bloquear directamente el flujo principal de la aplicación
gráfica.
```

```
## 6. Estructura del proyecto
```

```
La siguiente es una estructura recomendada para organizar los archivos del
repositorio:
```

```
```text
ChatLocal/
│
├── README.md
├── cliente.py
├── servidor.py
├── .gitignore
│
└── docs/
    └── documentacion_tecnica.md
```
```

```
Descripción de los archivos:
```

```
| Archivo | Descripción |
```

- `|---|---|` 

- `| `README.md` | Presentación general, instalación y ejecución del proyecto. |` 

- `| `cliente.py` | Implementación del cliente con interfaz gráfica. |` 

- `| `servidor.py` | Implementación del servidor y gestión de las conexiones. |` 

- `| `.gitignore` | Exclusión de archivos que no deben versionarse. |` 

- `| `docs/documentacion_tecnica.md` | Documentación técnica detallada. |` 

- `| `chat.db` | Base de datos generada por el servidor durante la ejecución. |` 

```
El archivo `chat.db` se genera automáticamente cuando el servidor inicializa la
base de datos. No es necesario crearlo manualmente.
```

```
La ubicación de la base de datos depende del directorio de trabajo desde el cual
se ejecute el servidor.
```

```
## 7. Requisitos
```

```
Para ejecutar el proyecto se requiere:
```

- `Un equipo con Windows, Linux o un sistema compatible con Python y Tkinter.` 

- `Python 3 instalado.` 

- `El módulo Tkinter disponible en la instalación de Python.` 

- `Los archivos `cliente.py` y `servidor.py`.` 

- `Una conexión de red local entre los equipos que participarán en el chat.` 

- `Permisos de red para permitir las conexiones entrantes al servidor.` 

```
No es necesario disponer de conexión a Internet para intercambiar mensajes una
vez que todos los equipos pueden comunicarse a través de la red local.
```

```
### Verificar la instalación de Python
```

```
En Windows, abre PowerShell o CMD y ejecuta:
```

```
```powershell
python --version
```
```

```
Si el comando anterior no funciona, prueba:
```

```
```powershell
py --version
```
```

```
En Linux puedes ejecutar:
```

```
```bash
python3 --version
```
```

```
La versión instalada debe ser compatible con el código utilizado en el proyecto.
## 8. Instalación
```

```
### 8.1. Descargar el proyecto
```

```
Clona el repositorio utilizando Git:
```

```
```bash
git clone URL_DEL_REPOSITORIO
```
```

```
Reemplaza `URL_DEL_REPOSITORIO` por la dirección real del repositorio de GitHub.
```

```
También puedes descargar el proyecto desde GitHub como un archivo ZIP y extraer
su contenido.
```

```
### 8.2. Abrir la carpeta del proyecto
```

```
Entra en la carpeta donde se encuentran los archivos:
```

```
```bash
cd ChatLocal
```
```

```
Si descargaste el proyecto en otra ubicación, utiliza la ruta correspondiente.
```

```
### 8.3. Verificar Tkinter
```

```
En Windows puedes comprobar que Tkinter está disponible con:
```

```
```powershell
python -m tkinter
```
```

```
Si la instalación es correcta, normalmente aparecerá una ventana de prueba.
```

```
En Linux, algunas distribuciones requieren instalar el paquete de Tkinter
mediante el administrador de paquetes del sistema.
```

```
No es necesario instalar Flask, Django ni un servidor web para ejecutar esta
aplicación.
```

```
## 9. Ejecución
```

```
El proyecto requiere ejecutar el servidor antes de conectar los clientes.
```

```
### 9.1. Iniciar el servidor
```

```
En el equipo que actuará como servidor, abre una terminal dentro de la carpeta
del proyecto y ejecuta:
```

```
```bash
python servidor.py
```
```

```
En Windows también puedes utilizar:
```

```
```powershell
py servidor.py
```
```

```
El servidor debe permanecer en ejecución mientras los clientes utilicen el chat.
```

```
### 9.2. Iniciar un cliente
```

```
En el mismo equipo o en otro equipo compatible, abre una terminal dentro de la
carpeta del proyecto y ejecuta:
```

```
```bash
python cliente.py
```
```

```
En Windows también puedes utilizar:
```

```
```powershell
py cliente.py
```

```
### 9.3. Conectarse
```

```
En la ventana del cliente:
```

`1. Introduce la dirección IP del equipo servidor.` 

`2. Introduce el puerto configurado en el servidor.` 

`3. Pulsa el botón para conectarse.` 

`4. Introduce el nombre con el que deseas participar.` 

`5. Espera a que se establezca la conexión.` 

`6. Escribe un mensaje y utiliza el botón de envío.` 

```
Si la conexión se establece correctamente, el cliente podrá recibir el historial
disponible y participar en la conversación.
> **Importante:** el código utiliza el puerto TCP `5000` de forma
predeterminada. Si se modifica en el servidor, debe actualizarse también la
configuración del cliente.
```

```
## 10. Conexión entre equipos de una red local
```

```
Para que otros computadores puedan participar, no basta con ejecutar el cliente
en cada equipo. También es necesario que exista conectividad entre ellos.
```

```
### 10.1. Configuración del servidor
```

```
El servidor utiliza la siguiente configuración:
```

```
```python
HOST = "0.0.0.0"
PORT = 5000
```
```

```
La dirección `0.0.0.0` permite que el socket escuche en las interfaces de red
disponibles, sujeto a las restricciones del sistema operativo.
```

```
**Esta dirección no debe introducirse como IP de destino en los clientes.** Los
clientes deben utilizar la dirección IP local real del equipo servidor.
```

```
### 10.2. Consultar la dirección IP del servidor
```

```
En Windows, ejecuta:
```

```
```powershell
ipconfig
```
```

```
Busca la dirección IPv4 correspondiente a la interfaz que se utilizará para la
comunicación entre los equipos.
```

```
Por ejemplo, si el equipo servidor tiene la dirección:
```

```
```text
192.168.137.1
```
```

```
esa sería la dirección que se introduciría en el cliente, siempre que
corresponda realmente a la red compartida por los equipos.
```

```
La dirección de ejemplo no es universal: cada red puede utilizar un rango
diferente.
```

```
### 10.3. Utilizar un punto de acceso o una red Wi-Fi local
```

```
Los equipos pueden conectarse mediante una misma red Wi-Fi o un punto de acceso
móvil que permita la comunicación entre dispositivos.
```

```
Una vez conectados:
```

`1. Inicia el servidor en el equipo principal.` 

`2. Consulta su dirección IPv4 correspondiente a esa red.` 

`3. Abre el cliente en los demás equipos.` 

`4. Introduce la dirección IP del servidor y el puerto `5000`.` 

`5. Intenta establecer la conexión.` 

```
Una red local no necesita acceso a Internet para transportar los mensajes entre
dispositivos. Sin embargo, algunos puntos de acceso pueden bloquear la
comunicación entre clientes.
```

```
### 10.4. Configurar el firewall
```

```
El firewall del sistema operativo puede bloquear las conexiones entrantes.
```

```
Si los clientes no pueden conectarse:
```

- `Comprueba que el servidor está en ejecución.` 

- `Verifica la dirección IP del equipo servidor.` 

- `Comprueba que todos los equipos están conectados a una red compatible.` 

- `Verifica que el puerto TCP `5000` está permitido para las conexiones necesarias.` 

- `Comprueba si el punto de acceso permite la comunicación entre dispositivos.` 

```
Cualquier regla de firewall debe limitarse al perfil y a las conexiones
necesarios para la práctica. No es recomendable desactivar permanentemente el
firewall.
```

```
### 10.5. Comprobar el puerto
```

```
Desde otro equipo Windows, puedes comprobar la conectividad con:
```

```
```powershell
```

```
Test-NetConnection DIRECCION_IP_DEL_SERVIDOR -Port 5000
```
```

```
Por ejemplo:
```

```
```powershell
Test-NetConnection 192.168.137.1 -Port 5000
```
```

```
Sustituye la dirección de ejemplo por la dirección real del servidor.
```

```
El resultado `TcpTestSucceeded : True` indica que se pudo establecer una
conexión TCP con ese destino y puerto. No demuestra por sí solo que todas las
funcionalidades del chat operen correctamente.
```

```
## 11. Funcionamiento del sistema
```

```
El flujo general de comunicación es el siguiente:
```

```
### Fase 1. Inicialización
```

```
El servidor inicializa la base de datos SQLite, crea el socket TCP y comienza a
escuchar conexiones entrantes.
```

```
### Fase 2. Conexión del cliente
```

```
El cliente crea su interfaz gráfica y establece una conexión con la dirección IP
y el puerto del servidor.
```

```
### Fase 3. Identificación
```

```
El cliente envía el nombre introducido por el usuario. El servidor registra la
conexión y asigna un color para la identificación visual.
```

```
### Fase 4. Recuperación del historial
```

```
El servidor consulta los mensajes almacenados y envía el historial disponible al
cliente que acaba de conectarse.
```

```
### Fase 5. Envío del mensaje
```

```
El usuario escribe un mensaje en la interfaz gráfica. El cliente lo transmite al
servidor mediante TCP.
```

```
### Fase 6. Procesamiento y almacenamiento
```

```
El servidor recibe el mensaje, lo procesa y lo almacena en SQLite.
```

```
### Fase 7. Distribución
```

```
El servidor transmite el mensaje a los demás clientes conectados.
```

```
### Fase 8. Desconexión
```

```
Cuando un cliente se desconecta, el servidor realiza las operaciones de limpieza
correspondientes a la conexión.
```

```
## 12. Almacenamiento de mensajes
```

```
El proyecto utiliza SQLite, una base de datos que almacena la información en un
archivo local.
```

```
El archivo utilizado es:
```

```
```text
chat.db
```

```
El servidor crea una tabla denominada `mensajes` con los siguientes campos:
```

```
| Campo | Función |
|---|---|
```

```
| `id` | Identificador del registro. |
```

```
| `usuario` | Nombre asociado al mensaje. |
```

```
| `mensaje` | Contenido del mensaje. |
```

```
| `fecha` | Fecha y hora registradas para el mensaje. |
```

```
| `color` | Color asociado al usuario al almacenar el mensaje. |
```

```
El servidor utiliza esta tabla para guardar los mensajes y recuperar el
historial.
```

# `### Persistencia` 

```
Los mensajes pueden permanecer disponibles después de reiniciar el programa
porque se guardan en un archivo de base de datos.
```

```
Para conservar el historial se deben cumplir estas condiciones:
```

- `El archivo `chat.db` no debe eliminarse.` 

- `El servidor debe ejecutarse con acceso de lectura y escritura al directorio` 

```
correspondiente.
```

```
- Las copias de seguridad deben incluir el archivo de base de datos si se desea
conservar el historial.
```

```
Si el archivo se elimina o se crea una nueva base de datos en otra ubicación, el
historial anterior podría no estar disponible.
```

```
## 13. Protocolo de comunicación
```

```
El cliente y el servidor intercambian mensajes de texto mediante TCP.
```

```
El protocolo de aplicación utiliza el carácter `|` para separar campos y el
carácter de nueva línea (`\n`) como terminador de los mensajes en los formatos
previstos por el programa.
```

```
### 13.1. Identificación del usuario
```

```
Al conectarse, el cliente envía su nombre seguido de un salto de línea:
```

```
```text
Nombre Apellido
```
```

```
### 13.2. Mensaje enviado por el cliente
```

```
El cliente utiliza el siguiente formato:
```

```
```text
MENSAJE|Contenido del mensaje
```
```

```
El mensaje se transmite terminado en `\n`.
```

```
### 13.3. Mensaje distribuido por el servidor
```

```
El servidor utiliza un formato que incluye el usuario, el contenido, la fecha y
el color:
```

```
```text
MENSAJE|Usuario|Contenido del mensaje|Fecha|Color
```
```

```
### 13.4. Historial
```

```
El servidor utiliza el tipo de mensaje `HISTORIAL` para comunicar el historial
almacenado al cliente que se conecta.
```

```
```text
HISTORIAL|...
```
```

```
El contenido completo del historial depende del formato implementado en el
código.
```

```
### 13.5. Mensajes del sistema
```

```
El cliente reconoce mensajes identificados con el tipo `SISTEMA`:
```

```
```text
SISTEMA|Contenido del mensaje
```
```

```
### 13.6. Errores
```

```
Los errores comunicados por el servidor utilizan el tipo `ERROR`:
```

```
```text
```

```
ERROR|Descripción del error
```

# `### Consideraciones sobre TCP` 

```
TCP proporciona un flujo de bytes fiable y ordenado, pero no conserva
automáticamente los límites de cada mensaje de la aplicación.
```

```
Por ello, un protocolo basado en saltos de línea debe implementar correctamente
el almacenamiento temporal y la separación de mensajes recibidos.
```

```
En la versión actual, el cliente mantiene un búfer para procesar líneas
completas. Sin embargo, la recepción del servidor y el tratamiento de las
primeras líneas de identificación presentan limitaciones que conviene revisar
antes de utilizar el sistema en condiciones exigentes.
```

```
Además, el uso de `|` como separador requiere cuidado si un nombre o mensaje
contiene ese carácter.
```

# `## 14. Limitaciones conocidas` 

```
El proyecto es una implementación académica orientada al aprendizaje de redes y
programación concurrente. Antes de utilizarlo en un entorno real, deben
considerarse las siguientes limitaciones.
```

# `### Seguridad` 

- `No implementa autenticación mediante contraseña.` 

- `No cifra las comunicaciones mediante TLS.` 

- `No incluye un sistema de permisos por usuario.` 

- `El nombre enviado por el cliente no constituye una identidad verificada.` 

# `### Identificación` 

- `No se garantiza que los nombres de usuario sean únicos.` 

- `No existe un sistema completo de gestión de cuentas.` 

- `La asignación de colores no garantiza una identificación visual única en todos los escenarios posibles.` 

# `### Mensajería` 

- `No se implementa edición o eliminación de mensajes.` 

- `No se implementa mensajería privada.` 

- `No existe un mecanismo completo de confirmación de entrega.` 

- `El protocolo requiere mejoras para gestionar de forma robusta mensajes que contienen separadores o que llegan fragmentados por TCP.` 

# `### Conexiones` 

- `El servidor utiliza un límite de diez clientes registrados.` 

- `No dispone de mecanismos avanzados de recuperación de errores de red.` 

- `La conectividad depende de la configuración de la red local y del firewall.` 

# `### Persistencia` 

- `El historial depende del archivo SQLite local.` 

- `No existe replicación de la base de datos.` 

- `No se implementa un sistema automático de copias de seguridad.` 

- `La base de datos debe protegerse frente a modificaciones o eliminaciones accidentales.` 

# `### Distribución` 

```
La versión actual se ejecuta mediante Python. Por tanto, los equipos cliente
necesitan disponer de un entorno compatible para ejecutar el programa.
```

```
La creación de instaladores o ejecutables independientes puede incorporarse como
una mejora futura.
```

# `## 15. Pruebas recomendadas` 

```
Antes de presentar el proyecto, se recomienda ejecutar y registrar las
siguientes pruebas.
```

```
| ID | Prueba | Resultado esperado | Estado |
|---|---|---|---|
```

```
| P01 | Iniciar el servidor. | El servidor comienza a escuchar conexiones. |
Pendiente |
| P02 | Conectar un cliente. | Se establece la conexión con el servidor. |
Pendiente |
| P03 | Enviar un mensaje. | El mensaje se procesa y se distribuye. | Pendiente
|
| P04 | Conectar dos clientes. | Ambos pueden participar en la conversación. |
Pendiente |
| P05 | Enviar mensajes desde ambos clientes. | Los clientes reciben los
mensajes distribuidos. | Pendiente |
```

```
| P06 | Reiniciar el servidor. | Los mensajes almacenados continúan disponibles
si se conserva la base de datos. | Pendiente |
```

```
| P07 | Conectar un cliente nuevo. | El servidor le proporciona el historial
disponible. | Pendiente |
```

```
| P08 | Intentar conectar más de diez clientes. | El servidor rechaza las
conexiones que excedan el límite implementado. | Pendiente |
```

```
| P09 | Desconectar un cliente. | El servidor gestiona la desconexión sin
detenerse. | Pendiente |
| P10 | Conectar desde otro computador. | El cliente puede conectarse mediante
la red local. | Pendiente |
```

```
**Nota:** los estados se dejan como pendientes para registrar los resultados
reales después de ejecutar las pruebas. No deben marcarse como satisfactorios
sin haberlas realizado.
```

```
## 16. Posibles mejoras
```

```
Las siguientes mejoras pueden incorporarse en versiones posteriores:
```

```
1. **Validación de nombres:** impedir nombres vacíos o duplicados.
```

```
2. **Protocolo robusto:** implementar un mecanismo de encuadre de mensajes que
gestione correctamente fragmentación, concatenación y caracteres separadores.
3. **Gestión de errores:** mejorar el tratamiento de desconexiones inesperadas y
fallos de transmisión.
4. **Seguridad:** incorporar autenticación, validación de entradas y cifrado
cuando corresponda.
```

```
5. **Persistencia mejorada:** añadir copias de seguridad y controles de
integridad.
```

```
6. **Registro de eventos:** almacenar información técnica sobre conexiones,
errores y desconexiones.
```

```
7. **Distribución:** generar ejecutables para facilitar la instalación en
equipos sin Python instalado.
```

`8. **Interfaz gráfica:** mejorar la presentación de usuarios conectados, estados de conexión y mensajes del sistema.` 

```
9. **Pruebas automatizadas:** implementar pruebas unitarias y de integración.
10. **Configuración externa:** permitir modificar la dirección IP, el puerto y
otros parámetros sin editar directamente el código.
```

```
11. **Control de concurrencia:** revisar la sincronización del acceso a las
estructuras compartidas.
```

```
12. **Despliegue:** preparar instrucciones específicas para Windows y Linux.
```

```
Estas mejoras no forman parte necesariamente de la implementación actual; se
presentan como propuestas para la evolución del proyecto.
```

```
## 17. Documentación técnica
```

```
La documentación técnica ampliada se encuentra en:
```

```
[`docs/documentacion_tecnica.md`](docs/documentacion_tecnica.md)
```

```
Este documento puede incluir:
```

- `Descripción detallada de la arquitectura.` 

- `Explicación de los componentes.` 

- `Flujo de comunicación entre clientes y servidor.` 

- `Estructura de la base de datos.` 

- `Descripción de las funciones principales.` 

- `Decisiones de diseño.` 

- `Riesgos técnicos y recomendaciones.` 

```
## 18. Autoría y propósito académico
```

```
ChatLocal es un proyecto de desarrollo de software orientado al aprendizaje de
conceptos de redes de computadores y programación concurrente.
```

```
El proyecto permite estudiar de forma práctica:
```

- `La arquitectura cliente-servidor.` 

- `La comunicación mediante sockets TCP.` 

- `La concurrencia mediante hilos.` 

- `El desarrollo de interfaces gráficas.` 

- `La persistencia de datos con SQLite.` 

- `La configuración de servicios en redes locales.` 

- `La documentación y organización de proyectos de software.` 

```
**Estado del proyecto:** versión inicial en desarrollo.
```

```
**Licencia:** no especificada.
```

