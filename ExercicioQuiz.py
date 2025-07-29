print('Das questões de multipla escolha abaixo resolva para ver sua pontuacacao')

print('tens 3 chances para escolher a repostosta correcta')




def quiz():
    score = 0
    print("\n🎮 Bem-vindo ao Quiz sobre Python!\n")

    # Lista de perguntas com alternativas e resposta correta
    perguntas = [
        {
            "pergunta": "1) Qual a palavra-chave para definir uma função em Python?",
            "A": "func",
            "B": "def",
            "C": "function",
            "D": "define",
            "resposta": "B"
        },
        {
            "pergunta": "2) O que a função len() retorna?",
            "A": "A soma de números",
            "B": "Imprime dados",
            "C": "O comprimento (tamanho)",
            "D": "Nada",
            "resposta": "C"
        },
        {
            "pergunta": "3) Qual destes é um tipo de dado em Python?",
            "A": "number",
            "B": "digit",
            "C": "int",
            "D": "value",
            "resposta": "C"
        }
    ]

    # Loop pelas perguntas
    for p in perguntas:
        print(p["pergunta"])
        print("A)", p["A"])
        print("B)", p["B"])
        print("C)", p["C"])
        print("D)", p["D"])

        resposta = input("Sua resposta (A/B/C/D): ").upper()

        if resposta == p["resposta"]:
            print("✅ Correto!\n")
            score += 1
        else:
            print("❌ Errado! A resposta certa era", p["resposta"], "\n")

    print("🏁 Quiz finalizado!")
    print("Sua pontuação foi:", score, "/", len(perguntas), "\n")


# Loop para repetir o jogo
while True:
    quiz()
    jogar = input("Deseja jogar novamente? (sim/não): ").lower()
    if jogar != "sim":
        print("Obrigado por jogar! 👋")
        break
