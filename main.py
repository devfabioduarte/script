from connect import conn #importa a conexao
import json

cur = conn.cursor() #faz um cursor, pra poder mexer no json

with open("json/allCharsUpdated.json", "r", encoding="utf-8") as file: #lê os arquivos no json
        characters = json.load(file)

with open("json/allEpisodesUpdated.json", "r", encoding='utf-8') as file:
        episodes = json.load(file)

# Cria tabela de characters
cur.execute("""CREATE TABLE IF NOT EXISTS characters( 
    id INTEGER PRIMARY KEY,
    name TEXT,
    status TEXT,
    species TEXT,
    type TEXT,
    gender TEXT,
    origin_name TEXT,
    origin_url TEXT,
    location_name TEXT,
    location_url TEXT,
    image TEXT,
    url TEXT
)
        """
)

# adiciona na tabela as informações do character
for chars in characters:
    cur.execute("""
        INSERT INTO characters (
            id, name, status, species, type, gender,
            origin_name, origin_url, location_name, location_url,
            image, url
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (
        chars["id"],
        chars["name"],
        chars["status"],
        chars["species"],
        chars["type"],
        chars["gender"],
        chars["origin"]["name"],
        chars["origin"]["url"],
        chars["location"]["name"],
        chars["location"]["url"],
        chars["image"],
        chars["url"],
    ))

# cria a tabela episodes
cur.execute("""CREATE TABLE IF NOT EXISTS episodes(
            id INTEGER PRIMARY KEY,
            name TEXT,
            air_date TEXT,
            episode TEXT,
            url TEXT)
            """)

#adiciona os episodios na tabela
for ep in episodes:
       cur.execute("""
            INSERT INTO episodes (
                   id, name, air_date, episode, url
                   )
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
            """, (
                    ep["id"],
                    ep["name"],
                    ep["air_date"],
                    ep["episode"],
                    ep["url"],
                    ))

#cria uma tabela relacional entre characters e episodes
cur.execute("""CREATE TABLE IF NOT EXISTS characters_episodes(
            character_id INTEGER REFERENCES characters(id),
            episode_id INTEGER REFERENCES episodes(id),
            PRIMARY KEY (character_id, episode_id)
            )""")

#adiciona os dados na tabela relacional
for chars in characters:
    character_id = chars["id"]
    for ep_url in chars["episode"]:
          ...



conn.commit()
cur.close()
conn.close()

        
    



# for chars in characters:
#     cur.execute("""
#             INSERT INTO charac """)""

"""
testando
"""