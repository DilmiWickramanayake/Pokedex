import requests
from tkinter import *
from tkinter import messagebox 



api_url = "https://pokeapi.co/api/v2/pokemon/"



root = Tk() 
root.geometry("800x600") 

title = Label(root, text ='Pokedex', font = "50") 
question = Label(root, text ='Enter the name of a Pokémon to get its information', font = "20")
pokemon_name = Entry(root, width = 50)
pokemon_info = Label(root, text = "", font = "20")

def get_pokemon_info():
    name = pokemon_name.get()
    response = requests.get(api_url + name.lower())
    if response.status_code == 200:
        data = response.json()
        poke_name = data['name']
        height = data['height']
        weight = data['weight']
        types = [t['type']['name'] for t in data['types']]
        info_text = f"Name: {poke_name}\nHeight: {height}\nWeight: {weight}\nTypes: {', '.join(types)}"
        pokemon_info.config(text=info_text)
    else:
        pokemon_info.config(text="Pokémon not found.")

getInfoButton = Button(root, text = "Get Info", command = get_pokemon_info)
title.pack() 
question.pack()
pokemon_name.pack()
getInfoButton.pack()
pokemon_info.pack()

if __name__ == "__main__":
    root.mainloop()

