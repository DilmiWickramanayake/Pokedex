import requests
api_url = "https://pokeapi.co/api/v2/pokemon/"
def get_pokemon_info(pokemon_name):
    response = requests.get(api_url + pokemon_name.lower())
    if response.status_code == 200:
        data = response.json()
        name = data['name']
        height = data['height']
        weight = data['weight']
        types = [t['type']['name'] for t in data['types']]
        return {
            'name': name,
            'height': height,
            'weight': weight,
            'types': types
        }
    else:
        return None
if __name__ == "__main__":
    pokemon_name = input("Enter the name of a Pokémon: ")
    info = get_pokemon_info(pokemon_name)
    if info:
        print(f"Name: {info['name']}")
        print(f"Height: {info['height']}")
        print(f"Weight: {info['weight']}")
        print(f"Types: {', '.join(info['types'])}")
    else:
        print("Pokémon not found.")