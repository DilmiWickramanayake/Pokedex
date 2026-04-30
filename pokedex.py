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

        return evolutions
    except Exception as e:
        return []
root = Tk() 
root.geometry("800x600") 

title = Label(root, text ='Pokedex', font = "50") 
question = Label(root, text ='Enter the name of a Pokemon to get its information', font = "20")
pokemon_name = Entry(root, width = 50)
pokemon_info = Label(root, text = "", font = "20")
evolution_frame = Frame(root)
image_label = Label(root, text = "No image")

def on_evolution_click(pokemon):
    pokemon_name.delete(0, END)
    pokemon_name.insert(0, pokemon)
    get_pokemon_info()

def get_pokemon_info():
    name = pokemon_name.get()
    response = requests.get(api_url + name.lower())
    if response.status_code == 200:
        data = response.json()
        poke_name = data['name']
        height = data['height']
        weight = data['weight']
        types = [t['type']['name'] for t in data['types']]
        evolutions = get_evolution_chain(name)
        info_text = f"Name: {poke_name}\nHeight: {height}\nWeight: {weight}\nTypes: {', '.join(types)}"
        pokemon_info.config(text=info_text)
        
        for widget in evolution_frame.winfo_children():
            widget.destroy()
        
        if evolutions:
            evo_label = Label(evolution_frame, text="Evolution Chain: ", font="15")
            evo_label.pack(side=LEFT)
            for i, evo in enumerate(evolutions):
                evo_btn = Button(evolution_frame, text=evo, fg="blue", bg="white", bd=0, 
                                command=lambda p=evo: on_evolution_click(p))
                evo_btn.pack(side=LEFT)
                if i < len(evolutions) - 1:
                    separator = Label(evolution_frame, text="-> ", font="15")
                    separator.pack(side=LEFT)
        
        img_url = data['sprites']['front_default']

        img_data = requests.get(img_url).content
        img = Image.open(BytesIO(img_data))
        img = img.resize((200, 200))

        photo = ImageTk.PhotoImage(img)

        image_label.config(image=photo)
        image_label.image = photo  
    else:
        pokemon_info.config(text="Pokemon not found.")

getInfoButton = Button(root, text = "Get Info", command = get_pokemon_info)
title.pack() 
question.pack()
pokemon_name.pack()
getInfoButton.pack()
pokemon_info.pack()
evolution_frame.pack()
image_label.pack()

if __name__ == "__main__":
    root.mainloop()