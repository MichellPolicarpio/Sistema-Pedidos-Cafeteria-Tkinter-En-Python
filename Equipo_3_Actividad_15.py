import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import time
from datetime import datetime
import threading
import tkcalendar
import json
import os
import uuid

class Ticket:
    def __init__(self, orden_id, bebidas, total, timestamp=None):
        self.ticket_id = str(uuid.uuid4())[:8].upper()
        self.orden_id = orden_id
        self.bebidas = bebidas
        self.total = total
        self.timestamp = timestamp or datetime.now()
        self.establecimiento = "Cafetería FIEE - UV"
        self.direccion = "Bv. Adolfo Ruiz Cortines,\nMar de Cortes y Costa Dorada"
        self.ciudad = "Boca del Río, Veracruz, México"
        self.telefono = "229 136 0054"
        self.redes_sociales = {
            "Facebook": "CafeteriaFIEE.UV",
            "Instagram": "@cafeteria_fiee",
            "Twitter": "@cafeteria_fiee"
        }

    def to_dict(self):
        return {
            'ticket_id': self.ticket_id,
            'orden_id': self.orden_id,
            'bebidas': [(b.tipo, b.cantidad, b.extras) for b in self.bebidas],
            'total': self.total,
            'timestamp': self.timestamp.isoformat(),
            'establecimiento': self.establecimiento,
            'direccion': self.direccion,
            'ciudad': self.ciudad,
            'telefono': self.telefono,
            'redes_sociales': self.redes_sociales
        }

    @classmethod
    def from_dict(cls, data):
        ticket = cls(
            data['orden_id'],
            [BebidaPersonalizada(tipo, cantidad, extras) 
             for tipo, cantidad, extras in data['bebidas']],
            data['total'],
            datetime.fromisoformat(data['timestamp'])
        )
        ticket.ticket_id = data['ticket_id']
        ticket.establecimiento = data['establecimiento']
        ticket.direccion = data.get('direccion', ticket.direccion)
        ticket.ciudad = data.get('ciudad', ticket.ciudad)
        ticket.telefono = data.get('telefono', ticket.telefono)
        ticket.redes_sociales = data.get('redes_sociales', ticket.redes_sociales)
        return ticket

class BebidaPersonalizada:
    def __init__(self, tipo, cantidad=1, extras=None):
        self.tipo = tipo
        self.cantidad = cantidad
        self.extras = extras if extras else []
    
    def calcular_subtotal(self, precios_bebidas, precios_extras):
        subtotal = precios_bebidas[self.tipo] * self.cantidad
        for extra in self.extras:
            subtotal += precios_extras[extra] * self.cantidad
        return subtotal
    
    def calcular_tiempo(self, tiempo_bebidas, tiempo_extras):
        tiempo_total = tiempo_bebidas[self.tipo]
        for extra in self.extras:
            tiempo_total += tiempo_extras[extra]
        return tiempo_total * self.cantidad
    
    def __str__(self):
        texto = f"{self.cantidad}x {self.tipo}"
        if self.extras:
            texto += f" con {', '.join(self.extras)}"
        return texto
    
class SistemaPedidosCafeteria:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sistema de Pedidos - Cafetería")
        self.window.geometry("1000x680")
        
        # Sistema de tickets
        self.tickets_dir = "tickets"
        if not os.path.exists(self.tickets_dir):
            os.makedirs(self.tickets_dir)
        self.tickets_file = os.path.join(self.tickets_dir, "tickets.json")
        self.tickets = self.cargar_tickets()
        
        self.conf_estilo()
        
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        
        # Variables y precios
        self.contador_orden = 1
        self.ordenes_activas = {}
        self.bebidas_en_carrito = []
        self.bebida_actual = None
        
        self.tiempo_bebidas = {
            "Café Americano": 180,
            "Cappuccino": 300,
            "Latte": 240,
            "Té": 120
        }
        
        self.precio_bebidas = {
            "Café Americano": 25,
            "Cappuccino": 35,
            "Latte": 30,
            "Té": 20
        }
        
        self.tiempo_extra = {
            "Leche extra": 60,
            "Shot extra de café": 120,
            "Sirope de sabor": 30
        }
        
        self.precio_extra = {
            "Leche extra": 10,
            "Shot extra de café": 15,
            "Sirope de sabor": 8
        }

        # Variables de interfaz
        self.preparing_canvas = None
        self.completed_canvas = None
        self.preparing_frame = None
        self.completed_frame = None
        self.tickets_canvas = None
        self.tickets_lista_frame = None
        self.tickets_list = None  # Para la lista de tickets
        
        self.conf_menu()
        self.conf_gui()
        self.conf_precio_menu()  # Primero el menú de precios
        self.setup_info_panel()  # Después el panel de información
        
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)

    def cargar_tickets(self):
        if os.path.exists(self.tickets_file):
            try:
                with open(self.tickets_file, 'r') as f:
                    data = json.load(f)
                    return [Ticket.from_dict(t) for t in data]
            except Exception as e:
                print(f"Error al cargar tickets: {e}")
                return []
        return []

    def guardar_tickets(self):
        try:
            with open(self.tickets_file, 'w') as f:
                json.dump([t.to_dict() for t in self.tickets], f, indent=4)
        except Exception as e:
            print(f"Error al guardar tickets: {e}")

    def generar_ticket(self, orden_id, bebidas, total):
        ticket = Ticket(orden_id, bebidas, total)
        self.tickets.append(ticket)
        self.guardar_tickets()
        return ticket

    def conf_estilo(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores principales
        PRIMARY_COLOR = "#4a90e2"
        SECONDARY_COLOR = "#2c3e50"
        BG_COLOR = "#f5f6fa"
        ACCENT_COLOR = "#2ecc71"
        WARNING_COLOR = "#e74c3c"
        
        # Configurar estilos generales
        style.configure(".",
                    background=BG_COLOR,
                    foreground=SECONDARY_COLOR,
                    font=('Segoe UI', 9))
        
        # Notebook
        style.configure("TNotebook",
                    background=BG_COLOR,
                    tabmargins=[2, 5, 2, 0])
        
        style.configure("TNotebook.Tab",
                    background=BG_COLOR,
                    foreground=SECONDARY_COLOR,
                    padding=[10, 5],
                    font=('Segoe UI', 9, 'bold'))
        
        style.map("TNotebook.Tab",
                background=[("selected", PRIMARY_COLOR)],
                foreground=[("selected", "white")])
        
        # Frames y otros estilos
        style.configure("TFrame", background=BG_COLOR)
        style.configure("TLabelframe", background=BG_COLOR, foreground=SECONDARY_COLOR)
        style.configure("TLabelframe.Label", background=BG_COLOR, foreground=SECONDARY_COLOR,
                    font=('Segoe UI', 9, 'bold'))
        
        # Botones
        style.configure("TButton", background=PRIMARY_COLOR, foreground="white",
                    padding=[10, 5], font=('Segoe UI', 9, 'bold'))
        style.map("TButton",
                background=[("active", SECONDARY_COLOR)],
                foreground=[("active", "white")])
        
        # Botón de advertencia
        style.configure("Warning.TButton", background=WARNING_COLOR, foreground="white",
                    padding=[10, 5], font=('Segoe UI', 9, 'bold'))
        style.map("Warning.TButton",
                background=[("active", "#c0392b")],
                foreground=[("active", "white")])
        
        # Botón de éxito
        style.configure("Success.TButton", background=ACCENT_COLOR, foreground="white",
                    padding=[10, 5], font=('Segoe UI', 9, 'bold'))
        style.map("Success.TButton",
                background=[("active", "#27ae60")],
                foreground=[("active", " white")])
        
        # Estilos para tickets
        style.configure("Ticket.TFrame", background="white")
        style.configure("Ticket.TLabel",
                    background="white",
                    font=('Segoe UI', 9))
        style.configure("TicketHeader.TLabel",
                    background="white",
                    font=('Segoe UI', 12, 'bold'))
        style.configure("TicketTitle.TLabel",
                    background="white",
                    font=('Segoe UI', 14, 'bold'))
        style.configure("TicketTotal.TLabel",
                    background="white",
                    font=('Segoe UI', 11, 'bold'))
        
        # Otros widgets
        style.configure("TLabel", background=BG_COLOR, foreground=SECONDARY_COLOR)
        style.configure("TCombobox", selectbackground=PRIMARY_COLOR,
                    selectforeground="white", fieldbackground="white")
        style.configure("TCheckbutton", background=BG_COLOR, foreground=SECONDARY_COLOR)
        style.configure("TProgressbar", troughcolor=BG_COLOR, background=ACCENT_COLOR)
        
        # Etiquetas especiales
        style.configure("Header.TLabel", font=('Segoe UI', 10, 'bold'),
                    foreground=SECONDARY_COLOR, background=BG_COLOR)
        style.configure("Title.TLabel", font=('Segoe UI', 20, 'bold'),
                    foreground=PRIMARY_COLOR, background=BG_COLOR)
        style.configure("Subtitle.TLabel", font=('Segoe UI', 12, 'bold'),
                    foreground=SECONDARY_COLOR, background=BG_COLOR)
        
        # Menú
        style.configure("Bold.TLabelframe.Label", font=('Segoe UI', 12, 'bold'),
                    foreground=PRIMARY_COLOR, background=BG_COLOR)
        
        self.window.configure(bg=BG_COLOR)
    
    def conf_menu(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        
        # Menú de Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Exportar Tickets", command=self.exportar_tickets)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.salir)
        
        # Menú de Tickets
        tickets_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tickets", menu=tickets_menu)
        tickets_menu.add_command(label="Buscar Ticket", command=self.buscar_ticket)
        tickets_menu.add_command(label="Ver Historial", command=lambda: self.notebook.select(2))
        
        # Menú de Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="¿Cómo funciona?", command=self.mostrar_ayuda)
        help_menu.add_command(label="Créditos", command=self.mostrar_creditos)

    def conf_gui(self):
        self.notebook = ttk.Notebook(self.window)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        self.new_order_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.new_order_frame, text="Nuevo Pedido")
        self.conf_nueva_orden_tab()

        self.ordenes_activas_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.ordenes_activas_frame, text="Pedidos Activos")
        self.setup_ordenes_activas_tab()
        
        # Nueva pestaña para tickets
        self.tickets_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tickets_frame, text="Historial de Tickets")
        self.conf_tickets_tab()

        self.conf_precio_menu()

    def conf_tickets_tab(self):
        self.tickets_frame.grid_columnconfigure(0, weight=1)
        self.tickets_frame.grid_rowconfigure(1, weight=1)
        
        # Panel superior con controles
        control_frame = ttk.Frame(self.tickets_frame)
        control_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        # Filtros de búsqueda
        ttk.Label(control_frame, text="Fecha:").pack(side="left", padx=5)
        
        # Configuración del calendario
        self.fecha_filtro = tkcalendar.DateEntry(
            control_frame,
            width=12,
            background='royal blue',
            foreground='white',
            borderwidth=2,
            date_pattern='dd/mm/yyyy',
            state='readonly',  # Hacer el campo de texto no editable
            locale='es_MX',
            showweeknumbers=False,  # Opcional: ocultar números de semana
            firstweekday='monday'   # Opcional: comenzar semana en lunes
        )
        self.fecha_filtro.pack(side="left", padx=5)

        # Variables de control para el manejo de eventos
        self.fecha_filtro.bind('<<DateEntrySelected>>', lambda e: self.after_date_selection())
        
        ttk.Label(control_frame, text="Buscar:").pack(side="left", padx=5)
        self.busqueda_var = tk.StringVar()
        ttk.Entry(control_frame, textvariable=self.busqueda_var, width=20).pack(
            side="left", padx=5)
        
        ttk.Button(control_frame, text="Buscar", 
                command=self.filtrar_tickets).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Limpiar Filtros", 
                command=self.limpiar_filtros).pack(side="left", padx=5)
        
        # Lista de tickets con scroll
        self.tickets_list = ttk.Treeview(self.tickets_frame, 
            columns=("fecha", "total", "estado", "items"),
            show="headings",
            height=15)
        
        # Configuracion de columnas
        self.tickets_list.heading("fecha", text="Fecha y Hora")
        self.tickets_list.heading("total", text="Total")
        self.tickets_list.heading("estado", text="Ticket ID")
        self.tickets_list.heading("items", text="Items")
        
        self.tickets_list.column("fecha", width=150)
        self.tickets_list.column("total", width=100)
        self.tickets_list.column("estado", width=100)
        self.tickets_list.column("items", width=400)
        
        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(self.tickets_frame, orient="vertical", 
                                command=self.tickets_list.yview)
        self.tickets_list.configure(yscrollcommand=scrollbar.set)
        
        self.tickets_list.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Botón para ver detalle
        ttk.Button(self.tickets_frame, text="Ver Detalle", 
                command=self.ver_ticket_seleccionado).grid(
            row=2, column=0, pady=5)
        
        # Cargar tickets iniciales
        self.actualizar_lista_tickets()
        
        # Bind doble click
        self.tickets_list.bind("<Double-1>", lambda e: self.ver_ticket_seleccionado())

    def after_date_selection(self):
        """Método para manejar la selección de fecha de manera segura"""
        try:
            self.filtrar_tickets()
        except Exception as e:
            print(f"Error al filtrar tickets: {e}")

    def limpiar_filtros(self):
        """Método actualizado para limpiar filtros de manera segura"""
        try:
            self.fecha_filtro.set_date(datetime.now())
            self.busqueda_var.set("")
            self.actualizar_lista_tickets()
        except Exception as e:
            print(f"Error al limpiar filtros: {e}")

    def filtrar_tickets(self):
        """Método actualizado para filtrar tickets de manera segura"""
        try:
            fecha = self.fecha_filtro.get_date()
            busqueda = self.busqueda_var.get().lower()
            
            tickets_filtrados = [
                t for t in self.tickets
                if (t.timestamp.date() == fecha and
                    (not busqueda or
                    busqueda in t.ticket_id.lower() or
                    busqueda in str(t.total).lower() or
                    any(busqueda in str(b).lower() for b in t.bebidas)))
            ]
            
            self.actualizar_lista_tickets(tickets_filtrados)
        except Exception as e:
            print(f"Error al filtrar tickets: {e}")
            # En caso de error, mostrar todos los tickets
            self.actualizar_lista_tickets()

    def actualizar_lista_tickets(self, tickets_filtrados=None):
        # Limpiar lista actual
        for item in self.tickets_list.get_children():
            self.tickets_list.delete(item)
        
        # Mostrar tickets
        tickets_a_mostrar = tickets_filtrados if tickets_filtrados is not None else self.tickets
        for ticket in reversed(tickets_a_mostrar):
            self.tickets_list.insert("", "end", values=(
                ticket.timestamp.strftime('%d/%m/%Y %H:%M'),
                f"${ticket.total:.2f}",
                ticket.ticket_id,
                ", ".join(str(b) for b in ticket.bebidas)
            ))

    def ver_ticket_seleccionado(self):
        seleccion = self.tickets_list.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un ticket")
            return
        
        ticket_id = self.tickets_list.item(seleccion[0])['values'][2]
        ticket = next((t for t in self.tickets if t .ticket_id == ticket_id), None)
        
        if ticket:
            self.mostrar_detalle_ticket(ticket)

    def mostrar_detalle_ticket(self, ticket):
        # Crear ventana de detalle
        detalle = tk.Toplevel(self.window)
        detalle.title(f"Ticket #{ticket.ticket_id}")
        detalle.geometry("400x600")  # Aumentar altura para el contenido adicional
        
        # Frame principal con estilo de ticket
        main_frame = ttk.Frame(detalle, style="Ticket.TFrame")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Encabezado
        ttk.Label(main_frame, text=ticket.establecimiento,
                style="TicketTitle.TLabel").pack(pady=5)
        
        # Información de ubicación
        ttk.Label(main_frame, text=ticket.ciudad,
                style="Ticket.TLabel").pack(pady=1)
        ttk.Label(main_frame, text=ticket.direccion,
                style="Ticket.TLabel").pack(pady=1)
        ttk.Label(main_frame, text=f"Tel: {ticket.telefono}",
                style="Ticket.TLabel").pack(pady=1)
        
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Información del ticket
        ttk.Label(main_frame, text=f"Ticket: #{ticket.ticket_id}",
                style="TicketHeader.TLabel").pack()
        ttk.Label(main_frame, 
                text=f"Fecha: {ticket.timestamp.strftime('%d/%m/%Y %H:%M')}",
                style="Ticket.TLabel").pack()
        
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Detalles de bebidas
        for bebida in ticket.bebidas:
            bebida_frame = ttk.Frame(main_frame, style="Ticket.TFrame")
            bebida_frame.pack(fill='x', pady=2)
            ttk.Label(bebida_frame, text=str(bebida),
                    style="Ticket.TLabel").pack(side='left')
        
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Total
        ttk.Label(main_frame, text=f"Total: ${ticket.total:.2f}",
                style="TicketTotal.TLabel").pack(pady=5)
        
        # Redes sociales
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=5)
        ttk.Label(main_frame, text="Síguenos en:",
                style="Ticket.TLabel").pack(pady=(5,0))
        for red, usuario in ticket.redes_sociales.items():
            ttk.Label(main_frame, text=f"{red}: {usuario}",
                    style="Ticket.TLabel").pack()
        
        # Mensaje final
        ttk.Label(main_frame, text="\n¡Gracias por su preferencia!",
                style="TicketHeader.TLabel").pack(pady=(10,5))
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Cerrar",
                command=detalle.destroy).pack(side='left', padx=5)

    def filtrar_tickets(self):
        fecha = self.fecha_filtro.get_date()
        busqueda = self.busqueda_var.get().lower()
        
        tickets_filtrados = [
            t for t in self.tickets
            if (t.timestamp.date() == fecha and
                (not busqueda or
                 busqueda in t.ticket_id.lower() or
                 busqueda in str(t.total).lower() or
                 any(busqueda in str(b).lower() for b in t.bebidas)))
        ]
        
        self.actualizar_lista_tickets(tickets_filtrados)

    def setup_ordenes_activas_tab(self):
        self.ordenes_activas_frame.grid_columnconfigure(0, weight=1)
        self.ordenes_activas_frame.grid_columnconfigure(1, weight=0)
        self.ordenes_activas_frame.grid_columnconfigure(2, weight=1)
        self.ordenes_activas_frame.grid_rowconfigure(1, weight=1)
        
        # Panel izquierdo: Pedidos en Preparación
        preparing_panel = ttk.Frame(self.ordenes_activas_frame)
        preparing_panel.grid(row=0, rowspan=2, column=0, sticky="nsew", padx=5, pady=5)
        preparing_panel.grid_rowconfigure(1, weight=1)
        preparing_panel.grid_columnconfigure(0, weight=1)
        
        ttk.Label(preparing_panel, text="Pedidos en Preparación", 
                style="Header.TLabel").grid(row=0, column=0, pady=5, sticky="w")
        
        # Scrollbar y Canvas para pedidos en preparación
        preparing_scroll = ttk.Scrollbar(preparing_panel)
        preparing_scroll.grid(row=1, column=1, sticky="ns")
        
        self.preparing_canvas = tk.Canvas(preparing_panel, 
                                        yscrollcommand=preparing_scroll.set,
                                        highlightthickness=0)
        self.preparing_canvas.grid(row=1, column=0, sticky="nsew")
        
        self.preparing_frame = ttk.Frame(self.preparing_canvas)
        self.preparing_frame.grid_columnconfigure(0, weight=1)
        
        self.preparing_canvas.create_window((0, 0), 
                                        window=self.preparing_frame,
                                        anchor="nw",
                                        tags="preparing_frame")
        
        preparing_scroll.config(command=self.preparing_canvas.yview)
        
        # Separador vertical
        ttk.Separator(self.ordenes_activas_frame, orient='vertical').grid(
            row=0, rowspan=2, column=1, sticky="ns", padx=10)
        
        # Panel derecho: Pedidos Listos
        completed_panel = ttk.Frame(self.ordenes_activas_frame)
        completed_panel.grid(row=0, rowspan=2, column=2, sticky="nsew", padx=5, pady=5)
        completed_panel.grid_rowconfigure(1, weight=1)
        completed_panel.grid_columnconfigure(0, weight=1)
        
        ttk.Label(completed_panel, text="Pedidos Listos", 
                style="Header.TLabel").grid(row=0, column=0, pady=5, sticky="w")
        
        completed_scroll = ttk.Scrollbar(completed_panel)
        completed_scroll.grid(row=1, column=1, sticky="ns")
        
        self.completed_canvas = tk.Canvas(completed_panel, 
                                        yscrollcommand=completed_scroll.set,
                                        highlightthickness=0)
        self.completed_canvas.grid(row=1, column=0, sticky="nsew")
        
        self.completed_frame = ttk.Frame(self.completed_canvas)
        self.completed_frame.grid_columnconfigure(0, weight=1)
        
        self.completed_canvas.create_window((0, 0), 
                                        window=self.completed_frame,
                                        anchor="nw", 
                                        tags="completed_frame")
        
        completed_scroll.config(command=self.completed_canvas.yview)
        
        # Configurar eventos para mantener la responsividad
        self.preparing_frame.bind('<Configure>', self.conf_on_frame)
        self.completed_frame.bind('<Configure>', self.conf_on_frame)

    def agregar_al_carrito(self):
        if not self.drink_var.get():
            messagebox.showwarning("Advertencia", "Por favor seleccione una bebida")
            return
        
        extras_seleccionados = [
            extra for extra, var in self.extra_vars.items() if var.get()
        ]
        
        bebida = BebidaPersonalizada(
            self.drink_var.get(),
            self.cantidad_var.get(),
            extras_seleccionados
        )
        
        self.bebidas_en_carrito.append(bebida)
        self.actualizar_carrito()
        
        # Limpiar selección
        self.drink_var.set('')
        self.cantidad_var.set(1)
        for var in self.extra_vars.values():
            var.set(False)

    def actualizar_carrito(self):
        self.cart_text.delete(1.0, tk.END)
        total = 0
        
        for i, bebida in enumerate(self.bebidas_en_carrito, 1):
            subtotal = bebida.calcular_subtotal(self.precio_bebidas, self.precio_extra)
            total += subtotal
            
            self.cart_text.insert(tk.END, 
                f"{i}. {bebida}\n   Subtotal: ${subtotal:.2f}\n\n")
        
        self.total_label.config(text=f"Total: ${total:.2f}")

    def vaciar_carrito(self):
        if self.bebidas_en_carrito and messagebox.askyesno(
            "Confirmar", "¿Está seguro de vaciar el carrito?"):
            self.bebidas_en_carrito = []
            self.actualizar_carrito()

    def crear_orden(self):
        if not self.bebidas_en_carrito:
            return
                
        order_number = self.contador_orden
        self.contador_orden += 1
        
        # Crear frame del pedido
        order_frame = ttk.LabelFrame(self.preparing_frame, text=f"Pedido #{order_number}")
        order_frame.grid(row=len(self.ordenes_activas), column=0, sticky="ew", padx=5, pady=5)
        order_frame.grid_columnconfigure(0, weight=1)
        
        content_frame = ttk.Frame(order_frame)
        content_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Mostrar bebidas
        for i, bebida in enumerate(self.bebidas_en_carrito):
            ttk.Label(content_frame, text=str(bebida)).grid(
                row=i, column=0, pady=2, sticky="ew")
        
        # Barra de progreso y tiempo
        progress = ttk.Progressbar(content_frame, length=200, mode='determinate')
        progress.grid(row=len(self.bebidas_en_carrito), column=0, pady=5, sticky="ew")
        
        time_label = ttk.Label(content_frame, text="Tiempo restante: --:--")
        time_label.grid(row=len(self.bebidas_en_carrito)+1, column=0, pady=2)
        
        # Calcular tiempo total
        total_time = sum(bebida.calcular_tiempo(self.tiempo_bebidas, self.tiempo_extra) 
                        for bebida in self.bebidas_en_carrito)
        
        # Guardar información del pedido
        self.ordenes_activas[order_number] = {
            'frame': order_frame,
            'progress': progress,
            'time_label': time_label,
            'total_time': total_time,
            'start_time': time.time(),
            'bebidas': self.bebidas_en_carrito.copy()
        }
        
        # Iniciar el proceso de preparación
        thread = threading.Thread(target=self.actualizar_progreso, args=(order_number,))
        thread.daemon = True
        thread.start()

    def actualizar_progreso(self, order_number):
        if order_number not in self.ordenes_activas:
            return
                
        orden = self.ordenes_activas[order_number]
        progress = orden['progress']
        time_label = orden['time_label']
        total_time = orden['total_time']
        start_time = orden['start_time']
        
        while True:
            if order_number not in self.ordenes_activas:
                return
                
            if not progress.winfo_exists():
                return
                    
            elapsed = time.time() - start_time
            remaining = max(0, total_time - elapsed)
            
            try:
                self.window.after(0, self.actualizar_progreso_ui, 
                                progress, time_label, elapsed, remaining, total_time)
                
                if elapsed >= total_time:
                    self.window.after(0, lambda: self.completar_orden(order_number))
                    break
                
                time.sleep(0.1)
            except tk.TclError:
                # Widget fue destruido
                break

    def actualizar_progreso_ui(self, progress, time_label, elapsed, remaining, total_time):
        if not progress.winfo_exists() or not time_label.winfo_exists():
            return
            
        progress_value = min(100, (elapsed / total_time) * 100)
        if abs(progress_value - progress['value']) >= 1:
            progress['value'] = progress_value
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        time_text = f"Tiempo restante: {minutes:02d}:{seconds:02d}"
        
        if time_label['text'] != time_text:
            time_label['text'] = time_text

    def on_tab_change(self, event):
        current_tab = self.notebook.select()
        tab_index = self.notebook.index(current_tab)
        
        if tab_index == 1:
            self.window.after(100, self.update_canvases)

    def conf_on_frame(self, event):
        canvas = event.widget.master
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig("preparing_frame", width=canvas.winfo_width())
        canvas.itemconfig("completed_frame", width=canvas.winfo_width())

    def update_canvases(self):
        try:
            if self.preparing_canvas and self.preparing_frame:
                self.preparing_canvas.configure(scrollregion=self.preparing_canvas.bbox("all"))
                self.preparing_canvas.itemconfig("preparing_frame", 
                                            width=self.preparing_canvas.winfo_width())
                
            if self.completed_canvas and self.completed_frame:
                self.completed_canvas.configure(scrollregion=self.completed_canvas.bbox("all"))
                self.completed_canvas.itemconfig("completed_frame", 
                                            width=self.completed_canvas.winfo_width())
                
            # Forzar actualización visual
            self.window.update_idletasks()
        except tk.TclError:
            pass  # Ignorar errores si los widgets fueron destruidos

    def mover_acompletados(self, order_number):
        if order_number in self.ordenes_activas:
            order = self.ordenes_activas[order_number]
            original_frame = order['frame']
            
            # Crear nuevo frame en la sección de completados
            completed_frame = ttk.LabelFrame(self.completed_frame, text=f"Pedido #{order_number}")
            completed_frame.grid(sticky="ew", padx=5, pady=5)
            completed_frame.grid_columnconfigure(0, weight=1)
            
            # Frame para el contenido
            content_frame = ttk.Frame(completed_frame)
            content_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
            content_frame.grid_columnconfigure(0, weight=1)
            
            # Mostrar las bebidas
            for idx, bebida in enumerate(order['bebidas']):
                bebida_frame = ttk.Frame(content_frame)
                bebida_frame.grid(row=idx, column=0, sticky="ew")
                bebida_frame.grid_columnconfigure(0, weight=1)
                
                ttk.Label(bebida_frame, text=str(bebida)).grid(
                    row=0, column=0, sticky="w", pady=2)
            
            # Mensaje de completado
            ttk.Label(content_frame, text="¡Pedido Completado!", 
                    style="Header.TLabel").grid(
                        row=len(order['bebidas']), column=0, sticky="ew", pady=5)
            
            # Botón eliminar
            ttk.Button(content_frame, text="Eliminar",
                    command=lambda num=order_number: self.remover_orden(num)).grid(
                        row=len(order['bebidas'])+1, column=0, pady=5)
            
            # Actualizar la referencia del frame en ordenes_activas
            order['frame'] = completed_frame
            
            # IMPORTANTE: Destruir el frame original DESPUÉS de crear el nuevo
            original_frame.destroy()
            
            # Actualizar los canvas para reflejar los cambios
            self.window.after(100, self.update_canvases)

    def conf_nueva_orden_tab(self):
        # Frame configuration
        self.new_order_frame.grid_columnconfigure(0, weight=1)
        self.new_order_frame.grid_rowconfigure(1, weight=1)
        
        # Variables
        self.drink_var = tk.StringVar()
        self.cantidad_var = tk.IntVar(value=1)
        self.extra_vars = {
            "Leche extra": tk.BooleanVar(),
            "Shot extra de café": tk.BooleanVar(),
            "Sirope de sabor": tk.BooleanVar()
        }
        
        # Configurar estilo para los elementos internos
        style = ttk.Style()
        style.configure("NewOrder.TLabel",
                    font=('Segoe UI', 14),  
                    foreground="#2c3e50",
                    background="#f5f6fa")
        
        # Order panel
        order_panel = ttk.LabelFrame(self.new_order_frame, text="Nuevo Pedido")
        order_panel.grid(row=0, column=0, sticky="n", padx=10, pady=5)
        
        # Configuracion de las columnas del order_panel
        order_panel.grid_columnconfigure(1, weight=1, minsize=200)
        
        # Drink selection con texto más grande
        ttk.Label(order_panel, text="Bebida:", width=15, style="NewOrder.TLabel").grid(
            row=0, column=0, pady=5, padx=15)

        drink_combo = ttk.Combobox(order_panel, 
                                textvariable=self.drink_var,
                                values=list(self.precio_bebidas.keys()),
                                width=30,
                                font=('Segoe UI', 11),
                                state="readonly")  
        drink_combo.grid(row=0, column=1, pady=5, padx=15)

        # Quantity con texto más grande
        ttk.Label(order_panel, text="Cantidad:", width=15, style="NewOrder.TLabel").grid(
            row=1, column=0, pady=5, padx=15)

        quantity_spin = ttk.Spinbox(order_panel,
                                from_=1, to=10,
                                textvariable=self.cantidad_var,
                                width=30,
                                font=('Segoe UI', 11),
                                state="readonly",     
                                wrap=True)            # Opcional: permite ciclar entre valores
        quantity_spin.grid(row=1, column=1, pady=5, padx=15)
        
        # Extras frame con texto 
        extras_frame = ttk.LabelFrame(order_panel, text="Extras")
        extras_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5, padx=15)
        
        extras_frame.grid_columnconfigure(0, weight=1)
        
        # Checkbuttons con texto 
        for i, (extra, var) in enumerate(self.extra_vars.items()):
            checkbutton = ttk.Checkbutton(extras_frame, 
                                        text=extra, 
                                        variable=var,
                                        style="NewOrder.TCheckbutton")
            checkbutton.grid(row=i, column=0, sticky="w", pady=2, padx=20)
        
        # Configurar estilo para checkbuttons
        style.configure("NewOrder.TCheckbutton",
                    font=('Segoe UI', 11),  
                    background="#f5f6fa")
        
        # Botón Agregar al Carrito
        style.configure("Green.TButton",
                    background="green",
                    foreground="white",
                    padding=(10, 5),
                    font=('Segoe UI', 11, 'bold'))  
        
        ttk.Button(order_panel, 
                text="Agregar al Carrito",
                command=self.agregar_al_carrito,
                style="Green.TButton").grid(
            row=3, column=0, columnspan=2, pady=10, padx=15, sticky="ew")
        
        # Cart frame con scrollbar
        cart_frame = ttk.LabelFrame(self.new_order_frame, text="Carrito")
        cart_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        cart_frame.grid_rowconfigure(0, weight=1)
        cart_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para contener el texto y el scrollbar
        text_frame = ttk.Frame(cart_frame)
        text_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_rowconfigure(0, weight=1)
        
        # Texto del carrito con scrollbar
        self.cart_text = tk.Text(text_frame, height=10, width=40)
        self.cart_text.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.cart_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.cart_text.configure(yscrollcommand=scrollbar.set)
        
        # Total label
        style = ttk.Style()
        style.configure("Total.TLabel",
                    font=('Segoe UI', 14, 'bold'),
                    foreground="#2c3e50")
        
        self.total_label = ttk.Label(cart_frame, 
                                    text="Total: $0.00",
                                    style="Total.TLabel")
        self.total_label.grid(row=1, column=0, sticky="w", padx=15, pady=10)
        
        # Botones
        button_frame = ttk.Frame(cart_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Estilo para el botón de eliminar
        style.configure("BigWarning.TButton",
                    padding=[20, 15],
                    font=('Segoe UI', 11, 'bold'),
                    background="#e74c3c",
                    foreground="white")
        
        # Estilo para el botón de crear pedido
        style.configure("BigCreate.TButton",
                    padding=[20, 15],
                    font=('Segoe UI', 11, 'bold'),
                    background="Blue",
                    foreground="white")
        
        # Botón Vaciar Carrito
        ttk.Button(button_frame, 
                text="Vaciar Carrito",
                command=self.vaciar_carrito,
                style="BigWarning.TButton").pack(side="left", padx=10)
        
        # Botón Crear Pedido
        ttk.Button(button_frame, 
                text="Crear Pedido",
                command=self.confirmar_orden,
                style="BigCreate.TButton").pack(side="left", padx=10)

    def conf_precio_menu(self):
        # Creacion del frame contenedor para menú de precios e información
        self.right_panel = ttk.Frame(self.window)
        self.right_panel.grid(row=1, column=1, sticky="n", padx=10, pady=5)
        
        # Price menu panel
        price_frame = ttk.LabelFrame(self.right_panel, text="Menú de Precios y Tiempos")
        price_frame.grid(row=0, column=0, sticky="n", pady=(0,5))
        
        # Encabezados
        ttk.Label(price_frame, text="", style="Bold.TLabelframe.Label").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(5,2))
        
        # Headers for columns
        ttk.Label(price_frame, text="Producto", style="Bold.TLabelframe.Label").grid(
            row=1, column=0, sticky="w", padx=5)
        ttk.Label(price_frame, text="Precio", style="Bold.TLabelframe.Label").grid(
            row=1, column=1, sticky="e", padx=5)
        ttk.Label(price_frame, text="Tiempo", style="Bold.TLabelframe.Label").grid(
            row=1, column=2, sticky="e", padx=5)
        
        row = 2
        for bebida, precio in self.precio_bebidas.items():
            tiempo = self.tiempo_bebidas[bebida]
            tiempo_str = f"{tiempo//60}:{tiempo%60:02d} min"
            
            ttk.Label(price_frame, text=bebida).grid(
                row=row, column=0, sticky="w", padx=5)
            ttk.Label(price_frame, text=f"${precio:.2f}").grid(
                row=row, column=1, sticky="e", padx=5)
            ttk.Label(price_frame, text=tiempo_str).grid(
                row=row, column=2, sticky="e", padx=5)
            row += 1
        
        # Extras prices and times
        ttk.Label(price_frame, text="Extras:", style="Bold.TLabelframe.Label").grid(
            row=row, column=0, columnspan=3, sticky="w", pady=(10,2))
        
        row += 1 
        for extra, precio in self.precio_extra.items():
            tiempo = self.tiempo_extra[extra]
            tiempo_str = f"{tiempo//60}:{tiempo%60:02d} min"
            
            ttk.Label(price_frame, text=extra).grid(
                row=row, column=0, sticky="w", padx=5)
            ttk.Label(price_frame, text=f"${precio:.2f}").grid(
                row=row, column=1, sticky="e", padx=5)
            ttk.Label(price_frame, text=tiempo_str).grid(
                row=row, column=2, sticky="e", padx=5)
            row += 1

    def setup_info_panel(self):
        """Configura el panel de información con fecha, hora y ubicación"""
        info_frame = ttk.LabelFrame(self.right_panel, text="Información")
        info_frame.grid(row=1, column=0, sticky="n", pady=(0,5))
        
        self.time_label = ttk.Label(info_frame, text="")
        self.time_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        self.actualizar_tiempo()
        
        current_date = datetime.now().strftime("%d/%m/%Y")
        ttk.Label(info_frame, text=f"Fecha: {current_date}",
                style="Bold.TLabelframe.Label").grid(
            row=0, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        
        ttk.Label(info_frame, text="Ubicación:",
                style="Bold.TLabelframe.Label").grid(
            row=2, column=0, columnspan=2, sticky="w", padx=5, pady=(10,2))
        
        ttk.Label(info_frame, text="Boca del Río, Veracruz, Mexico").grid(
            row=3, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        
        ttk.Label(info_frame, text="Dirección:",
                style="Bold.TLabelframe.Label").grid(
            row=4, column=0, columnspan=2, sticky="w", padx=5, pady=(10,2))
        
        direccion_text = "Bv. Adolfo Ruiz Cortines, Mar de Cortes    \n y Costa Dorada, Col: Costa Verde\n CP: 94294"
        ttk.Label(info_frame, text=direccion_text).grid(
            row=5, column=0, columnspan=2, sticky="w", padx=5, pady=2)

    def actualizar_tiempo(self):
        """Actualiza la hora en tiempo real"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=f"Hora: {current_time}")
        # Actualizar cada segundo
        self.window.after(1000, self.actualizar_tiempo)

    def remover_orden(self, order_number):
        """Método para remover órdenes"""
        if order_number in self.ordenes_activas:
            if self.ordenes_activas[order_number]['frame'].winfo_exists():
                self.ordenes_activas[order_number]['frame'].destroy()
            del self.ordenes_activas[order_number]
            self.update_canvases()

    def limpiar_filtros(self):
        self.fecha_filtro.set_date(datetime.now())
        self.busqueda_var.set("")
        self.actualizar_lista_tickets()

    def buscar_ticket(self):
        ticket_id = tk.simpledialog.askstring("Buscar Ticket", 
                                            "Ingrese el ID del ticket:")
        if ticket_id:
            ticket = next((t for t in self.tickets if t.ticket_id == ticket_id.upper()), 
                         None)
            if ticket:
                self.mostrar_detalle_ticket(ticket)
            else:
                messagebox.showwarning("No encontrado", 
                                     "No se encontró el ticket especificado")

    def exportar_tickets(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump([t.to_dict() for t in self.tickets], f, indent=4)
                messagebox.showinfo("Éxito", "Tickets exportados correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar tickets: {str(e)}")

    def completar_orden(self, order_number):
        """Método para manejar la completación de órdenes"""
        if order_number in self.ordenes_activas:
            # Mover a completados
            self.mover_acompletados(order_number)
            # Reproducir sonido
            self.window.bell()
            # Actualizar los canvas
            self.update_canvases()

    def confirmar_orden(self):
        if not self.bebidas_en_carrito:
            messagebox.showwarning("Advertencia", "El carrito está vacío")
            return
        
        total = sum(bebida.calcular_subtotal(self.precio_bebidas, self.precio_extra) 
                   for bebida in self.bebidas_en_carrito)
        
        confirm_msg = "¿Confirmar pedido?\n\n"
        for i, bebida in enumerate(self.bebidas_en_carrito, 1):
            subtotal = bebida.calcular_subtotal(self.precio_bebidas, self.precio_extra)
            confirm_msg += f"{i}. {bebida}\n   Subtotal: ${subtotal:.2f}\n\n"
        confirm_msg += f"\nTotal: ${total:.2f}"
        
        if messagebox.askyesno("Confirmar Pedido", confirm_msg):
            # Generar ticket antes de crear la orden
            ticket = self.generar_ticket(self.contador_orden, 
                                       self.bebidas_en_carrito.copy(), 
                                       total)
            
            # Crear la orden
            self.crear_orden()
            
            # Limpiar carrito
            self.bebidas_en_carrito = []
            self.actualizar_carrito()
            
            # Mostrar mensaje de éxito con información del ticket
            success_msg = f"¡Pedido creado exitosamente!\n\nTicket #{ticket.ticket_id}"
            messagebox.showinfo("Éxito", success_msg)
            
            # Preguntar si desea ver el ticket
            if messagebox.askyesno("Ver Ticket", 
                                 "¿Desea ver el detalle del ticket?"):
                self.mostrar_detalle_ticket(ticket)
            
            # Actualizar lista de tickets
            self.actualizar_lista_tickets()
            
            # Cambiar a la pestaña de pedidos activos
            self.notebook.select(1)

    def salir(self):
        # Guardar tickets antes de salir
        self.guardar_tickets()
        self.window.quit()

    def mostrar_creditos(self):
        credits_text = """
SISTEMA DE PEDIDOS PARA CAFETERÍA

Desarrollado por:
- Michell Alexis Policarpio Moran (zs21002379)
- Contreras Matla Luis Fernando (zs21020225)
- Bravo Ibañez Luis Fernando (zS21002428)
- García Velandia Samuel Obded (zS21002413)

Características:
- Sistema de pedidos en tiempo real
- Gestión de bebidas y extras
- Sistema de tickets
- Historial de pedidos
- Exportación de tickets

© 2024 - Todos los derechos reservados
Universidad Veracruzana
Facultad de Ingeniería Eléctrica y Electrónica
"""
        messagebox.showinfo("Créditos", credits_text)

    def mostrar_ayuda(self):
        texto_ayuda = """
SISTEMA DE PEDIDOS PARA CAFETERÍA - GUÍA DE USO

1. REALIZAR UN NUEVO PEDIDO:
   - Seleccione el tipo de bebida del menú desplegable
   - Ajuste la cantidad deseada
   - Seleccione los extras deseados
   - Presione "Agregar al Carrito"
   - Puede agregar más bebidas repitiendo el proceso
   - Cuando termine, presione "Crear Pedido"

2. TIEMPOS DE PREPARACIÓN:
   Bebidas:
   - Café Americano: 3 minutos
   - Cappuccino: 5 minutos
   - Latte: 4 minutos
   - Té: 2 minutos

   Extras:
   - Leche extra: +1 minuto
   - Shot extra de café: +2 minutos
   - Sirope de sabor: +30 segundos

3. SEGUIMIENTO DE PEDIDOS:
   - Los pedidos en preparación muestran una barra de progreso
   - Al completarse, pasan automáticamente a "Pedidos Listos"
   - Puede eliminar los pedidos listos usando el botón "Eliminar"

4. SISTEMA DE TICKETS:
   - Cada pedido genera automáticamente un ticket
   - Puede ver el historial de tickets en la pestaña correspondiente
   - Puede buscar tickets por fecha o contenido
   - El historial de tickets se guarda automáticamente
"""
        messagebox.showinfo("Ayuda - Cómo Funciona", texto_ayuda)

    def run(self):
        self.window.protocol("WM_DELETE_WINDOW", self.salir)
        self.window.mainloop()

if __name__ == "__main__":
    app = SistemaPedidosCafeteria()
    app.run() 

