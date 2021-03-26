from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

# from kivy.config import Config
# Config.set('graphics', 'resizable', '1')
# Config.set('graphics', 'width', '1920')
# Config.set('graphics', 'height', '1080')
# Config.write()

import time
from random import choice
from os import listdir
from dungeon_raiders import *

for i in listdir("musica"):
    musica=SoundLoader.load(f'musica/{i}')
musica.loop=True
musicas=[]
# Clock.schedule_interval(lambda x: musica.play() if musica.loop else None, 0)

class Manager(ScreenManager):
    pass

class Regras(Screen):
    p=1
    def passar(self):
        if self.p<6:
            self.p+=1
        self.ids['pag'].source=f'cartas/regras/p{self.p}.jpg'
    
    def voltar(self):
        if self.p>1:
            self.p-=1
        self.ids['pag'].source=f'cartas/regras/p{self.p}.jpg'

class Inicio(Screen):
    def on_enter(self):
        musica.source='musica/menu.ogg'
        musica.loop=True
        if musica.state == "stop" and musica.source == 'musica/menu.ogg':
            musica.play()

num_masm, controle= 1, 0
class Escolha(Screen):
    escolha=''
    qjog=0
    def on_pre_enter(self):
        global qjog, num_masm, controle
        self.escolha, self.qjog, num_masm, controle = '', 0, 1, 0
        for i in ['mago','ladra','cavaleiro','guerreiro','exploradora','aleatorio']:
            self.ids[i].background_normal=f'cartas/personagens/{i}.png'
        for i in [2,3,4,5]:
            self.ids[str(i)].background_normal='cartas/personagens/numero.png'

    def on_enter(self):
        musica.source='musica/menu.ogg'
        musica.loop=True
        if musica.state == "stop" and musica.source == 'musica/menu.ogg':
            musica.play()
        musicas[:]=list('54321')

    def troca(self,p):
        self.escolha=p
        for i in ['mago','ladra','cavaleiro','guerreiro','exploradora','aleatorio']:
            if i==p: self.ids[i].background_normal=f'cartas/personagens/{i}selec.png'
            else: self.ids[i].background_normal=f'cartas/personagens/{i}.png'

    def trocabt(self,b):
        self.qjog=b
        for i in [2,3,4,5]:
            if i==b: self.ids[str(i)].background_normal='cartas/personagens/numeroselec.png'
            else: self.ids[str(i)].background_normal='cartas/personagens/numero.png'

    def seguir(self):
        if self.qjog and self.escolha:
            players(self.qjog, self.escolha)
            gerar_salas()
            gerador_masmorras()
            self.manager.current = 'porta'
        else:
            if not self.qjog:
                self.animate_selec(self.ids['n_qjog'])
            if not self.escolha:
                self.animate_selec(self.ids['n_jogs'])

    #caso nenhuma carta seja escolhida
    animate_selec=lambda self, Widget, *args: (Animation(opacity=1) + Animation(duration=1) + Animation(opacity=0)).start(Widget)

class Porta(Screen):    
    def on_pre_enter(self):
        global num_masm
        self.ids['porta_text'].text=f'Masmorra {num_masm}'
        num_masm+=1

    def on_enter(self, *args):
        for i in range(10,-1,-1):
            musica.volume=.1*i
            time.sleep(.2)
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
class Per_stats(Label):
    pass

class Mapa_pop(Popup):
    def __init__(self, mapa=[],m='', **kwargs):
        super().__init__(**kwargs)
        self.title=f'Masmorra {m+1}'
        for i in reversed(mapa.children):
            self.ids['mapa_pop'].add_widget(Image(source=i.source))

class Jogo(Screen):
    global jogs, masmorras
    m,s=0,0
    esc_cart=''
    t=0

    def on_pre_enter(self, *args):
        global controle
        if controle==0:
            self.m, self.s = 0, 0
            self.esc_cart=''
            self.t=0
            controle=1

        self.ids['bt_seguir'].unbind(on_press=self.boladecristal_pt2)
        self.ids['bt_seguir'].bind(on_press=self.prox)

        #conteudo da sala
        self.ids['mons'].source=masmorras[self.m][self.s].imagem
        masmorras[self.m][self.s].escuro=False

        self.ids['mapa_sala'].clear_widgets()
        for i in range(5):
            if masmorras[self.m][i].escuro:
                if masmorras[self.m][i].tipo=='Chefe':
                    self.ids['mapa_sala'].add_widget(Image(source='cartas/chefes/chefe.png'))
                else:
                    self.ids['mapa_sala'].add_widget(Image(source='cartas/salas/vazio.jpg'))
            else:
                self.ids['mapa_sala'].add_widget(Image(source=masmorras[self.m][i].imagem))
            
        #cartas do jogador
        self.cartas_jogador()

        #irformações dos personagens
        self.jogs_info()

        if len(jogs[0].cartas)==0:
            self.ids['bt_seguir'].unbind(on_press=self.prox)
            self.esc_cart='0'
            self.t=1
            self.chefe_prox()

    def on_enter(self):
        musica.source=f"musica/jogo{musicas.pop()}.ogg"
        musica.volume=1
        musica.play()

    #cartas do jogador
    def cartas_jogador(self):
        self.ids['cartas'].clear_widgets()
        for y,i in enumerate(jogs[0].cartas):       
            if i=='chave' and masmorras[self.m][self.s].tipo!='Tesouro' and masmorras[self.m][self.s].tipo!='Chefe':
                self.ids['cartas'].add_widget(But_cart(id2=i,id=str(y),disabled=True))
            elif i=='espada' and ( (masmorras[self.m][self.s].tipo!='Monstro' and masmorras[self.m][self.s].tipo!='Chefe') or (3 in getattr(masmorras[self.m][self.s], "hab", [])) ):
                self.ids['cartas'].add_widget(But_cart(id2=i,id=str(y),disabled=True))
            elif i=='boladecristal' and (7 in getattr(masmorras[self.m][self.s], "hab", [])):
                self.ids['cartas'].add_widget(But_cart(id2=i,id=str(y),disabled=True))
            else:
                self.ids['cartas'].add_widget(But_cart(id2=i,id=str(y)))

    #irformações dos personagens
    def jogs_info(self):
        self.ids['per_card'].clear_widgets()
        self.ids['per_coracao'].clear_widgets()
        self.ids['per_saco'].clear_widgets()
        for i in jogs:
            self.ids['per_card'].add_widget(Image(source=f'cartas/personagens/{i.nome[:3].lower()}.png',size_hint=[0.165,0.15]))
            self.ids['per_coracao'].add_widget(But_kokoro(text=str(i.vida)))
            self.ids['per_saco'].add_widget(But_saco(text=str(i.moedas)))
        for i in range(5-len(jogs)):
            self.ids['per_coracao'].add_widget(But_kokoro(background_normal='cartas/personagens/nada.png', background_down='cartas/personagens/nada.png'))
            self.ids['per_saco'].add_widget(But_saco(background_normal='cartas/personagens/nada.png', background_down='cartas/personagens/nada.png'))

    #mostra qual carta fora selecionada
    def cart_selec(self,x):
        if self.m!=4 or self.s!=4:
            for i in self.ids['cartas'].children:
                if i.id==x: 
                    i.background_normal=f'cartas/cartas_de_ataque/{i.id2}selec.png'
                    self.esc_cart=i.id2
                else:        
                    i.background_normal=f'cartas/cartas_de_ataque/{i.id2}.png'
        else:
            self.chefe_selec(x)

    #botao seguir
    def prox(self, *args):
        if (self.esc_cart and (self.m!=4 or self.s!=4)) or self.t==1:
            for i in self.ids['cartas'].children:
                if not i.disabled:
                    i.background_disabled_normal=i.background_normal
                i.disabled=True

        if self.m!=4 or self.s!=4:
            if self.esc_cart:
                if self.esc_cart=='tocha':                
                    for i in masmorras[self.m]:
                        i.escuro=False
                    jogs[0].cartas.remove(self.esc_cart)
                    self.on_pre_enter()
                    return
                if self.esc_cart=='boladecristal':
                    self.boladecristal()
                    return

                self.ids['bt_seguir'].unbind(on_press=self.prox)
                self.resolver() 
            else:
                self.ids['mensagem'].text='Escolhe uma carta'
                self.animate_selec(self.ids['mensagem'])
        else:
            self.chefe_prox()

    def resolver(self):
        if self.m!=4 or self.s!=4:
            jogs[0].ultima=self.esc_cart
            jogs[0].cartas.remove(self.esc_cart)        
            self.esc_cart=''  
            
            tipo=masmorras[self.m][self.s].tipo
            for i in jogs[1:]:
                i.jogar(tipo)

            self.ids['per_carta'].clear_widgets()
            for i in jogs:
                self.ids['per_carta'].add_widget(Per_carta(source=f'cartas/cartas_de_ataque/{i.ultima}.png'))

            self.animate_per_carta(self.ids['per_carta'])

            x=masmorras[self.m][self.s].resolver()
            self.ids['mensagem_monstro'].text=x[0]

            self.ids['mensagem_monstro_dano'].clear_widgets()
            for i in x[1]:
                if i[0] not in ['espada','chave','tocha','boladecristal']:
                    self.ids['mensagem_monstro_dano'].add_widget(Per_stats(text=i[0], color=i[1]))
                else:
                    self.ids['mensagem_monstro_dano'].add_widget(Per_carta(source=f'cartas/cartas_de_ataque/{i[0]}.png', size_hint=[0.15,0.15]))

            if x[2]:
                self.animate_monstro_morte(self.ids['mons'])

            self.animate_stats_per(self.ids['mensagem_monstro_dano'])
            self.animate_result(self.ids['mensagem_monstro']) 
        else:
            self.chefe_resolver()
    animate_stats_per= lambda self, Widget, *args: (Animation(opacity=1) + Animation(duration=3) + Animation(opacity=0)).start(Widget)
    animate_monstro_morte= lambda self, Widget, *args: (Animation(color=[1,0,0,1]) + Animation(duration=2) + Animation(color=[1,1,1,1])).start(Widget)
    
    animate_bola= lambda self, Widget, *args: Animation(opacity=1, padding=[self.width/6.5, self.height/10*1.5, 0, 0]).start(Widget)
    def boladecristal(self):
        jogs[0].ultima=self.esc_cart
        jogs[0].cartas.remove(self.esc_cart)        
        self.esc_cart=''

        tipo=masmorras[self.m][self.s].tipo
        for i in jogs[1:]:
            i.jogar(tipo)

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

            x=masmorras[self.m][self.s].resolver()
            self.ids['mensagem_monstro'].text=x[0]

            self.ids['mensagem_monstro_dano'].clear_widgets()
            for i in x[1]:
                if i[0] not in ['espada','chave','tocha','boladecristal']:
                    self.ids['mensagem_monstro_dano'].add_widget(Per_stats(text=i[0], color=i[1]))
                else:
                    self.ids['mensagem_monstro_dano'].add_widget(Per_carta(source=f'cartas/cartas_de_ataque/{i[0]}.png', size_hint=[0.15,0.10]))

            if x[2]:
                self.animate_monstro_morte(self.ids['mons'])

            self.animate_stats_per(self.ids['mensagem_monstro_dano'])
            self.animate_result(self.ids['mensagem_monstro']) 
        else:
            self.ids['mensagem'].text='Escolhe uma carta'
            self.animate_selec(self.ids['mensagem'])         

    #caso nenhuma carta seja escolhida
    def animate_selec(self, Widget, *args):         
        no_selec=Animation(opacity=1)
        no_selec+=Animation(opacity=0)
        no_selec.start(Widget)

    #animação das cartas jogadas
    def animate_per_carta(self, Widget, *args):
        per_carta=Animation(opacity=1, padding=[self.width/6, self.height/10, 0, 0])
        per_carta+=Animation(duration=3)
        per_carta+=Animation(opacity=0)
        per_carta+=Animation(padding=[self.width/9, self.height/10, 0, 0])
        per_carta.start(Widget)

    #animação resultado
    def animate_result(self, Widget, *args):              
        result=Animation(opacity=1)
        result+=Animation(duration=3)
        result+=Animation(opacity=0) 
        result.bind(on_complete=self.sair)
        result.start(Widget)

    def chefe_animate_per_carta(self, Widget, *args):
        per_carta=Animation(opacity=1, padding=[self.width/4.7, self.height/10, 0, 0])
        per_carta+=Animation(duration=3)
        per_carta+=Animation(opacity=0)
        per_carta+=Animation(padding=[self.width/6, self.height/10, 0, 0])
        per_carta.start(Widget)

    def chefe_prox(self):
        if self.t==0:
            if self.esc_cart:
                self.ids['mensagem'].text='Escolhe mais uma ou pressiona seguir'
                self.animate_selec(self.ids['mensagem'])
                self.t=1
            else:
                self.ids['mensagem'].text='Escolhe uma carta'
                self.animate_selec(self.ids['mensagem'])
        else:
            self.ids['bt_seguir'].unbind(on_press=self.prox)
            self.chefe_resolver()
    
    def chefe_selec(self, x):
        if self.t==0:
            for i in self.ids['cartas'].children:
                if i.id==x: 
                    i.background_normal=f'cartas/cartas_de_ataque/{i.id2}selec.png'
                    self.esc_cart=[i.id2, '0']
                else:        
                    i.background_normal=f'cartas/cartas_de_ataque/{i.id2}.png'
        else:
            for i in self.ids['cartas'].children:
                if i.id2 == self.esc_cart[0]:
                    self.esc_cart[1]='0'
                    continue
                if i.id==x: 
                    i.background_normal=f'cartas/cartas_de_ataque/{i.id2}selec.png'
                    self.esc_cart[1]=i.id2
                else:        
                    i.background_normal=f'cartas/cartas_de_ataque/{i.id2}.png'

    def chefe_resolver(self):
        if self.esc_cart != '0':
            jogs[0].ultima=self.esc_cart
            jogs[0].cartas.remove(self.esc_cart[0])
            if self.esc_cart[1]!='0':
                jogs[0].cartas.remove(self.esc_cart[1])
        else:
            jogs[0].ultima=['0','0']
        self.esc_cart=['','']
        
        for i in jogs[1:]:
            i.chefe_jogar(masmorras[self.m][self.s].hab)

        self.ids['per_carta'].clear_widgets()
        self.ids['per_carta2'].clear_widgets()
        for i in jogs:
            self.ids['per_carta'].add_widget(Per_carta(source=f'cartas/cartas_de_ataque/{i.ultima[0]}.png'))
            self.ids['per_carta2'].add_widget(Per_carta(source=f'cartas/cartas_de_ataque/{i.ultima[1]}.png'))

        self.animate_per_carta(self.ids['per_carta'])
        self.chefe_animate_per_carta(self.ids['per_carta2'])

        x=masmorras[self.m][self.s].resolver()
        self.ids['mensagem_monstro'].text=x[0]

        self.ids['mensagem_chefe_dano'].clear_widgets()
        for i in x[1]:
            self.ids['mensagem_chefe_dano'].add_widget(Per_stats(text=i[0], color=i[1]))

        if x[2]:
            self.animate_monstro_morte(self.ids['mons'])

        self.animate_stats_per(self.ids['mensagem_chefe_dano'])
        self.animate_result(self.ids['mensagem_monstro'])

    def chefe_sair(sair):
        pass

    #termina a sala ou masmorra
    hid=1
    def sair(self, widget, item):        
        if jogs[0].vida==0:
            self.manager.current = 'derrota'
            return

        jogs[:]=[i for i in jogs if i.vida>0]
        
        if len(jogs)==1:
            self.manager.current = 'vitoria'
            return
        
        if self.s<4:
            self.s+=1
            self.on_pre_enter()
        elif self.m==4 and self.s==4:
            #hidra
            if masmorras[self.m][self.s].nome=='Hídra' and self.hid:
                self.on_pre_enter()
                self.hid=0
                self.t=0
                return
            self.hid=1

            self.jogs_info()

            self.manager.current = 'vitoria'
        else:
            self.jogs_info()

            self.s=0
            self.m+=1
            for i in jogs:
                i.redefinir()
            self.manager.current = 'porta'

plural=lambda n: 0 if n==1 else 1
s  = ["","s"]
es = ["","es"]
m  = ["","m"]
ser= ["é","são"]

class Fim_de_jogo(Screen):
    def jogs_info(self):
        self.ids['per_card_fim'].clear_widgets()
        self.ids['per_coracao_fim'].clear_widgets()
        self.ids['per_saco_fim'].clear_widgets()
        for i in jogs:
            self.ids['per_card_fim'].add_widget(Image(source=f'cartas/personagens/{i.nome[:3].lower()}.png',size_hint=[0.165,0.15]))
            self.ids['per_coracao_fim'].add_widget(But_kokoro(text=str(i.vida)))
            self.ids['per_saco_fim'].add_widget(But_saco(text=str(i.moedas)))
        for i in range(5-len(jogs)):
            self.ids['per_coracao_fim'].add_widget(But_kokoro(background_normal='cartas/personagens/nada.png', background_down='cartas/personagens/nada.png'))
            self.ids['per_saco_fim'].add_widget(But_saco(background_normal='cartas/personagens/nada.png', background_down='cartas/personagens/nada.png'))

    def on_pre_enter(self):
        global jogs
        global m , es
        self.ids['morre'].text=''
        self.ids['ganha'].text=''
        self.jogs_info()

        jogs[:]=[i for i in jogs if i.vida>0]
        
        if len(jogs)==1:
            self.ids['morre'].text='Todos estão mortos, exceto tu'
            self.ids['ganha'].text='Venceste'

        elif len(jogs)>2:
            vida=sorted([i.vida for i in jogs])    
            nomes=[]
            if len(set(vida))>1:
                for i in jogs:
                    if i.vida==vida[0]:
                        i.vida-=10
                        nomes+=[i.nome]
                self.ids['morre'].text=f'Jogador{es[plural(len(nomes))]} '+', '.join(nomes)+f' morre{m[plural(len(nomes))]}'

                moeda=sorted([i.moedas for i in jogs if i.vida>0])
                nomes=[]
                for i in jogs:
                    if i.moedas==moeda[-1] and i.vida>0:
                        nomes+=[i.nome]
                self.ids['ganha'].text=f'Jogador{es[plural(len(nomes))]} '+', '.join(nomes)+f' vence{m[plural(len(nomes))]} a partida'

            elif len(set(vida))==1 and len(set(moeda))>1:
                self.ids['morre'].text='Ninguém morre'
                for i in jogs:
                    if i.moedas==moeda[-1]:
                        nomes+=[i.nome]
                self.ids['ganha'].text=f'Jogador{es[plural(len(nomes))]} '+', '.join(nomes)+f' vence{m[plural(len(nomes))]} a partida'

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

    def on_enter(self):
        musica.source="musica/fim.ogg"
        musica.loop=False
        musica.play()

class Morte(Screen):
    def on_enter(self):
        musica.source="musica/perda.ogg"
        musica.loop=True
        musica.play()

class Dungeon_RaidersApp(App):
    def build(self):
        return Manager()

if __name__ == '__main__':
    Dungeon_RaidersApp().run()