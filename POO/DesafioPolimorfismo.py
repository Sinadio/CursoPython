# Classe base (opcional)
class Transporte:
    def move(self):
        raise NotImplementedError("Subclasse deve implementar este método.")

# Subclasse 1: Carro
class Car:
    def move(self):
        return "Condução 🚗"

# Subclasse 2: Avião
class Plane:
    def move(self):
        return "Voar ✈️"

# Subclasse 3: Barco
class Boat:
    def move(self):
        return "Navegação 🚤"

# Subclasse 4: Animal
class Cheetah:
    def move(self):
        return "Corrida rápida 🐆"

# Subclasse 5: Pássaro
class Bird:
    def move(self):
        return "A voar nas alturas 🐦"

# Lista de objetos diferentes
meios = [Car(), Plane(), Boat(), Cheetah(), Bird()]

# Usar polimorfismo para chamar move()
for item in meios:
    print(item.move())
