@echo off
title ManuReport - Inicialização

REM Vai até o diretório onde o .bat está localizado
cd /d %~dp0

echo Iniciando o servidor Flask...

REM Abre o navegador após pequeno delay
start "" "http://127.0.0.1:5000"

REM Inicia o app
python app.py

pause