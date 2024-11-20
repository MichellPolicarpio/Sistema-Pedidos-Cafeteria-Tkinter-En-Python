# 🍵 Sistema de Pedidos para Cafetería FIEE-UV

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![tkinter](https://img.shields.io/badge/GUI-tkinter-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📝 Descripción

Sistema de gestión integral para cafeterías desarrollado con Python y tkinter. Permite administrar pedidos en tiempo real, gestionar tickets, controlar tiempos de preparación y mantener un registro detallado de las transacciones. Diseñado específicamente para la Cafetería de la Facultad de Ingeniería Eléctrica y Electrónica de la Universidad Veracruzana.

## 📑 Tabla de Contenidos
- [Características Principales](#-características-principales)
- [Detalles Técnicos](#-detalles-técnicos)
- [Requisitos del Sistema](#-requisitos-del-sistema)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Funcionalidades Detalladas](#-funcionalidades-detalladas)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Solución de Problemas](#-solución-de-problemas-comunes)
- [Contribuidores](#-contribuidores)
- [Licencia](#-licencia)

## ✨ Características Principales

- 📝 Sistema de pedidos en tiempo real
- 🎫 Generación automática de tickets
- ⏱️ Control de tiempos de preparación
- 📊 Gestión de inventario y precios
- 💾 Almacenamiento persistente de datos
- 📱 Interfaz gráfica intuitiva y moderna
- 📈 Historial completo de transacciones
- 🔍 Búsqueda y filtrado avanzado de tickets

## 🔧 Detalles Técnicos

### Arquitectura del Sistema

#### 1. Interfaz Gráfica (GUI)
- Desarrollada con `tkinter` y `ttk` para una experiencia moderna
- Sistema de pestañas para navegación intuitiva:
  - Nuevo Pedido: Interfaz para crear órdenes
  - Pedidos Activos: Monitoreo en tiempo real
  - Historial de Tickets: Gestión y búsqueda de transacciones
- Diseño responsive con grid system
- Tema personalizado con estilo profesional
- Widgets modernos como calendarios y barras de progreso

#### 2. Gestión de Estados
- Implementación orientada a objetos con clases principales:
  - `Ticket`: Manejo de información de tickets
    - Generación de IDs únicos
    - Almacenamiento de detalles de la orden
    - Cálculo de totales
  - `BebidaPersonalizada`: Gestión de bebidas y extras
    - Control de cantidades
    - Cálculo de precios
    - Gestión de modificadores
  - `SistemaPedidosCafeteria`: Controlador principal
    - Coordinación de operaciones
    - Gestión de GUI
    - Control de flujo de trabajo

#### 3. Procesamiento Asíncrono
- Uso de `threading` para operaciones no bloqueantes
  - Preparación de bebidas en segundo plano
  - Actualización de progreso en tiempo real
  - Manejo de múltiples pedidos simultáneos
- Sistema de temporizadores precisos
- Actualización dinámica de interfaces
- Prevención de bloqueos de GUI

#### 4. Persistencia de Datos
- Almacenamiento en formato JSON
  - Estructura optimizada para tickets
  - Respaldo automático
  - Recuperación de estado
- Sistema de IDs único con `uuid`
- Manejo de fechas con `datetime`
- Exportación de datos

#### 5. Características Avanzadas

##### Sistema de Notificaciones
- Alertas visuales para pedidos completados
- Indicadores de progreso en tiempo real
- Notificaciones de sistema integradas
- Alertas sonoras configurables

##### Gestión de Tiempo
- Cálculo automático de tiempos de preparación
- Temporizadores precisos para cada bebida
- Ajuste dinámico según extras seleccionados
- Sistema de prioridad de pedidos

##### Interfaz de Búsqueda
- Filtrado por múltiples criterios
  - Fecha
  - ID de ticket
  - Contenido de orden
- Búsqueda en tiempo real
- Sistema de calendario integrado
- Exportación de resultados

##### Manejo de Errores
- Sistema robusto de validación de entradas
- Recuperación automática de errores
- Mensajes de error informativos
- Logging de eventos críticos

### Diagrama de Clases Principal

```
+----------------+     +----------------------+     +------------------+
|     Ticket     |     | BebidaPersonalizada |     |  SistemaPedidos |
+----------------+     +----------------------+     +------------------+
| - ticket_id    |     | - tipo              |     | - ordenes       |
| - orden_id     |     | - cantidad          |     | - tickets       |
| - bebidas      |     | - extras            |     | - GUI elements  |
| - total        |     | + calcular_subtotal |     | + crear_orden   |
| - timestamp    |     | + calcular_tiempo   |     | + generar_ticket|
+----------------+     +----------------------+     +------------------+
```

### Flujo de Trabajo Principal

1. **Inicio del Sistema**
   - Carga de configuración
   - Inicialización de GUI
   - Restauración de estado previo
   - Verificación de directorios

2. **Proceso de Pedido**
   - Selección de productos
   - Cálculo de tiempos/precios
   - Generación de ticket
   - Inicio de preparación
   - Monitoreo de progreso

3. **Monitoreo de Pedidos**
   - Actualización en tiempo real
   - Control de estados
   - Notificaciones
   - Finalización automática
   - Gestión de completados

## 💻 Requisitos del Sistema

### Python y Sistema Operativo
- Python 3.7 o superior
- Compatible con Windows, macOS y Linux

### Librerías Requeridas

#### Librerías Incluidas en Python (no requieren instalación)
- `tkinter`: Biblioteca estándar de Python para crear interfaces gráficas
- `json`: Manejo de archivos JSON para almacenamiento de datos
- `datetime`: Manejo de fechas y tiempos
- `threading`: Soporte para multihilos
- `uuid`: Generación de identificadores únicos
- `os`: Operaciones del sistema de archivos

#### Librerías Externas (requieren instalación)
- `tkcalendar`: Widget de calendario para la interfaz gráfica
  ```bash
  pip install tkcalendar
  ```

## 🚀 Instalación

1. Asegúrese de tener Python 3.7+ instalado:
```bash
python --version
```

2. Clone el repositorio:
```bash
git clone https://github.com/MichellPolicarpio/Sistema-Pedidos-Cafeteria-Tkinter-En-Python.git
cd sistema-pedidos-cafeteria
```

3. Cree y active un entorno virtual (opcional pero recomendado):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

4. Instale las dependencias:
```bash
pip install tkcalendar
```

5. Verifique la instalación:
```bash
python -c "import tkinter, tkcalendar"
```

6. Ejecute el programa:
```bash
python Equipo_3_Actividad_15.py
```

## 🎯 Uso

### Realizar un Nuevo Pedido
1. Seleccione la pestaña "Nuevo Pedido"
2. Elija la bebida del menú desplegable
3. Ajuste la cantidad y seleccione extras
4. Presione "Agregar al Carrito"
5. Confirme el pedido

### Seguimiento de Pedidos
- Monitoree los pedidos en preparación en tiempo real
- Visualice el progreso mediante barras de estado
- Reciba notificaciones cuando los pedidos estén listos

### Gestión de Tickets
- Acceda al historial completo de tickets
- Filtre por fecha y contenido
- Exporte datos en formato JSON
- Visualice detalles completos de cada transacción

## 🛠️ Funcionalidades Detalladas

### Menú de Bebidas
| Bebida | Tiempo de Preparación | Precio |
|--------|----------------------|---------|
| Café Americano | 3 min | $25.00 |
| Cappuccino | 5 min | $35.00 |
| Latte | 4 min | $30.00 |
| Té | 2 min | $20.00 |

### Extras Disponibles
| Extra | Tiempo Adicional | Precio |
|-------|-----------------|---------|
| Leche extra | 1 min | $10.00 |
| Shot extra de café | 2 min | $15.00 |
| Sirope de sabor | 30 seg | $8.00 |

## 📁 Estructura del Proyecto

```
sistema-pedidos-cafeteria/
│
├── Equipo_3_Actividad_15.py   # Archivo principal del sistema
├── tickets/                   # Directorio para almacenamiento de tickets
│   └── tickets.json          # Base de datos JSON de tickets
├── README.md                 # Documentación del proyecto
```

## 🔧 Solución de Problemas Comunes

### Error: No module named 'tkcalendar'
```bash
pip install tkcalendar --upgrade
```

### Error: No module named 'tkinter'
- Windows:
```bash
pip install tk
```
- Linux:
```bash
sudo apt-get install python3-tk
```
- macOS:
```bash
brew install python-tk
```

### Error: JSON file not found
Crear el directorio 'tickets' manualmente:
```bash
mkdir tickets
```

## 👥 Creditos de los creadores:

Este proyecto fue desarrollado por estudiantes de la Universidad Veracruzana:

- 👨‍💻 Michell Alexis Policarpio Moran
- 👨‍💻 Contreras Matla Luis Fernando
- 👨‍💻 Bravo Ibañez Luis Fernando 
- 👨‍💻 García Velandia Samuel Obded

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🏛️ Institución

<div align="center">
    <p><b>Universidad Veracruzana</b></p>
    <p>Facultad de Ingeniería Eléctrica y Electrónica</p>
</div>

---

<div align="center">
    <p>© 2024 - Todos los derechos reservados</p>
    <p>
        <a href="https://www.uv.mx/">Universidad Veracruzana</a> |
        <a href="https://www.uv.mx/fiee/">FIEE</a>
    </p>
</div>
