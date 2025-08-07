# Classe base
class SuperHero:
    def __init__(self, nome, poder, energia):
        self.nome = nome
        self.poder = poder
        self.energia = energia

    def atacar(self):
        return f"{self.nome} ataca com {self.poder}! 💥"

    def descansar(self):
        self.energia += 10
        return f"{self.nome} está a recuperar energia. Energia atual: {self.energia}"

# Subclasse com polimorfismo
class SuperVillain(SuperHero):
    def atacar(self):
        return f"{self.nome} lança um ataque sombrio com {self.poder}! 😈"

    def plano_malvado(self):
        return f"{self.nome} está a arquitetar um plano maligno... 🧠"

# Criar objetos
heroi = SuperHero("SolarMan", "Luz Solar", 80)
vilao = SuperVillain("DarkMist", "Névoa Negra", 70)

# Usar os métodos
print(heroi.atacar())
print(vilao.atacar())  # Polimorfismo: mesmo método, comportamento diferente
print(vilao.plano_malvado())
print(heroi.descansar())
