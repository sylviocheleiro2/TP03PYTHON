import sqlite3
import pandas as pd
import sqlalchemy as sqla
from sqlalchemy import Engine, create_engine, MetaData, Table, Column, Integer, String, Float


def exercicio_1():

    # Crie três arquivos Excel em Python chamados inventory1.xlsx, inventory2.xlsx, e inventory3.xlsx, cada um com uma tabela com os dados dos produtos: produtoID, produto e quantidade.
    print("Exercicio 1")

    # ----------------#
    inventory1_xlsx = {
        "produtoID": [1, 2, 3, 4],
        "produto": ["Casaco", "Camisa", "Bermuda", "Luva"],
        "quantidade": [15, 18, 17, 10]
    }
    df1 = pd.DataFrame(inventory1_xlsx)
    with pd.ExcelWriter("Q1/inventory1.xlsx", engine="openpyxl") as writer:
        df1.to_excel(writer, sheet_name="Sheet1", index=False)
     # ----------------#

     # ----------------#
    inventory2_xlsx = {
        "produtoID": [5, 6, 7, 8],
        "produto": ["Casaco", "Camisa", "Bermuda", "Luva"],
        "quantidade": [15, 18, 17, 10]
    }

    df2 = pd.DataFrame(inventory2_xlsx)
    with pd.ExcelWriter("Q1/inventory2.xlsx", engine="openpyxl") as writer:
        df2.to_excel(writer, sheet_name="Sheet2", index=False)
     # ----------------#

     # ----------------#
    inventory3_xlsx = {
        "produtoID": [9, 10, 11, 12],
        "produto": ["Calça", "Sunga", "Cueca", "Bone"],
        "quantidade": [15, 18, 17, 10]
    }
    df3 = pd.DataFrame(inventory3_xlsx)
    with pd.ExcelWriter("Q1/inventory3.xlsx", engine="openpyxl") as writer:
        df3.to_excel(writer, sheet_name="Sheet3", index=False)
     # ----------------#


def exercicio_2():
    print("Exercicio 2")
    # Combine os dados dos três arquivos Excel em um único DataFrame.
    df1 = pd.read_excel("Q1/inventory1.xlsx")
    df2 = pd.read_excel("Q1/inventory2.xlsx")
    df3 = pd.read_excel("Q1/inventory3.xlsx")
    df_combined = pd.concat([df1, df2, df3])
    print(df_combined)


def exercicio_3():
    # Calcule o estoque total disponível por produto
    print("Exercicio 3")
    df1 = pd.read_excel("Q1/inventory1.xlsx")
    df2 = pd.read_excel("Q1/inventory2.xlsx")
    df3 = pd.read_excel("Q1/inventory3.xlsx")
    df_combined = pd.concat([df1, df2, df3])
    estoque_total = df_combined.groupby(
        "produto")["quantidade"].sum().reset_index()
    print(estoque_total)


def exercicio_4():
    # Identifique o produto com o maior estoque total.
    print("Exercicio 4")
    df1 = pd.read_excel("Q1/inventory1.xlsx")
    df2 = pd.read_excel("Q1/inventory2.xlsx")
    df3 = pd.read_excel("Q1/inventory3.xlsx")
    df_combined = pd.concat([df1, df2, df3])
    estoque_total = df_combined.groupby(
        "produto")["quantidade"].sum().reset_index()
    produto_mais_estoque = estoque_total.loc[estoque_total["quantidade"].idxmax(
    )]
    print(produto_mais_estoque)


def exercicio_5():
    # Adicione uma coluna adicional chamada status no DataFrame resultante, que indica se o estoque total é Alto (acima de 20 unidades) ou Baixo (20 unidades ou menos).
    print("Exercicio 5")

    df1 = pd.read_excel("Q1/inventory1.xlsx")
    df2 = pd.read_excel("Q1/inventory2.xlsx")
    df3 = pd.read_excel("Q1/inventory3.xlsx")
    df_combined = pd.concat([df1, df2, df3])
    estoque_total = df_combined.groupby(
        "produto")["quantidade"].sum().reset_index()

    estoque_total["status"] = ["Alto" if quantidade >
                               20 else "Baixo" for quantidade in estoque_total["quantidade"]]

    print(estoque_total)


def exercicio_6():
    print("Exercicio 6")
    df1 = pd.read_excel("Q1/inventory1.xlsx")
    df2 = pd.read_excel("Q1/inventory2.xlsx")
    df3 = pd.read_excel("Q1/inventory3.xlsx")
    df_combined = pd.concat([df1, df2, df3])
    estoque_total = df_combined.groupby(
        "produto")["quantidade"].sum().reset_index()

    estoque_total["status"] = ["Alto" if quantidade >
                               20 else "Baixo" for quantidade in estoque_total["quantidade"]]
    estoque_total.to_excel("Q6/total_inventory_summary.xlsx", index=False)

    print(estoque_total)


def exercicio_7():
    # Crie a tabela vendas com as colunas produto, quantidade e valor_unitario. Após a criação da tabela, use SQLAlchemy para verificar e imprimir a estrutura da tabela.
    print("Exercicio 7")
    engine = sqla.create_engine("sqlite:///banco_dados.db")

    with engine.connect() as connection:
        with connection.begin():
            connection.execute(sqla.text('DROP TABLE IF EXISTS vendas'))
            connection.execute(sqla.text('''
            CREATE TABLE IF NOT EXISTS vendas (
                produtoID INTEGER PRIMARY KEY AUTOINCREMENT,
                produto TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                valor_unitario FLOAT NOT NULL
            );
            '''))

    metadata = sqla.MetaData()
    metadata.reflect(bind=engine)
    vendas = sqla.Table('vendas', metadata, autoload_with=engine)

    print("Estrutura da tabela 'vendas':")
    for column in vendas.columns:
        print(f"Nome: {column.name}, Tipo: {column.type}")


def exercicio_8():
    # Crie um DataFrame com os dados de vendas: produto, quantidade e valor_unitario. Salve esse DataFrame na tabela vendas no banco de dados SQL usando Pandas.
    print("Exercicio 8")

    dados_vendas = {
        "produto": ["Casaco", "Camisa", "Produto A", "Luva"],
        "quantidade": [21, 12, 20, 22],
        "valor_unitario": [4, 300, 60, 156]
    }
    df_vendas = pd.DataFrame(dados_vendas)

    df_vendas.to_sql('vendas', con="sqlite:///banco_dados.db",
                     if_exists='append', index=False)


def exercicio_9():
    # Atualize o valor_unitario de Produto A para 30.0 na tabela vendas.
    print("Exercicio 9")

    df_vendas = pd.read_sql('vendas', con="sqlite:///banco_dados.db")
    df_vendas.loc[df_vendas['produto'] == 'Produto A', 'valor_unitario'] = 30.0

    df_vendas.to_sql('vendas', con="sqlite:///banco_dados.db",
                     if_exists='replace', index=False)


def exercicio_10():
    # Exclua todos os registros da tabela vendas onde a quantidade é menor que 20.
    print("Exercicio 10")

    engine = create_engine('sqlite:///banco_dados.db')

    df_vendas = pd.read_sql('vendas', con=engine)

    df_vendas_filtrado = df_vendas[df_vendas['quantidade'] >= 20]

    df_vendas_filtrado.to_sql('vendas', con=engine,
                              if_exists='replace', index=False)


def exercicio_11():
    # Calcule o total de valor_unitario por produto e exiba o resultado em um DataFrame.
    print("Exercicio 11")
    engine = sqla.create_engine("sqlite:///banco_dados.db")
    query = '''
    SELECT produto, SUM(valor_unitario * quantidade) AS total_valor
    FROM vendas
    GROUP BY produto;
    '''
    df_total = pd.read_sql(query, con=engine)
    print(df_total)


def exercicio_12():
    # Carregue os dados da tabela vendas apenas para os produtos com valor_unitario maior que 10.0 em um DataFrame.
    print("Exercicio 12")
    engine = sqla.create_engine("sqlite:///banco_dados.db")
    query = '''
    SELECT *
    FROM vendas
    WHERE valor_unitario > 10.0;
    '''
    df = pd.read_sql(query, con=engine)
    print(df)


def exercicio_13():
    # Crie um índice na coluna produto da tabela vendas para melhorar o desempenho das consultas que utilizam essa coluna.
    print("Exercicio 13")
    engine = sqla.create_engine("sqlite:///banco_dados.db")
    df = pd.read_sql(
        sql="SELECT produtoID FROM vendas WHERE produtoID > 0", con=engine)
    print(df)


def exercicio_14():
    # Exporte os dados da tabela vendas para um arquivo CSV e depois importe esses dados de volta para uma nova tabela chamada vendas_backup.
    print("Exercicio 14")
    engine = sqla.create_engine("sqlite:///banco_dados.db")
    df = pd.read_sql(
        sql="SELECT * FROM vendas WHERE produtoID > 0", con=engine)
    df.to_csv("Q14/vendas_backup.csv", index=False)

    df = pd.read_csv("Q14/vendas_backup.csv")
    df = pd.DataFrame(df)
    print(df)


def exercicio_15():
    print("Exercicio 15")
    engine = sqla.create_engine("sqlite:///banco_dados.db")

    dados_vendas = [
        {"produto": "Casaco", "quantidade": 10, "valor_unitario": 120.50},
        {"produto": "Camisa", "quantidade": 20, "valor_unitario": 50.30},
        {"produto": "Bermuda", "quantidade": 15, "valor_unitario": 70.00},
        {"produto": "Luva", "quantidade": 5, "valor_unitario": 35.90}
    ]

    insert_query = sqla.text('''
    INSERT INTO vendas (produto, quantidade, valor_unitario)
    VALUES (:produto, :quantidade, :valor_unitario);
    ''')
    with engine.connect() as connection:
        with connection.begin():
            try:
                for item in dados_vendas:
                    connection.execute(insert_query, item)
            except Exception as e:
                print(f"Erro ao inserir dados: {e}")


def exercicio_16():
    # Como podemos prevenir SQL Injection ao usar SQLAlchemy? De um exemplo de código.
    print("Exercicio 16")

    def consulta_banco_dados(query, **params):
        engine = sqla.create_engine("sqlite:///banco_dados.db")
        with engine.connect() as connection:
            result = connection.execute(sqla.text(query), **params)
            return pd.DataFrame(result.fetchall(), columns=result.keys())

    def buscar_produto(produto):
        print(f"Buscando dados para o produto: {produto}")
        query = '''
      SELECT * 
      FROM vendas 
      WHERE produto = :produto;
      '''
        resultado = consulta_banco_dados(query, produto=produto)
        print(resultado)
    buscar_produto("Camisa")


# NÃO EDITE O CÓDIGO ABAIXO


def main():
    functions = [
        exercicio_1, exercicio_2, exercicio_3, exercicio_4, exercicio_5,
        exercicio_6, exercicio_7, exercicio_8, exercicio_9, exercicio_10,
        exercicio_11, exercicio_12, exercicio_13, exercicio_14, exercicio_15, exercicio_16
    ]

    for func in functions:
        print(f"Executando exercício {func.__name__}()")
        try:
            func()
        except Exception as e:
            print(f"Ocorreu um erro ao executar o exercício {func.__name__}()")
            print(e)


if __name__ == "__main__":
    main()
