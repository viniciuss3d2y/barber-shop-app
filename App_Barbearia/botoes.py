
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.animation import Animation
from kivy.properties import ObjectProperty, ColorProperty
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.utils import get_color_from_hex
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.app import App
import requests



class ImageButton(ButtonBehavior, Image):
    pass

class LabelButton(ButtonBehavior, Label):
    pass



# class GridlayoutCuston(ButtonBehavior, GridLayout):
#     def __init__(self, **kwargs):
#         self.rows = 1
#         super().__init__(**kwargs)
    
#     def on_touch_down(self, touch):
#         if self.collide_point(*touch.pos):
#             with self.canvas.before:
#                 self.color = Color(rgba=(0, 0, 0, 0.5))
#                 self.rect_sombra = RoundedRectangle(pos= self.pos, size =self.size,
#                                                 radius = [20,])
#             self.bind(pos=self.atualizar_rect, size=self.atualizar_rect)
        
#             anim = Animation(r=0,g=0.7, b=0, a=0.9)
#             anim.start(self.color)
    
  
    
#     def atualizar_rect(self):
#         self.rect_sombra.pos = self.pos
#         self.rect_sombra.size = self.size




# class LabelButtonCustom(ButtonBehavior, Label):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

#         with self.canvas.before:
#             self.color_botao = Color(rgba= get_color_from_hex("#4e3487"))
#             self.rect = RoundedRectangle(pos= self.pos, size= self.size, radius = [20])
        
#         self.cor_original = self.color_botao.rgba
#         self.bind(pos= self.atualizar_rect, size= self.atualizar_rect)
#         Window.bind(mouse_pos= self.verificar_pos_mouse)
  

#     def atualizar_rect(self, *args):
#         self.rect.pos = self.pos
#         self.rect.size = self.size
    
#     def verificar_pos_mouse(self, *args):
#         mouse_x, mouse_y = Window.mouse_pos

#         if self.collide_point(mouse_x, mouse_y):
#             self.color_botao.rgba = self.color_botao.rgba[0], self.color_botao.rgba[1], self.color_botao.rgba[2], 0.92

#         else:
#             self.color_botao.rgba = self.cor_original
    
#     def on_touch_down(self, touch):
#         if self.collide_point(*touch.pos):
#             anim = Animation(rgba = get_color_from_hex("#2D1E4D"), duration = 0.2)+Animation(rgba=self.cor_original, duration = 0.2)
#             anim.start(self.color_botao)
        
#         return super().on_touch_down(touch)




class LabelButtonHorarios(ButtonBehavior, Label):
    disponivel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  
        # booleana auxiliar para que a variavel quem contein o valor da altura original do widget permaneça com mesmo valor do inicio 
        # e nao acumule
        self.boo_height = True
        if self.boo_height:
            self.tamanho_original_height = self.height
            self.boo_height = False

        with self.canvas.before:    

            if self.disponivel == True:
                self.cor_rect = Color(rgba=get_color_from_hex("#0aab0a"))
                self.cor_original = self.cor_rect.rgba
            else:
                self.cor_rect = Color(rgba=get_color_from_hex("#e80822"))
                self.cor_original = self.cor_rect.rgba
            self.rect = RoundedRectangle(pos= self.pos, size= self.size, radius= [20])
        
        self.bind(pos= self.atualizar_rect, size= self.atualizar_rect)
        Window.bind(mouse_pos= self.verificar_pos_mous)

    

    def atualizar_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def verificar_pos_mous(self, *args):
        mouse_x, mouse_y = Window.mouse_pos
        local_x, local_y = self.to_widget(mouse_x, mouse_y)
        if self.collide_point(local_x, local_y):

            self.size_hint_y = None
            #self.size_hint_x = None
            self.height = self.tamanho_original_height + 10

            self.cor_rect.rgba = self.cor_original[0], self.cor_original[1], self.cor_original[2], 0.85

        else:

            self.height = self.tamanho_original_height
            self.cor_rect.rgba = self.cor_original
    
    def on_touch_down(self, touch):

        if self.collide_point(*touch.pos):
            # anim = Animation(rgba= get_color_from_hex("#033F03"), duration = 0.2)+Animation(rgba= self.cor_original, duration = 0.2)
            # anim.start(self.cor_rect)
            self.cor_rect.rgba =  self.cor_rect.rgba[0],  self.cor_rect.rgba[1],  self.cor_rect.rgba[2], 0.4


        return super().on_touch_down(touch)




class LabelButtonCustomizado(ButtonBehavior, Label):
    cor_canvas = ColorProperty((0, 0, 0, 0))
    # tamnho do wwidget passado no arquivo   
    tamanho_original =  ObjectProperty((0.2, 1))
    font_size_original = ObjectProperty('17sp')  
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mudar_cor_botao = False

        with self.canvas.before:
            self.cor = Color(rgba= self.cor_canvas)
            self.rect = RoundedRectangle(pos= self.pos, size= self.size, radius= [20])
        self.bind(pos= self.atualizar_rect,size= self.atualizar_rect)

        Window.bind(mouse_pos= self.update_cor_canvas)

    def update_cor_canvas(self, *args):
        mouse_x, mouse_y = Window.mouse_pos
        
        if self.collide_point(mouse_x, mouse_y):

            self.size_hint = (self.tamanho_original[0]* 1.1, self.tamanho_original[1]* 1.1)
            #self.cor.rgba = self.cor_canvas[0], self.cor_canvas[1], self.cor_canvas[2], 0.8
            tamanho_font = int(self.font_size_original.replace("sp", "")) + 3
            self.font_size = str(tamanho_font)+'sp'

            
            if self.mudar_cor_botao:             
                # dark_color = [x * 0.1 for x in self.cor.rgba[:3]]+ [1]
                self.cor.rgba = self.dark_color

        else:
            self.font_size = self.font_size_original
            self.mudar_cor_botao = False
            self.size_hint = self.tamanho_original
            self.cor.rgba = self.cor_canvas



    def atualizar_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


    def on_touch_down(self, touch):   #get_color_from_hex("#2D1E4D")
          
        if self.collide_point(*touch.pos):

            self.mudar_cor_botao = True
            self.dark_color = [x * 0.5 for x in self.cor.rgba[:3]]+ [1]
            # anim = Animation(rgba = dark_color, duration = 0.2)+Animation(rgba=self.cor_canvas, duration = 0.2)
            # anim.start(self.cor)
            self.cor.rgba = self.dark_color
        
        return super().on_touch_down(touch)
    


class ImageButtonPerfil(ButtonBehavior, Image):
    tamanho_original = ObjectProperty([100.0, 50.0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
        Window.bind(mouse_pos= self.aumentar_tamanho_foto)

    def aumentar_tamanho_foto(self, *args):
        mouse_x, mouse_y = Window.mouse_pos
        local_x, local_y = self.to_widget(mouse_x, mouse_y)

        if self.collide_point(local_x, local_y):

            self.size_hint_x = None
            self.size_hint_y = None
            self.size = [self.tamanho_original[0] + 7, self.tamanho_original[1] + 7]

        else:
            self.size = self.tamanho_original



class ImageButtonZoom(ButtonBehavior, Image):
    tamanho_original = ObjectProperty((1, 1))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



    def on_touch_down(self, touch):

        if self.collide_point(*touch.pos) and self.size_hint == [*self.tamanho_original]:
                
                self.size_hint = [self.tamanho_original[0]* 2, self.tamanho_original[1]* 2]

        else:
            self.size_hint = self.tamanho_original




class TongleButtonCuston(ButtonBehavior, FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.is_open = False

        with self.canvas.before:#get_color_from_hex("#c2c3c3"     
            self.cor_canvas = Color(rgba= (get_color_from_hex("FFFFFF")))
            self.rect = RoundedRectangle(pos= self.pos, size= self.size, radius= [20])


        self.widget_circle = FloatLayout()
        self.widget_circle.size_hint = (None, None)
        self.widget_circle.pos = self.pos
        self.widget_circle.size = (self.size[1] * 0.88, self.size[1] * 0.88)
        

        with self.widget_circle.canvas.after:
            self.cor = Color(rgba= get_color_from_hex("#FFFFFF"))
            self.circle = Ellipse(size =self.widget_circle.size, pos= self.widget_circle.pos)
        
        self.bind(pos= self.atualizar_rect, size= self.atualizar_rect)
        self.widget_circle.bind(pos= self.atualizar_circle, size= self.atualizar_circle)

        self.add_widget(self.widget_circle)

    def atualizar_rect(self, *args):
        # a interface carrega primeiro entao self.meu_aplicativo.is_open nao sera iniciado e nao tera nenhum valor 
        # entao coloca try-except pra nao dar erro
        try:
            self.meu_aplicativo = App.get_running_app()
            self.is_open = self.meu_aplicativo.is_open
        except:
            pass

        if self.is_open == True:
            self.cor_canvas.rgba = get_color_from_hex("#4dfd4e")
            self.widget_circle.right = self.right - (self.size[0]* 0.017)

        else:
            self.cor_canvas.rgba = get_color_from_hex("#fb2b38")
            self.widget_circle.x = self.x + (self.size[0]* 0.017)
            
        self.rect.pos = self.pos
        self.rect.size = self.size

        self.widget_circle.y = self.y + 4
        self.widget_circle.size = (self.size[1] * 0.88, self.size[1] * 0.88)
        

    def atualizar_circle(self, *args):
        self.circle.pos = self.widget_circle.pos
        self.circle.size = self.widget_circle.size

    
    def on_touch_move(self, touch):
        if self.widget_circle.collide_point(*touch.pos):    #self.widget_circle.right <= self.right or     
    
            if  touch.pos[0] < self.right : 
                if touch.pos[0] > self.x:

                    self.widget_circle.center_x = touch.pos[0]
                    self.widget_circle.center_y = self.center_y
            
        return super().on_touch_move(touch)
    
    
    def on_touch_up(self, *args):
        self.is_open = self.meu_aplicativo.is_open

        if self.widget_circle.center_x >= self.center_x:
            self.widget_circle.right = self.right - (self.size[0]* 0.017)

            if self.is_open != True:
                self.cor_canvas.rgba = get_color_from_hex("#4dfd4e")            
                self.meu_aplicativo.alterar_valor_is_open_thread(self.is_open)
                self.meu_aplicativo.verificar_barbearia_aberta()

        else:
            self.widget_circle.x = self.x + (self.size[0]* 0.017)

            if self.is_open == True:
                self.cor_canvas.rgba = get_color_from_hex("#fb2b38")             
                self.meu_aplicativo.alterar_valor_is_open_thread(self.is_open)
                self.meu_aplicativo.verificar_barbearia_aberta()




class ImageButtonVoltar(ButtonBehavior, Image):

    size_hint_original = ObjectProperty((1, 1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            self.cor_canvas = Color(rgba=(1, 1, 1, 1))
            self.ellipse = Ellipse(size= (self.size[1], self.size[1]), pos= self.pos)
        self.cor_original = self.cor_canvas.rgba
        self.size_hint_original = self.size_hint

        Window.bind(mouse_pos= self.verificar_pos_mouse)
        self.bind(pos= self.atualizar_rect, size= self.atualizar_rect, parent= self.on_parent)



        
    
    def verificar_pos_mouse(self, *args):

        mouse_x, mouse_y = (Window.mouse_pos)
        local_x, local_y = self.to_widget(mouse_x, mouse_y)

        if self.collide_point(local_x, local_y):
            self.cor_canvas.rgba = (0, 0, 0, 0.15)

        else: 
            self.cor_canvas.rgba = self.cor_original



    def atualizar_rect(self, *args):
        self.tamanho = [self.size_hint_original[0] * Window.width, self.size_hint_original[0] * Window.width] 
        self.size = self.tamanho
        self.size_hint_x = None
        self.size_hint_y = None  
        self.ellipse.pos = [self.pos[0] - 2.5, self.pos[1] - 2.5]
        self.ellipse.size= [self.size[0] + 5, self.size[0]+ 5]

        
        

    def on_size(self, *args):

        self.ellipse.pos = (self.pos[0] - 2.5, self.pos[1] - 2.5)
        self.ellipse.size= [self.size[0] + 5, self.size[0] + 5]

    def on_parent(self, *args):
        self.tamanho = [self.size_hint_original[0] * Window.width, self.size_hint_original[0] * Window.width] 
        self.size = self.tamanho
        