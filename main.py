import json
import os
import pyttsx3

def configurar_motor(motor):
    """Ajusta a velocidade, volume e seleciona a voz em português de forma segura."""
    motor.setProperty('rate', 300)
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
    """Função responsável por transformar texto em áudio aplicando a fonética correta."""
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

def carregar_conteudos():
    """Carrega os dados educacionais garantindo o caminho absoluto da pasta."""
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(diretorio_atual, "dados.json")
    
    if not os.path.exists(caminho_arquivo):
        print(f"[ERRO] O arquivo '{caminho_arquivo}' não foi encontrado!")
        return {}
    
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except Exception as e:
        print(f"[ERRO] Falha ao ler o arquivo JSON: {e}")
        return {}

def estudar_modulo(opcao_escolhida, conteudos):
    """Executa a aula e interage pelas questões do módulo com alternativas, dicas e opção de saída."""
    modulo = conteudos.get(opcao_escolhida)
    
    if not modulo:
        falar("Módulo não encontrado.")
        return

    falar(f"Você escolheu estudar: {modulo['tema']}.")
    falar(modulo['explicacao'])
    
    questoes = modulo.get("questoes", [])
    
    for i, q in enumerate(questoes, start=1):
        falar(f"Questão {i}: {q['pergunta']}")
        
        # Exibe as alternativas no terminal e lê em voz alta
        print("\n--- ALTERNATIVAS ---")
        texto_alternativas = "As alternativas são: "
        for letra, texto_alt in q['alternativas'].items():
            print(f"[{letra}] {texto_alt}")
            texto_alternativas += f"Letra {letra}: {texto_alt}. "
        
        falar(texto_alternativas)
        falar("Digite a letra da sua resposta, ou digite 'sair' para voltar ao menu.")
        
        # Sistema de Tentativas com Dica
        tentativas = 0
        acertou = False
        
        while tentativas < 2:
            resposta = input("Sua resposta (a, b, c, d ou sair): ").strip().lower()
            
            if resposta == "sair":
                falar("Encerrando o módulo atual e voltando ao menu principal.")
                return
            
            if resposta == q['resposta_certa']:
                falar("Parabéns! Resposta correta, você mandou muito bem.")
                acertou = True
                break
            else:
                tentativas += 1
                if tentativas == 1:
                    falar("Ops, resposta incorreta! Mas calma, vou te dar uma dica.")
                    falar(f"Dica: {q['dica']}")
                    falar("Tente novamente!")
                else:
                    falar(f"Ops! Acabaram suas tentativas. A resposta correta era a letra {q['resposta_certa'].upper()}.")
                    
    falar("Você concluiu todas as questões deste módulo! Excelente trabalho.")

def menu_principal():
    conteudos = carregar_conteudos()
    if not conteudos:
        falar("Aviso: Nenhum conteúdo foi carregado. Verifique o arquivo de dados.")
        return

    while True:
        print("\n--- MENU ECHOCODE ---")
        for chave, dados in conteudos.items():
            print(f"{chave}. Estudar {dados['tema']}")
        print(f"{str(len(conteudos) + 1)}. Sair")
        
        texto_fala_menu = "Menu principal do EchoCode. "
        for chave, dados in conteudos.items():
            texto_fala_menu += f"Digite {chave} para estudar {dados['tema']}. "
        texto_fala_menu += f"Ou digite {str(len(conteudos) + 1)} para sair."
        
        falar(texto_fala_menu)
        
        opcao = input(f"Escolha uma opção (1 a {len(conteudos) + 1}): ").strip()
        opcao_sair = str(len(conteudos) + 1)
        
        if opcao in conteudos:
            estudar_modulo(opcao, conteudos)
        elif opcao == opcao_sair or opcao.lower() == "sair":
            falar("Encerrando o EchoCode. Até a próxima e bons estudos!")
            break
        else:
            falar("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    falar("Bem-vindo ao EchoCode, seu assistente de programação acessível.")
    menu_principal()