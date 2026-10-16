import pyttsx3

def falar(texto):
    """Função segura para falar no Windows usando SAPI5."""
    print(f"Assistente: {texto}")
    
    try:
        motor = pyttsx3.init('sapi5')
        
        # Opcional: listar e selecionar uma voz em português se houver
        vozes = motor.getProperty('voices')
        for voz in vozes:
            if 'portuguese' in voz.name.lower() or 'brazil' in voz.name.lower():
                motor.setProperty('voice', voz.id)
                break
                
        motor.say(texto)
        motor.runAndWait()
        motor.stop() # Garante que o motor libera os recursos após falar
    except Exception as e:
        print(f"Erro no áudio: {e}")

def apresentar_desafio():
    """Função que apresenta o conceito e faz uma pergunta simples."""
    falar("Olá! Seja bem-vindo ao seu assistente de programação acessível.")
    falar("Vamos praticar estruturas condicionais, o famoso if e else.")
    
    pergunta = (
        "Imagine que queremos verificar se uma pessoa é maior de idade. "
        "Qual palavra-chave em Python nós usamos para representar a condição "
        "de 'se' algo acontecer? É a opção 1 para 'if', ou opção 2 para 'while'?"
    )
    falar(pergunta)

def verificar_resposta():
    """Função que recebe a resposta do usuário e valida."""
    # Por enquanto, usando input de texto (depois podemos evoluir para voz!)
    resposta = input("Digite o número da sua resposta (1 ou 2): ")
    
    if resposta == "1":
        falar("Parabéns! Resposta correta. O if é usado para criar condições.")
    else:
        falar("Ops, não foi bem isso. A resposta certa é a opção 1, o if.")

# --- Execução Principal ---
def main():
    apresentar_desafio()
    verificar_resposta()
    falar("Fim do nosso primeiro desafio. Até a próxima!")

# Chama o programa principal
if __name__ == "__main__":
    main()