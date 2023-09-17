import discord
import requests
from discord import app_commands

MY_GUILD = discord.Object(id='804734200464408626')  # replace with your guild id


def get_query(query):
    url = 'https://beta.pokeapi.co/graphql/v1beta'
    response = requests.post(url, json={'query': query})
    data = response.json()
    return data


def get_translated_move(move_name):
    query = f'''
    query namequery {{
      movenames: pokemon_v2_move(where: {{name: {{_ilike: "{move_name}"}}}}) {{
        pokemon_v2_movenames(where: {{language_id: {{_eq: 6}}}}) {{
          name
        }}
      }}
    }}
    '''

    data = get_query(query)
    try:
        return data.get('data').get('movenames')[0].get('pokemon_v2_movenames')[0].get('name')
    except:
        return f"Ungültige Attacke: {move_name}"


def get_translated_pokemon(pokemon_name):
    query = f'''
    query namequery {{
      pokemonname: pokemon_v2_pokemonspecies(where: {{name: {{_ilike: "{pokemon_name}"}}}}) {{
        pokemon_v2_pokemonspeciesnames(where: {{language_id: {{_eq: 6}}}}) {{
          pokemon_species_id
        }}
      }}
    }}
    '''

    data = get_query(query)
    try:
        return data.get('data').get('pokemonname')[0].get('pokemon_v2_pokemonspeciesnames')[0].get('pokemon_species_id')
    except:
        return f"Ungültiger Pokemon Name: {pokemon_name}"


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.tree.command()
@app_commands.describe(
    pokemon='Der zu übersetzende Pokemon Name',
)
async def tlp(interaction: discord.Interaction, pokemon: str):
    """Übersetzt einen Pokemon Namen vom Englischen ins Deutsche"""
    await interaction.response.send_message(f'https://www.bisafans.de/pokedex/{get_translated_pokemon(pokemon)}.php')


@client.tree.command()
@app_commands.describe(
    move='Die zu übersetzende Pokemon Attacke',
)
async def tlm(interaction: discord.Interaction, move: str):
    """Übersetzt eine Pokemon Attacke vom Englischen ins Deutsche"""
    await interaction.response.send_message(f'{get_translated_move(move)}')


@client.tree.command()
@app_commands.describe(
    id='Die Pokédex-Nummer',
)
async def pkdx(interaction: discord.Interaction, id: int):
    """Gibt einen Pokédex-Eintrag für eine ID wieder"""
    await interaction.response.send_message(f'https://www.bisafans.de/pokedex/{str(id)}.php')


client.run('redacted')
