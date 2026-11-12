import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# --- BASE DE DATOS LOCAL ---
def inicializar_bd():
    conn = sqlite3.connect("manufacturas_andina.db")
    cursor = conn.cursor()
    
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
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ordenes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_activo TEXT NOT NULL,
            tipo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            estado TEXT NOT NULL
        )
    ''')
    
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
    conn.commit()
    conn.close()

# --- APLICACIÓN MODERNA PREMIUM (DARK MODE SAAST) ---
class AppManufacturasAndina:
    def __init__(self, root):
        self.root = root
        self.root.title("Manufacturas Andina S.A. | SGMA Enterprise")
        self.root.geometry("980x640")
        self.root.configure(bg="#0F172A") # Dark Slate Deep

        # Paleta de Colores Ultra Moderna
        self.BG_DARK = "#0F172A"
        self.SIDEBAR_BG = "#1E293B"
        self.CARD_BG = "#1E293B"
        self.INPUT_BG = "#334155"
        self.TEXT_COLOR = "#F8FAFC"
        self.TEXT_MUTED = "#94A3B8"
        self.CYAN_ACCENT = "#38BDF8"
        self.GREEN_SUCCESS = "#22C55E"
        self.RED_ALERT = "#EF4444"

        self.configurar_estilos()

        # Layout Principal (Sidebar + Área de Contenido)
        self.sidebar = tk.Frame(self.root, bg=self.SIDEBAR_BG, width=240)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.main_area = tk.Frame(self.root, bg=self.BG_DARK)
        self.main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Construir Interfaz
        self.crear_sidebar()

        # Pantallas
        self.frame_activos = tk.Frame(self.main_area, bg=self.BG_DARK)
        self.frame_reportes = tk.Frame(self.main_area, bg=self.BG_DARK)

        self.crear_pantalla_activos()
        self.crear_pantalla_reportes()

        # Pantalla Inicial
        self.mostrar_pantalla("activos")
        self.cargar_activos()

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Estilo de Tabla Oscura Neón
        style.configure("Treeview", 
                        font=("Segoe UI", 10),
                        rowheight=32,
                        background="#1E293B",
                        fieldbackground="#1E293B",
                        foreground="#F8FAFC",
                        borderwidth=0)
        style.configure("Treeview.Heading", 
                        font=("Segoe UI", 10, "bold"),
                        background="#334155",
                        foreground="#38BDF8",
                        relief="flat")
        style.map("Treeview", 
                  background=[("selected", "#0284C7")], 
                  foreground=[("selected", "#FFFFFF")])

    def crear_sidebar(self):
        # Header / Logo Marca
        lbl_brand = tk.Label(self.sidebar, text="⚡ ANDINA S.A.", font=("Segoe UI", 18, "bold"), 
                             bg=self.SIDEBAR_BG, fg=self.CYAN_ACCENT)
        lbl_brand.pack(pady=(30, 2))
        
        lbl_sub = tk.Label(self.sidebar, text="Gestión & Mantención Activos", font=("Segoe UI", 9), 
                           bg=self.SIDEBAR_BG, fg=self.TEXT_MUTED)
        lbl_sub.pack(pady=(0, 30))

        # Botones de Navegación Estilizados
        self.btn_nav_activos = tk.Button(self.sidebar, text="  📊  Inventario Activos", font=("Segoe UI", 11, "bold"),
                                         bg="#0284C7", fg="white", activebackground="#0284C7",
                                         activeforeground="white", bd=0, relief="flat", anchor="w", padx=20, pady=12,
                                         cursor="hand2", command=lambda: self.mostrar_pantalla("activos"))
        self.btn_nav_activos.pack(fill=tk.X, padx=15, pady=6)

        self.btn_nav_reportes = tk.Button(self.sidebar, text="  🛠️  Reportar Falla / OT", font=("Segoe UI", 11, "bold"),
                                          bg="#334155", fg=self.TEXT_MUTED, activebackground="#0284C7",
                                          activeforeground="white", bd=0, relief="flat", anchor="w", padx=20, pady=12,
                                          cursor="hand2", command=lambda: self.mostrar_pantalla("reportes"))
        self.btn_nav_reportes.pack(fill=tk.X, padx=15, pady=6)

        # Widget Informativo en Sidebar
        card_info = tk.Frame(self.sidebar, bg="#334155", padx=15, pady=15)
        card_info.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=20)
        
        lbl_info_title = tk.Label(card_info, text="Estado Planta", font=("Segoe UI", 9, "bold"), bg="#334155", fg=self.CYAN_ACCENT)
        lbl_info_title.pack(anchor="w")
        
        lbl_info_desc = tk.Label(card_info, text="● Sistema en Línea\n● Conexión DB Activa", font=("Segoe UI", 8), bg="#334155", fg=self.TEXT_COLOR, justify="left")
        lbl_info_desc.pack(anchor="w", pady=(5,0))

    def mostrar_pantalla(self, pantalla):
        self.frame_activos.pack_forget()
        self.frame_reportes.pack_forget()

        if pantalla == "activos":
            self.btn_nav_activos.configure(bg="#0284C7", fg="white")
            self.btn_nav_reportes.configure(bg="#334155", fg=self.TEXT_MUTED)
            self.frame_activos.pack(fill=tk.BOTH, expand=True)
        else:
            self.btn_nav_reportes.configure(bg="#0284C7", fg="white")
            self.btn_nav_activos.configure(bg="#334155", fg=self.TEXT_MUTED)
            self.frame_reportes.pack(fill=tk.BOTH, expand=True)

    def crear_pantalla_activos(self):
        # Título
        lbl_titulo = tk.Label(self.frame_activos, text="Control General de Maquinarias", 
                              font=("Segoe UI", 18, "bold"), bg=self.BG_DARK, fg=self.TEXT_COLOR)
        lbl_titulo.pack(anchor="w", pady=(0, 15))

        # Card de Formulario
        card_form = tk.Frame(self.frame_activos, bg=self.CARD_BG, padx=20, pady=15)
        card_form.pack(fill=tk.X, pady=(0, 20))

        lbl_form = tk.Label(card_form, text="➕ Registrar Nuevo Activo Industrial", font=("Segoe UI", 12, "bold"), bg=self.CARD_BG, fg=self.CYAN_ACCENT)
        lbl_form.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 15))

        # Campos
        tk.Label(card_form, text="Código Interno:", font=("Segoe UI", 9, "bold"), bg=self.CARD_BG, fg=self.TEXT_MUTED).grid(row=1, column=0, sticky="w", padx=(0,5))
        self.ent_codigo = tk.Entry(card_form, bg=self.INPUT_BG, fg="white", insertbackground="white", bd=0, relief="flat", font=("Segoe UI", 10))
        self.ent_codigo.grid(row=1, column=1, sticky="ew", padx=(0,15), ipady=5)

        tk.Label(card_form, text="Nombre Equipo:", font=("Segoe UI", 9, "bold"), bg=self.CARD_BG, fg=self.TEXT_MUTED).grid(row=1, column=2, sticky="w", padx=(0,5))
        self.ent_nombre = tk.Entry(card_form, bg=self.INPUT_BG, fg="white", insertbackground="white", bd=0, relief="flat", font=("Segoe UI", 10))
        self.ent_nombre.grid(row=1, column=3, sticky="ew", ipady=5)

        tk.Label(card_form, text="Tipo Maquinaria:", font=("Segoe UI", 9, "bold"), bg=self.CARD_BG, fg=self.TEXT_MUTED).grid(row=2, column=0, sticky="w", padx=(0,5), pady=(12,0))
        self.cmb_tipo = ttk.Combobox(card_form, values=["Extrusora", "Inyectora", "Compresor", "Caldera", "Cinta Transportadora"], state="readonly")
        self.cmb_tipo.grid(row=2, column=1, sticky="ew", padx=(0,15), pady=(12,0), ipady=3)

        tk.Label(card_form, text="Ubicación Planta:", font=("Segoe UI", 9, "bold"), bg=self.CARD_BG, fg=self.TEXT_MUTED).grid(row=2, column=2, sticky="w", padx=(0,5), pady=(12,0))
        self.ent_ubicacion = tk.Entry(card_form, bg=self.INPUT_BG, fg="white", insertbackground="white", bd=0, relief="flat", font=("Segoe UI", 10))
        self.ent_ubicacion.grid(row=2, column=3, sticky="ew", pady=(12,0), ipady=5)

        card_form.columnconfigure(1, weight=1)
        card_form.columnconfigure(3, weight=1)

        btn_guardar = tk.Button(card_form, text=" Guardar Equipo ", bg=self.GREEN_SUCCESS, fg="white", font=("Segoe UI", 10, "bold"),
                                bd=0, relief="flat", cursor="hand2", padx=20, pady=8, activebackground="#16A34A", activeforeground="white",
                                command=self.guardar_activo)
        btn_guardar.grid(row=3, column=3, sticky="e", pady=(15,0))

        # Tabla de Visualización
        frame_tabla = tk.Frame(self.frame_activos, bg=self.CARD_BG)
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        self.tabla = ttk.Treeview(frame_tabla, columns=("ID", "Código", "Nombre", "Tipo", "Ubicación", "Estado"), show="headings")
        for col in ("ID", "Código", "Nombre", "Tipo", "Ubicación", "Estado"):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120, anchor=tk.CENTER)
        
        self.tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def crear_pantalla_reportes(self):
        lbl_titulo = tk.Label(self.frame_reportes, text="Centro de Solicitudes y Mantención", 
                              font=("Segoe UI", 18, "bold"), bg=self.BG_DARK, fg=self.TEXT_COLOR)
        lbl_titulo.pack(anchor="w", pady=(0, 15))

        card = tk.Frame(self.frame_reportes, bg=self.CARD_BG, padx=25, pady=25)
        card.pack(fill=tk.BOTH, expand=True)

        lbl_sec = tk.Label(card, text="⚠️ Generar Orden de Trabajo por Falla", font=("Segoe UI", 13, "bold"), bg=self.CARD_BG, fg=self.RED_ALERT)
        lbl_sec.pack(anchor="w", pady=(0, 15))

        tk.Label(card, text="Código del Activo:", font=("Segoe UI", 10, "bold"), bg=self.CARD_BG, fg=self.TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.ent_rep_codigo = tk.Entry(card, bg=self.INPUT_BG, fg="white", insertbackground="white", bd=0, relief="flat", font=("Segoe UI", 10), width=35)
        self.ent_rep_codigo.pack(anchor="w", pady=(0, 12), ipady=6)

        tk.Label(card, text="Tipo de Mantención:", font=("Segoe UI", 10, "bold"), bg=self.CARD_BG, fg=self.TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.cmb_rep_tipo = ttk.Combobox(card, values=["Correctiva (Falla Urgente)", "Preventiva Planificada"], state="readonly", width=33)
        self.cmb_rep_tipo.set("Correctiva (Falla Urgente)")
        self.cmb_rep_tipo.pack(anchor="w", pady=(0, 12), ipady=3)

        tk.Label(card, text="Descripción del Problema u Observación:", font=("Segoe UI", 10, "bold"), bg=self.CARD_BG, fg=self.TEXT_MUTED).pack(anchor="w", pady=(5, 2))
        self.txt_desc = tk.Text(card, bg=self.INPUT_BG, fg="white", insertbackground="white", bd=0, relief="flat", font=("Segoe UI", 10), width=55, height=5)
        self.txt_desc.pack(anchor="w", pady=(0, 20))

        btn_reportar = tk.Button(card, text=" 🚀 EMITIR ORDEN DE TRABAJO ", bg=self.RED_ALERT, fg="white", font=("Segoe UI", 10, "bold"),
                                 bd=0, relief="flat", cursor="hand2", padx=25, pady=10, activebackground="#DC2626", activeforeground="white",
                                 command=self.guardar_reporte)
        btn_reportar.pack(anchor="w")

    def cargar_activos(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        conn = sqlite3.connect("manufacturas_andina.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activos")
        for fila in cursor.fetchall():
            self.tabla.insert("", tk.END, values=fila)
        conn.close()

    def guardar_activo(self):
        cod, nom, tipo, ubi = self.ent_codigo.get(), self.ent_nombre.get(), self.cmb_tipo.get(), self.ent_ubicacion.get()
        if not (cod and nom and tipo and ubi):
            messagebox.showwarning("Campos Incompletos", "Por favor completa todos los datos requeridos.")
            return
        
        try:
            conn = sqlite3.connect("manufacturas_andina.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO activos (codigo, nombre, tipo, ubicacion, estado) VALUES (?, ?, ?, ?, 'Operativo')",
                           (cod, nom, tipo, ubi))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", f"El equipo {cod} fue registrado correctamente.")
            self.cargar_activos()
            self.ent_codigo.delete(0, tk.END)
            self.ent_nombre.delete(0, tk.END)
            self.ent_ubicacion.delete(0, tk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error de Duplicidad", f"El código '{cod}' ya existe en la base de datos.")

    def guardar_reporte(self):
        cod = self.ent_rep_codigo.get()
        tipo = self.cmb_rep_tipo.get()
        desc = self.txt_desc.get("1.0", tk.END).strip()
        
        if not (cod and desc):
            messagebox.showwarning("Campos Incompletos", "Por favor indica el código del activo y la descripción de la falla.")
            return
            
        conn = sqlite3.connect("manufacturas_andina.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ordenes (codigo_activo, tipo, descripcion, estado) VALUES (?, ?, ?, 'Pendiente')",
                       (cod, tipo, desc))
        cursor.execute("UPDATE activos SET estado = 'Detenido por Falla' WHERE codigo = ?", (cod,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Orden Creada", f"Se ha emitido la orden de trabajo para el equipo {cod}.\nEstado actualizado a 'Detenido por Falla'.")
        self.cargar_activos()
        self.ent_rep_codigo.delete(0, tk.END)
        self.txt_desc.delete("1.0", tk.END)

if __name__ == "__main__":
    inicializar_bd()
    root = tk.Tk()
    app = AppManufacturasAndina(root)
    root.mainloop()