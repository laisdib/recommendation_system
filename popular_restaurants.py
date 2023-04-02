import pandas as pd


'''Código usado para novos usuários ou àqueles que ainda não avaliaram nenhum restaurante'''

# Função para ordenar os dados de acordo com uma métrica
def sort_most_rating_score(dataframe, metric):
    # Agrupando os restaurantes de acordo com a nota e quantidade de avalições recebidas
    data_grouped = dataframe.groupby('placeID').agg({'total_rating': 'mean', 'userID': 'count'}).reset_index()
    data_grouped.rename(columns = {'total_rating': 'rating', 'userID': 'score'}, inplace = True)
    pop_recom = pd.DataFrame()

    # Rankeando os restaurantes de acordo com a nota
    if metric == "rating":
        data_sort = data_grouped.sort_values(['rating','score','placeID'], ascending = False)  
        data_sort['rank'] = data_sort['rating'].rank(ascending = 0, method = 'first').astype(int)
        pop_recom = data_sort

    # Rankeando os restaurantes de acordo com a quantidade de avaliações
    elif metric == "score":
        data_sort = data_grouped.sort_values(['score', 'rating', 'placeID'], ascending = False)
        data_sort['rank'] = data_sort['score'].rank(ascending = 0, method = 'first').astype(int)
        pop_recom = data_sort

    return pop_recom


# Função para retornar os nomes dos restaurantes mapeados pelo ID
def return_name_restaurants(rank, dataframe):
    places_id = rank["placeID"]
    names = []

    for id in places_id:
        rest_data = dataframe.loc[dataframe["placeID"] == id]
        rest_data = rest_data.to_dict("index")
        rest_data = [value for value in rest_data.values()]
        names.append(rest_data[0]["name"])
    
    rank.drop("placeID", axis=1, inplace=True)
    rank.drop("rank", axis=1, inplace=True)
    rank.insert(0, "place_name", names, True)

    return rank


# Abrindo o arquivo com as avalições dos usuários e os dados dos restaurantes
data_rating = pd.read_csv("./dataset/rating_final.csv", sep=',')
restaurants_data = pd.read_csv("./dataset/restaurants.csv", sep=',')

# Ordenando os restaurantes por nota ou maior quantidade de avaliações
rating_rank = sort_most_rating_score(data_rating, "rating")
rating_rank = return_name_restaurants(rating_rank, restaurants_data)

score_rank = sort_most_rating_score(data_rating, "score")
score_rank = return_name_restaurants(score_rank, restaurants_data)
