-- ============================================================================
-- DISEÑO DE BASE DE DATOS - SISTEMA DE GESTIÓN Y MANTENCIÓN DE ACTIVOS (SGMA)
-- Empresa: Manufacturas Andina S.A.
-- ============================================================================

-- 1. Tabla de Roles de Personal (Técnicos, Supervisores, Operadores, Bodega, Jefatura)
CREATE TABLE roles (
    id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE
);

-- 2. Tabla de Usuarios del Sistema
CREATE TABLE usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_completo VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    id_rol INTEGER NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);

-- 3. Tabla Maestra de Activos Industriales (Soluciona duplicidad e identificación)
CREATE TABLE activos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo VARCHAR(30) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    ubicacion VARCHAR(100) NOT NULL,
    estado VARCHAR(30) NOT NULL DEFAULT 'Operativo'
);

-- 4. Tabla de Órdenes de Trabajo e Historial de Intervenciones
CREATE TABLE ordenes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_activo VARCHAR(30) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_reporte DATETIME NOT NULL,
    diagnostico TEXT DEFAULT 'Pendiente de revisión',
    estado VARCHAR(30) NOT NULL DEFAULT 'Pendiente',
    FOREIGN KEY (codigo_activo) REFERENCES activos(codigo)
);

-- 5. Tabla de Bodega de Repuestos e Insumos
CREATE TABLE repuestos (
    id_repuesto INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_bodega VARCHAR(30) NOT NULL UNIQUE,
    nombre_repuesto VARCHAR(100) NOT NULL,
    stock_actual INTEGER NOT NULL DEFAULT 0
);

-- 6. Tabla Intermedia Consumo de Repuestos por Orden de Trabajo
CREATE TABLE orden_repuestos (
    id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
    id_orden INTEGER NOT NULL,
    id_repuesto INTEGER NOT NULL,
    cantidad_usada INTEGER NOT NULL,
    FOREIGN KEY (id_orden) REFERENCES ordenes(id),
    FOREIGN KEY (id_repuesto) REFERENCES repuestos(id_repuesto)
);
