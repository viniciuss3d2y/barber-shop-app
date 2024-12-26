from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle


class IsOpen(FloatLayout):
    def __init__(self, **kwargs) :
        super().__init__()

        self.text = kwargs['text']
        self.cor_canvas = kwargs['cor_canvas']

        self.label = Label(text= self.text, pos_hint= {"center_x": 0.5, "top": 0.66}, size_hint = (0.25, 0.09),
                           bold= True, font_size= '20sp')
        
        with self.label.canvas.before:
            Color(rgba= self.cor_canvas)
            self.rect = RoundedRectangle(pos= self.label.pos, size = self.label.size, radius = [20])

        self.label.bind(pos= self.atualizar_rect, size= self.atualizar_rect)

        self.add_widget(self.label)

    def atualizar_rect(self, *args):
        self.rect.pos = self.label.pos
        self.rect.size = self.label.size