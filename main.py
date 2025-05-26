import tkinter as tk
from tkinter import ttk
from visao.main_view import MainView
from visao.cliente_create_view import ClientView
from visao.veiculo_create_view import VehicleView
from visao.locacao_create_view import RentalView
from visao.multa_create_view import FineView
from persistencia.database import Database # Importe o módulo do banco de dados

def iniciar_aplicacao():
    app = MainView()
    app.mainloop()

iniciar_aplicacao()

