# Festival de Votaciones — Entrega 2

Aplicación web en **Python + Django (patrón MVT) + MySQL** para gestionar las ediciones anuales de un festival,
sus categorías, votaciones y opciones participantes, con autenticación de usuarios.

```
EDICIÓN → CATEGORÍA → VOTACIÓN → OPCIÓN
```

> **¿Prisa?** Sigue [INSTALACION_RAPIDA.md](INSTALACION_RAPIDA.md): la base de datos con datos de prueba se carga con un solo archivo (`database/festival_votaciones.sql`).

## Requisitos

- Python 3.10 o superior
- MySQL 8 (o MariaDB 10.6+) en ejecución
- Git

## Instalación

```bash
# 1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd festival

# 2. Crear y activar el entorno virtual
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

## Base de datos MySQL

Entra a MySQL como administrador y crea la base de datos y el usuario:

```sql
CREATE DATABASE festival_votaciones CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'festival'@'localhost' IDENTIFIED BY 'cambia_esta_clave';
GRANT ALL PRIVILEGES ON festival_votaciones.* TO 'festival'@'localhost';
GRANT ALL PRIVILEGES ON test_festival_votaciones.* TO 'festival'@'localhost';  -- para las pruebas
FLUSH PRIVILEGES;
```

Configura las credenciales con variables de entorno (ver `.env.example`; **nunca subas el `.env`**):

```bash
export DB_NAME=festival_votaciones
export DB_USER=festival
export DB_PASSWORD=cambia_esta_clave
export DB_HOST=127.0.0.1
export DB_PORT=3306
# Windows (PowerShell): $env:DB_PASSWORD="cambia_esta_clave"
```

## Ejecución

```bash
python manage.py migrate                 # crea las tablas en MySQL
python manage.py cargar_datos_prueba     # ediciones, categorías, votaciones y opciones de ejemplo
python manage.py createsuperuser         # usuario para entrar a /admin/
python manage.py runserver
```

Abre <http://127.0.0.1:8000/>.

| Ruta | Descripción |
|---|---|
| `/` | Inicio: edición destacada y listado de ediciones |
| `/ediciones/` | Tabla de ediciones |
| `/ediciones/<año>/` | Categorías de una edición |
| `/categorias/<id>/` | Votaciones de una categoría |
| `/votaciones/<id>/` | Opciones participantes |
| `/cuentas/registro/` · `/cuentas/login/` · `/cuentas/logout/` | Autenticación |
| `/admin/` | Django Admin (CRUD de ediciones, categorías, votaciones y opciones) |

## Pruebas

```bash
python manage.py test
```

## Estructura

```
config/        configuración del proyecto (settings, urls)
cuentas/       registro, inicio y cierre de sesión (django.contrib.auth)
votaciones/    modelos, admin, vistas, rutas y comando de datos de prueba
templates/     plantillas base, públicas y de autenticación
static/css/    estilos
```

## Alcance de esta entrega

Incluye: proyecto Django, MySQL, modelos relacionados, migraciones, autenticación, administración vía Django Admin
y visualización dinámica. **No incluye** (siguientes entregas): registro de votos, control de duplicados,
reglas de elegibilidad y publicación de resultados.
