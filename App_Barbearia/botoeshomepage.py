from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from botoes import LabelButtonCustomizado
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex
from kivy.animation import Animation




class BotoesHomepage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.rows = 1
        self.meu_aplicativo = App.get_running_app()

        self.texto = kwargs['texto']
        self.imagem = kwargs['imagem']    
        self.funcao_botao = kwargs["funcao_botao"]                              #text_size=(50, None),

        self.layout = FloatLayout()
        
        self.botao = LabelButtonCustomizado(text = self.texto, pos_hint = {"center_x": 0.5, "center_y":0.5},                                           
                                          bold = True, font_size = '17sp',  size_hint=(0.8, 1),
                                           on_release= self.funcao_botao,tamanho_original= (0.8, 1), 
                                           cor_canvas = get_color_from_hex("#4e3487"), font_size_original = '17sp')
        
        self.image = Image(source= self.imagem, pos_hint = {"right": self.botao.pos[0] + 25/100 , "center_y":0.5},
                            size_hint=(0.1, 0.5))
        self.botao.bind(size_hint= self.atualizar_tamanho_image)
        
        self.botao.bind(pos= self.atualizar_pos_imagem)
        
        
        self.layout.add_widget(self.botao)
        self.layout.add_widget(self.image)
        self.add_widget(self.layout)

    
    def atualizar_pos_imagem(self, *args):
        self.image.pos[0] = self.botao.pos[0] + 30/100

    
    def atualizar_tamanho_image(self, *args):
  
        if self.image.size_hint == [0.1, 0.5]:
            self.image.size_hint = [0.15, 0.8]
        else:
            self.image.size_hint = [0.1, 0.5]