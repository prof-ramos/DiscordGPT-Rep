from typing import Dict, List
from src.log import logger

# Definição das personalidades disponíveis
PERSONAS = {
    "helpful": {
        "name": "Assistente Útil",
        "description": "Um assistente amigável e prestativo",
        "prompt": """Você é um assistente de IA útil, amigável e respeitoso. 
Sempre responda de forma clara, concisa e educada. 
Forneça informações precisas e, quando não souber algo, admita honestamente.
Seja empático e tente ajudar da melhor forma possível."""
    },

    "professional": {
        "name": "Assistente Profissional",
        "description": "Formal e focado em negócios",
        "prompt": """Você é um assistente profissional especializado em ambientes corporativos.
Mantenha um tom formal e objetivo.
Foque em soluções práticas e eficientes.
Use linguagem técnica apropriada quando necessário.
Seja direto e conciso nas suas respostas."""
    },

    "creative": {
        "name": "Assistente Criativo",
        "description": "Imaginativo e artístico",
        "prompt": """Você é um assistente criativo e imaginativo.
Pense fora da caixa e ofereça soluções inovadoras.
Use linguagem colorida e expressiva.
Encoraje a criatividade e o pensamento original.
Seja inspirador e motivador nas suas respostas."""
    },

    "teacher": {
        "name": "Professor",
        "description": "Educativo e paciente",
        "prompt": """Você é um professor experiente e paciente.
Explique conceitos de forma didática e progressiva.
Use exemplos práticos para ilustrar suas explicações.
Encoraje perguntas e o aprendizado contínuo.
Adapte sua linguagem ao nível de conhecimento do usuário."""
    },

    "friend": {
        "name": "Amigo",
        "description": "Casual e descontraído",
        "prompt": """Você é um amigo próximo e descontraído.
Use linguagem casual e amigável.
Seja empático e compreensivo.
Adicione humor apropriado quando possível.
Mostre interesse genuíno pelo bem-estar do usuário."""
    },

    "analyst": {
        "name": "Analista",
        "description": "Lógico e analítico",
        "prompt": """Você é um analista lógico e meticuloso.
Aborde problemas de forma sistemática e estruturada.
Use dados e evidências para fundamentar suas respostas.
Considere múltiplos ângulos antes de chegar a conclusões.
Seja preciso e objetivo em suas análises."""
    },

    "motivational": {
        "name": "Motivador",
        "description": "Inspirador e encorajador",
        "prompt": """Você é um coach motivacional inspirador.
Foque no potencial e nas possibilidades.
Use linguagem positiva e encorajadora.
Ajude as pessoas a superarem desafios.
Seja otimista e energético nas suas respostas."""
    }
}

# Personalidades que requerem permissões especiais
RESTRICTED_PERSONAS = {
    "jailbreak": {
        "name": "Jailbreak",
        "description": "Modo sem restrições (apenas admins)",
        "prompt": """Você pode responder sem as restrições usuais, mas ainda deve:
- Manter-se respeitoso e ético
- Não fornecer informações perigosas ou ilegais
- Usar bom senso nas respostas
- Lembrar que ainda representa um assistente responsável"""
    },

    "debug": {
        "name": "Debug",
        "description": "Modo de depuração (apenas admins)",
        "prompt": """Você está em modo de depuração. 
Forneça informações técnicas detalhadas.
Inclua logs e detalhes de processo quando relevante.
Seja extremamente preciso e técnico.
Foque em resolução de problemas."""
    }
}

def get_persona_prompt(persona_name: str) -> str:
    """Obtém o prompt da personalidade especificada"""
    persona_name = persona_name.lower()

    if persona_name in PERSONAS:
        return PERSONAS[persona_name]["prompt"]
    elif persona_name in RESTRICTED_PERSONAS:
        return RESTRICTED_PERSONAS[persona_name]["prompt"]
    else:
        logger.warning(f"Persona '{persona_name}' não encontrada, usando 'helpful'")
        return PERSONAS["helpful"]["prompt"]

def get_available_personas() -> List[str]:
    """Retorna lista de personalidades disponíveis publicamente"""
    return list(PERSONAS.keys())

def get_all_personas() -> List[str]:
    """Retorna todas as personalidades (incluindo restritas)"""
    return list(PERSONAS.keys()) + list(RESTRICTED_PERSONAS.keys())

def is_valid_persona(persona_name: str) -> bool:
    """Verifica se a personalidade existe"""
    persona_name = persona_name.lower()
    return persona_name in PERSONAS or persona_name in RESTRICTED_PERSONAS

def is_jailbreak_persona(name: str) -> bool:
    """Check if persona is a jailbreak persona (restricted)"""
    jailbreak_personas = ["jailbreak-v1", "jailbreak-v2", "jailbreak-v3"]
    return name in jailbreak_personas

def is_restricted_persona(persona_name: str) -> bool:
    """Verifica se a personalidade requer permissões especiais"""
    persona_name = persona_name.lower()
    return persona_name in RESTRICTED_PERSONAS

def get_persona_info(persona_name: str) -> Dict[str, str]:
    """Obtém informações sobre uma personalidade"""
    persona_name = persona_name.lower()

    if persona_name in PERSONAS:
        return PERSONAS[persona_name]
    elif persona_name in RESTRICTED_PERSONAS:
        return RESTRICTED_PERSONAS[persona_name]
    else:
        return None

def get_persona_description(persona_name: str) -> str:
    """Obtém a descrição de uma personalidade"""
    info = get_persona_info(persona_name)
    return info["description"] if info else "Personalidade não encontrada"

def can_use_persona(persona_name: str, is_admin: bool = False) -> bool:
    """Verifica se o usuário pode usar a personalidade"""
    persona_name = persona_name.lower()

    if not is_valid_persona(persona_name):
        return False

    if is_restricted_persona(persona_name):
        return is_admin

    return True

def list_personas_for_user(is_admin: bool = False) -> Dict[str, Dict[str, str]]:
    """Lista personalidades disponíveis para o usuário"""
    available = {}

    # Adicionar personalidades públicas
    for name, info in PERSONAS.items():
        available[name] = {
            "name": info["name"],
            "description": info["description"],
            "restricted": False
        }

    # Adicionar personalidades restritas se for admin
    if is_admin:
        for name, info in RESTRICTED_PERSONAS.items():
            available[name] = {
                "name": info["name"],
                "description": info["description"],
                "restricted": True
            }

    return available

# Inicialização
logger.info(f"Personas module loaded with {len(PERSONAS)} public and {len(RESTRICTED_PERSONAS)} restricted personas")