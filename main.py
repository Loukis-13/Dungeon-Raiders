from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.animation import Animation

#from kivy.config import Config
#Config.set('graphics', 'resizable', '1')
#Config.set('graphics', 'width', '1920')
#Config.set('graphics', 'height', '1080')
#Config.write()

import time
from dungeon_raiders import *

class Manager(ScreenManager):
    pass

class Inicio(Screen):
    pass

num_masm, controle= 1, 0
class Escolha(Screen):
    def on_pre_enter(self):
        global jogs, qjog, num_masm, controle
        jogs[0], qjog, num_masm, controle = '', 0, 1, 0
        for i in ['mago','ladra','cavaleiro','guerreiro','exploradora','aleatorio']:
            self.ids[i].background_normal=f'cartas/personagens/{i}.png'
        for i in [2,3,4,5]:
            self.ids[str(i)].background_normal='cartas/personagens/numero.png'

    def troca(self,p):
        global jogs
        jogs[0]=p
        for i in ['mago','ladra','cavaleiro','guerreiro','exploradora','aleatorio']:
            if i==p: self.ids[i].background_normal=f'cartas/personagens/{i}selec.png'
            else: self.ids[i].background_normal=f'cartas/personagens/{i}.png'

    def trocabt(self,b):
        global qjog
        qjog=b
        for i in [2,3,4,5]:
            if i==b: self.ids[str(i)].background_normal='cartas/personagens/numeroselec.png'
            else: self.ids[str(i)].background_normal='cartas/personagens/numero.png'

    def seguir(self):
        global jogs, qjog
        if qjog and jogs[0]:
            jogs=players(qjog)
            gerar_salas(qjog)
            gerador_masmorras()
            self.manager.current = 'porta'


class Porta(Screen):    
    def on_pre_enter(self):
        global num_masm
        self.ids['porta_text'].text=f'Masmorra {num_masm}'
        num_masm+=1

    def on_enter(self, *args):
        time.sleep(2)
        self.manager.current = 'jogo'

class But_cart(Button):
    def __init__(self,id='',id2='',**kwargs):
        super().__init__(**kwargs)
        self.id=id
        self.id2=id2
        self.background_normal=f'cartas/cartas_de_ataque/{id2}.png'
        self.background_down=f'cartas/cartas_de_ataque/{id2}selec.png'
        self.background_disabled_normal=f'cartas/cartas_de_ataque/{id2}desabilitada.png'

class But_kokoro(Button):
    pass
class But_saco(Button):
    pass
class Per_carta(Image):
    pass

class Jogo(Screen):
    global jogs, masmorras
    m,s=0,0
    ma=['m1','m2','m3','m4','m5']
    esc_cart=''

    def on_pre_enter(self, *args):
        global controle
        if controle==0:
            self.m, self.s = 4, 3
            controle=1
        
        self.ids['bt_seguir'].unbind(on_press=self.boladecristal_pt2)
        self.ids['bt_seguir'].bind(on_press=self.prox)

        #conteudo da sala
        self.ids['mons'].source=masmorras[self.m][self.s].imagem
        masmorras[self.m][self.s].escuro=False

        #mapa da sala
        for i,ii in enumerate(self.ma):
            if masmorras[self.m][i].escuro:
                if masmorras[self.m][i].tipo=='Chefe':
                    self.ids[ii].source='cartas/chefes/chefe.png'
                else:
                    self.ids[ii].source='cartas/salas/vazio.jpg'
            else:
                self.ids[ii].source=masmorras[self.m][i].imagem
            
        
        #cartas do jogador
        self.cartas_jogador()

        #irformações dos personagens
        self.jogs_info()

    #cartas do jogador
    def cartas_jogador(self):
        self.ids['cartas'].clear_widgets()
        for y,i in enumerate(jogs[0].cartas):       
            if i=='chave' and masmorras[self.m][self.s].tipo!='Tesouro':
                self.ids['cartas'].add_widget(But_cart(id2=i,id=str(y),disabled=True))
            elif i=='espada' and masmorras[self.m][self.s].tipo!='Monstro' and masmorras[self.m][self.s].tipo!='Chefe':
                self.ids['cartas'].add_widget(But_cart(id2=i,id=str(y),disabled=True))
            else:
                self.ids['cartas'].add_widget(But_cart(id2=i,id=str(y)))

    #irformações dos personagens
    def jogs_info(self):
        self.ids['per_card'].clear_widgets()
        self.ids['per_coracao'].clear_widgets()
        self.ids['per_saco'].clear_widgets()
        for i in jogs:
            self.ids['per_card'].add_widget(Image(source=f'cartas/personagens/{i.nome[:3].lower()}.png',size_hint=[0.15,0.15]))
            self.ids['per_coracao'].add_widget(But_kokoro(text=str(i.vida)))
            self.ids['per_saco'].add_widget(But_saco(text=str(i.moedas)))
        for i in range(5-len(jogs)):
            self.ids['per_coracao'].add_widget(But_kokoro(background_normal='cartas/personagens/nada.png', background_down='cartas/personagens/nada.png'))
            self.ids['per_saco'].add_widget(But_saco(background_normal='cartas/personagens/nada.png', background_down='cartas/personagens/nada.png'))

    #mostra qual carta fora selecionada
    def cart_selec(self,x):
        for i in self.ids['cartas'].children:
            if i.id==x: 
                i.background_normal=f'cartas/cartas_de_ataque/{i.id2}selec.png'
                self.esc_cart=i.id2
            else:        
                i.background_normal=f'cartas/cartas_de_ataque/{i.id2}.png'

    #botao seguir
    def prox(self, *args):
        if self.esc_cart:
            #tocha
            if self.esc_cart=='tocha':                
                for i in masmorras[self.m]:
                    i.escuro=False
                jogs[0].cartas.remove(self.esc_cart)
                self.on_pre_enter()
                return
            if self.esc_cart=='boladecristal':
                self.boladecristal()
                return

            self.resolver() 
        else:
            self.ids['mensagem'].text='Escolhe uma carta'
            self.animate_selec(self.ids['mensagem'])
    
    animate_bola= lambda self, Widget, *args: Animation(opacity=1, padding=[self.width/6.5, self.height/10*1.5, 0, 0]).start(Widget)
    def boladecristal(self):
        jogs[0].ultima=self.esc_cart
        jogs[0].cartas.remove(self.esc_cart)        
        self.esc_cart=''

        for i in jogs[1:]:
            i.jogar()

        self.ids['per_carta'].clear_widgets()
        for i in jogs:
            self.ids['per_carta'].add_widget(Per_carta(source=f'cartas/cartas_de_ataque/{i.ultima}.png'))

        self.animate_bola(self.ids['per_carta'])
        self.cartas_jogador()

        self.ids['bt_seguir'].unbind(on_press=self.prox)
        self.ids['bt_seguir'].bind(on_press=self.boladecristal_pt2)

    animate_bola_pt2= lambda self, Widget, *args: (Animation(duration=4)+Animation(opacity=0)+Animation(padding=[self.width/9.8, self.height/10*1.5, 0, 0])).start(Widget)
    def boladecristal_pt2(self, *args):
        if self.esc_cart:
            if self.esc_cart=='boladecristal':
                self.ids['mensagem'].text='Escolhe outra'
                self.animate_selec(self.ids['mensagem'])
                return

            jogs[0].ultima=self.esc_cart
            jogs[0].cartas.remove(self.esc_cart)
            self.esc_cart=''

            self.ids['per_carta'].clear_widgets()
            for i in jogs:
                self.ids['per_carta'].add_widget(Per_carta(source=f'cartas/cartas_de_ataque/{i.ultima}.png'))
            
            self.animate_bola_pt2(self.ids['per_carta'])
            self.ids['mensagem'].text= masmorras[self.m][self.s].resolver() 
            self.animate_result(self.ids['mensagem'])  
        else:
            self.ids['mensagem'].text='Escolhe uma carta'
            self.animate_selec(self.ids['mensagem'])


    def resolver(self):
        jogs[0].ultima=self.esc_cart
        jogs[0].cartas.remove(self.esc_cart)        
        self.esc_cart=''  
        
        for i in jogs[1:]:
            i.jogar()

        self.ids['per_carta'].clear_widgets()
        for i in jogs:
            self.ids['per_carta'].add_widget(Per_carta(source=f'cartas/cartas_de_ataque/{i.ultima}.png'))

        self.animate_per_carta(self.ids['per_carta'])

        self.ids['mensagem'].text= masmorras[self.m][self.s].resolver() 
        self.animate_result(self.ids['mensagem'])             

    #caso nenhuma carta seja escolhida
    def animate_selec(self, Widget, *args):         
        no_selec=Animation(opacity=1)
        no_selec+=Animation(opacity=0)
        no_selec.start(Widget)

    #animação das cartas jogadas
    def animate_per_carta(self, Widget, *args):
        per_carta=Animation(opacity=1, padding=[self.width/6.5, self.height/10*1.5, 0, 0])
        per_carta+=Animation(duration=3)
        per_carta+=Animation(opacity=0)
        per_carta+=Animation(padding=[self.width/9.8, self.height/10*1.5, 0, 0])
        per_carta.start(Widget)

    #animação resultado
    def animate_result(self, Widget, *args):              
        result=Animation(opacity=1)
        result+=Animation(duration=3)
        result+=Animation(opacity=0) 
        result.bind(on_complete=self.sair)
        result.start(Widget)

    #termina a sala ou masmorra
    def sair(self, widget, item):        
        if jogs[0].vida==0:
            self.manager.current = 'derrota'
            return
        for i in jogs:
            if i.vida==0:
                i.vivo=False
                jogs.remove(i)
        if len(jogs)==1:
            self.manager.current = 'vitoria'
            return
        
        if self.s<4:
            self.s+=1
            self.on_pre_enter()
        elif self.m==4 and self.s==4:
            self.jogs_info()

            self.m,self.s=0,0
            self.manager.current = 'vitoria'
        else:
            self.jogs_info()

            self.s=0
            self.m+=1
            for i in jogs:
                i.redefinir()
            self.manager.current = 'porta'

class Fim_de_jogo(Screen):
    def on_pre_enter(self):
        global jogs

        for i in jogs:
            if not i.vivo:
                jogs.remove(i)
        
        if len(jogs)==1:
            self.ids['morre'].text='Todos estão mortos, exceto tu'
            self.ids['ganha'].text='Venceste'

        if len(jogs)>2:
            vida=sorted([i.vida for i in jogs])    
            nomes=[]
            if len(set(vida))>1:
                for i in jogs:
                    if i.vida==vida[0]:
                        nomes+=[i.nome]
                        i.vivo=False
                self.ids['morre'].text='Jogador '+', '.join(nomes)+' morre'

                for i in jogs:
                    if not i.vivo:
                        jogs.remove(i)
                moeda=sorted([i.moedas for i in jogs])
                nomes=[]
                for i in jogs:
                    if i.moedas==moeda[-1]:
                        nomes+=[i.nome]
                self.ids['ganha'].text='Jogador '+', '.join(nomes)+' vence a partida'

            elif len(set(vida))==1 and len(set(moeda))>1:
                self.ids['morre'].text='Ninguém morre'
                for i in jogs:
                    if i.moedas==moeda[-1]:
                        nomes+=[i.nome]
                self.ids['ganha'].text='Jogador '+', '.join(nomes)+' vence a partida'

            elif len(set(vida))==1 and len(set(moeda))==1:
                self.ids['ganha'].text='Empate'

        else:
            if jogs[0].moedas>jogs[1].moedas:
                self.ids['ganha'].text=f'Jogador {jogs[0].nome} vence a partida'
            elif jogs[1].moedas>jogs[0].moedas:
                self.ids['ganha'].text=f'Jogador {jogs[1].nome} vence a partida'
            elif jogs[0].vida>jogs[1].vida:
                self.ids['ganha'].text=f'Jogador {jogs[0].nome} vence a partida'
            elif jogs[1].vida>jogs[0].vida:
                self.ids['ganha'].text=f'Jogador {jogs[1].nome} vence a partida'
            else:
                self.ids['ganha'].text='Empate'

class DungeonApp(App):
    def build(self):
        return Manager()

if __name__ == '__main__':
    DungeonApp().run()