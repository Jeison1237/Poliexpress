@echo off
echo ===============================
echo  Configurando Poliexpress...
echo ===============================

:: Verificar si Python está instalado
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Python no está instalado. Instálalo y vuelve a ejecutar este script.
    exit /b
)

:: Crear entorno virtual
echo Creando entorno virtual...
python -m venv venv

:: Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate

:: Instalar dependencias
echo Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

:: Realizar migraciones
echo Ejecutando migraciones de la base de datos...
python manage.py migrate

:: Ejecutar servidor de desarrollo
echo Iniciando servidor de desarrollo...
python manage.py runserver

echo ===============================
echo  Configuración completada.
echo  Accede a http://127.0.0.1:8000
echo ===============================
pause
