from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from botoes import ImageButton, LabelButton



class MyPopUp(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__()
        self.meu_aplicativo = App.get_running_app()

        self.text_popup = kwargs["text_popup"]
        self.funcao_botao_sim = kwargs["funcao_botao_sim"]
        self.funcao_botao_nao = kwargs["funcao_botao_nao"]



        self.image_x = ImageButton(source= "icones/x.png",  pos_hint = {"right": 1.03, "top":1.03}, size_hint=(0.09, 0.09),
                                   on_release= self.funcao_botao_nao)


        self.label_texto = Label(text = self.text_popup,
                             pos_hint = {"center_x": 0.5, "top":0.87}, size_hint=(0.8, 0.1),
                                            bold = True, markup = True, text_size = (200, 100),
                                              halign='center', valign='middle', font_size = "23sp")

        self.label_desistir =  LabelButton(text = "Não", pos_hint = {"right": 0.4, "top":0.45}, size_hint=(0.3, 0.2),
                                            font_size = "20sp", bold = True, on_release= self.funcao_botao_nao)
        
        with self.label_desistir.canvas.before:
            Color(rgba=get_color_from_hex("#00796B"))
            self.rect_desistir = RoundedRectangle(pos=self.pos, size= self.size, radius = [16,])
        self.label_desistir.bind(pos= self.atualizar_rect_labels, size= self.atualizar_rect_labels)


        self.label_confirmar =  LabelButton(text = "Sim", pos_hint = {"right": 0.9, "top":0.45}, size_hint=(0.3, 0.2),
                                              font_size = "20sp", bold = True,
                                              on_release= self.funcao_botao_sim)
        
        with self.label_confirmar.canvas.before:
            Color(rgba=get_color_from_hex("#00796B"))
            self.rect_confirmar = RoundedRectangle(pos=self.pos, size= self.size, radius = [16,])
        self.label_confirmar.bind(pos= self.atualizar_rect_labels, size= self.atualizar_rect_labels)

        # canvas do Gridlayou
        with self.canvas.before:
            Color(rgba= get_color_from_hex("#4e3487"))
            self.rect = RoundedRectangle(pos=self.pos, size= self.size, radius = [11,])
        self.bind(pos = self.atualizar_rect, size = self.atualizar_rect)


        self.add_widget(self.label_texto)
        self.add_widget(self.label_desistir)
        self.add_widget(self.label_confirmar)
        self.add_widget(self.image_x)


    def atualizar_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def atualizar_rect_labels(self, *args):
        self.rect_confirmar.pos = self.label_confirmar.pos
        self.rect_confirmar.size = self.label_confirmar.size

        self.rect_desistir.pos = self.label_desistir.pos
        self.rect_desistir.size = self.label_desistir.size