import pyttsx3

def configurar_motor(motor):
    """Ajusta a velocidade e tenta encontrar uma voz em português mais natural."""
    motor.setProperty('rate', 180)  # Velocidade da fala (padrão costuma ser 200, abaixar ajuda na clareza)
    motor.setProperty('volume', 1.0) # Volume de 0.0 a 1.0
    
    # Tenta selecionar uma voz em português do Brasil, se disponível
    vozes = motor.getProperty('voices')
    for voz in vozes:
        if 'portuguese' in voz.name.lower() or 'brazil' in voz.name.lower() or 'pt-br' in voz.id.lower():
            motor.setProperty('voice', voz.id)
            break

def falar(texto):
    """Função responsável por transformar texto em áudio de forma segura."""
    # Substitui a grafia oficial pela fonética correta para o leitor do Windows falar bonito
    texto_falado = texto.replace("EchoCode", "Ekocoude").replace("echocode", "ekocoude")
    
    print(f"EchoCode: {texto}") # No terminal continua escrito certinho
    try:
        motor = pyttsx3.init('sapi5')
        configurar_motor(motor)
        motor.say(texto_falado) # O motor lê a versão fonética
        motor.runAndWait()
        motor.stop()
    except Exception as e:
        print(f"Erro no áudio: {e}")

def apresentar_conceito():
    falar("Você escolheu aprender conceitos. O tema de hoje é: Variáveis.")
    falar("Uma variável é como uma caixinha na memória do computador onde guardamos um valor para usar depois.")

def iniciar_desafio():
    falar("Iniciando desafio de código.")
    falar("Qual comando em Python nós usamos para mostrar algo na tela? É print ou input?")
    
    # Aqui mantemos o input de texto para a resposta por enquanto
    resposta = input("Digite sua resposta: ").strip().lower()
    
    if resposta == "print":
        falar("Parabéns! Resposta correta, o print exibe informações na tela.")
    else:
        falar("Ops! A resposta correta seria print.")

def menu_principal():
    while True:
        print("\n--- MENU ECOCODE ---")
        print("1. Ouvir Conceito do Dia")
        print("2. Praticar Desafio")
        print("3. Sair")
        
        # Texto completo que o assistente vai ler para o usuário
        texto_menu = (
            "Menu principal. "
            "Digite 1 para ouvir o conceito do dia. "
            "Digite 2 para praticar um desafio. "
            "Ou digite 3 para sair."
        )
        falar(texto_menu)
        
        opcao = input("Escolha uma opção (1, 2 ou 3): ").strip()
        
        if opcao == "1":
            apresentar_conceito()
        elif opcao == "2":
            iniciar_desafio()
        elif opcao == "3":
            falar("Encerrando o EchoCode. Bons estudos!")
            break
        else:
            falar("Opção inválida. Por favor, escolha entre 1, 2 ou 3.")

if __name__ == "__main__":
    falar("Bem-vindo ao EchoCode, seu assistente de programação acessível.")
    menu_principal()