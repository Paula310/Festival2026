# Instalación rápida (5 pasos)

Requisitos: Python 3.10+, MySQL 8 en ejecución y Git.

## 1. Descargar el proyecto y preparar Python

```bash
git clone https://github.com/Paula310/Festival2026.git
cd Festival2026
python -m venv venv
venv\Scripts\activate          # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

## 2. Crear la base de datos

En MySQL Workbench (conectado como `root`), cambiando `TuClaveAqui` por la contraseña que prefieras:

```sql
CREATE DATABASE festival_votaciones CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'festival'@'localhost' IDENTIFIED BY 'TuClaveAqui';
GRANT ALL PRIVILEGES ON festival_votaciones.* TO 'festival'@'localhost';
GRANT ALL PRIVILEGES ON test_festival_votaciones.* TO 'festival'@'localhost';
FLUSH PRIVILEGES;
```

Las tablas se crean con las migraciones y los datos de prueba (ficticios) del Festival de la Leyenda Vallenata 2026 y 2027 con el comando `cargar_datos_prueba` (paso 4).

> El archivo `database/festival_votaciones.sql` corresponde a la Entrega 2 y no incluye la tabla de votos; para la Entrega 3 se usan `migrate` y `cargar_datos_prueba`.

## 3. Indicar la contraseña (variable de entorno, nunca en el código)

PowerShell:
```powershell
$env:DB_PASSWORD='TuClaveAqui'
```
CMD: `set DB_PASSWORD=TuClaveAqui` · Linux/Mac: `export DB_PASSWORD='TuClaveAqui'`

## 4. Aplicar migraciones, crear un administrador y arrancar

```bash
python manage.py migrate                # crea las tablas, incluida la de votos
python manage.py cargar_datos_prueba    # datos ficticios del Festival Vallenato
python manage.py createsuperuser
python manage.py runserver
```

## 5. Abrir en el navegador

- Sitio público: <http://127.0.0.1:8000/>
- Administración: <http://127.0.0.1:8000/admin/>

El archivo `.sql` no contiene usuarios ni contraseñas; por eso hay que crear el administrador en el paso 4.

## Problemas frecuentes

| Mensaje | Causa |
|---|---|
| `Access denied for user 'festival'` | La contraseña de `DB_PASSWORD` no coincide con la del `CREATE USER`, o la variable se definió en otra ventana de la terminal. |
| `Unknown database 'festival_votaciones'` | Falta ejecutar el `CREATE DATABASE` del paso 2. |
| `django-admin` / `manage.py` no se reconoce | El entorno virtual no está activado (`venv\Scripts\activate`). |
| Se ve el código `{% ... %}` en el navegador | Se abrió el `.html` con doble clic; las plantillas solo funcionan a través de `runserver`. |