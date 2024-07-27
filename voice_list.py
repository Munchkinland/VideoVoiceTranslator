import pyttsx3

def listar_voces():
    engine = pyttsx3.init()
    voces = engine.getProperty('voices')

    for voz in voces:
        print(f"ID: {voz.id}")
        print(f"Nombre: {voz.name}")
        print(f"Lenguaje: {voz.languages}")
        print(f"Género (si disponible): {voz.gender if hasattr(voz, 'gender') else 'No especificado'}")
        print('---')

if __name__ == "__main__":
    listar_voces()
