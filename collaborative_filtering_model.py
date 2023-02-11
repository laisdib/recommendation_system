import pandas as pd


'''Código usado para usuários da base de dados que já avaliaram pelo menos um restaurante'''

# Função para o cálculo da Similaridade Cosseno
def cosine_similarity(userID, dataframe):
    # Listando os índices do dataframe e removendo o que será analisado
    index_df = [i for i in dataframe.index]
    index_df.remove(userID)

    # Calculando o comprimento do vetor do usuário a ser analisado
    sum_x2 = (dataframe.loc[userID] ** 2).sum()
    sum_y2 = []
    xy = []
    
    cos_sim = dict()

    # Percorrendo os índices do dataframe
    for index in index_df:
        # Calculando o somatório para cada usuário da base de dados
        summation = (dataframe.loc[index] ** 2).sum()
        sum_y2.append(summation)

        # Calculando o produto dos vetores para toda a base de dados
        product = (dataframe.loc[userID] * dataframe.loc[index]).sum()
        xy.append(product)

    # Calculando a Similaridade Cosseno para cada usuário
    for i, j, k in zip(index_df, xy, sum_y2):
        if j == 0:
            cos_sim[i] = 0
        else:
            cos_sim[i] = (j / ((sum_x2 ** 0.5) * (k ** 0.5)))
      
    # Ordenando decrescentemente as similaridades obtidas e reservando as chaves
    cos_sim = {k: v for k, v in sorted(cos_sim.items(), key=lambda item: item[1], reverse=True)}
    most_similar = [*cos_sim]

    return most_similar


# Função para recomendar os restaurantes dos usuários com maior similaridade
def recommendation(userID, most_similar, dataframe):
    restaurants = []

    for i in most_similar:
        dataframe.sort_values(by=i, axis=1, ascending=False)
        
        for j in dataframe.columns:
            if (dataframe.loc[i][j] != 0) and (dataframe.loc[userID][j] == 0):
                if j not in restaurants:
                    restaurants.append(j)

    return restaurants


# Função para localizar os dados dos restaurantes recomendados
def restaurants_data(recommended_restaurants, dataframe):
    restaurants = pd.DataFrame()

    for restaurant in recommended_restaurants:
        restaurants = restaurants.append(dataframe.loc[dataframe["placeID"] == restaurant], ignore_index=True)

    restaurants.drop("placeID", axis=1, inplace=True)

    return restaurants
  

# Abrindo o arquivo com as avalições dos usuários
data_rating = pd.read_csv("./dataset/rating_final.csv", sep=',')

# Criando a matrix de avaliação contendo os usuários e suas notas aos restaurantes
final_ratings_matrix = data_rating.pivot(
    index = 'userID',
    columns = 'placeID',
    values = 'rating').fillna(0)
    
# Abrindo o arquivo com os dados dos restaurantes e expondo os selecionados
restaurants = pd.read_csv("./dataset/restaurants.csv", sep=',')
