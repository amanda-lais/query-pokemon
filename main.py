import requests
from string import Template

def query_pokemon_by_name_or_id(poke_query: str) -> str:
    """Usando a PokeAPI, obtém informação sobre um pokemon pelo nome ou ID (poke_query).
    Retorna uma string com as informações em questão, ou uma mensagem de erro."""

    api_url = "https://pokeapi.co/api/v2/pokemon/{}".format(poke_query)
    response = requests.get(api_url)
    poke_info = "O Pokémon de número {} chama-se {}. A sua altura é {} e seu peso é {}."
    if response.status_code == 404:
        return("Nome ou ID de Pokémon inválido!")
    else:
        poke_data = response.json()
        return(poke_info.format(poke_data['id'], poke_data['name'].capitalize() , poke_data['height'], poke_data['weight']))

def query_pokemon_by_characteristic(poke_query: str, field: str) -> str:
    """Usando GraphQL, busca pokemons por característica (no momento peso ou altura).
    Depois, chama query_pokemon_by_name_or_id com o id de cada pokemon encontrado.
    Retorna uma string com as informações de cada um, ou uma mensagem de erro."""

    graphql_url = "https://beta.pokeapi.co/graphql/v1beta/"
    graph_query = Template("""{
        pokemon_v2_pokemon(where: {$field: {_eq: $query}}){
            id
        }
    }""")
    graph_query = graph_query.substitute(field=field, query=poke_query)
    response = requests.post(graphql_url, json={'query': graph_query})
    if response.status_code != 200:
        return("Erro ou nenhum Pokémon foi encontrado!")
    else:
        pokes_found = response.json()['data']['pokemon_v2_pokemon']
        info_pokes_found = ""
        for i in pokes_found:
            info_pokes_found += query_pokemon_by_name_or_id(str(i['id'])) + "\n"
        return(info_pokes_found)

def query_pokemon(query: str | int, field: str = "") -> str:
    """Trata o parâmetro query e chama as funções query_pokemon_by_name_or_id
    e query_pokemon_by_characteristic. Assume-se que, caso field seja vazio,
    a query busca pelo nome. Retorna uma string com as informações de cada
    Pokémon encontrado, ou uma mensagem de erro.
    
    query: nome, ID, peso ou altura buscada
    field: se a query é pelo nome, ID, peso ou altura"""

    if isinstance(query, int):
        query = str(query)
    query = query.strip().lower()
    field = field.strip().lower()
    if field == "" or field == "id" or field == "name":
        return query_pokemon_by_name_or_id(query)
    elif field == "height" or field == "weight":
        return query_pokemon_by_characteristic(query, field)

print(query_pokemon(" 151"))
