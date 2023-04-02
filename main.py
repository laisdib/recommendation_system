import collaborative_filtering_model as cfm
import interface_functions as ifs
import popular_restaurants as pr
import customtkinter
import pandas as pd
import tkinter as tk


SUBTITLE_FONT = "Poppins Medium"
SEMIBOLD_FONT = "Poppins Semibold"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("500x300")
        self.title("MoFomme")
        self.minsize(1000, 600)

        # create 2x2 grid system
        self.grid_columnconfigure((0, 1), weight=1)

        self.title = customtkinter.CTkLabel(master=self, 
                                            text="MoFomme",
                                            font=self.create_font("Poppins Bold", 40))
        self.title.grid(row=0, column=0, columnspan=2, pady=20, sticky="n")

        self.subtitle = customtkinter.CTkLabel(master=self, 
                                            text="Sistema de Recomendação de Restaurante",
                                            font=self.create_font(SUBTITLE_FONT, 24))
        self.subtitle.grid(row=0, column=0, columnspan=2, pady=(70, 100), sticky="n")

        self.text_total_rest = customtkinter.CTkLabel(master=self, 
                                            text="Quantidade de Restaurantes Cadastrados: %d" %len(cfm.restaurants),
                                            font=self.create_font("Poppins", 18))
        self.text_total_rest.grid(row=3, column=0, padx=20, sticky="nsew")
        self.text_total_rest.anchor()

        self.text_total_users = customtkinter.CTkLabel(master=self, 
                                            text="Quantidade de Usuários Cadastrados: %d" %ifs.total_users,
                                            font=self.create_font("Poppins", 18))
        self.text_total_users.grid(row=4, column=0, padx=20, sticky="nsew")
        self.text_total_users.anchor()

        self.label_textbox = customtkinter.CTkLabel(master=self, 
                                            text="Insira o ID do Usuáio",
                                            font=self.create_font("Poppins", 18))
        self.label_textbox.grid(row=5, column=0, padx=20, pady=(50, 0), sticky="nsew")
        self.label_textbox.anchor()

        self.insert_userID = customtkinter.CTkEntry(master=self,
                                                border_width=0,  
                                                placeholder_text="Ex.: U1001", 
                                                font=self.create_font(SUBTITLE_FONT, 18))
        self.insert_userID.grid(row=6, column=0, padx=(50, 20), pady=(5, 0), sticky="nsew")
        self.insert_userID.anchor()

        self.button = customtkinter.CTkButton(master=self,
                                            command=self.button_callback, 
                                            text="Gerar Recomendações", 
                                            font=self.create_font(SUBTITLE_FONT, 18))
        self.button.grid(row=7, column=0, padx=(50, 20), pady=(15, 0), sticky="nsew")
        self.button.anchor()

        self.user_data = customtkinter.CTkLabel(master=self, 
                                            text='',
                                            font=self.create_font(SEMIBOLD_FONT, 18))
        self.user_data.grid(row=8, column=0, pady=(50, 0), sticky="nsew")

        self.amount_ratings_user = customtkinter.CTkLabel(master=self, 
                                            text='',
                                            font=self.create_font(SEMIBOLD_FONT, 18))
        self.amount_ratings_user.grid(row=9, column=0, sticky="nsew")

        self.recommendation_type = customtkinter.CTkLabel(master=self, 
                                            text="As recomendações aparecerão aqui",
                                            font=self.create_font(SEMIBOLD_FONT, 18))
        self.recommendation_type.grid(row=3, column=1, padx=(0, 20), pady=(0, 10), sticky="nsew")
        self.recommendation_type.anchor()
    
    def create_font(self, font_name, font_size):
        return customtkinter.CTkFont(family=font_name, size=font_size)

    def button_callback(self):
        user_id = self.insert_userID.get()
        username = ifs.return_user(user_id, ifs.user_profile)
        amount_ratings = ifs.counting_ratings_user(user_id, ifs.ratings_data)

        self.user_data.configure(text="Usuário: " + username)
        self.amount_ratings_user.configure(text="Restaurantes avaliados: %d" %amount_ratings)
        self.recommendation_type.configure(text=ifs.recommendation_type(amount_ratings))

        if amount_ratings == 0:
            self.option_var = customtkinter.StringVar(master=self)
            self.option_menu = customtkinter.CTkOptionMenu(master=self, 
                                                        values=["Maiores Notas", "Mais Avaliados"], 
                                                        variable=self.option_var,
                                                        command=self.optionmenu_callback, 
                                                        font=self.create_font(SUBTITLE_FONT, 16), 
                                                        dropdown_font=self.create_font("Poppins", 16))
            self.option_menu.grid(row=4, column=1, padx=(0, 20), sticky="ew")
            self.option_menu.anchor()
        else:
            self.scroll = customtkinter.CTkScrollbar(master=self)
            self.scroll.grid(row=4, column=1, rowspan=8, padx=(0, 0), sticky="e")

            self.recommendation = tk.Listbox(master=self, 
                                            font=self.create_font(SUBTITLE_FONT, 16), 
                                            yscrollcommand=self.scroll.set,
                                            highlightthickness=0,
                                            border=0,
                                            bg="#242424", fg="#fff")
            self.recommendation.grid(row=4, column=1, rowspan=8, padx=(0, 20), sticky="nsew")
            self.recommendation.anchor()

            self.scroll.configure(command=self.recommendation.yview)

            most_similar = cfm.cosine_similarity(user_id, cfm.final_ratings_matrix)
            recommended_restaurants = cfm.recommendation(user_id, most_similar, cfm.final_ratings_matrix)
            restaurants_data = cfm.restaurants_data(recommended_restaurants, cfm.restaurants)
            restaurants_data = [i for i in restaurants_data["name"]]
            
            for i in restaurants_data:
                self.recommendation.insert(tk.END, i)

        self.update_idletasks()

    def optionmenu_callback(self, option_var):
        order_by = self.option_menu.get()

        self.scroll = customtkinter.CTkScrollbar(master=self)
        self.scroll.grid(row=5, column=1, rowspan=8, padx=(0, 0), sticky="e")

        self.recommendation = tk.Listbox(master=self, 
                                        font=self.create_font(SUBTITLE_FONT, 16), 
                                        yscrollcommand=self.scroll.set,
                                        highlightthickness=0,
                                        border=0,
                                        bg="#242424", fg="#fff")
        self.recommendation.grid(row=5, column=1, rowspan=8, padx=(0, 20), pady=(10, 0), sticky="nsew")
        self.recommendation.anchor()

        self.scroll.configure(command=self.recommendation.yview)

        if order_by == "Maiores Notas":
            restaurants_data = pr.rating_rank
            restaurants_data = ["%s (%.2f | %d)" %(i, j, k) for i, j, k in zip(restaurants_data["place_name"], restaurants_data["rating"], restaurants_data["score"])]

            for i in restaurants_data:
                self.recommendation.insert(tk.END, i)
        else:
            restaurants_data = pr.score_rank
            restaurants_data = ["%s (%d | %.2f)" %(i, j, k) for i, j, k in zip(restaurants_data["place_name"], restaurants_data["score"], restaurants_data["rating"])]

            for i in restaurants_data:
                self.recommendation.insert(tk.END, i)
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
