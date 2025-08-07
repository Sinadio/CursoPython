class Smart:

    def __init__(self, cor, memoria, sim, amperes):

        self.cor = cor
        self.memoria = memoria
        self.sim = sim
        self.amperes = amperes

    def info(self):
        return f"Smartphone {self.cor}, {self.memoria}, {self.sim}, bateria: {self.amperes} mAh"


smart1 = Smart("Black", "128 GB", " Dual Sim", "5000")
smart2 = Smart("Blue", "228 GB", " Dual no", "5000")

print("O telefone: ",smart1.cor, "Com memoria: ", smart1.memoria)
print("O telefone: ", smart2.cor)

class Bombinha(Smart):
    def __init__(self, cor, memoria, sim, amperes, marca, capacidade):
        super().__init__(cor, memoria, sim, amperes)  # chama o construtor da classe mãe
        self.marca = marca
        self.capacidade = capacidade  # capacidade da bombinha, ex: 120 PSI

    def caracteristicas(self):
        return (f"Bombinha inteligente da marca {self.marca} com capacidade de {self.capacidade} PSI.\n"
                f"Atributos Smart: {self.info()}")

# Criar objeto da classe Bombinha
bombinha1 = Bombinha("Vermelha", "32 GB", "Single Sim", "3000", "AirTech", 120)

# Imprimir as características
print(bombinha1.caracteristicas())