# Desafio: Crie um programa que leia um ficheiro de texto,
# processe o seu conteúdo e grave os resultados num novo ficheiro

# Conteúdo do ficheiro de exemplo (input.txt):
# Esta é a primeira linha.
# Aqui está a segunda linha de texto.
# Mais uma linha qualquer.
# Python é uma linguagem poderosa.
# Última linha do ficheiro!.

def leitorFicheiro(input_file, output_file):
    try:
        # Lendo o conteúdo
        with open(input_file, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        # Contando palavras
        palavras = conteudo.split()
        num_palavras = len(palavras)

        # Convertendo para maiúsculas
        conteudo_maiusculas = conteudo.upper()

        # Criando o conteúdo final
        resultado = f"{conteudo_maiusculas}\n\nNúmero de palavras: {num_palavras}"

        # Escrevendo no ficheiro de saída
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(resultado)

        print(f"✅ Sucesso! O ficheiro '{output_file}' foi criado com os resultados.")

    except FileNotFoundError:
        print(f"❌ Erro: O ficheiro '{input_file}' não foi encontrado.")
    except Exception as e:
        print(f"❌ Ocorreu um erro: {e}")

# Chamar a função
leitorFicheiro('input.txt', 'output.txt')
