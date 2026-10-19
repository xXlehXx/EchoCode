import pyttsx3

def configurar_motor(motor):
    """Ajusta a velocidade e seleciona uma voz em português."""
    motor.setProperty('rate', 200)
    motor.setProperty('volume', 1.0)
    
    vozes = motor.getProperty('voices')
    for voz in vozes:
        if 'portuguese' in voz.name.lower() or 'brazil' in voz.name.lower() or 'pt-br' in voz.id.lower():
            motor.setProperty('voice', voz.id)
            break

def falar(texto):
    """Função responsável por transformar texto em áudio aplicando a fonética correta."""
    # Apenas o áudio recebe a alteração fonética para o SAPI5 ler certinho
    texto_falado = texto.replace("EchoCode", "Ekocoude").replace("echocode", "ekocoude")
    
    # O terminal exibe a grafia oficial sem alterações
    print(f"EchoCode: {texto}")
    try:
        motor = pyttsx3.init('sapi5')
        configurar_motor(motor)
        motor.say(texto_falado)
        motor.runAndWait()
        motor.stop()
    except Exception as e:
        print(f"Erro no áudio: {e}")

# Base de dados dos conteúdos
CONTEUDOS = {
    "1": {
        "tema": "Variáveis",
        "explicacao": "Uma variável é como uma caixinha na memória do computador onde guardamos um valor para usar depois.",
        "pergunta": "Qual comando em Python usamos para mostrar algo na tela? É print ou input?",
        "resposta_certa": "print"
    },
    "2": {
        "tema": "Estruturas Condicionais",
        "explicacao": "As condicionais permitem que o programa tome decisões usando if, elif e else, executando blocos de código dependendo de uma condição.",
        "pergunta": "Qual palavra-chave em inglês usamos para representar o 'senão se' em Python?",
        "resposta_certa": "elif"
    },
    "3": {
        "tema": "Estruturas de Repetição (Loops)",
        "explicacao": "Os loops servem para repetir um bloco de código várias vezes. O while repete enquanto uma condição for verdadeira.",
        "pergunta": "Qual estrutura de repetição usamos quando queremos repetir algo enquanto uma condição for verdadeira?",
        "resposta_certa": "while"
    }
}

def estudar_modulo(opcao_escolhida):
    """Executa a aula e o desafio baseado no módulo escolhido."""
    modulo = CONTEUDOS.get(opcao_escolhida)
    
    if not modulo:
        falar("Módulo não encontrado.")
        return

    falar(f"Você escolheu estudar: {modulo['tema']}.")
    falar(modulo['explicacao'])
    
    falar("Hora do desafio!")
    falar(modulo['pergunta'])
    
    resposta = input("Digite sua resposta: ").strip().lower()
    
    if resposta == modulo['resposta_certa']:
        falar("Parabéns! Resposta correta, você mandou muito bem.")
    else:
        falar(f"Ops! A resposta correta era {modulo['resposta_certa']}.")

def menu_principal():
    while True:
        print("\n--- MENU ECHOCODE ---")
        print("1. Estudar Variáveis")
        print("2. Estudar Estruturas Condicionais (if/else)")
        print("3. Estudar Loops (while)")
        print("4. Sair")
        
        # Mensagem falada ajustada para o nome oficial sem citar a faculdade na saída
        texto_menu = (
            "Menu principal do EchoCode. "
            "Digite 1 para estudar variáveis. "
            "Digite 2 para estudar condicionais. "
            "Digite 3 para estudar loops. "
            "Ou digite 4 para sair."
        )
        falar(texto_menu)
        
        opcao = input("Escolha uma opção (1 a 4): ").strip()
        
        if opcao in ["1", "2", "3"]:
            estudar_modulo(opcao)
        elif opcao == "4":
            falar("Encerrando o EchoCode. Até a próxima e bons estudos!")
            break
        else:
            falar("Opção inválida. Por favor, escolha um número entre 1 e 4.")

if __name__ == "__main__":
    falar("Bem-vindo ao EchoCode, seu assistente de programação acessível.")
    menu_principal()