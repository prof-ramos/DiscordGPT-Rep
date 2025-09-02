#!/usr/bin/env python3
"""
Discord ChatGPT Bot - Admin Panel Launcher
Script para iniciar o painel administrativo do bot Discord.

Uso:
    python start_admin.py
    python3 start_admin.py

O painel será aberto automaticamente no navegador em:
http://localhost:8501

Requisitos:
- Streamlit instalado (pip install streamlit)
- Bot Discord configurado (arquivo .env)

Autor: Prof. Ramos
GitHub: https://github.com/prof-ramos/DiscordGPT
"""

import os
import sys
import subprocess
import webbrowser
import time
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_requirements():
    """Verifica se as dependências estão instaladas"""
    logger.info("🔍 Verificando dependências...")
    
    try:
        import streamlit
        import psutil
        import pandas
        logger.info("✅ Todas as dependências estão instaladas")
        return True
    except ImportError as e:
        logger.error(f"❌ Dependência faltando: {e}")
        logger.info("💡 Execute: pip install -r requirements.txt")
        return False

def check_bot_config():
    """Verifica se o bot está configurado"""
    logger.info("⚙️ Verificando configuração do bot...")
    
    env_file = Path(".env")
    if not env_file.exists():
        logger.warning("⚠️ Arquivo .env não encontrado")
        logger.info("💡 Copie .env.example para .env e configure as variáveis")
        return False
    
    # Verificar se há pelo menos o token do Discord
    with open(env_file, 'r') as f:
        content = f.read()
        if 'DISCORD_BOT_TOKEN=' in content and len(content.split('DISCORD_BOT_TOKEN=')[1].split('\n')[0].strip()) > 20:
            logger.info("✅ Configuração básica encontrada")
            return True
        else:
            logger.warning("⚠️ Token do Discord não configurado em .env")
            return False

def start_admin_panel():
    """Inicia o painel administrativo"""
    logger.info("🚀 Iniciando painel administrativo...")
    
    # Verificar se o arquivo admin_panel.py existe
    admin_file = Path("admin_panel.py")
    if not admin_file.exists():
        logger.error("❌ Arquivo admin_panel.py não encontrado!")
        return False
    
    try:
        # Comando para iniciar Streamlit
        cmd = [sys.executable, "-m", "streamlit", "run", "admin_panel.py", "--server.port", "8501"]
        
        logger.info("🌐 Iniciando servidor Streamlit na porta 8501...")
        
        # Iniciar processo em background
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Aguardar um pouco para o servidor iniciar
        time.sleep(3)
        
        # Abrir no navegador
        url = "http://localhost:8501"
        logger.info(f"🔗 Abrindo painel em: {url}")
        webbrowser.open(url)
        
        # Mostrar output do processo
        logger.info("✅ Painel administrativo iniciado com sucesso!")
        logger.info("📊 Para parar o painel, pressione Ctrl+C")
        
        try:
            # Aguardar o processo
            process.wait()
        except KeyboardInterrupt:
            logger.info("⏹️ Parando painel administrativo...")
            process.terminate()
            process.wait()
            
        return True
        
    except FileNotFoundError:
        logger.error("❌ Streamlit não encontrado!")
        logger.info("💡 Execute: pip install streamlit")
        return False
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar painel: {e}")
        return False

def main():
    """Função principal"""
    print("""
╔════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                        ║
║    ██████╗██╗  ██╗ █████╗ ████████╗ ██████╗ ██████╗ ████████╗    ██████╗  ██████╗ ████████╗  ║
║   ██╔════╝██║  ██║██╔══██╗╚══██╔══╝██╔════╝ ██╔══██╗╚══██╔══╝    ██╔══██╗██╔═══██╗╚══██╔══╝  ║
║   ██║     ███████║███████║   ██║   ██║  ███╗██████╔╝   ██║       ██████╔╝██║   ██║   ██║     ║
║   ██║     ██╔══██║██╔══██║   ██║   ██║   ██║██╔═══╝    ██║       ██╔══██╗██║   ██║   ██║     ║
║   ╚██████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║        ██║       ██████╔╝╚██████╔╝   ██║     ║
║    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝        ╚═╝       ╚═════╝  ╚═════╝    ╚═╝     ║
║                                                                                        ║
║                          🚀 ADMIN PANEL LAUNCHER 🚀                                   ║
║                       Desenvolvido por Prof. Ramos                                     ║
╚════════════════════════════════════════════════════════════════════════════════════════╝
    """)
    
    logger.info("🎯 Iniciando launcher do painel administrativo...")
    
    # Verificações pré-execução
    if not check_requirements():
        logger.error("❌ Falha na verificação de dependências")
        sys.exit(1)
    
    if not check_bot_config():
        logger.warning("⚠️ Bot pode não estar totalmente configurado")
        response = input("Deseja continuar mesmo assim? (s/N): ").strip().lower()
        if response not in ['s', 'sim', 'yes', 'y']:
            logger.info("👋 Operação cancelada pelo usuário")
            sys.exit(0)
    
    # Iniciar painel
    success = start_admin_panel()
    
    if success:
        logger.info("✅ Painel administrativo encerrado com sucesso")
        sys.exit(0)
    else:
        logger.error("❌ Falha ao iniciar painel administrativo")
        sys.exit(1)

if __name__ == "__main__":
    main()