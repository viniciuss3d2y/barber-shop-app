from kivy.app import App
import requests


class MyFirebase:
    API_KEY = "AIzaSyC3TGzyg1EgeJ53MFMtVy9Gf4vGFS9UViU"

    def criar_conta(self, email, senha, nome):
        meu_aplicativo = App.get_running_app()
        contagem_caractere = ""
        for caractere in nome:
            try:
                tenta = int(caractere)
            except:
                contagem_caractere += caractere
                pass
            
        if len(nome) <= 35:
            if len(nome) > 5:
                if len(contagem_caractere) >= 4:

                    info = {"email": email,
                            "password": senha,
                            "returnSecureToken": True}
                    requisicao = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}",
                                            json=info)
                    requisicao_dic = requisicao.json()
                    
                    
                    if requisicao.ok:

                        local_id = requisicao_dic['localId']
                        id_token = requisicao_dic['idToken']
                        refresh_token = requisicao_dic['refreshToken']

                        # requisicao pegar id para este novo usuario e atualizar o id para o proximo novo usuario
                        requisicao_id = requests.get(f"https://users-arbearia-default-rtdb.firebaseio.com/id_proximo_usuario.json?auth={id_token}") 
                        id_novo_usuario = requisicao_id.json()

                        id_proximo_usuario = int(requisicao_id.json()) + 1
                        info_id_prox_user = {"id_proximo_usuario": id_proximo_usuario}
                        requests.patch(f"https://users-arbearia-default-rtdb.firebaseio.com/.json?auth={id_token}",
                                    json=info_id_prox_user)      

                        meu_aplicativo.id_token = id_token
                        meu_aplicativo.local_id = local_id
                        email_usuario = requisicao_dic['email']
                        # requisicao salvar informacoes do novo usuario
                        info_new_user = {"email": email_usuario,
                                         "nome_usuario": nome,
                                        "id_usuario":id_novo_usuario,
                                        "is_admin": False,
                                        "foto_usuario": "foto0.png"}
                        requests.patch(f"https://users-arbearia-default-rtdb.firebaseio.com/users/{local_id}.json?auth={id_token}",
                                            json=info_new_user)
                                        
                        with open("refresh_token.txt", "w") as  arquivo:
                            arquivo.write(refresh_token)


                        meu_aplicativo.mensagem_homepage_aviso()
                        meu_aplicativo.carregar_foto_usuario()
                        meu_aplicativo.adicionar_botoes_homepage()
                        meu_aplicativo.carregar_admin_page()   
                        meu_aplicativo.verificar_barbearia_aberta()                    
                        meu_aplicativo.mudar_tela("homepage")

                    else:
                        pagina_criar_conta = meu_aplicativo.root.ids["criarcontapage"]
                        pagina_criar_conta.ids["mensagem_alerta"].text = requisicao_dic['error']['message']
                        pagina_criar_conta.ids["mensagem_alerta"].color = (1, 0, 0, 1)

                else:

                    pagina_criar_conta = meu_aplicativo.root.ids["criarcontapage"] 
                    pagina_criar_conta.ids["mensagem_alerta"].text = "Seu nome deve conter 4 ou mais letras"
                    pagina_criar_conta.ids["mensagem_alerta"].color = (1, 0, 0, 1)

            else:             
                pagina_criar_conta = meu_aplicativo.root.ids["criarcontapage"] 
                pagina_criar_conta.ids["mensagem_alerta"].text = "Porfavor escolha um nome com mais de 5 caracteres"
                pagina_criar_conta.ids["mensagem_alerta"].color = (1, 0, 0, 1)

        else:
            pagina_criar_conta = meu_aplicativo.root.ids["criarcontapage"] 
            pagina_criar_conta.ids["mensagem_alerta"].text = "Porfavor escolha um nome com menos de 35 caracteres"
            pagina_criar_conta.ids["mensagem_alerta"].color = (1, 0, 0, 1)

            

    def fazer_login(self, email, senha):
        meu_aplicativo = App.get_running_app()

        info = {"email": email,
                "password": senha,
                "returnSecureToken": True}
        requisicao = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}",
                                json=info)
        requisicao_dic = requisicao.json()

        if requisicao.ok:
            local_id = requisicao_dic['localId']
            id_token = requisicao_dic['idToken']
            refresh_token = requisicao_dic['refreshToken']
            
            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token
            with open("refresh_token.txt", "w") as arquivo:
                arquivo.write(refresh_token)


            meu_aplicativo.mensagem_homepage_aviso()
            meu_aplicativo.carregar_foto_usuario()
            meu_aplicativo.carregar_admin_page()
            meu_aplicativo.adicionar_botoes_homepage()
            meu_aplicativo.comprimento_usuario()
            meu_aplicativo.verificar_barbearia_aberta()
            meu_aplicativo.mudar_tela("homepage")
        
        else:
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            pagina_login.ids["mensagem_alerta"].text = requisicao_dic['error']['message']
            pagina_login.ids["mensagem_alerta"].color = (1, 0, 0, 1)

    

    def trocar_token(self):
        meu_aplicativo = App.get_running_app()
        try:
            with open("refresh_token.txt" , "r") as arquivo:
                conteudo = arquivo.read()

            info = {"grant_type" :"refresh_token",
                    "refresh_token": conteudo}

            requisicao = requests.post(f"https://securetoken.googleapis.com/v1/token?key={self.API_KEY}",
                                    json=info)
            requisicao_dic = requisicao.json()
            print(requisicao_dic)
            if requisicao.ok:
                local_id = requisicao_dic['user_id']
                id_token = requisicao_dic['id_token']
                meu_aplicativo.local_id = local_id
                meu_aplicativo.id_token = id_token
                with open("refresh_token.txt", "w") as arquivo:
                    arquivo.write(requisicao_dic['refresh_token'])
                
                
                meu_aplicativo.mensagem_homepage_aviso()
                meu_aplicativo.carregar_foto_usuario()
                meu_aplicativo.adicionar_botoes_homepage()
                meu_aplicativo.carregar_admin_page()
                meu_aplicativo.comprimento_usuario()
                meu_aplicativo.verificar_barbearia_aberta()
                meu_aplicativo.mudar_tela("homepage")
        except:
            pass

    

    def salvar_nome_usuario(self, nome):
        meu_aplicativo = App.get_running_app()
        contagem_caractere = ""
        for caractere in nome:
            try:
                tenta = int(caractere)
            except:
                contagem_caractere += caractere
                pass

        

        if len(nome) <= 35:
            if len(nome) > 5:
                if len(contagem_caractere) >= 4:
                    local_id = meu_aplicativo.local_id
                    id_token = meu_aplicativo.id_token
                    info = {"nome_usuario": nome}
                    requisicao =requests.patch(f"https://users-arbearia-default-rtdb.firebaseio.com/users/{local_id}.json?auth={id_token}",
                                json=info)
                    if requisicao.ok:
                        meu_aplicativo.comprimento_usuario()
                        meu_aplicativo.mudar_tela("homepage")
                        
                
                else:

                    pagina_nome_usuarios = meu_aplicativo.root.ids["nomeusuariopage"] 
                    label_mensagem = pagina_nome_usuarios.ids["mensagem_nome_usuario"]
                    label_mensagem.text = "Seu nome deve conter 4 ou mais letras"
                    label_mensagem.color = (1, 0, 0, 1)

                
            else:
                
                pagina_nome_usuarios = meu_aplicativo.root.ids["nomeusuariopage"] 
                label_mensagem = pagina_nome_usuarios.ids["mensagem_nome_usuario"]
                label_mensagem.text = "Porfavor escolha um nome com mais de 5 caracteres"
                label_mensagem.color = (1, 0, 0, 1)
        
        else:
            pagina_nome_usuarios = meu_aplicativo.root.ids["nomeusuariopage"] 
            label_mensagem = pagina_nome_usuarios.ids["mensagem_nome_usuario"]
            label_mensagem.text = "Porfavor escolha um nome com menos de 35 caracteres"
            label_mensagem.color = (1, 0, 0, 1)