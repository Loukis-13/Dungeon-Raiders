from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader

import time
from os import listdir
from os.path import abspath
from dungeon_raiders import *

for i in listdir("musica"):
    musica = SoundLoader.load(f'musica/{i}')
musica.loop = True
musicas = []


class Manager(ScreenManager):
    pass


class Regras(Screen):
    pagina = 1

    def passar(self):
        if self.pagina < 6:
            self.pagina += 1
        self.ids['pag'].source = f'cartas/regras/p{self.pagina}.jpg'

    def voltar(self):
        if self.pagina > 1:
            self.pagina -= 1
        self.ids['pag'].source = f'cartas/regras/p{self.pagina}.jpg'


class Inicio(Screen):
    def on_enter(self):
        musica.source=abspath('musica/menu.ogg')
        musica.loop=True
        if musica.state == "stop" and musica.source == abspath('musica/menu.ogg'):
            musica.play()


numero_masmorra, controle = 1, 0
class Escolha(Screen):
    quant_jogs = 0

    def on_pre_enter(self):
        global quant_jogs, numero_masmorra, controle

        self.quant_jogs = 0
        numero_masmorra = 1
        controle =  0

        for carta_jog in ['mago', 'ladra', 'cavaleiro', 'guerreiro', 'exploradora', 'aleatorio']:
            self.ids[carta_jog].background_normal = f'cartas/personagens/{carta_jog}.png'
        for num in [2, 3, 4, 5]:
            self.ids[str(num)].background_normal = 'cartas/personagens/numero.png'

    def on_enter(self):
        musica.source = abspath('musica/menu.ogg')
        musica.loop = True
        if musica.state == "stop" and musica.source == abspath('musica/menu.ogg'):
            musica.play()
        musicas[:] = list('54321')

    # trocar escolha de personagem
    escolha = ''
    def troca(self, escolha):
        if self.escolha:
            self.ids[self.escolha].background_normal = f'cartas/personagens/{self.escolha}.png'
        self.escolha = escolha
        self.ids[escolha].background_normal = f'cartas/personagens/{escolha}selec.png'

    # trocar quantidade de jogadores
    def trocabt(self, quantidade):
        if self.quant_jogs:
            self.ids[str(self.quant_jogs)].background_normal = 'cartas/personagens/numero.png'
        self.quant_jogs = quantidade
        self.ids[str(quantidade)].background_normal = 'cartas/personagens/numeroselec.png'

    def seguir(self):
        if self.quant_jogs and self.escolha:
            gerar_jogadores(self.quant_jogs, self.escolha)
            gerar_masmorra()
            self.manager.current = 'porta'
        else:
            if not self.quant_jogs:
                self.animate_selec(self.ids['n_qjog'])
            if not self.escolha:
                self.animate_selec(self.ids['n_jogs'])

    #caso nenhuma carta seja escolhida
    def animate_selec(self, Widget, *args): 
        (Animation(opacity=1) + Animation(duration=1) + Animation(opacity=0)).start(Widget)


class Porta(Screen):
    def on_pre_enter(self):
        global numero_masmorra
        self.ids['porta_text'].text = f'Masmorra {numero_masmorra}'
        numero_masmorra += 1

    def on_enter(self, *args):
        for v in range(10, -1, -1):
            musica.volume = .1*v
            time.sleep(.2)
        self.manager.current = 'jogo'


class CartasDoJogador(Button):
    def __init__(self, id='', nome='', **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.nome = nome
        self.background_normal = f'cartas/cartas_de_ataque/{nome}.png'
        self.background_down = f'cartas/cartas_de_ataque/{nome}selec.png'
        self.background_disabled_normal = f'cartas/cartas_de_ataque/{nome}desabilitada.png'


class VidaJogador(Button):
    pass


class DinheiroJogador(Button):
    pass


class CartaJogada(Image):
    pass


class ResultadoSala(Label):
    pass


class MapaPopup(Popup):
    def __init__(self, mapa=[], numero_masmorra=0, **kwargs):
        super().__init__(**kwargs)
        self.title = f'Masmorra {numero_masmorra+1}'
        for sala in reversed(mapa.children):
            self.ids['mapa_pop'].add_widget(Image(source=sala.source))


class Jogo(Screen):
    global jogs, masmorras
    masmorra, sala = 0, 0
    ecolha_carta = ''

    chefe_turno_escolha = 0
    chefe_escolha_carta_id = ''

    def on_pre_enter(self, *args):
        global controle
        if controle == 0:
            self.masmorra, self.sala = 0, 0
            self.ecolha_carta = ''
            self.chefe_turno_escolha = 0
            self.chefe_escolha_carta_id = ''
            controle = 1

        self.ids['bt_seguir'].unbind(on_press=self.boladecristal_pt2)
        self.ids['bt_seguir'].bind(on_press=self.prox)

        #conteudo da sala
        self.ids['imagem_conteudo_sala'].source = masmorras[self.masmorra][self.sala].imagem
        masmorras[self.masmorra][self.sala].escuro = False

        self.ids['mapa_sala'].clear_widgets()
        for i in range(5):
            if masmorras[self.masmorra][i].escuro:
                if masmorras[self.masmorra][i].tipo == 'Chefe':
                    self.ids['mapa_sala'].add_widget(
                        Image(source='cartas/chefes/chefe.jpg'))
                else:
                    self.ids['mapa_sala'].add_widget(
                        Image(source='cartas/salas/vazio.jpg'))
            else:
                self.ids['mapa_sala'].add_widget(
                    Image(source=masmorras[self.masmorra][i].imagem))

        # cartas do jogador
        self.cartas_jogador()

        # informações dos personagens
        self.jogs_info()

        if len(jogs[0].cartas) == 0:
            self.ids['bt_seguir'].unbind(on_press=self.prox)
            self.ecolha_carta = '0'
            self.chefe_turno_escolha = 1
            self.chefe_prox()

    def on_enter(self):
        musica.source = abspath(f"musica/jogo{musicas.pop()}.ogg")
        musica.volume = 1
        musica.play()

    # cartas do jogador
    def cartas_jogador(self):
        self.ids['cartas'].clear_widgets()
        for y, i in enumerate(jogs[0].cartas):
            if i == 'chave' and masmorras[self.masmorra][self.sala].tipo != 'Tesouro' and masmorras[self.masmorra][self.sala].tipo != 'Chefe':
                self.ids['cartas'].add_widget(CartasDoJogador(nome=i, id=str(y), disabled=True))
            elif i == 'espada' and ((masmorras[self.masmorra][self.sala].tipo != 'Monstro' and masmorras[self.masmorra][self.sala].tipo != 'Chefe') or (3 in getattr(masmorras[self.masmorra][self.sala], "hab", []))):
                self.ids['cartas'].add_widget(CartasDoJogador(nome=i, id=str(y), disabled=True))
            elif i == 'boladecristal' and (7 in getattr(masmorras[self.masmorra][self.sala], "hab", [])):
                self.ids['cartas'].add_widget(CartasDoJogador(nome=i, id=str(y), disabled=True))
            else:
                self.ids['cartas'].add_widget(CartasDoJogador(nome=i, id=str(y)))

    # informações dos personagens
    def jogs_info(self):
        self.ids['per_card'].clear_widgets()
        self.ids['per_coracao'].clear_widgets()
        self.ids['per_saco'].clear_widgets()
        for i in jogs:
            self.ids['per_card'].add_widget(Image(source=f'cartas/personagens/{i.nome[:3].lower()}.png', size_hint=[0.165, 0.15]))
            self.ids['per_coracao'].add_widget(VidaJogador(text=str(i.vida)))
            self.ids['per_saco'].add_widget(DinheiroJogador(text=str(i.moedas)))
        for i in range(5-len(jogs)):
            self.ids['per_coracao'].add_widget(VidaJogador(background_normal='cartas/personagens/nada.png', background_down='cartas/personagens/nada.png'))
            self.ids['per_saco'].add_widget(DinheiroJogador(background_normal='cartas/personagens/nada.png', background_down='cartas/personagens/nada.png'))

    # organizar miniaturas das cartas jogadas
    def miniatura_de_catas_jogadas(self):
        self.ids['per_carta'].clear_widgets()
        for i in jogs:
            self.ids['per_carta'].add_widget(CartaJogada(source=f'cartas/cartas_de_ataque/{i.ultima}.png'))

    # mostra qual carta fora selecionada
    def cart_selec(self, x):
        if self.masmorra != 4 or self.sala != 4:
            for i in self.ids['cartas'].children:
                if i.id == x:
                    i.background_normal = f'cartas/cartas_de_ataque/{i.nome}selec.png'
                    self.ecolha_carta = i.nome
                else:
                    i.background_normal = f'cartas/cartas_de_ataque/{i.nome}.png'
        else:
            self.chefe_selec(x)

    # botao seguir
    def prox(self, *args):
        if (self.ecolha_carta and (self.masmorra != 4 or self.sala != 4)) or self.chefe_turno_escolha == 1:
            for i in self.ids['cartas'].children:
                if not i.disabled:
                    i.background_disabled_normal = i.background_normal
                i.disabled = True

        if self.masmorra != 4 or self.sala != 4:
            if self.ecolha_carta:
                if self.ecolha_carta == 'tocha':
                    for i in masmorras[self.masmorra]:
                        i.escuro = False
                    jogs[0].cartas.remove(self.ecolha_carta)
                    self.on_pre_enter()
                    return
                if self.ecolha_carta == 'boladecristal':
                    self.boladecristal()
                    return

                self.ids['bt_seguir'].unbind(on_press=self.prox)
                self.resolver()
            else:
                self.ids['mensagem'].text = 'Escolhe uma carta'
                self.animate_selec(self.ids['mensagem'])
        else:
            self.chefe_prox()

    # resolve a sala
    def resolver(self):
        if self.masmorra != 4 or self.sala != 4:
            jogs[0].ultima = self.ecolha_carta
            jogs[0].cartas.remove(self.ecolha_carta)
            self.ecolha_carta = ''

            tipo = masmorras[self.masmorra][self.sala].tipo
            for i in jogs[1:]:
                i.jogar(tipo)

            self.miniatura_de_catas_jogadas()

            self.animate_per_carta(self.ids['per_carta'])

            resultado = masmorras[self.masmorra][self.sala].resolver()
            self.ids['mensagem_monstro'].text = resultado[0]

            self.ids['mensagem_monstro_dano'].clear_widgets()
            for i in resultado[1]:
                if i[0] not in ['espada', 'chave', 'tocha', 'boladecristal']:
                    self.ids['mensagem_monstro_dano'].add_widget(ResultadoSala(text=i[0], color=i[1]))
                else:
                    self.ids['mensagem_monstro_dano'].add_widget(CartaJogada(source=f'cartas/cartas_de_ataque/{i[0]}.png', size_hint=[0.15, 0.15]))

            if resultado[2]:
                self.animate_monstro_morte(self.ids['imagem_conteudo_sala'])

            self.animate_stats_per(self.ids['mensagem_monstro_dano'])
            self.animate_result(self.ids['mensagem_monstro'])
        else:
            self.chefe_resolver()

    #termina a sala ou masmorra
    hid = 1
    def sair(self, widget, item):
        if jogs[0].vida == 0:
            self.manager.current = 'derrota'
            return

        jogs[:] = [i for i in jogs if i.vida > 0]

        if len(jogs) == 1:
            self.manager.current = 'vitoria'
            return

        if self.sala < 4:
            self.sala += 1
            self.on_pre_enter()
        # chefe sair
        elif self.masmorra == 4 and self.sala == 4:
            #hidra
            if masmorras[self.masmorra][self.sala].nome == 'Hídra' and self.hid:
                self.on_pre_enter()
                self.hid = 0
                self.chefe_turno_escolha = 0
                return
            self.hid = 1

            self.manager.current = 'vitoria'
        else:
            self.sala = 0
            self.masmorra += 1
            for i in jogs:
                i.redefinir()
            self.manager.current = 'porta'
    

    """ Bola de cristal """

    def animate_bola(self, Widget, *args):
        Animation(opacity=1, padding=[self.width/6, self.height/10, 0, 0]).start(Widget)

    def boladecristal(self):
        jogs[0].ultima = self.ecolha_carta
        jogs[0].cartas.remove(self.ecolha_carta)
        self.ecolha_carta = ''

        tipo = masmorras[self.masmorra][self.sala].tipo
        for i in jogs[1:]:
            i.jogar(tipo)

        self.miniatura_de_catas_jogadas()

        self.animate_bola(self.ids['per_carta'])
        self.cartas_jogador()

        self.ids['bt_seguir'].unbind(on_press=self.prox)
        self.ids['bt_seguir'].bind(on_press=self.boladecristal_pt2)

    def animate_bola_pt2(self, Widget, *args):
        (Animation(duration=4)+Animation(opacity=0)+Animation(padding=[self.width/9, self.height/10, 0, 0])).start(Widget)

    def boladecristal_pt2(self, *args):
        if self.ecolha_carta:
            if self.ecolha_carta == 'boladecristal':
                self.ids['mensagem'].text = 'Escolhe outra'
                self.animate_selec(self.ids['mensagem'])
                return

            jogs[0].ultima = self.ecolha_carta
            jogs[0].cartas.remove(self.ecolha_carta)
            self.ecolha_carta = ''

            self.miniatura_de_catas_jogadas()

            self.animate_bola_pt2(self.ids['per_carta'])

            resultado = masmorras[self.masmorra][self.sala].resolver()
            self.ids['mensagem_monstro'].text = resultado[0]

            self.ids['mensagem_monstro_dano'].clear_widgets()
            for i in resultado[1]:
                if i[0] not in ['espada', 'chave', 'tocha', 'boladecristal']:
                    self.ids['mensagem_monstro_dano'].add_widget(ResultadoSala(text=i[0], color=i[1]))
                else:
                    self.ids['mensagem_monstro_dano'].add_widget(CartaJogada(source=f'cartas/cartas_de_ataque/{i[0]}.png', size_hint=[0.15, 0.15]))

            if resultado[2]:
                self.animate_monstro_morte(self.ids['imagem_conteudo_sala'])

            self.animate_stats_per(self.ids['mensagem_monstro_dano'])
            self.animate_result(self.ids['mensagem_monstro'])
        else:
            self.ids['mensagem'].text = 'Escolhe uma carta'
            self.animate_selec(self.ids['mensagem'])


    """ Chefe """

    def chefe_prox(self):
        if self.chefe_turno_escolha == 0:
            if self.ecolha_carta:
                self.ids['mensagem'].text = 'Escolhe mais uma ou pressiona seguir'
                self.animate_selec(self.ids['mensagem'])
                self.chefe_turno_escolha = 1
            else:
                self.ids['mensagem'].text = 'Escolhe uma carta'
                self.animate_selec(self.ids['mensagem'])
        else:
            self.ids['bt_seguir'].unbind(on_press=self.prox)
            self.chefe_resolver()
    
    def chefe_selec(self, escolha):
        if self.chefe_turno_escolha == 0:
            for carta in self.ids['cartas'].children:
                if carta.id == escolha:
                    carta.background_normal = f'cartas/cartas_de_ataque/{carta.nome}selec.png'
                    self.ecolha_carta = [carta.nome, '0']
                    self.chefe_escolha_carta_id = escolha
                else:
                    carta.background_normal = f'cartas/cartas_de_ataque/{carta.nome}.png'
        else:
            for carta in self.ids['cartas'].children:
                if carta.id == self.chefe_escolha_carta_id:
                    continue
                if carta.id == escolha:
                    carta.background_normal = f'cartas/cartas_de_ataque/{carta.nome}selec.png'
                    self.ecolha_carta[1] = carta.nome
                else:
                    carta.background_normal = f'cartas/cartas_de_ataque/{carta.nome}.png'

    def chefe_resolver(self):
        if self.ecolha_carta != '0':
            jogs[0].ultima = self.ecolha_carta
            jogs[0].cartas.remove(self.ecolha_carta[0])
            if self.ecolha_carta[1] != '0':
                jogs[0].cartas.remove(self.ecolha_carta[1])
        else:
            jogs[0].ultima = ['0', '0']
        self.ecolha_carta = ['', '']

        for i in jogs[1:]:
            i.chefe_jogar(masmorras[self.masmorra][self.sala].hab)

        self.ids['per_carta'].clear_widgets()
        self.ids['per_carta2'].clear_widgets()
        for i in jogs:
            self.ids['per_carta'].add_widget(CartaJogada(source=f'cartas/cartas_de_ataque/{i.ultima[0]}.png'))
            self.ids['per_carta2'].add_widget(CartaJogada(source=f'cartas/cartas_de_ataque/{i.ultima[1]}.png'))

        self.animate_per_carta(self.ids['per_carta'])
        self.chefe_animate_per_carta(self.ids['per_carta2'])

        x = masmorras[self.masmorra][self.sala].resolver()
        self.ids['mensagem_monstro'].text = x[0]

        self.ids['mensagem_chefe_dano'].clear_widgets()
        for i in x[1]:
            self.ids['mensagem_chefe_dano'].add_widget(ResultadoSala(text=i[0], color=i[1]))

        if x[2]:
            self.animate_monstro_morte(self.ids['imagem_conteudo_sala'])

        self.animate_stats_per(self.ids['mensagem_chefe_dano'])
        self.animate_result(self.ids['mensagem_monstro'])


    """ Animações """

    # mostrar mensagem de resolução da sala
    def animate_stats_per(self, Widget, *args):
        (Animation(opacity=1) + Animation(duration=3) + Animation(opacity=0)).start(Widget)

    # animação de morte de monstro
    def animate_monstro_morte(self, Widget, *args):
        (Animation(color=[1, 0, 0, 1]) + Animation(duration=2) + Animation(color=[1, 1, 1, 1])).start(Widget)

    # caso nenhuma carta seja escolhida
    def animate_selec(self, Widget, *args):         
        (Animation(opacity=1) + Animation(opacity=0)).start(Widget)

    # animação das cartas jogadas
    def animate_per_carta(self, Widget, *args):
        per_carta=Animation(opacity=1, padding=[self.width/6, self.height/10, 0, 0])
        per_carta+=Animation(duration=3)
        per_carta+=Animation(opacity=0)
        per_carta+=Animation(padding=[self.width/9, self.height/10, 0, 0])
        per_carta.start(Widget)

    # animação resultado
    def animate_result(self, Widget, *args):              
        result=Animation(opacity=1)
        result+=Animation(duration=3)
        result+=Animation(opacity=0) 
        result.bind(on_complete=self.sair)
        result.start(Widget)

    # animação segunda carta escolhida para o chefe
    def chefe_animate_per_carta(self, Widget, *args):
        per_carta=Animation(opacity=1, padding=[self.width/4.7, self.height/10, 0, 0])
        per_carta+=Animation(duration=3)
        per_carta+=Animation(opacity=0)
        per_carta+=Animation(padding=[self.width/6, self.height/10, 0, 0])
        per_carta.start(Widget)


plural = lambda n: 0 if n==1 else 1
es = ["", "es"]
m  = ["", "m"]

class Fim_de_jogo(Screen):
    def jogs_info(self):
        self.ids['per_card_fim'].clear_widgets()
        self.ids['per_coracao_fim'].clear_widgets()
        self.ids['per_saco_fim'].clear_widgets()
        for i in jogs:
            self.ids['per_card_fim'].add_widget(Image(source=f'cartas/personagens/{i.nome[:3].lower()}.png', size_hint=[0.165, 0.15]))
            self.ids['per_coracao_fim'].add_widget(VidaJogador(text=str(i.vida)))
            self.ids['per_saco_fim'].add_widget(DinheiroJogador(text=str(i.moedas)))
        for i in range(5-len(jogs)):
            self.ids['per_coracao_fim'].add_widget(VidaJogador(background_normal='cartas/personagens/nada.png', background_down='cartas/personagens/nada.png'))
            self.ids['per_saco_fim'].add_widget(DinheiroJogador(background_normal='cartas/personagens/nada.png', background_down='cartas/personagens/nada.png'))

    def on_pre_enter(self):
        global jogs

        self.ids['morre'].text = ''
        self.ids['ganha'].text = ''

        jogs[:] = [i for i in jogs if i.vida > 0]
        self.jogs_info()

        if len(jogs) == 1:
            self.ids['morre'].text = 'Todos estão mortos, exceto tu'
            self.ids['ganha'].text = 'Venceste'

        elif len(jogs) > 2:
            vida = sorted([i.vida for i in jogs])
            moeda = sorted([i.moedas for i in jogs if i.vida > 0])
            nomes = []

            if len(set(vida)) > 1:
                for jog in jogs:
                    if jog.vida == vida[0]:
                        jog.vida -= 10
                        nomes.append(jog.nome)
                self.ids['morre'].text = f'Jogador{es[plural(len(nomes))]} '+', '.join(nomes)+f' morre{m[plural(len(nomes))]}'

                nomes.clear()
                for jog in jogs:
                    if jog.moedas == moeda[-1] and jog.vida > 0:
                        nomes.append(jog.nome)
                self.ids['ganha'].text = f'Jogador{es[plural(len(nomes))]} '+', '.join(nomes)+f' vence{m[plural(len(nomes))]} a partida'

            elif len(set(vida)) == 1 and len(set(moeda)) > 1:
                self.ids['morre'].text = 'Ninguém morre'
                for jog in jogs:
                    if jog.moedas == moeda[-1]:
                        nomes.append(jog.nome)
                self.ids['ganha'].text = f'Jogador{es[plural(len(nomes))]} '+', '.join(nomes)+f' vence{m[plural(len(nomes))]} a partida'

            elif len(set(vida)) == 1 and len(set(moeda)) == 1:
                self.ids['ganha'].text = 'Empate'

        else:
            if jogs[0].moedas > jogs[1].moedas:
                self.ids['ganha'].text = f'Jogador {jogs[0].nome} vence a partida'
            elif jogs[1].moedas > jogs[0].moedas:
                self.ids['ganha'].text = f'Jogador {jogs[1].nome} vence a partida'
            elif jogs[0].vida > jogs[1].vida:
                self.ids['ganha'].text = f'Jogador {jogs[0].nome} vence a partida'
            elif jogs[1].vida > jogs[0].vida:
                self.ids['ganha'].text = f'Jogador {jogs[1].nome} vence a partida'
            else:
                self.ids['ganha'].text = 'Empate'

    def on_enter(self):
        musica.source = abspath("musica/fim.ogg")
        musica.loop = False
        musica.play()


class Morte(Screen):
    def on_enter(self):
        musica.source = abspath("musica/perda.ogg")
        musica.loop = True
        musica.play()


class Dungeon_RaidersApp(App):
    def build(self):
        return Manager()


if __name__ == '__main__':
    Dungeon_RaidersApp().run()
