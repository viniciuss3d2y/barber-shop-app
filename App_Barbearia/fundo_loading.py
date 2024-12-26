from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Color
from kivy.app import App
from kivy.clock import Clock
from loading import Loading


class FundoLoading(GridLayout):
    def __init__(self, **kwargs):
        super().__init__()

        self.pagina = kwargs['pagina']
        self.tempo_execucao = kwargs['tempo_execucao']


        self.meu_aplicativo = App.get_running_app()
        self.pagina = self.meu_aplicativo.root.ids[self.pagina]
        self.loading = Loading()

        self.pos_hint = {"right": 1, "top": 1}
        self.size_hint = (1, 1)

        with self.canvas.after:
            Color(rgba=(0, 0, 0, 0.7))
            self.rect = Rectangle(pos= self.pos, size= self.size)
        self.bind(pos= self.atualizar_rect, size= self.atualizar_rect)
        
        
        self.pagina.add_widget(self)
        self.pagina.add_widget(self.loading)
        self.desativar_interacao()
    

    def desativar_interacao(self):
        self.pagina.disabled = True

        Clock.schedule_once(self.reativar_interacao, self.tempo_execucao)

    def reativar_interacao(self, time):
        self.pagina.disabled = False
        self.pagina.remove_widget(self)
        self.pagina.remove_widget(self.loading)





    def atualizar_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


    