# Sistema de Gestión y Mantención de Activos Industriales (SGMA)
**Empresa:** Manufacturas Andina S.A.  
**Entrega:** Cierre Sprint 1 (Hito 2)  

## 📌 Funcionalidades del Sprint 1 Terminadas
- **Gestión Centralizada de Activos (CRUD):** Registro de equipos industriales con código único, tipo y ubicación en planta.
- **Emisión de Órdenes de Trabajo (OT):** Reporte de fallas correctivas y mantenciones preventivas con cambio automático del estado del equipo.
- **Historial y Cierre Técnico:** Seguimiento de fallas históricas, registro de diagnóstico técnico y cierre de órdenes que devuelven la maquinaria a estado operativo.

## 🗄️ Diseño de Base de Datos (Modelo Relacional)

```mermaid
erDiagram
    ROLES ||--o{ USUARIOS : tiene
    ACTIVOS ||--o{ ORDENES : registra
    ORDENES ||--o{ ORDEN_REPUESTOS : consume
    REPUESTOS ||--o{ ORDEN_REPUESTOS : utilizado_en

    ACTIVOS {
        int id PK
        string codigo UK
        string nombre
        string tipo
        string ubicacion
        string estado
    }
    ORDENES {
        int id PK
        string codigo_activo FK
        string tipo
        string descripcion
        datetime fecha_reporte
        string diagnostico
        string estado
    }
    REPUESTOS {
        int id_repuesto PK
        string codigo_bodega UK
        string nombre_repuesto
        int stock_actual
    }
