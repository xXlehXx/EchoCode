import json
import os
import pyttsx3
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

# Carrega a chave GEMINI_API_KEY do arquivo .env
load_dotenv()

# --- ESQUEMA DE DADOS PARA A IA (Garante o mesmo formato do seu dados.json) ---
class Alternativas(BaseModel):
    a: str
    b: str
    c: str
    d: str

class Questao(BaseModel):
    pergunta: str
    alternativas: Alternativas
    resposta_certa: str  # "a", "b", "c" ou "d"
    dica: str

class ModuloIA(BaseModel):
    tema: str
    explicacao: str
    questoes: list[Questao]

# --- MOTOR DE ÁUDIO (Mantido intacto da v1) ---
def configurar_motor(motor):
    motor.setProperty('rate', 250)
    motor.setProperty('volume', 1.0)
    try:
        vozes = motor.getProperty('voices')
        for voz in vozes:
            if 'portuguese' in voz.name.lower() or 'brazil' in voz.name.lower() or 'pt-br' in voz.id.lower():
                motor.setProperty('voice', voz.id)
                break
    except Exception as e:
        print(f"Aviso ao configurar voz: {e}")

def falar(texto):
    texto_falado = texto.replace("EchoCode", "Ekocoude").replace("echocode", "ekocoude")
    print(f"EchoCode: {texto}")
    try:
        motor = pyttsx3.init('sapi5')
        configurar_motor(motor)
        motor.say(texto_falado)
        motor.runAndWait()
        motor.stop()
    except Exception as e:
        print(f"Erro no áudio: {e}")

# --- CARREGAMENTO LOCAL (Fallback / Offline) ---
def carregar_conteudos():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(diretorio_atual, "dados.json")
    if not os.path.exists(caminho_arquivo):
        return {}
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except Exception as e:
        print(f"[ERRO] Falha ao ler dados.json: {e}")
        return {}

# --- INTEGRAÇÃO COM IA (NOVIDADE DA V2) ---
def gerar_modulo_com_ia(tema_escolhido):
    """Consulta o Gemini para gerar explicação e questões inéditas no padrão EchoCode."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        falar("Chave da API não encontrada. Verifique o arquivo ponto env.")
        return None

    falar(f"Gerando aula personalizada sobre {tema_escolhido} com inteligência artificial. Aguarde um instante...")
    
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    Você é o EchoCode, um tutor de programação acessível e socrático para iniciantes e pessoas com deficiência visual.
    Crie um módulo de estudo sobre: '{tema_escolhido}' em Python.
    Regras:
    1. 'explicacao': clara, objetiva, sem depender de elementos visuais (máximo 3 frases) e deve conter a base para responder às perguntas.
    2. 'questoes': crie exatamente 2 questões de múltipla escolha (alternativas a, b, c, d).
    3. 'resposta_certa': apenas a letra minúscula ('a', 'b', 'c' ou 'd').
    4. 'dica': uma dica pedagógica socrática que ajude o aluno a raciocinar sem entregar a letra diretamente.
    """

    # Lista de modelos em ordem de velocidade/prioridade (se um estiver lento ou indisponível, tenta o próximo)
    # Modelos ativos na sua chave (3.5-flash-lite é ultra-rápido e não sofre com picos de demanda)
    modelos_para_tentar = [
        'gemini-3.5-flash-lite',
        'gemini-3.8-flash',
    ]

    for modelo in modelos_para_tentar:
        try:
            print(f"[DEBUG] Tentando modelo: {modelo}...")
            
            # O lite não aceita thinking_config; no 3.8-flash desativamos o thinking para ser instantâneo
            if 'lite' in modelo:
                config_geracao = types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ModuloIA,
                    temperature=0.7,
                )
            else:
                config_geracao = types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ModuloIA,
                    temperature=0.7,
                    thinking_config=types.ThinkingConfig(thinking_budget=0)
                )

            response = client.models.generate_content(
                model=modelo,
                contents=prompt,
                config=config_geracao,
            )
            print(f"[DEBUG] Sucesso com o modelo {modelo}!")
            return json.loads(response.text)
        except Exception as e:
            print(f"[AVISO] Falha no modelo {modelo}: {type(e).__name__} - {e}")
            continue

    falar("Não consegui conectar à inteligência artificial agora. Tente novamente ou use os módulos offline.")
    return None

# --- FLUXO DE ESTUDO ---
def executar_aula(modulo):
    """Executa qualquer módulo (vindo do JSON local ou gerado pela IA)."""
    falar(f"Iniciando estudo sobre: {modulo['tema']}.")
    falar(modulo['explicacao'])
    
    questoes = modulo.get("questoes", [])
    
    for i, q in enumerate(questoes, start=1):
        falar(f"Questão {i}: {q['pergunta']}")
        
        print("\n--- ALTERNATIVAS ---")
        texto_alternativas = "As alternativas são: "
        for letra, texto_alt in q['alternativas'].items():
            print(f"[{letra}] {texto_alt}")
            texto_alternativas += f"Letra {letra}: {texto_alt}. "
        
        falar(texto_alternativas)
        falar("Digite a letra da sua resposta, ou digite 'sair' para voltar ao menu.")
        
        tentativas = 0
        while tentativas < 2:
            resposta = input("Sua resposta (a, b, c, d ou sair): ").strip().lower()
            
            if resposta == "sair":
                falar("Voltando ao menu principal.")
                return
            
            if resposta == q['resposta_certa'].lower():
                falar("Parabéns! Resposta correta, você mandou muito bem.")
                break
            else:
                tentativas += 1
                if tentativas == 1:
                    falar("Ops, resposta incorreta! Vou te dar uma dica.")
                    falar(f"Dica: {q['dica']}")
                    falar("Tente novamente!")
                else:
                    falar(f"Fim das tentativas. A resposta correta era a letra {q['resposta_certa'].upper()}.")
                    
    falar("Módulo concluído! Excelente trabalho.")

def menu_principal():
    conteudos_locais = carregar_conteudos()

    while True:
        print("\n=== MENU ECHOCODE V2 (IA INTEGRADA) ===")
        for chave, dados in conteudos_locais.items():
            print(f"{chave}. [Offline] Estudar {dados['tema']}")
        
        opcao_ia = str(len(conteudos_locais) + 1)
        opcao_sair = str(len(conteudos_locais) + 2)
        
        print(f"{opcao_ia}. [IA] Estudar qualquer tema livre (Gerado na hora)")
        print(f"{opcao_sair}. Sair")
        
        texto_menu = "Menu do EchoCode versão 2. "
        for chave, dados in conteudos_locais.items():
            texto_menu += f"Digite {chave} para {dados['tema']}. "
        texto_menu += f"Digite {opcao_ia} para criar uma aula com Inteligência Artificial sobre qualquer assunto. Ou {opcao_sair} para sair."
        
        falar(texto_menu)
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao in conteudos_locais:
            executar_aula(conteudos_locais[opcao])
        elif opcao == opcao_ia:
            falar("Qual tema de programação você quer estudar agora? Por exemplo: listas, dicionários ou funções.")
            tema = input("Digite o tema desejado: ").strip()
            if tema.lower() == "sair" or not tema:
                continue
            modulo_ia = gerar_modulo_com_ia(tema)
            if modulo_ia:
                executar_aula(modulo_ia)
        elif opcao == opcao_sair or opcao.lower() == "sair":
            falar("Encerrando o EchoCode. Até a próxima!")
            break
        else:
            falar("Opção inválida.")

if __name__ == "__main__":
    falar("Bem-vindo ao EchoCode versão 2, agora com inteligência artificial.")
    menu_principal()