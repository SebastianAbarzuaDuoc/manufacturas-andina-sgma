import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# --- BASE DE DATOS LOCAL ---
def inicializar_bd():
    conn = sqlite3.connect("manufacturas_andina.db")
    cursor = conn.cursor()
    
    # Tabla Activos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            ubicacion TEXT NOT NULL,
            estado TEXT NOT NULL
        )
    ''')
    
    # Tabla Órdenes de Trabajo (Actualizada con fecha y diagnóstico)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ordenes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_activo TEXT NOT NULL,
            tipo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            fecha_reporte TEXT NOT NULL,
            diagnostico TEXT DEFAULT 'Pendiente de revisión',
            estado TEXT NOT NULL
        )
    ''')
    
    # Datos iniciales de ejemplo
    cursor.execute("SELECT COUNT(*) FROM activos")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO activos (codigo, nombre, tipo, ubicacion, estado)
            VALUES (?, ?, ?, ?, ?)
        ''', [
            ('EXT-001', 'Extrusora Principal A', 'Extrusora', 'Planta 1 - Sector Norte', 'Operativo'),
            ('INY-002', 'Inyectora de Moldes B', 'Inyectora', 'Planta 1 - Sector Sur', 'Detenido por Falla'),
            ('CAL-001', 'Caldera de Vapor', 'Caldera', 'Área de Servicios', 'Operativo'),
            ('CMP-003', 'Compresor Industrial', 'Compresor', 'Planta 2', 'En Mantención')
        ])
        
        cursor.execute('''
            INSERT INTO ordenes (codigo_activo, tipo, descripcion, fecha_reporte, diagnostico, estado)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('INY-002', 'Correctiva (Falla Urgente)', 'Sobrecalentamiento en cilindro de inyección', '2026-11-11 09:30', 'Pendiente de revisión', 'Pendiente'))
        
    conn.commit()
    conn.close()

# --- APLICACIÓN SPRINT 1 TERMINADO ---
class AppManufacturasAndina:
    def __init__(self, root):
        self.root = root
        self.root.title("Manufacturas Andina S.A. | SGMA - Sprint 1 Completo")
        self.root.geometry("1050x660")
        self.root.configure(bg="#0F172A")

        # Paleta de Colores
        self.BG_DARK = "#0F172A"
        self.SIDEBAR_BG = "#1E293B"
        self.CARD_BG = "#1E293B"
        self.INPUT_BG = "#334155"
        self.TEXT_COLOR = "#F8FAFC"
        self.TEXT_MUTED = "#94A3B8"
        self.CYAN_ACCENT = "#38BDF8"
        self.GREEN_SUCCESS = "#22C55E"
        self.RED_ALERT = "#EF4444"
        self.AMBER_WARN = "#F59E0B"

        self.configurar_estilos()

        # Layout Principal
        self.sidebar = tk.Frame(self.root, bg=self.SIDEBAR_BG, width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.main_area = tk.Frame(self.root, bg=self.BG_DARK)
        self.main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.crear_sidebar()

        # Pantallas del Sprint 1
        self.frame_activos = tk.Frame(self.main_area, bg=self.BG_DARK)
        self.frame_reportes = tk.Frame(self.main_area, bg=self.BG_DARK)
        self.frame_historial = tk.Frame(self.main_area, bg=self.BG_DARK)

        self.crear_pantalla_activos()
        self.crear_pantalla_reportes()
        self.crear_pantalla_historial()

        # Cargar datos e iniciar
        self.mostrar_pantalla("activos")
        self.cargar_activos()
        self.cargar_ordenes()

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Treeview", 
                        font=("Segoe UI", 9),
                        rowheight=30,
                        background="#1E293B",
                        fieldbackground="#1E293B",
                        foreground="#F8FAFC",
                        borderwidth=0)
        style.configure("Treeview.Heading", 
                        font=("Segoe UI", 9, "bold"),
                        background="#334155",
                        foreground="#38BDF8",
                        relief="flat")
        style.map("Treeview", 
                  background=[("selected", "#0284C7")], 
                  foreground=[("selected", "#FFFFFF")])

    def crear_sidebar(self):
        lbl_brand = tk.Label(self.sidebar, text="⚡ ANDINA S.A.", font=("Segoe UI", 18, "bold"), 
                             bg=self.SIDEBAR_BG, fg=self.CYAN_ACCENT)
        lbl_brand.pack(pady=(30, 2))
        
        lbl_sub = tk.Label(self.sidebar, text="Gestión & Mantención Activos", font=("Segoe UI", 9), 
                           bg=self.SIDEBAR_BG, fg=self.TEXT_MUTED)
        lbl_sub.pack(pady=(0, 30))

        # Botones de Navegación
        self.btn_nav_activos = tk.Button(self.sidebar, text="  📊  Inventario Activos", font=("Segoe UI", 10, "bold"),
                                         bg="#0284C7", fg="white", bd=0, relief="flat", anchor="w", padx=20, pady=12,
                                         cursor="hand2", command=lambda: self.mostrar_pantalla("activos"))
        self.btn_nav_activos.pack(fill=tk.X, padx=15, pady=5)

        self.btn_nav_reportes = tk.Button(self.sidebar, text="  🛠️  Reportar Falla / OT", font=("Segoe UI", 10, "bold"),
                                          bg="#334155", fg=self.TEXT_MUTED, bd=0, relief="flat", anchor="w", padx=20, pady=12,
                                          cursor="hand2", command=lambda: self.mostrar_pantalla("reportes"))
        self.btn_nav_reportes.pack(fill=tk.X, padx=15, pady=5)

        self.btn_nav_historial = tk.Button(self.sidebar, text="  📋  Historial & Cierre OT", font=("Segoe UI", 10, "bold"),
                                           bg="#334155", fg=self.TEXT_MUTED, bd=0, relief="flat", anchor="w", padx=20, pady=12,
                                           cursor="hand2", command=lambda: self.mostrar_pantalla("historial"))
        self.btn_nav_historial.pack(fill=tk.X, padx=15, pady=5)

        # Panel Estado
        card_info = tk.Frame(self.sidebar, bg="#334155", padx=15, pady=15)
        card_info.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=20)
        
        tk.Label(card_info, text="Sprint 1 - Operativo", font=("Segoe UI", 9, "bold"), bg="#334155", fg=self.GREEN_SUCCESS).pack(anchor="w")
        tk.Label(card_info, text="● BD SQLite Conectada\n● Módulo CRUD Activos\n● Flujo Completo OT", font=("Segoe UI", 8), bg="#334155", fg=self.TEXT_COLOR, justify="left").pack(anchor="w", pady=(5,0))

    def mostrar_pantalla(self, pantalla):
        self.frame_activos.pack_forget()
        self.frame_reportes.pack_forget()
        self.frame_historial.pack_forget()

        # Resetear colores botones
        for btn in (self.btn_nav_activos, self.btn_nav_reportes, self.btn_nav_historial):
            btn.configure(bg="#334155", fg=self.TEXT_MUTED)

        if pantalla == "activos":
            self.btn_nav_activos.configure(bg="#0284C7", fg="white")
            self.frame_activos.pack(fill=tk.BOTH, expand=True)
            self.cargar_activos()
        elif pantalla == "reportes":
            self.btn_nav_reportes.configure(bg="#0284C7", fg="white")
            self.frame_reportes.pack(fill=tk.BOTH, expand=True)
        else:
            self.btn_nav_historial.configure(bg="#0284C7", fg="white")
            self.frame_historial.pack(fill=tk.BOTH, expand=True)
            self.cargar_ordenes()

    # --- PANTALLA 1: INVENTARIO ---
    def crear_pantalla_activos(self):
        tk.Label(self.frame_activos, text="Inventario General de Maquinarias", font=("Segoe UI", 18, "bold"), bg=self.BG_DARK, fg=self.TEXT_COLOR).pack(anchor="w", pady=(0, 15))

        card_form = tk.Frame(self.frame_activos, bg=self.CARD_BG, padx=20, pady=15)
        card_form.pack(fill=tk.X, pady=(0, 15))

        tk.Label(card_form, text="➕ Registrar Nuevo Activo", font=("Segoe UI", 11, "bold"), bg=self.CARD_BG, fg=self.CYAN_ACCENT).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        tk.Label(card_form, text="Código Interno:", font=("Segoe UI", 9, "bold"), bg=self.CARD_BG, fg=self.TEXT_MUTED).grid(row=1, column=0, sticky="w", padx=(0,5))
        self.ent_codigo = tk.Entry(card_form, bg=self.INPUT_BG, fg="white", insertbackground="white", bd=0, font=("Segoe UI", 10))
        self.ent_codigo.grid(row=1, column=1, sticky="ew", padx=(0,15), ipady=5)

        tk.Label(card_form, text="Nombre Equipo:", font=("Segoe UI", 9, "bold"), bg=self.CARD_BG, fg=self.TEXT_MUTED).grid(row=1, column=2, sticky="w", padx=(0,5))
        self.ent_nombre = tk.Entry(card_form, bg=self.INPUT_BG, fg="white", insertbackground="white", bd=0, font=("Segoe UI", 10))
        self.ent_nombre.grid(row=1, column=3, sticky="ew", ipady=5)

        tk.Label(card_form, text="Tipo Maquinaria:", font=("Segoe UI", 9, "bold"), bg=self.CARD_BG, fg=self.TEXT_MUTED).grid(row=2, column=0, sticky="w", padx=(0,5), pady=(10,0))
        self.cmb_tipo = ttk.Combobox(card_form, values=["Extrusora", "Inyectora", "Compresor", "Caldera", "Cinta Transportadora", "Montacargas"], state="readonly")
        self.cmb_tipo.grid(row=2, column=1, sticky="ew", padx=(0,15), pady=(10,0), ipady=3)

        tk.Label(card_form, text="Ubicación Planta:", font=("Segoe UI", 9, "bold"), bg=self.CARD_BG, fg=self.TEXT_MUTED).grid(row=2, column=2, sticky="w", padx=(0,5), pady=(10,0))
        self.ent_ubicacion = tk.Entry(card_form, bg=self.INPUT_BG, fg="white", insertbackground="white", bd=0, font=("Segoe UI", 10))
        self.ent_ubicacion.grid(row=2, column=3, sticky="ew", pady=(10,0), ipady=5)

        card_form.columnconfigure(1, weight=1)
        card_form.columnconfigure(3, weight=1)

        btn_guardar = tk.Button(card_form, text=" Guardar Equipo ", bg=self.GREEN_SUCCESS, fg="white", font=("Segoe UI", 9, "bold"),
                                bd=0, cursor="hand2", padx=18, pady=7, command=self.guardar_activo)
        btn_guardar.grid(row=3, column=3, sticky="e", pady=(12,0))

        # Tabla Activos
        frame_tabla = tk.Frame(self.frame_activos, bg=self.CARD_BG)
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        self.tabla = ttk.Treeview(frame_tabla, columns=("ID", "Código", "Nombre", "Tipo", "Ubicación", "Estado"), show="headings")
        for col in ("ID", "Código", "Nombre", "Tipo", "Ubicación", "Estado"):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120, anchor=tk.CENTER)
        self.tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # --- PANTALLA 2: REPORTAR FALLA ---
    def crear_pantalla_reportes(self):
        tk.Label(self.frame_reportes, text="Generar Orden de Trabajo (OT)", font=("Segoe UI", 18, "bold"), bg=self.BG_DARK, fg=self.TEXT_COLOR).pack(anchor="w", pady=(0, 15))

        card = tk.Frame(self.frame_reportes, bg=self.CARD_BG, padx=25, pady=25)
        card.pack(fill=tk.BOTH, expand=True)

        tk.Label(card, text="⚠️ Reportar Anomalía o Solicitud de Mantención", font=("Segoe UI", 12, "bold"), bg=self.CARD_BG, fg=self.RED_ALERT).pack(anchor="w", pady=(0, 15))

        tk.Label(card, text="Código del Activo (ej. EXT-001):", font=("Segoe UI", 10, "bold"), bg=self.CARD_BG, fg=self.TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.ent_rep_codigo = tk.Entry(card, bg=self.INPUT_BG, fg="white", insertbackground="white", bd=0, font=("Segoe UI", 10), width=35)
        self.ent_rep_codigo.pack(anchor="w", pady=(0, 12), ipady=6)

        tk.Label(card, text="Tipo de Mantención:", font=("Segoe UI", 10, "bold"), bg=self.CARD_BG, fg=self.TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.cmb_rep_tipo = ttk.Combobox(card, values=["Correctiva (Falla Urgente)", "Preventiva Planificada"], state="readonly", width=33)
        self.cmb_rep_tipo.set("Correctiva (Falla Urgente)")
        self.cmb_rep_tipo.pack(anchor="w", pady=(0, 12), ipady=3)

        tk.Label(card, text="Descripción del Problema:", font=("Segoe UI", 10, "bold"), bg=self.CARD_BG, fg=self.TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.txt_desc = tk.Text(card, bg=self.INPUT_BG, fg="white", insertbackground="white", bd=0, font=("Segoe UI", 10), width=60, height=5)
        self.txt_desc.pack(anchor="w", pady=(0, 20))

        btn_reportar = tk.Button(card, text=" 🚀 EMITIR ORDEN DE TRABAJO ", bg=self.RED_ALERT, fg="white", font=("Segoe UI", 10, "bold"),
                                 bd=0, cursor="hand2", padx=25, pady=10, command=self.guardar_reporte)
        btn_reportar.pack(anchor="w")

    # --- PANTALLA 3: HISTORIAL Y CIERRE OT ---
    def crear_pantalla_historial(self):
        tk.Label(self.frame_historial, text="Historial de Fallas y Cierre de Órdenes", font=("Segoe UI", 18, "bold"), bg=self.BG_DARK, fg=self.TEXT_COLOR).pack(anchor="w", pady=(0, 15))

        # Tabla Órdenes
        frame_tabla_ot = tk.Frame(self.frame_historial, bg=self.CARD_BG)
        frame_tabla_ot.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        self.tabla_ot = ttk.Treeview(frame_tabla_ot, columns=("ID OT", "Activo", "Tipo", "Problema", "Fecha", "Diagnóstico / Solución", "Estado"), show="headings")
        anchos = [60, 90, 130, 180, 120, 180, 90]
        for col, ancho in zip(("ID OT", "Activo", "Tipo", "Problema", "Fecha", "Diagnóstico / Solución", "Estado"), anchos):
            self.tabla_ot.heading(col, text=col)
            self.tabla_ot.column(col, width=ancho, anchor=tk.CENTER)
        self.tabla_ot.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Panel de Cierre Técnico
        card_cierre = tk.Frame(self.frame_historial, bg=self.CARD_BG, padx=20, pady=15)
        card_cierre.pack(fill=tk.X)

        tk.Label(card_cierre, text="✅ Registrar Diagnóstico y Cerrar Orden Seleccionada", font=("Segoe UI", 11, "bold"), bg=self.CARD_BG, fg=self.AMBER_WARN).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        tk.Label(card_cierre, text="Trabajo Realizado / Repuestos:", font=("Segoe UI", 9, "bold"), bg=self.CARD_BG, fg=self.TEXT_MUTED).grid(row=1, column=0, sticky="w", padx=(0,10))
        self.ent_diagnostico = tk.Entry(card_cierre, bg=self.INPUT_BG, fg="white", insertbackground="white", bd=0, font=("Segoe UI", 10), width=50)
        self.ent_diagnostico.grid(row=1, column=1, sticky="ew", padx=(0,15), ipady=5)

        btn_cerrar_ot = tk.Button(card_cierre, text=" Cerrar OT y Habilitar Equipo ", bg=self.GREEN_SUCCESS, fg="white", font=("Segoe UI", 9, "bold"),
                                  bd=0, cursor="hand2", padx=15, pady=7, command=self.cerrar_orden)
        btn_cerrar_ot.grid(row=1, column=2)
        card_cierre.columnconfigure(1, weight=1)

    # --- LÓGICA DE DATOS ---
    def cargar_activos(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        conn = sqlite3.connect("manufacturas_andina.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activos")
        for fila in cursor.fetchall():
            self.tabla.insert("", tk.END, values=fila)
        conn.close()

    def cargar_ordenes(self):
        for row in self.tabla_ot.get_children():
            self.tabla_ot.delete(row)
        conn = sqlite3.connect("manufacturas_andina.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ordenes ORDER BY id DESC")
        for fila in cursor.fetchall():
            self.tabla_ot.insert("", tk.END, values=fila)
        conn.close()

    def guardar_activo(self):
        cod, nom, tipo, ubi = self.ent_codigo.get().strip().upper(), self.ent_nombre.get().strip(), self.cmb_tipo.get(), self.ent_ubicacion.get().strip()
        if not (cod and nom and tipo and ubi):
            messagebox.showwarning("Campos Incompletos", "Por favor completa todos los datos del activo.")
            return
        try:
            conn = sqlite3.connect("manufacturas_andina.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO activos (codigo, nombre, tipo, ubicacion, estado) VALUES (?, ?, ?, ?, 'Operativo')", (cod, nom, tipo, ubi))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", f"Equipo {cod} registrado.")
            self.cargar_activos()
            self.ent_codigo.delete(0, tk.END)
            self.ent_nombre.delete(0, tk.END)
            self.ent_ubicacion.delete(0, tk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", f"El código '{cod}' ya existe.")

    def guardar_reporte(self):
        cod = self.ent_rep_codigo.get().strip().upper()
        tipo = self.cmb_rep_tipo.get()
        desc = self.txt_desc.get("1.0", tk.END).strip()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        if not (cod and desc):
            messagebox.showwarning("Campos Incompletos", "Ingresa el código del activo y el detalle de la falla.")
            return
            
        conn = sqlite3.connect("manufacturas_andina.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM activos WHERE codigo = ?", (cod,))
        if not cursor.fetchone():
            messagebox.showerror("No Encontrado", f"No existe ningún activo con el código '{cod}'.")
            conn.close()
            return

        cursor.execute("INSERT INTO ordenes (codigo_activo, tipo, descripcion, fecha_reporte, estado) VALUES (?, ?, ?, ?, 'Pendiente')", (cod, tipo, desc, fecha))
        estado_nuevo = "Detenido por Falla" if "Correctiva" in tipo else "En Mantención"
        cursor.execute("UPDATE activos SET estado = ? WHERE codigo = ?", (estado_nuevo, cod))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Orden Creada", f"OT registrada para {cod}. Estado actualizado a '{estado_nuevo}'.")
        self.ent_rep_codigo.delete(0, tk.END)
        self.txt_desc.delete("1.0", tk.END)
        self.mostrar_pantalla("historial")

    def cerrar_orden(self):
        seleccion = self.tabla_ot.selection()
        if not seleccion:
            messagebox.showwarning("Selección Requerida", "Haz clic sobre una orden en la tabla para cerrarla.")
            return
            
        item = self.tabla_ot.item(seleccion[0])
        id_ot, cod_activo, estado_actual = item['values'][0], item['values'][1], item['values'][6]
        diagnostico = self.ent_diagnostico.get().strip()

        if estado_actual == "Completada":
            messagebox.showinfo("Aviso", "Esta orden ya fue cerrada anteriormente.")
            return
        if not diagnostico:
            messagebox.showwarning("Falta Diagnóstico", "Escribe el trabajo realizado o repuestos utilizados antes de cerrar.")
            return

        conn = sqlite3.connect("manufacturas_andina.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE ordenes SET diagnostico = ?, estado = 'Completada' WHERE id = ?", (diagnostico, id_ot))
        cursor.execute("UPDATE activos SET estado = 'Operativo' WHERE codigo = ?", (cod_activo,))
        conn.commit()
        conn.close()

        messagebox.showinfo("OT Cerrada", f"Orden #{id_ot} completada. El equipo {cod_activo} volvió a estado 'Operativo'.")
        self.ent_diagnostico.delete(0, tk.END)
        self.cargar_ordenes()

if __name__ == "__main__":
    inicializar_bd()
    root = tk.Tk()
    app = AppManufacturasAndina(root)
    root.mainloop()
