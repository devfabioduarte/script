import json

def load_json_data():
    """Carrega todos os arquivos JSON e retorna como dicionários."""
    with open("json/allCharsUpdated.json", "r", encoding="utf-8") as file:
        characters = json.load(file)
    
    with open("json/allEpisodesUpdated.json", "r", encoding='utf-8') as file:
        episodes = json.load(file)
    
    with open("json/allLocations.json", "r", encoding='utf-8') as file:
        locations = json.load(file)
    
    return characters, episodes, locations