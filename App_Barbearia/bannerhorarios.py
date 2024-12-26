from kivy.uix.gridlayout import GridLayout
#from kivy.utils import get_color_from_hex
from botoes import  LabelButtonHorarios
from popup import MyPopUp
from functools import partial
from kivy.app import App
from kivy.animation import Animation
import time




class BannerHorarios(GridLayout):
    
    def __init__(self, **kwargs):
        
        super().__init__()
        self.rows = 1

        self.horario = kwargs["horario"]
        self.disponivel = kwargs["disponivel"]
        
        self.layout = GridLayout()  
        self.layout.rows = 1

        self.label_horario =LabelButtonHorarios(text = self.horario + ":00",
                      font_size = '20sp', bold = True, size = (50, 70),
                      on_release = self.mostrar_popup, disponivel = self.disponivel)
               
        #print(f'neymar {self.label_horario.height}')
                
        self.layout.add_widget(self.label_horario)

        self.add_widget(self.layout)


    def mostrar_popup(self, *args):
        #time.sleep(0.3)
        meu_aplicativo = App.get_running_app()
        pagina_horarios = meu_aplicativo.root.ids["horariospage"]

        horario = self.label_horario.text
        # requisicao = requests.get(f"https://app-barbearia-a2a48-default-rtdb.firebaseio.com/{horario}.json")
        # requisicao_dic = requisicao.json()
        
        if self.disponivel == True:
            for widget in list(pagina_horarios.ids["pop_up"].children):
                pagina_horarios.ids["pop_up"].remove_widget(widget)
            text_popup = f"Você quer agendar horario para as [color=#f8ff00]{self.horario + ":00"}[/color]?"
            popup = MyPopUp(text_popup = text_popup, 
                            funcao_botao_sim = partial(meu_aplicativo.salvar_horario_agendado, self.horario),
                            funcao_botao_nao = meu_aplicativo.remover_popup_horarios)
                              
                            
            pagina_horarios.ids["pop_up"].add_widget(popup)
            
    

            

        
