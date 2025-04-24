from connect import conn #importa a conexao
from load_data import load_json_data #importa os dados em dicionário

character, episodes, locations = load_json_data

cur = conn.cursor() #faz um cursor, pra poder mexer no json

#cria a tabela locations
cur.execute("""CREATE TABLE IF NOT EXISTS locations(
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            dimension TEXT,
            residents TEXT,
            url TEXT)
            """)

#adiciona dados na tabela locations
for loc in locations:
    cur.execute("""INSERT INTO locations(id, name, type, dimension, residents, url)
                VALUES(%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """, (
                      loc["id"],
                      loc["name"],
                      loc["type"],
                      loc["dimension"],
                      loc["residents"],
                      loc["url"],
                ))

#cria tabela de characters
cur.execute("""CREATE TABLE IF NOT EXISTS characters( 
    id INTEGER PRIMARY KEY,
    name TEXT,
    status TEXT,
    species TEXT,
    type TEXT,
    gender TEXT,
    origin_id INTEGER REFERENCES locations(id),
    location_id INTEGER REFERENCES locations(id),
    image TEXT,
    url TEXT
)
        """
)

#adiciona dados na tabela characters
for chars in characters:
    origin_id = chars["origin"]["url"].split("/")[-1] if chars["origin"]["url"] and chars["origin"]["url"].strip() != "" else None
    location_id =chars["location"]["url"].split("/")[-1] if chars["origin"]["url"] and chars["location"]["url"].strip() != "" else None

    cur.execute("""
        INSERT INTO characters (
            id, name, status, species, type, gender,
            origin_id, location_id, image, url
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (
        chars["id"],
        chars["name"],
        chars["status"],
        chars["species"],
        chars["type"],
        chars["gender"],
        origin_id,
        location_id,
        chars["image"],
        chars["url"],
    ))

#cria a tabela episodes
cur.execute("""CREATE TABLE IF NOT EXISTS episodes(
            id INTEGER PRIMARY KEY,
            name TEXT,
            air_date TEXT,
            episode TEXT,
            url TEXT)
            """)

#adiciona os dados na tabela episodes
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
cur.execute("""CREATE TABLE IF NOT EXISTS character_episode(
            character_id INTEGER REFERENCES characters(id),
            episode_id INTEGER REFERENCES episodes(id),
            PRIMARY KEY (character_id, episode_id)
            )""")

#adiciona dados na tabela relacional
for chars in characters:
    character_id = chars["id"]
    for ep_url in chars["episode"]:
        episode_id = ep_url.split("/")[-1]
        cur.execute("""
            INSERT INTO character_episode (character_id, episode_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (character_id, episode_id))


conn.commit()
cur.close()
conn.close()

        
    



# for chars in characters:
#     cur.execute("""
#             INSERT INTO charac """)""

"""
testando
"""