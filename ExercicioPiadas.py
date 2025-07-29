import random

piadas = [
    "Why do Python programmers wear glasses? Because they can't C!",
    "I told my code I needed a break, and it said 'try/except'!",
    "Why did the Python developer go broke? Because he used up all his cache.",
    "How do you comfort a JavaScript bug? You console it. (Oops, wrong language!) 😂",
    "Why did the function return early? It had a date with 'None'."
]

print("🪄 Welcome to the Python Joke Generator!")
input("Press Enter to hear a joke...")

# Selecionar uma piada aleatória
piada = random.choice(piadas)
print("\n🤣", piada)
