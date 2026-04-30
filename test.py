import requests

def get_pokemon_info(name, api_url):
    if not name:
        raise ValueError("Pokemon name cannot be empty")

    response = requests.get(api_url + name.lower())

    if response.status_code != 200:
        raise ValueError("Pokemon not found")

    data = response.json()

    return {
        "name": data["name"],
        "height": data["height"],
        "weight": data["weight"],
        "types": [t["type"]["name"] for t in data["types"]],
    }
print(get_pokemon_info("pikachu", "https://pokeapi.co/api/v2/pokemon/"))
