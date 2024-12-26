from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle



class BannerAdmin(GridLayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.rows = 1                                                                                     

        self.nome_cliente = kwargs['nome_cliente']
        self.horario_marcado = kwargs['horario_marcado']


        with self.canvas.before:
            Color(rgba=(76 / 255, 30 / 255, 86 / 255, 0.76))
            self.rect = RoundedRectangle(pos=self.pos, size= self.size, radius= [20])
        self.bind(pos= self.atualizar_rect, size= self.atualizar_rect)

        with self.canvas.before:
            Color(rgba=(0, 0, 0, 0.16))
            self.rect_sombra = RoundedRectangle(pos=(self.pos[0] + 5, self.pos[1] + 5), size= self.size, radius = [20])


        self.layout = FloatLayout()

        self.label_nome = Label(text = self.nome_cliente, pos_hint = {"right": 0.5, "top":0.5}, size_hint=(0.5, 0.1),
                                   bold = True, font_size = '20sp')
        
        self.label_horario = Label(text = self.horario_marcado, pos_hint = {"right": 1, "top":0.5}, size_hint=(0.5, 0.1),
                                   bold = True, font_size = '20sp')

        self.layout.add_widget(self.label_nome)
        self.layout.add_widget(self.label_horario)

        self.add_widget(self.layout)


    def atualizar_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

        self.rect_sombra.pos = self.pos#(self.pos[0] + 5, self.pos[1] + 5)
        self.rect_sombra.size = (self.size[0] + 5, self.size[1] + 5)