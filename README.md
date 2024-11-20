# 🍵 Sistema de Pedidos para Cafetería FIEE-UV

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![tkinter](https://img.shields.io/badge/GUI-tkinter-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📝 Descripción

Sistema de gestión integral para cafeterías desarrollado con Python y tkinter. Permite administrar pedidos en tiempo real, gestionar tickets, controlar tiempos de preparación y mantener un registro detallado de las transacciones. Diseñado específicamente para la Cafetería de la Facultad de Ingeniería Eléctrica y Electrónica de la Universidad Veracruzana.

## 📑 Tabla de Contenidos
- [Características Principales](#-características-principales)
- [Requisitos del Sistema](#-requisitos-del-sistema)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Funcionalidades Detalladas](#-funcionalidades-detalladas)
- [Estructura del Proyecto](#-estructura-del-proyecto)
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
python main.py
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
│   └── tickets.json           # Base de datos JSON de tickets
├── README.md                  # Documentación del proyecto
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

## 👥 Contribuidores

Este proyecto fue desarrollado por estudiantes de la Universidad Veracruzana:

- 👨‍💻 Michell Alexis Policarpio Moran (zs21002379)
- 👨‍💻 Contreras Matla Luis Fernando (zs21020225)
- 👨‍💻 Bravo Ibañez Luis Fernando (zS21002428)
- 👨‍💻 García Velandia Samuel Obded (zS21002413)

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🏛️ Institución

<div align="center">
    <img src="/api/placeholder/200/200" alt="Logo UV"/>
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
