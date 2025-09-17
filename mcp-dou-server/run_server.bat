@echo off
REM Script para executar o servidor MCP DOU no ambiente pandas-course
REM 
REM Este script garante que o servidor seja executado no diretório correto

echo Iniciando servidor MCP DOU...
echo Ambiente: pandas-course
echo Python: C:\Users\94512868372\Anaconda3\envs\pandas-course\python.exe

cd /d "d:\Git_Projects\MCP\mcp-dou-server"
C:\Users\94512868372\Anaconda3\envs\pandas-course\python.exe run_server_standalone.py

pause