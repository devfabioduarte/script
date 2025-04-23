import psycopg2
import json

# 1. Conecta ao banco
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="rickandmorty",
    user="postgres",
    password="123456"
)
cur = conn.cursor()

# 2. Abre o arquivo JSON
with open("json/allCharsUpdated.json", "r", encoding="utf-8") as file:
    personagens = json.load(file)

# 3. Para cada personagem, insere no banco
for p in personagens:
    cur.execute("""
        INSERT INTO characters (
            id, name, status, species, type, gender,
            origin_name, origin_url, location_name, location_url,
            image, url, created
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (
        p["id"],
        p["name"],
        p["status"],
        p["species"],
        p["type"],
        p["gender"],
        p["origin"]["name"],
        p["origin"]["url"],
        p["location"]["name"],
        p["location"]["url"],
        p["image"],
        p["url"],
        p["created"]
    ))

# 4. Salva e fecha
conn.commit()
cur.close()
conn.close()
print("✅ Personagens inseridos com sucesso!")
