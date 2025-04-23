import psycopg2 #importou a biblioteca pra conectar

try:
    conn = psycopg2.connect( #ta conectando o banco
        host="localhost",
        port="5432",
        database="rickandmorty",
        user="postgres",
        password="123456"  
)
    print('Conexão feita com sucesso')
except:
    print('Erro de conexão')

