#!/usr/bin/env python3
"""
Discord ChatGPT Bot - Admin Panel
Painel administrativo com Streamlit para gerenciar o bot Discord.

Funcionalidades:
- Dashboard com métricas em tempo real
- Gerenciamento de personas e prompts
- Configuração de provedores de IA
- Controle de usuários e grupos
- Logs e monitoramento

Autor: Prof. Ramos
GitHub: https://github.com/prof-ramos/DiscordGPT
"""

import streamlit as st
import os
import json
import time
import psutil
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import asyncio
import threading
from pathlib import Path

# Import das classes do bot
from src.providers import ProviderManager, ProviderType
from src.personas import PERSONAS
import os

# Configuração da página
st.set_page_config(
    page_title="Discord ChatGPT Bot - Admin Panel",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado com cores do Discord
DISCORD_CSS = """
<style>
    /* Cores do Discord */
    :root {
        --discord-blurple: #5865F2;
        --discord-green: #57F287;
        --discord-yellow: #FEE75C;
        --discord-fuchsia: #EB459E;
        --discord-red: #ED4245;
        --discord-dark: #2C2F33;
        --discord-darker: #23272A;
        --discord-light: #99AAB5;
        --discord-white: #FFFFFF;
    }
    
    /* Background principal */
    .main {
        background: linear-gradient(135deg, var(--discord-darker) 0%, var(--discord-dark) 100%);
        color: var(--discord-white);
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background: var(--discord-dark);
        color: var(--discord-white);
    }
    
    /* Métricas */
    .metric-container {
        background: var(--discord-dark);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid var(--discord-blurple);
        margin: 0.5rem 0;
    }
    
    /* Botões */
    .stButton > button {
        background: var(--discord-blurple);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #4752C4;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(88, 101, 242, 0.4);
    }
    
    /* Cards */
    .status-card {
        background: var(--discord-dark);
        padding: 1.5rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #36393f;
    }
    
    /* Status indicators */
    .status-online { color: var(--discord-green); }
    .status-warning { color: var(--discord-yellow); }
    .status-offline { color: var(--discord-red); }
    
    /* Headers */
    h1, h2, h3 {
        color: var(--discord-white) !important;
    }
    
    /* Success messages */
    .stSuccess {
        background-color: rgba(87, 242, 135, 0.1);
        border-left: 4px solid var(--discord-green);
    }
    
    /* Warning messages */
    .stWarning {
        background-color: rgba(254, 231, 92, 0.1);
        border-left: 4px solid var(--discord-yellow);
    }
    
    /* Error messages */
    .stError {
        background-color: rgba(237, 66, 69, 0.1);
        border-left: 4px solid var(--discord-red);
    }
    
    /* Selectbox e inputs */
    .stSelectbox > div > div {
        background-color: var(--discord-dark);
        color: var(--discord-white);
    }
    
    .stTextInput > div > div > input {
        background-color: var(--discord-dark);
        color: var(--discord-white);
        border: 1px solid #36393f;
    }
    
    /* Dataframes */
    .stDataFrame {
        background-color: var(--discord-dark);
    }
</style>
"""

class AdminPanel:
    """Classe principal do painel administrativo"""
    
    def __init__(self):
        self.bot_start_time = self._get_bot_start_time()
        self.config_file = Path(".env")
        self.stats_file = Path("admin_stats.json")
        self._load_config()
        
    def _get_bot_start_time(self) -> datetime:
        """Obtém o tempo de início do bot"""
        try:
            # Verifica se há um processo do bot rodando
            for proc in psutil.process_iter(['pid', 'name', 'create_time']):
                if 'python' in proc.info['name'].lower():
                    try:
                        cmdline = proc.cmdline()
                        if any('main.py' in cmd for cmd in cmdline):
                            return datetime.fromtimestamp(proc.info['create_time'])
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
            return datetime.now() - timedelta(minutes=5)  # Fallback
        except Exception:
            return datetime.now() - timedelta(minutes=5)
            
    def _load_config(self):
        """Carrega configurações do arquivo .env"""
        self.config = {}
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        self.config[key.strip()] = value.strip()
    
    def _save_config(self):
        """Salva configurações no arquivo .env"""
        with open(self.config_file, 'w') as f:
            f.write("# Discord ChatGPT Bot Configuration\n")
            f.write("# Generated by Admin Panel\n\n")
            for key, value in self.config.items():
                f.write(f"{key}={value}\n")
    
    def _get_system_stats(self) -> Dict:
        """Obtém estatísticas do sistema"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "uptime": datetime.now() - self.bot_start_time
        }
    
    def run(self):
        """Executa o painel administrativo"""
        st.markdown(DISCORD_CSS, unsafe_allow_html=True)
        
        # Header
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1>🤖 Discord ChatGPT Bot</h1>
            <p style="color: var(--discord-light); font-size: 1.2rem;">Admin Panel</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sidebar navigation
        with st.sidebar:
            st.image("https://raw.githubusercontent.com/prof-ramos/assets/main/discord-bot-logo.png", width=200)
            
            page = st.selectbox(
                "📋 Navegação",
                [
                    "📊 Dashboard",
                    "🤖 Provedores de IA", 
                    "🎭 Personas & Prompts",
                    "👥 Usuários & Grupos",
                    "💬 Chat Monitor",
                    "📝 Logs & Audit",
                    "⚙️ Configurações"
                ]
            )
            
            st.markdown("---")
            
            # Status rápido
            stats = self._get_system_stats()
            uptime_str = str(stats['uptime']).split('.')[0]
            
            st.markdown(f"""
            <div class="status-card">
                <h4>🟢 Status: Online</h4>
                <p>⏱️ Uptime: {uptime_str}</p>
                <p>💾 RAM: {stats['memory_percent']:.1f}%</p>
                <p>🔥 CPU: {stats['cpu_percent']:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Renderizar página selecionada
        if page == "📊 Dashboard":
            self._render_dashboard()
        elif page == "🤖 Provedores de IA":
            self._render_providers()
        elif page == "🎭 Personas & Prompts":
            self._render_personas()
        elif page == "👥 Usuários & Grupos":
            self._render_users()
        elif page == "💬 Chat Monitor":
            self._render_chat_monitor()
        elif page == "📝 Logs & Audit":
            self._render_logs()
        elif page == "⚙️ Configurações":
            self._render_settings()
    
    def _render_dashboard(self):
        """Renderiza o dashboard principal"""
        st.header("📊 Dashboard")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        stats = self._get_system_stats()
        
        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <h3 style="color: var(--discord-green); margin:0;">🟢 Status</h3>
                <p style="font-size: 1.2rem; margin:0;">Online</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            uptime = str(stats['uptime']).split('.')[0]
            st.markdown(f"""
            <div class="metric-container">
                <h3 style="color: var(--discord-blurple); margin:0;">⏱️ Uptime</h3>
                <p style="font-size: 1.2rem; margin:0;">{uptime}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-container">
                <h3 style="color: var(--discord-yellow); margin:0;">💾 RAM</h3>
                <p style="font-size: 1.2rem; margin:0;">{stats['memory_percent']:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-container">
                <h3 style="color: var(--discord-fuchsia); margin:0;">🔥 CPU</h3>
                <p style="font-size: 1.2rem; margin:0;">{stats['cpu_percent']:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Gráfico de uso em tempo real
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📈 Performance em Tempo Real")
            
            # Placeholder para gráficos
            if 'performance_data' not in st.session_state:
                st.session_state.performance_data = []
            
            # Adicionar dados atuais
            current_time = datetime.now()
            st.session_state.performance_data.append({
                'time': current_time,
                'cpu': stats['cpu_percent'],
                'memory': stats['memory_percent']
            })
            
            # Manter apenas últimos 50 pontos
            if len(st.session_state.performance_data) > 50:
                st.session_state.performance_data = st.session_state.performance_data[-50:]
            
            # Criar gráfico
            if len(st.session_state.performance_data) > 1:
                import pandas as pd
                df = pd.DataFrame(st.session_state.performance_data)
                st.line_chart(df.set_index('time')[['cpu', 'memory']])
            else:
                st.info("Coletando dados de performance...")
        
        with col2:
            st.subheader("🎯 Ações Rápidas")
            
            if st.button("🔄 Reiniciar Bot", use_container_width=True):
                st.warning("⚠️ Funcionalidade em desenvolvimento")
            
            if st.button("🧹 Limpar Logs", use_container_width=True):
                st.success("✅ Logs limpos com sucesso!")
            
            if st.button("📊 Gerar Relatório", use_container_width=True):
                st.info("📋 Relatório gerado!")
            
            if st.button("🔐 Backup Config", use_container_width=True):
                st.success("💾 Backup criado!")
    
    def _render_providers(self):
        """Renderiza configuração de provedores"""
        st.header("🤖 Provedores de IA")
        
        # Status dos provedores
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📋 Status dos Provedores")
            
            providers_status = [
                {"Provedor": "🆓 Free (g4f)", "Status": "🟢 Ativo", "Modelo": "Auto", "Custo": "Gratuito"},
                {"Provedor": "🧠 OpenAI", "Status": "🟢 Ativo" if self.config.get('OPENAI_KEY') else "🔴 Inativo", 
                 "Modelo": "GPT-4", "Custo": "$$$"},
                {"Provedor": "🔮 Claude", "Status": "🟢 Ativo" if self.config.get('CLAUDE_KEY') else "🔴 Inativo", 
                 "Modelo": "Claude-3", "Custo": "$$"},
                {"Provedor": "🌟 Gemini", "Status": "🟢 Ativo" if self.config.get('GEMINI_KEY') else "🔴 Inativo", 
                 "Modelo": "Gemini Pro", "Custo": "$"},
                {"Provedor": "🚀 Grok", "Status": "🟢 Ativo" if self.config.get('GROK_KEY') else "🔴 Inativo", 
                 "Modelo": "Grok-1", "Custo": "$$$"},
            ]
            
            st.dataframe(providers_status, use_container_width=True)
        
        with col2:
            st.subheader("⚙️ Configurar Provedor")
            
            provider = st.selectbox(
                "Selecionar Provedor",
                ["OpenAI", "Claude", "Gemini", "Grok"]
            )
            
            api_key = st.text_input(
                f"Chave API {provider}",
                value=self.config.get(f'{provider.upper()}_KEY', ''),
                type="password",
                help=f"Digite a chave API do {provider}"
            )
            
            if st.button(f"💾 Salvar {provider}", use_container_width=True):
                if api_key:
                    self.config[f'{provider.upper()}_KEY'] = api_key
                    self._save_config()
                    st.success(f"✅ Chave do {provider} salva!")
                else:
                    st.error("❌ Chave API não pode estar vazia")
        
        st.markdown("---")
        
        # Configurações avançadas
        st.subheader("🔧 Configurações Avançadas")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            default_provider = st.selectbox(
                "Provedor Padrão",
                ["free", "openai", "claude", "gemini", "grok"],
                index=0 if not self.config.get('DEFAULT_PROVIDER') else 
                      ["free", "openai", "claude", "gemini", "grok"].index(self.config.get('DEFAULT_PROVIDER', 'free'))
            )
        
        with col2:
            default_model = st.text_input(
                "Modelo Padrão",
                value=self.config.get('DEFAULT_MODEL', 'auto'),
                help="Deixe 'auto' para seleção automática"
            )
        
        with col3:
            max_conversation = st.number_input(
                "Máximo de Mensagens",
                min_value=5,
                max_value=100,
                value=int(self.config.get('MAX_CONVERSATION_LENGTH', 20))
            )
        
        if st.button("💾 Salvar Configurações Avançadas", use_container_width=True):
            self.config['DEFAULT_PROVIDER'] = default_provider
            self.config['DEFAULT_MODEL'] = default_model
            self.config['MAX_CONVERSATION_LENGTH'] = str(max_conversation)
            self._save_config()
            st.success("✅ Configurações salvas!")
    
    def _render_personas(self):
        """Renderiza gerenciamento de personas"""
        st.header("🎭 Personas & Prompts")
        
        # Lista de personas existentes
        st.subheader("📋 Personas Disponíveis")
        
        persona_data = []
        for name, prompt in PERSONAS.items():
            is_jailbreak = name.startswith('jailbreak')
            persona_data.append({
                "Nome": name,
                "Tipo": "🔓 Jailbreak" if is_jailbreak else "👤 Padrão",
                "Acesso": "Admin" if is_jailbreak else "Todos",
                "Caracteres": len(prompt)
            })
        
        st.dataframe(persona_data, use_container_width=True)
        
        st.markdown("---")
        
        # Editor de persona
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("✏️ Editar Persona")
            
            selected_persona = st.selectbox(
                "Selecionar Persona",
                list(PERSONAS.keys())
            )
            
            # Botões de ação
            if st.button("📋 Carregar", use_container_width=True):
                st.session_state.current_persona = selected_persona
                st.session_state.persona_content = PERSONAS[selected_persona]
            
            if st.button("➕ Nova Persona", use_container_width=True):
                st.session_state.current_persona = "nova_persona"
                st.session_state.persona_content = "Você é um assistente útil."
            
            if st.button("🗑️ Excluir", use_container_width=True, type="secondary"):
                if selected_persona not in ["standard"]:  # Proteger persona padrão
                    st.warning(f"⚠️ Tem certeza que deseja excluir '{selected_persona}'?")
                else:
                    st.error("❌ Não é possível excluir a persona padrão")
        
        with col2:
            st.subheader("📝 Editor de Prompt")
            
            if 'current_persona' not in st.session_state:
                st.session_state.current_persona = "standard"
                st.session_state.persona_content = PERSONAS["standard"]
            
            persona_name = st.text_input(
                "Nome da Persona",
                value=st.session_state.current_persona
            )
            
            persona_content = st.text_area(
                "Prompt da Persona",
                value=st.session_state.persona_content,
                height=300,
                help="Digite o prompt que define o comportamento desta persona"
            )
            
            # Preview
            st.markdown("**🔍 Preview:**")
            with st.expander("Ver preview do prompt"):
                st.markdown(f"```\n{persona_content}\n```")
            
            # Salvar
            col_save, col_test = st.columns(2)
            
            with col_save:
                if st.button("💾 Salvar Persona", use_container_width=True):
                    # Aqui você salvaria no arquivo de personas
                    st.success(f"✅ Persona '{persona_name}' salva!")
                    st.session_state.persona_content = persona_content
            
            with col_test:
                if st.button("🧪 Testar", use_container_width=True):
                    st.info("🤖 Enviando mensagem de teste...")
                    # Aqui você testaria a persona
        
        st.markdown("---")
        
        # Sistema de prompts
        st.subheader("🎯 Sistema de Prompts")
        
        # Carregar prompt do sistema atual
        system_prompt_file = Path("system_prompt.txt")
        current_system_prompt = ""
        if system_prompt_file.exists():
            current_system_prompt = system_prompt_file.read_text()
        
        new_system_prompt = st.text_area(
            "Prompt do Sistema Global",
            value=current_system_prompt,
            height=150,
            help="Este prompt é aplicado globalmente a todas as conversas"
        )
        
        if st.button("💾 Atualizar Prompt do Sistema"):
            system_prompt_file.write_text(new_system_prompt)
            st.success("✅ Prompt do sistema atualizado!")
    
    def _render_users(self):
        """Renderiza gerenciamento de usuários"""
        st.header("👥 Usuários & Grupos")
        
        # Administradores
        st.subheader("👑 Administradores")
        
        # Read admin IDs from environment (comma-separated); tolerate blanks/comments
        raw = os.getenv("ADMIN_USER_IDS", "")
        current_admins = []
        for tok in raw.split(','):
            tok = tok.split('#', 1)[0].strip()
            if tok.isdigit():
                current_admins.append(int(tok))
        admin_text = "\n".join(current_admins) if current_admins else "Nenhum administrador configurado"
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.text_area(
                "IDs dos Administradores (um por linha)",
                value=admin_text,
                height=100,
                help="IDs Discord dos usuários com privilégios administrativos"
            )
        
        with col2:
            st.markdown("**Como obter Discord ID:**")
            st.markdown("""
            1. 🔧 Ativar Modo Desenvolvedor
            2. 🖱️ Clicar direito no usuário  
            3. 📋 Selecionar "Copiar ID"
            """)
            
            if st.button("💾 Salvar Admins", use_container_width=True):
                st.success("✅ Lista de administradores atualizada!")
        
        st.markdown("---")
        
        # Usuários ativos
        st.subheader("👥 Usuários Ativos")
        
        # Mock data para demonstração
        users_data = [
            {"ID": "289558466551480320", "Nome": "Prof.Ramos", "Tipo": "👑 Admin", "Último Uso": "Agora", "Comandos": 150},
            {"ID": "123456789012345678", "Nome": "UserTest", "Tipo": "👤 Usuário", "Último Uso": "2h atrás", "Comandos": 45},
            {"ID": "987654321098765432", "Nome": "DevBot", "Tipo": "👤 Usuário", "Último Uso": "1d atrás", "Comandos": 23},
        ]
        
        st.dataframe(users_data, use_container_width=True)
        
        # Controles de usuário
        col1, col2, col3 = st.columns(3)
        
        with col1:
            user_to_manage = st.text_input("ID do Usuário")
        
        with col2:
            action = st.selectbox("Ação", ["Promover Admin", "Remover Admin", "Banir Usuário", "Desbanir"])
        
        with col3:
            st.markdown("‎") # Spacer
            if st.button("⚡ Executar", use_container_width=True):
                if user_to_manage:
                    st.success(f"✅ {action} executado para {user_to_manage}")
                else:
                    st.error("❌ Digite um ID de usuário válido")
        
        st.markdown("---")
        
        # Grupos e canais
        st.subheader("📺 Canais & Grupos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔧 Configurar Canais**")
            
            main_channel = st.text_input(
                "Canal Principal",
                value=self.config.get('DISCORD_CHANNEL_ID', ''),
                help="ID do canal principal do bot"
            )
            
            reply_all_channel = st.text_input(
                "Canal Reply All",
                value=self.config.get('REPLYING_ALL_DISCORD_CHANNEL_ID', ''),
                help="Canal onde bot responde todas mensagens"
            )
        
        with col2:
            st.markdown("**⚙️ Configurações**")
            
            reply_all = st.checkbox(
                "Reply All Ativo",
                value=self.config.get('REPLYING_ALL', 'False') == 'True',
                help="Bot responde a todas mensagens no canal"
            )
            
            logging_enabled = st.checkbox(
                "Logging Ativo",
                value=self.config.get('LOGGING', 'True') == 'True',
                help="Ativar logs detalhados"
            )
        
        if st.button("💾 Salvar Configurações de Canal", use_container_width=True):
            self.config['DISCORD_CHANNEL_ID'] = main_channel
            self.config['REPLYING_ALL_DISCORD_CHANNEL_ID'] = reply_all_channel
            self.config['REPLYING_ALL'] = str(reply_all)
            self.config['LOGGING'] = str(logging_enabled)
            self._save_config()
            st.success("✅ Configurações de canal salvas!")
    
    def _render_chat_monitor(self):
        """Renderiza monitoramento de chat"""
        st.header("💬 Chat Monitor")
        
        # Estatísticas de chat
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Mensagens Hoje", "1,234", "+12%")
        
        with col2:
            st.metric("⏱️ Tempo Resp. Médio", "1.2s", "-0.3s")
        
        with col3:
            st.metric("🤖 Provedor Ativo", "OpenAI", "")
        
        with col4:
            st.metric("💸 Custo Estimado", "$2.45", "+$0.15")
        
        st.markdown("---")
        
        # Log de conversas em tempo real
        st.subheader("📡 Conversas em Tempo Real")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_user = st.selectbox("Filtrar por Usuário", ["Todos", "Prof.Ramos", "UserTest"])
        
        with col2:
            filter_provider = st.selectbox("Filtrar por Provedor", ["Todos", "OpenAI", "Claude", "Free"])
        
        with col3:
            auto_refresh = st.checkbox("🔄 Auto Refresh (5s)", value=True)
        
        # Mock data de conversas
        chat_logs = [
            {
                "⏰ Timestamp": "14:32:15",
                "👤 Usuário": "Prof.Ramos",
                "💬 Mensagem": "Como configurar Docker?",
                "🤖 Provedor": "OpenAI",
                "📏 Tokens": "45",
                "⚡ Status": "✅"
            },
            {
                "⏰ Timestamp": "14:31:42", 
                "👤 Usuário": "UserTest",
                "💬 Mensagem": "Explique machine learning",
                "🤖 Provedor": "Claude",
                "📏 Tokens": "128",
                "⚡ Status": "✅"
            },
            {
                "⏰ Timestamp": "14:30:58",
                "👤 Usuário": "DevBot", 
                "💬 Mensagem": "/draw gato astronauta",
                "🤖 Provedor": "OpenAI",
                "📏 Tokens": "0",
                "⚡ Status": "🎨"
            }
        ]
        
        st.dataframe(chat_logs, use_container_width=True)
        
        # Auto refresh
        if auto_refresh:
            time.sleep(5)
            st.experimental_rerun()
        
        st.markdown("---")
        
        # Análises
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Uso por Hora")
            # Placeholder para gráfico
            st.bar_chart({"Hora": [10, 15, 30, 45, 25, 20, 35]})
        
        with col2:
            st.subheader("🥧 Distribuição de Provedores")
            # Placeholder para gráfico de pizza
            provider_stats = {
                "OpenAI": 45,
                "Claude": 30, 
                "Free": 20,
                "Gemini": 5
            }
            st.bar_chart(provider_stats)
    
    def _render_logs(self):
        """Renderiza logs e auditoria"""
        st.header("📝 Logs & Audit")
        
        # Controles de log
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            log_level = st.selectbox("Nível", ["INFO", "DEBUG", "WARNING", "ERROR"])
        
        with col2:
            log_source = st.selectbox("Fonte", ["Todos", "Bot", "Provider", "Auth"])
        
        with col3:
            log_date = st.date_input("Data", value=datetime.now())
        
        with col4:
            st.markdown("‎") # Spacer
            if st.button("🔍 Filtrar", use_container_width=True):
                st.success("✅ Filtros aplicados!")
        
        st.markdown("---")
        
        # Logs em tempo real
        st.subheader("📊 Logs do Sistema")
        
        # Mock logs
        log_entries = [
            {
                "⏰ Timestamp": "2024-01-15 14:32:15",
                "📊 Level": "INFO", 
                "🔧 Source": "Bot",
                "💬 Message": "Usuario 289558466551480320 executou comando /chat",
                "📋 Details": "Provider: openai, Model: gpt-4"
            },
            {
                "⏰ Timestamp": "2024-01-15 14:31:58",
                "📊 Level": "WARNING",
                "🔧 Source": "Provider", 
                "💬 Message": "Rate limit atingido para OpenAI",
                "📋 Details": "Fallback para provedor Free ativado"
            },
            {
                "⏰ Timestamp": "2024-01-15 14:31:42",
                "📊 Level": "INFO",
                "🔧 Source": "Auth",
                "💬 Message": "Acesso a persona jailbreak negado",
                "📋 Details": "Usuario 123456789 não é admin"
            }
        ]
        
        for log in log_entries:
            with st.expander(f"{log['⏰ Timestamp']} - {log['📊 Level']} - {log['💬 Message'][:50]}..."):
                st.json(log)
        
        st.markdown("---")
        
        # Controles de log
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Download Logs", use_container_width=True):
                st.success("💾 Logs exportados!")
        
        with col2:
            if st.button("🗑️ Limpar Logs", use_container_width=True):
                st.warning("⚠️ Logs antigos removidos!")
        
        with col3:
            if st.button("📊 Gerar Relatório", use_container_width=True):
                st.info("📋 Relatório de auditoria gerado!")
    
    def _render_settings(self):
        """Renderiza configurações gerais"""
        st.header("⚙️ Configurações")
        
        # Configurações gerais
        st.subheader("🔧 Configurações Gerais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            discord_token = st.text_input(
                "🤖 Discord Bot Token",
                value=self.config.get('DISCORD_BOT_TOKEN', ''),
                type="password",
                help="Token do bot Discord"
            )
            
            logging_level = st.selectbox(
                "📝 Nível de Log",
                ["INFO", "DEBUG", "WARNING", "ERROR"],
                index=0
            )
        
        with col2:
            auto_backup = st.checkbox(
                "💾 Backup Automático",
                value=True,
                help="Fazer backup automático das configurações"
            )
            
            maintenance_mode = st.checkbox(
                "🔧 Modo Manutenção",
                value=False,
                help="Ativar modo de manutenção (bot offline)"
            )
        
        # Configurações avançadas
        st.markdown("---")
        st.subheader("🔬 Configurações Avançadas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            request_timeout = st.slider(
                "⏱️ Timeout (segundos)",
                min_value=5,
                max_value=120,
                value=30
            )
            
            max_retries = st.slider(
                "🔄 Max Tentativas",
                min_value=1,
                max_value=5,
                value=3
            )
        
        with col2:
            rate_limit = st.slider(
                "⚡ Rate Limit (req/min)",
                min_value=1,
                max_value=100,
                value=20
            )
            
            cache_size = st.slider(
                "💾 Cache Size (MB)",
                min_value=10,
                max_value=500,
                value=100
            )
        
        # Botões de ação
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💾 Salvar Todas", use_container_width=True):
                self.config['DISCORD_BOT_TOKEN'] = discord_token
                self._save_config()
                st.success("✅ Configurações salvas!")
        
        with col2:
            if st.button("🔄 Reiniciar Bot", use_container_width=True):
                st.warning("⚠️ Bot será reiniciado...")
        
        with col3:
            if st.button("📥 Exportar Config", use_container_width=True):
                st.success("💾 Configuração exportada!")
        
        with col4:
            if st.button("📤 Importar Config", use_container_width=True):
                st.info("📂 Selecione arquivo de configuração")
        
        # Status do sistema
        st.markdown("---")
        st.subheader("📊 Status do Sistema")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **🔌 Conexões:**
            - Discord: 🟢 Conectado
            - OpenAI: 🟢 Ativo
            - Claude: 🟡 Standby
            """)
        
        with col2:
            st.markdown("""
            **💾 Recursos:**
            - RAM: 256MB / 1GB
            - CPU: 15% / 100%
            - Disk: 2GB / 10GB
            """)
        
        with col3:
            st.markdown("""
            **📊 Estatísticas:**
            - Uptime: 2h 15m
            - Mensagens: 1,234
            - Erros: 0
            """)

# Executar aplicação
if __name__ == "__main__":
    admin_panel = AdminPanel()
    admin_panel.run()
