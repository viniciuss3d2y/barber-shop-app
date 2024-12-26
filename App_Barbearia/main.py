from kivy.config import Config

# Ativar anti-aliasing
Config.set('graphics', 'multisamples', '8')
from kivy.app import App
from kivy.lang import Builder
import requests
import os
import certifi
from telas import*
from botoes import*
from bannerhorarios import BannerHorarios
from myfirebase import MyFirebase
from datetime import datetime
import pytz
from banneradmin import BannerAdmin
from botoeshomepage import BotoesHomepage
from popup import MyPopUp
from fundo_loading import FundoLoading
import threading
from bannerperfil import BannerPerfil
import time
from isopen import IsOpen
from bannerhorarios import BannerHorarios
from firebaseadmin import FirebaseAdmin
from firebase_admin import db

__version__ = "1.0.1"
os.environ["SSL_CERT_FILE"] = certifi.where()

GUI = Builder.load_file("main.kv")
class MainApp(App):
    myfirebase = MyFirebase()


    horario_agendado = None

    def build(self):
        return GUI

    def on_start(self):
        self.myfirebase.trocar_token()
        #self.carregar_foto_usuario()
        #self.verificar_barbearia_aberta()
        #self.adicionar_botoes_homepage())

        
    
    def mudar_tela(self, id_tela):
        screenmanager = self.root.ids["screenmanager"]
        screenmanager.current = id_tela
        
        if id_tela == "homepage":
            self.adicionar_botoes_homepage()

    

    def carregar_horarios(self, *args):
        dict_horarios = {}
        requisicao = requests.get("https://app-barbearia-a2a48-default-rtdb.firebaseio.com/.json")
        requisicao_dic = requisicao.json()
        pagina_horarios = self.root.ids["horariospage"]
        for horario in requisicao_dic:
            horario_formatado = horario.replace(":00", "")
            dict_horarios[horario_formatado] = requisicao_dic[horario]['disponivel']
            dict_horarios =  dict(sorted(dict_horarios.items(), key=lambda item: int(item[0])))
        # toda vez que o usuario entra nesta pagina todos os widgets sao removidos e criados novamente , isso evita que eles se multipliquem
        for widget in list(pagina_horarios.ids["lista_horarios"].children):
            pagina_horarios.ids["lista_horarios"].remove_widget(widget)

        for chave in dict_horarios:
            banner = BannerHorarios(horario = chave, disponivel = dict_horarios[chave])
            pagina_horarios.ids["lista_horarios"].add_widget(banner)

        self.remover_horario()
        self.mudar_tela("horariospage")


    def remover_popup_horarios(self, *args):
        pagina_horarios = self.root.ids["horariospage"]
        popup = pagina_horarios.ids["pop_up"]
        for widget in list(popup.children):
            popup.remove_widget(widget)
    

    def comprimento_usuario(self):
        link = "https://users-arbearia-default-rtdb.firebaseio.com"
        requisicao = requests.get(f"{link}/users/{self.local_id}/nome_usuario.json?auth={self.id_token}")

        nome_usuario = requisicao.json()
        homepage = self.root.ids["homepage"]
        homepage.ids["mensagem_comprimentar_usuario"].text = f"[color=#4e3487]Eai,[/color] [color=#00ff2e]{nome_usuario}[/color]"



    def salvar_horario_agendado(self, horario, *args):

        self.horario_agendado = horario+":00"
        
        requisicao = requests.get(f"https://users-arbearia-default-rtdb.firebaseio.com/users/{self.local_id}.json?auth={self.id_token}")
        requisicao_dic = requisicao.json()
        nome_cliente = requisicao_dic['nome_usuario']

        info = {"cliente": nome_cliente}
        requests.patch(f"https://users-arbearia-default-rtdb.firebaseio.com/horarios_agendados/{horario+":00"}.json?auth={self.id_token}",
                       json= info)

        # alterar a disponibilidade do horario
        info_dispo_horario = {"disponivel": False}
        requests.patch(f"https://app-barbearia-a2a48-default-rtdb.firebaseio.com/{horario+":00"}.json",
                       json=info_dispo_horario)
        
        self.remover_popup_horarios()
    	


    def carregar_horarios_admin(self, *args):

        #requisicao = requests.get(f"https://users-arbearia-default-rtdb.firebaseio.com/horarios_agendados.json?auth={self.id_token}")
        ref = db.reference('/horarios_agendados')
        requisicao_dic = ref.get()

        admin_page = self.root.ids["adminpage"]
        for widget in list(admin_page.ids["lista_horarios_marcados"].children):
            admin_page.ids["lista_horarios_marcados"].remove_widget(widget)

        try:
            for horario in requisicao_dic:
                banner_admin = BannerAdmin(nome_cliente = requisicao_dic[horario]['cliente'], horario_marcado = horario)
                admin_page.ids["lista_horarios_marcados"].add_widget(banner_admin)
        except:
            pass  
        
        self.mudar_tela("adminpage")

    
    def carregar_admin_page(self):

        requisicao = requests.get(f"https://users-arbearia-default-rtdb.firebaseio.com/users/{self.local_id}.json?auth={self.id_token}")
        requisicao_dic = requisicao.json()
        
        is_admin = requisicao_dic['is_admin']

        if is_admin:
            self.firebase_admin = FirebaseAdmin()
            homepage = self.root.ids["homepage"]
            botao_admin = BotoesHomepage(texto = "Admin", imagem = "icones/admin.png",
                                          funcao_botao = self.carregar_horarios_admin)
            homepage.ids["grid_botoes"].add_widget(botao_admin)

        
    def remover_horario(self):
        horarios_page = self.root.ids["horariospage"]
        fuso_brasilia = pytz.timezone('America/Sao_Paulo')
        hora_atual = datetime.now(fuso_brasilia).strftime('%H')
        
        lista_horarios = horarios_page.ids["lista_horarios"]

      
        for widget_pai in list(lista_horarios.children):
            for widget in list(widget_pai.children):
                for widinho in list(widget.children):

                    if hasattr(widinho, 'text'):
                        busca_doispontos = widinho.text.find(":")
                        horario = widinho.text[:busca_doispontos]

                        if int(hora_atual) > int(horario):
                            lista_horarios.remove_widget(widget_pai)




    
    def abrir_todos_horarios(self, *args):
      
        requisicao = requests.get("https://app-barbearia-a2a48-default-rtdb.firebaseio.com/.json")
        requisicao_dic = requisicao.json()
        for horario in requisicao_dic:
            if requisicao_dic[horario]['disponivel'] == False:
                info = {"disponivel": True}
                requests.patch(f"https://app-barbearia-a2a48-default-rtdb.firebaseio.com/{horario}.json",
                            json=info)     

    # executar a funcao abrir_todos_horarios em outra thread
    def abrir_todos_hrr_thread(self, *args):
        self.desenhar_loading("adminpage", 6)
        self.remover_popup_admin()
        thread = threading.Thread(target= self.abrir_todos_horarios)
        thread.start()
        


    def fechar_todos_horarios(self, *args):
        requisicao = requests.get("https://app-barbearia-a2a48-default-rtdb.firebaseio.com/.json")
        requisicao_dic = requisicao.json()

        for horario in requisicao_dic:
            if requisicao_dic[horario]['disponivel'] == True:

                info = {"disponivel": False}
                requests.patch(f"https://app-barbearia-a2a48-default-rtdb.firebaseio.com/{horario}.json",
                            json=info)
                
        self.remover_popup_admin()      

    # executar a funcao fechar_todos_horarios em outra thread
    def fechar_todos_hrr_thread(self, *args):
        self.desenhar_loading("adminpage", 6)
        self.remover_popup_admin()
        thread = threading.Thread(target= self.fechar_todos_horarios)
        thread.start()






    
    def excluir_horarios_agendados(self):
        ref = db.reference('/horarios_agendados')
        ref.delete()
        #requests.delete(f"https://users-arbearia-default-rtdb.firebaseio.com/horarios_agendados.json?auth={self.id_token}")




    def adicionar_botoes_homepage(self):

        homepage = self.root.ids["homepage"]
        # remove o botao de perfil e horarios e adiciona eles novamente para nao acumular
        try:
            for widget_pai in list(homepage.ids["grid_botoes"].children):
                for widget_filho in list(widget_pai.children):
                    for widget_neto in list(widget_filho.children):
                       
                        if hasattr(widget_neto, "text") and widget_neto.text != "Admin":

                            #homepage.ids["grid_botoes"].remove_widget(widget)
                            homepage.ids["grid_botoes"].remove_widget(widget_pai)
                    
        except Exception as e:

            pass

        botao_horario = BotoesHomepage(texto = "Horários", imagem = "icones/horarios.png",
                                          funcao_botao = self.carregar_horarios)
        botao_perfil = BotoesHomepage(texto = "Perfíl", imagem = f"fotos_perfil/{self.foto_perfil_usuario}",
                                          funcao_botao = self.carregar_fotos_perfil)
        homepage.ids["grid_botoes"].add_widget(botao_horario)
        homepage.ids["grid_botoes"].add_widget(botao_perfil)



    def mostrar_popup_admin(self, texto , funcao_botao_sim):
        self.remover_popup_admin()
        adminpage = self.root.ids["adminpage"]
        popup = MyPopUp(text_popup = texto, funcao_botao_sim = funcao_botao_sim,
                        funcao_botao_nao = self.remover_popup_admin)
                        
        adminpage.ids["pop_up"].add_widget(popup)
    
    def remover_popup_admin(self, *args):
        pagina_horarios = self.root.ids["adminpage"]
        popup = pagina_horarios.ids["pop_up"]
        for widget in list(popup.children):
            popup.remove_widget(widget)




    def desenhar_loading(self, pagina, tempo_execucao):
        fundo_loading = FundoLoading(pagina = pagina, tempo_execucao = tempo_execucao)




    def carregar_fotos_perfil(self, *args):

        perfilpage = self.root.ids["perfilpage"]
        lista_arquivos_fotos = os.listdir("fotos_perfil")
        for widget in list(perfilpage.ids["lista_fotos_perfil"].children):
            perfilpage.ids["lista_fotos_perfil"].remove_widget(widget)

        for arquivo in lista_arquivos_fotos:
            banner_perfil = BannerPerfil(foto = arquivo)
            perfilpage.ids["lista_fotos_perfil"].add_widget(banner_perfil)


        
        self.mudar_tela("perfilpage")

    
    def carregar_foto_usuario(self):
        requisicao = requests.get(f"https://users-arbearia-default-rtdb.firebaseio.com/users/{self.local_id}.json?auth={self.id_token}")
        requisicao_dic = requisicao.json()
        
        self.foto_perfil_usuario = requisicao_dic['foto_usuario']
        perfil_page = self.root.ids["perfilpage"]
        perfil_page.ids["foto_usuario"].source = f"fotos_perfil/{self.foto_perfil_usuario}"
    

    def mudando_foto_perfil(self, nova_foto, *args):

        info = {"foto_usuario": nova_foto}
        requests.patch(f"https://users-arbearia-default-rtdb.firebaseio.com/users/{self.local_id}.json?auth={self.id_token}",
                                    json= info)
        self.carregar_foto_usuario()

    def mudar_foto_perfil_thread(self, nova_foto, *args):

        thread = threading.Thread(target= self.mudando_foto_perfil, args=(nova_foto,))
        thread.start()
        carregamento = FundoLoading(tempo_execucao = 0.8, pagina = "perfilpage")
        

    def verificar_barbearia_aberta(self):

        requisicao = requests.get(f"https://users-arbearia-default-rtdb.firebaseio.com/is_open.json?auth={self.id_token}") 
        homepage = self.root.ids["homepage"]
        self.is_open = requisicao.json()

        for widget in list(homepage.ids["teste"].children):
            if hasattr(widget, "text"):
                if widget.text == "ABERTO" or widget.text == "FECHADO":
                    homepage.ids["teste"].remove_widget(widget)

        if requisicao.json() == True:
 
            barbearia_aberta = IsOpen(text = "ABERTO", cor_canvas = get_color_from_hex("#25be31"))
            homepage.ids["teste"].add_widget(barbearia_aberta)

        else:

            barbearia_aberta = IsOpen(text = "FECHADO", cor_canvas = get_color_from_hex("#fb0c2d"))
            homepage.ids["teste"].add_widget(barbearia_aberta)



    
    def alterar_valor_is_open(self, valor):
        
        if valor != True:
            ref = db.reference('/')
            ref.update({"is_open": True})

            #requests.patch(f"https://users-arbearia-default-rtdb.firebaseio.com/.json?auth={self.id_token}",
                        #json= info)
        else:
            
            ref = db.reference('/')
            ref.update({"is_open": False})
            # requests.patch(f"https://users-arbearia-default-rtdb.firebaseio.com/.json?auth={self.id_token}",
            #     json= info)

    def alterar_valor_is_open_thread(self, valor):
        thread = threading.Thread(target= self.alterar_valor_is_open, args= (valor,))
        thread.start()


    def mensagem_homepage_aviso(self):

        requisicao = requests.get(f"https://users-arbearia-default-rtdb.firebaseio.com/mensagem.json?auth={self.id_token}")
        homepage = self.root.ids["homepage"]
        homepage.ids["mensagem_aviso"].text = requisicao.json()


MainApp().run()
