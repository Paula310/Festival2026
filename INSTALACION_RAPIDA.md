# Instalación rápida (5 pasos)

Requisitos: Python 3.10+, MySQL 8 en ejecución y Git.

## 1. Descargar el proyecto y preparar Python

```bash
git clone <URL_DEL_REPOSITORIO>
cd festival
python -m venv venv
venv\Scripts\activate          # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

## 2. Crear la base de datos con datos de prueba

Entra a MySQL (`mysql -u root -p`) y ejecuta, cambiando `TuClaveAqui` por la contraseña que prefieras:

```sql
CREATE DATABASE festival_votaciones CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'festival'@'localhost' IDENTIFIED BY 'TuClaveAqui';
GRANT ALL PRIVILEGES ON festival_votaciones.* TO 'festival'@'localhost';
GRANT ALL PRIVILEGES ON test_festival_votaciones.* TO 'festival'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Carga la estructura y los datos de prueba (ediciones 2025 y 2026, categorías, votaciones y opciones):

```bash
mysql -u root -p festival_votaciones < database/festival_votaciones.sql
```

> Alternativa sin el archivo `.sql`: `python manage.py migrate` y luego `python manage.py cargar_datos_prueba`.
> En MySQL Workbench también puedes usar *File → Open SQL Script* sobre `database/festival_votaciones.sql` y ejecutarlo con la base `festival_votaciones` seleccionada.

## 3. Indicar la contraseña (variable de entorno, nunca en el código)

PowerShell:
```powershell
$env:DB_PASSWORD='TuClaveAqui'
```
CMD: `set DB_PASSWORD=TuClaveAqui` · Linux/Mac: `export DB_PASSWORD='TuClaveAqui'`

## 4. Crear un administrador y arrancar

```bash
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
