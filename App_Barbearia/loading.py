
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock
import math



class Loading(Widget):
    def __init__(self, **kwargs):
        super().__init__()
        self.velocidade_angular = 200
        self.raio = 40
        self.cx, self.cy = self.center
        self.nmr_bolas = 10
        self.raio_bola = 7
        self.lista_angulos = [i * 35 for i in range(self.nmr_bolas)]

        self.lista_bolas = []
        for j in range(self.nmr_bolas):
            with self.canvas:
                Color(rgba=(1, 1, 1, j/10))
                self.bola = Ellipse(size=(self.raio_bola*2, self.raio_bola*2))
            self.lista_bolas.append(self.bola)
        Clock.schedule_interval(self.update, 0.020)

    def update(self, dt):
        for i in range(self.nmr_bolas):

            radius_ang = math.radians(self.lista_angulos[i])

            x = self.cx + self.raio * math.cos(radius_ang) - self.raio_bola
            y = self.cy + self.raio * math.sin(radius_ang) - self.raio_bola

            self.lista_bolas[i].pos = (x, y)

            self.lista_angulos[i] += self.velocidade_angular * dt

            if self.lista_angulos[i] >= 360:
                self.lista_angulos[i] -= 360
        
    def on_size(self, *args):
        self.cx, self.cy = self.center

