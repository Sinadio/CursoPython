def ler_modificar():
    # solicitar o nome

    nome = input("Insira seu nome completo: ")

    try:

        with open(nome, 'r', encoding='utf-8') as f:
            conteudo = f.read()

            #Modicando para maiusculas
            conteudo_modificado = conteudo.upper()

            nome_saida = "cena_modificada.txt"

            #gravando o conteudo modificado

            with open(nome_saida, 'w', encoding='utf-8') as f:

                f.write(conteudo_modificado)

            print(f"✅ Sucesso! O conteúdo modificado foi gravado em '{nome_saida}'.")



    except FileNotFoundError:
        print(f"❌ Erro: O ficheiro '{nome}' não foi encontrado.")
    except IOError:
        print(f"❌ Erro: O ficheiro '{nome}' não pode ser lido ou escrito.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

ler_modificar()