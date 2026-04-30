import requests
from tkinter import *
from tkinter import messagebox 
from PIL import Image, ImageTk
from io import BytesIO

api_url = "https://pokeapi.co/api/v2/pokemon/"

def get_evolution_chain(name):
    try:
        pkmn = requests.get(api_url + name.lower()).json()
        species_url = pkmn["species"]["url"]

        species = requests.get(species_url).json()
        evo_url = species["evolution_chain"]["url"]

        evo_data = requests.get(evo_url).json()["chain"]

        evolutions = []

        while evo_data:
            evolutions.append(evo_data["species"]["name"])
            evo_data = evo_data["evolves_to"][0] if evo_data["evolves_to"] else None

        return " -> ".join(evolutions)
    except Exception as e:
        return f"Error fetching evolution chain: {e}"
root = Tk() 
root.geometry("800x600") 

title = Label(root, text ='Pokedex', font = "50") 
question = Label(root, text ='Enter the name of a Pokémon to get its information', font = "20")
pokemon_name = Entry(root, width = 50)
pokemon_info = Label(root, text = "", font = "20")
image_label = Label(root, text = "No image")

def get_pokemon_info():
    name = pokemon_name.get()
    response = requests.get(api_url + name.lower())
    if response.status_code == 200:
        data = response.json()
        poke_name = data['name']
        height = data['height']
        weight = data['weight']
        types = [t['type']['name'] for t in data['types']]
        evolution = get_evolution_chain(name)
        info_text = f"Name: {poke_name}\nHeight: {height}\nWeight: {weight}\nTypes: {', '.join(types)}\nEvolution: {evolution}"
        pokemon_info.config(text=info_text)
        img_url = data['sprites']['front_default']

        img_data = requests.get(img_url).content
        img = Image.open(BytesIO(img_data))
        img = img.resize((200, 200))

        photo = ImageTk.PhotoImage(img)

        image_label.config(image=photo)
        image_label.image = photo  
    else:
        pokemon_info.config(text="Pokémon not found.")

getInfoButton = Button(root, text = "Get Info", command = get_pokemon_info)
title.pack() 
question.pack()
pokemon_name.pack()
getInfoButton.pack()
pokemon_info.pack()
image_label.pack()

if __name__ == "__main__":
    root.mainloop()