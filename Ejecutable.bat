REM

set original_dir=%CD%
set venv_root_dir="C:\Users\RPARPRO03\Documents\Python\RPA_TIPIFICACIONES_ORANGE_F1\env"

cd %venv_root_dir%

call %venv_root_dir%\Scripts\activate.bat

python C:\Users\RPARPRO03\Documents\Python\RPA_TIPIFICACIONES_ORANGE_F1\src\Tipificar_Orange\main.py

cd %original_dir%

exit /B 1
