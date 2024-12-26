from kivy.uix.gridlayout import GridLayout
from botoes import ImageButtonPerfil
from functools import partial
from kivy.app import App


class BannerPerfil(GridLayout):
    def __init__(self, **kwargs):
        self.rows = 1
        super().__init__()    
        self.meu_aplicativo = App.get_running_app()                           

        self.foto = kwargs['foto']
        
        self.image = ImageButtonPerfil(source = f"fotos_perfil/{self.foto}",
                                       tamanho_original = self.size, on_release = partial(self.meu_aplicativo.mudar_foto_perfil_thread, self.foto))

        self.add_widget(self.image)