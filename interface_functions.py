# from popular_restaurants import rating_rank, score_rank
# from collaborative_filtering_model import recommended_restaurants
import pandas as pd


# Função para retornar o nome de usuário
def return_user(userID, dataframe):
  user_data = dataframe.loc[dataframe["userID"] == userID]
  user_data = user_data.to_dict("index")

  user_data = [value for value in user_data.values()]
  username = user_data[0]["first_name"] + ' ' + user_data[0]["last_name"]
  
  return username


# Função para retornar a quantidade de avaliações um usuário já fez
def counting_ratings_user(userID, dataset):
  amount_ratings = dataset["userID"].value_counts()

  if userID in amount_ratings:
    return amount_ratings[userID]
  else:
    return 0


def recommendation_type(amount_ratings):
  if amount_ratings == 0:
    return "Restaurantes Mais Populares"
  else:
    return "Restaurantes Recomendados"


# Abrindo o arquivo com os dados dos usuários
user_profile = pd.read_csv("./dataset/userprofile.csv", sep=',')
# Calculando quantos são os usuário cadastrados
total_users = len(user_profile)

# Abrindo o arquivo com as avaliações dos usuários
ratings_data = pd.read_csv("./dataset/rating_final.csv", sep=',')
