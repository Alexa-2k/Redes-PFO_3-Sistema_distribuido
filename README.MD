# PFO 3: Rediseño como Sistema Distribuido (Cliente-Servidor)
## Alejandra Lorena Rachich - Programación sobre redes - Com. 3E

Este proyecto corresponde a la Práctica Formativa Obligatoria 3, donde el objetivo es transformar un sistema monolítico en una arquitectura distribuida básica, implementando el modelo cliente-servidor mediante sockets y concurrencia.

---

<details>
<summary><strong>Ver Consigna del Trabajo Práctico</strong> (click para expandir)</summary>

> ### PFO 3: Rediseño como Sistema Distribuido (Cliente-Servidor)
> 
> **Objetivo:** Transformar el sistema en una arquitectura distribuida usando sockets.
> 
> **Consignas:**
> 1. Diseñar un diagrama que incluya:
>    * Clientes (móviles, web).
>    * Balanceador de carga (Nginx/HAProxy).
>    * Servidores workers (cada uno con su pool de hilos).
>    * Cola de mensajes (RabbitMQ) para comunicación entre servidores.
>    * Almacenamiento distribuido (PostgreSQL, S3).
> 2. Implementar en Python:
>    * Un servidor que reciba tareas por socket y las distribuya a workers.
>    * Un cliente que envíe tareas y reciba resultados.
> 
> **Entregables:**
> * Diagrama del sistema.
> * Código del servidor y cliente en repositorio de Github

</details>

---


## Arquitectura distribuida Cliente–Servidor con balanceo de carga y procesamiento asíncrono
## 1. Diagrama de la Arquitectura

Se diseñó un diagrama de arquitectura distribuida que incluye los siguientes componentes, según lo solicitado en la consigna:

* **Clientes:** (Móvil, Web)
* **Balanceador de Carga:** (Nginx)
* **Servidores de Aplicación/API:** (Workers con pool de hilos)
* **Sistema de Colas:** (RabbitMQ)
* **Almacenamiento Distribuido:** (PostgreSQL y S3)

![Diagrama de Arquitectura Distribuida](./capturas/01-esquema.png)


### Descripción general
El sistema se diseñó bajo una **arquitectura distribuida orientada a tareas**, donde múltiples clientes (web y móvil) envían solicitudes mediante **sockets**.  
Un **balanceador de carga** (Nginx o HAProxy) distribuye las conexiones entre varios **servidores de aplicación (API Gateway)**, que a su vez colocan las tareas en una **cola de mensajes (RabbitMQ)** para su procesamiento asíncrono.

Las tareas en cola son consumidas por un conjunto de **servidores de procesamiento (workers)**, cada uno con su propio **pool de hilos** para ejecutar múltiples trabajos en paralelo.  
Los resultados se almacenan en un **sistema de almacenamiento distribuido**, compuesto por una base de datos relacional (**PostgreSQL**) y un sistema de archivos en la nube (**S3 / MinIO**).

---

### Flujo de ejecución
1. El cliente envía una tarea mediante un socket.  
2. El balanceador distribuye la solicitud entre los servidores API.  
3. El servidor coloca la tarea en la cola de RabbitMQ.  
4. Los workers consumen las tareas y las procesan.  
5. Los resultados se guardan en PostgreSQL o en S3/MinIO.

---


## 2. Implementación en Python (Sockets)

La implementación se centra en la comunicación directa entre clientes y un servidor concurrente usando sockets TCP.

### Archivos

* `servidor.py`: Un servidor TCP concurrente. Utiliza el módulo `threading` para crear un "pool de hilos", asignando un hilo "worker" a cada cliente que se conecta. Esto permite al servidor manejar múltiples clientes de forma simultánea sin bloquearse.

* `cliente.py`: Un cliente TCP que se conecta al servidor. Permite al usuario introducir una "tarea" (un string) que se envía al servidor. Luego, el cliente espera la respuesta de confirmación del servidor.

### Cómo ejecutar el proyecto

Se necesitan al menos dos terminales (idealmente tres para probar la concurrencia).

**1. Iniciar el Servidor**

En una terminal se ejecuta el servidor, que quedará escuchando conexiones en `127.0.0.1:65432`.

```bash
python servidor.py
```


**2. Iniciar Clientes**

En una o más terminales nuevas, se ejecuta el script del cliente.

```bash
python cliente.py

```

![Iniciar servidor y cliente](./capturas/02-servidor_y_cliente_1.png)

**3. Ejecutar tareas**

El script pedirá que se introduzca una tarea.

Escribir la tarea y presionar Enter.
![Primera tarea](./capturas/03a-primera_tarea.png)

El cliente enviará la tarea al servidor y esperará la respuesta.

Se pueden ejecutar múltiples instancias del cliente al mismo tiempo para demostrar cómo el servidor las maneja en hilos separados.
![Dos tareas](./capturas/03b-dos_tareas.png)

### Vistas del servidor y clientes

![Vista servidor](./capturas/05-ma_tareas-vista_servidor.png)

![vista clientes](./capturas/04-más_%20tareas-Vista_clientes.png)




