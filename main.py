from connect import conn #importa a conexao
from load_data import load_json_data #importa os dados em dicionário

characters, episodes, locations = load_json_data()

cur = conn.cursor() #faz um cursor, pra poder mexer no json

#cria a tabela locations
cur.execute("""CREATE TABLE IF NOT EXISTS locations(
            id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            type VARCHAR(100),
            dimension VARCHAR(100),
            url VARCHAR(255))
            """)

#adiciona dados na tabela locations
for loc in locations:
    cur.execute("""INSERT INTO locations(id, name, type, dimension, url)
                VALUES(%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """, (
                      loc["id"],
                      loc["name"],
                      loc["type"],
                      loc["dimension"],
                      loc["url"],
                ))

#cria a tabela episodes
cur.execute("""CREATE TABLE IF NOT EXISTS episodes(
            id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            air_date VARCHAR(50),
            episode VARCHAR(20),
            url VARCHAR(255))
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

#cria tabela de characters
cur.execute("""CREATE TABLE IF NOT EXISTS characters( 
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    status VARCHAR(20),
    species VARCHAR(50),
    type VARCHAR(50),
    gender VARCHAR(20),
    origin_id INTEGER REFERENCES locations(id),
    location_id INTEGER REFERENCES locations(id),
    image VARCHAR(255),
    url VARCHAR(255)
)
        """
)

#cria uma tabela relacional entre characters e episodes
cur.execute("""CREATE TABLE IF NOT EXISTS character_episode(
            character_id INTEGER REFERENCES characters(id),
            episode_id INTEGER REFERENCES episodes(id),
            PRIMARY KEY (character_id, episode_id)
            )""")

#adiciona dados na tabela characters e na relacional
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
