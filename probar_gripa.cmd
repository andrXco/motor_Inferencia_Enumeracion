@echo off
python "%~dp0main.py" --estructura "%~dp0relaciones_gripa_compleja.txt" --tablas "%~dp0tabla_gripa_compleja.txt" --consulta Gripa --evidencia Congestion=yes Fiebre=yes
exit /b %errorlevel%
