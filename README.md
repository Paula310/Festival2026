# Sistema Web de Votaciones – Festival de la Leyenda Vallenata 2027

Proyecto académico de **Desarrollo Web** (Fundación Universitaria del Área Andina) – **Entrega 3: registro de votos y control de unicidad**.

Aplicación web construida con **Python 3.12, Django 5.2 LTS (patrón MVT) y MySQL 8** (conector PyMySQL 1.2).

**Integrantes:** Paula Catalina Hincapié Huertas · Paula Andrea Cano Calvo · Jesús Daniel Vega Jiménez · Eliezer Omar Vielma Castro

**Tutor:** Deivys Morales Uribe · **NRC:** 4326-63

---

## Funcionalidades de esta entrega

| Funcionalidad | Dirección |
|---|---|
| Opciones de una votación y formulario para votar (requiere sesión) | `/votaciones/<id>/` |
| Confirmación y registro del voto (POST + CSRF) | `/votaciones/<id>/votar/` |
| Historial de participación del usuario | `/mis-votos/` |
| Panel administrativo: resultados y registro de votos (solo staff) | `/panel/votos/` |
| **API GET**: categorías con sus votaciones y opciones en JSON | `/api/categorias/` |

**Regla central:** cada usuario elige **una sola opción por categoría y edición**. Puede votar en otras categorías, pero no emitir un segundo voto en la misma, aunque tenga varios subeventos. La regla se valida en Django y además la garantiza MySQL con un índice único.

De la Entrega 2 se conservan: ediciones, categorías, votaciones y opciones en MySQL; registro, inicio y cierre de sesión; consulta pública (`/`, `/ediciones/`, `/ediciones/<año>/`, `/categorias/<id>/`). Las votaciones en **borrador** no se muestran al público.

## Modelo de datos

```
Edicion ──1:N──► Categoria ──1:N──► Votacion ──1:N──► Opcion

Voto = usuario + edicion + categoria + votacion + opcion + fecha
       UNIQUE (usuario, categoria, edicion)
```

- Una **categoría** pertenece a una edición y una **votación** (subevento) pertenece a una categoría (`PROTECT`: no se pueden borrar si tienen datos asociados).
- Las **opciones** pertenecen a una votación (`CASCADE`).
- Cada **voto** guarda quién votó, en qué edición, categoría, votación y por cuál opción. Todas sus relaciones son `PROTECT`, para conservar la trazabilidad.
- La restricción `un_voto_por_usuario_categoria_edicion` impide en la base de datos un segundo voto del mismo usuario en la misma categoría y edición.

## Requisitos

- Python 3.12
- MySQL Server 8 (8.0.11 o superior) y MySQL Workbench
- Git

## Instalación (Windows · Símbolo del sistema)

```
git clone https://github.com/Paula310/Festival2026.git
cd Festival2026
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Base de datos MySQL (sin secretos)

En MySQL Workbench, conectado como `root`, cambiando `CLAVE_SEGURA` por una contraseña propia:

```sql
CREATE DATABASE festival_votaciones CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'festival'@'localhost' IDENTIFIED BY 'CLAVE_SEGURA';
GRANT ALL PRIVILEGES ON festival_votaciones.* TO 'festival'@'localhost';
GRANT ALL PRIVILEGES ON test_festival_votaciones.* TO 'festival'@'localhost';  -- base temporal de pruebas
FLUSH PRIVILEGES;
```

Las credenciales se leen de **variables de entorno** (nunca se escriben en el código). En cada terminal nueva:

```
set "DB_PASSWORD=CLAVE_SEGURA"
cls
```

Variables disponibles (ver `.env.example`): `DB_NAME` (por defecto `festival_votaciones`), `DB_USER` (`festival`), `DB_PASSWORD`, `DB_HOST` (`127.0.0.1`), `DB_PORT` (`3306`), `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`.

## Migraciones, datos de prueba y ejecución

```
python manage.py migrate
python manage.py cargar_datos_prueba
python manage.py createsuperuser
python manage.py runserver
```

Abrir <http://127.0.0.1:8000/>.

`cargar_datos_prueba` crea datos **ficticios** del Festival de la Leyenda Vallenata, coherentes con la Entrega 1:

- **Edición 2027** (60.° Festival · Rey de Reyes, del 28 de abril al 1 de mayo de 2027): activa, con votaciones **abiertas**.
- **Edición 2026**: anterior, con votaciones **cerradas** (sirve para probar una categoría no habilitada).
- Categorías: Acordeón Profesional (con dos subeventos: ronda clasificatoria y gran final), Acordeoneras Mayor, Canción Vallenata Inédita, Piquería Mayor y Piloneras Mayores.

Para borrar todo (incluidos los votos) y volver a crear los datos: `python manage.py cargar_datos_prueba --limpiar`.

## Rutas principales

| Ruta | Descripción | Acceso |
|---|---|---|
| `/` · `/ediciones/` · `/ediciones/<año>/` · `/categorias/<id>/` | Consulta pública de ediciones y categorías | Público |
| `/votaciones/<id>/` | Opciones de una votación y formulario para votar | Público (votar exige sesión) |
| `/votaciones/<id>/votar/` | Confirmación y registro del voto (POST + CSRF) | Usuario autenticado |
| `/mis-votos/` | Categorías en las que el usuario ya votó | Usuario autenticado |
| `/panel/votos/` | Resultados por votación y registro de todos los votos | Administrador (`is_staff`) |
| **`/api/categorias/`** | **API GET**: categorías con sus votaciones y opciones en JSON. Filtro opcional `?edicion=2026` | Público, solo GET |
| `/cuentas/registro/` · `/cuentas/login/` · `/cuentas/logout/` | Autenticación | — |
| `/admin/` | Django Admin, solo para verificación interna | Administrador |

## Dónde está cada parte

| Elemento | Archivo |
|---|---|
| Modelo `Voto` y restricción de unicidad en la base de datos (`un_voto_por_usuario_categoria_edicion`) | `votaciones/models.py` |
| Reglas del voto: sesión, votación habilitada, opción válida, un voto por categoría e integridad ante duplicados y concurrencia | `votaciones/servicios.py` |
| Vistas de votar, mis votos, panel administrativo y API | `votaciones/views.py` |
| Rutas | `votaciones/urls.py` |
| Migración del modelo de votos | `votaciones/migrations/0003_remove_votacion_votos_por_usuario_voto.py` |
| Plantillas | `templates/votaciones/` |
| Prueba de concurrencia contra MySQL | `votaciones/management/commands/probar_concurrencia.py` |
| Pruebas automáticas | `votaciones/tests.py` |

## Pruebas

```
python manage.py test
```

Las pruebas funcionales de la Entrega 3 están en la clase `VotosTests` de `votaciones/tests.py`:

| Caso | Prueba automática |
|---|---|
| CP-01 Voto válido | `test_cp01_voto_valido_se_registra` |
| CP-02 Segundo voto en la misma categoría (otra opción u otro subevento) | `test_cp02_segundo_voto_misma_categoria_se_rechaza` |
| CP-03 Voto en otra categoría | `test_cp03_voto_en_otra_categoria_se_permite` |
| CP-04 Usuario sin sesión | `test_cp04_sin_sesion_se_exige_autenticacion` |
| CP-05 Categoría no habilitada | `test_cp05_categoria_no_habilitada_se_rechaza` |
| CP-06 Opción de otra categoría | `test_cp06_opcion_de_otra_categoria_se_rechaza` |
| CP-07 Mis votos | `test_cp07_mis_votos_muestra_mis_registros` |
| CP-08 Consulta administrativa | `test_cp08_administrador_consulta_los_votos` |
| CP-09 Solicitudes simultáneas | `test_cp09_dos_solicitudes_simultaneas_dejan_un_solo_voto` y `test_cp09_la_base_de_datos_impide_el_duplicado` |
| CP-10 API GET | `test_cp10_api_categorias_devuelve_json` |

Prueba de concurrencia real contra MySQL (dos hilos votan al mismo tiempo; debe quedar un solo voto):

```
python manage.py probar_concurrencia
```

## Seguridad

- Sin contraseñas ni claves en el código: se leen de variables de entorno. El archivo `.env` real no se sube (`.gitignore`).
- Formularios con método POST y protección CSRF; el cierre de sesión es por POST.
- Contraseñas de usuarios guardadas con hash.
- Las relaciones usan `PROTECT` para no perder datos (no se puede borrar una edición, categoría u opción con información asociada).
- Las votaciones en borrador no se muestran al público y responden 404 si se escribe su dirección.
