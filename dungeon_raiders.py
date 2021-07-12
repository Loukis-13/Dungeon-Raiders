import random
import copy


class Personagem():
	def __init__(self, nome, vida, moedas, imagem, cartas):
		self.nome = nome
		self.vida = vida
		self.moedas = moedas
		self.imagem = imagem
		self.cartas = cartas
		self.ultima = ''

	def jogar(self, tipo):
		while True:
			carta = random.choice(self.cartas)
			if (carta == 'chave' and tipo != 'Tesouro') or (carta == 'espada' and tipo != 'Monstro'):
				continue
			if carta == 'tocha' or carta == 'boladecristal':
				continue
			break
		self.ultima = carta
		self.cartas.remove(carta)

	def chefe_jogar(self, hab):
		while True:
			carta = random.choice(self.cartas)
			if 3 in hab and carta == 'espada':
				continue
			if 7 in hab and carta == 'boladecristal':
				continue
			break
		self.ultima = [carta, '0']
		self.cartas.remove(carta)

		self.cartas += ['0', '0', '0']
		while True:
			carta = random.choice(self.cartas)
			if 3 in hab and carta == 'espada':
				continue
			if 7 in hab and carta == 'boladecristal':
				continue
			break
		self.ultima[1] = carta
		self.cartas.remove(carta)

	def redefinir(self):
		for i in ['1', '2', '3', '4', '5']:
			if i in self.cartas:
				self.cartas.remove(i)
		self.cartas = ['1', '2', '3', '4', '5'] + self.cartas


DICT_CARTAS = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, 'espada': 5, 'chave': 5, 'boladecristal': 0, 'tocha': 0}


class Aboboda():
	def __init__(self, item1, item2, item3, item4, item5, imagem):
		self.item1 = item1
		self.item2 = item2
		self.item3 = item3
		self.item4 = item4
		self.item5 = item5
		self.imagem = imagem
		self.tipo = 'Abóboda'
		self.escuro = False

	def resolver(self):
		val = [['', [0, 0, 0, 0]]]*5

		for i, jog in enumerate(jogs):
			if DICT_CARTAS[jog.ultima] == 1:
				if isinstance(self.item1, str):
					jog.cartas += [self.item1]
					val[i] = [self.item1, [1, 1, 1, 1]]
				else:
					jog.moedas += 1
					val[i] = ['+1', [1, 1, 0, 1]]
					if jog.moedas > 20:
						jog.moedas = 20
			elif DICT_CARTAS[jog.ultima] == 2:
				if isinstance(self.item2, str):
					jog.cartas += [self.item2]
					val[i] = [self.item2, [1, 1, 1, 1]]
				else:
					jog.moedas += 2
					val[i] = ['+2', [1, 1, 0, 1]]
					if jog.moedas > 20:
						jog.moedas = 20
			elif DICT_CARTAS[jog.ultima] == 3:
				if isinstance(self.item3, str):
					jog.cartas += [self.item3]
					val[i] = [self.item3, [1, 1, 1, 1]]
				else:
					jog.vida += 1
					val[i] = ['+1', [1, 0, 0, 1]]
					if jog.vida > 10:
						jog.vida = 10
			elif DICT_CARTAS[jog.ultima] == 4:
				if isinstance(self.item4, str):
					jog.cartas += [self.item4]
					val[i] = [self.item4, [1, 1, 1, 1]]
				else:
					jog.moedas += 3
					val[i] = ['+3', [1, 1, 0, 1]]
					if jog.moedas > 20:
						jog.moedas = 20
			elif DICT_CARTAS[jog.ultima] == 5:
				if isinstance(self.item2, str):
					jog.vida += 1
					val[i] = ['+1', [1, 0, 0, 1]]
					if jog.vida > 10:
						jog.vida = 10
				else:
					jog.vida += 2
					val[i] = ['+2', [1, 0, 0, 1]]
					if jog.vida > 10:
						jog.vida = 10
		return ('', val, False)


class Monstro():
	def __init__(self, nome, vida, dano, imagem):
		self.nome = nome
		self.vida = vida
		self.dano = dano
		self.imagem = imagem
		self.tipo = 'Monstro'
		self.escuro = False

	def resolver(self):
		val_cartas = sorted([DICT_CARTAS[i.ultima] for i in jogs])
		danos = [['', [0, 0, 0, 0]]]*5
		morto = False

		# dois jogadores
		if len(jogs) == 2:
			if val_cartas[0] == val_cartas[1]:
				return ('? ? ?', danos, morto)

		if sum(val_cartas) < self.vida[len(jogs)]:
			for i, jog in enumerate(jogs):
				if DICT_CARTAS[jog.ultima] == val_cartas[0]:
					jog.vida += self.dano
					danos[i] = [str(self.dano), [1, 0, 0, 1]]
					if jog.vida < 0:
						jog.vida = 0
		else:
			morto = True
		return (str(sum(val_cartas)), danos, morto)


class Tesouro():
	def __init__(self, bau1, bau2, imagem):
		self.bau1 = bau1
		self.bau2 = bau2
		self.imagem = imagem
		self.tipo = 'Tesouro'
		self.escuro = False

	def resolver(self):
		val_cartas = sorted([DICT_CARTAS[i.ultima] for i in jogs])
		din = [['', [0, 0, 0, 0]]]*5

		for i, jog in enumerate(jogs):
			if DICT_CARTAS[jog.ultima] == val_cartas[-1]:
				x = self.bau1//val_cartas.count(val_cartas[-1])
				jog.moedas += x
				if jog.moedas > 20:
					jog.moedas = 20
				din[i] = [f'+{x}', [1, 1, 0, 1]]

		if self.bau2:
			val_cartas = [i for i in val_cartas if i != val_cartas[-1]]
			if len(val_cartas) == 0:
				return ('', din, False)
			for i, jog in enumerate(jogs):
				if DICT_CARTAS[jog.ultima] == val_cartas[-1]:
					x = self.bau2//val_cartas.count(val_cartas[-1])
					jog.moedas += x
					if jog.moedas > 20:
						jog.moedas = 20
					din[i] = [f'+{x}', [1, 1, 0, 1]]
		return ('', din, False)


class Armadilha():
	def __init__(self, nome, afeto, valor, quant, imagem):
		self.nome = nome
		self.afeto = afeto
		self.valor = valor
		self.quant = quant
		self.imagem = imagem
		self.tipo = 'Armadilha'
		self.escuro = False

	def resolver(self):
		val_cartas = sorted([DICT_CARTAS[i.ultima] for i in jogs])
		val = [['', [0, 0, 0, 0]]]*5

		if self.afeto == 'todos':
			if 1 in val_cartas:
				for i, jog in enumerate(jogs):
					if self.valor == 'moedas':
						jog.moedas //= 2
						val[i] = ['/2', [1, 1, 0, 1]]
					else:
						jog.vida //= 2
						val[i] = ['/2', [1, 0, 0, 1]]
			elif 2 in val_cartas:
				for i, jog in enumerate(jogs):
					if self.valor == 'moedas':
						jog.moedas -= 2
						if jog.moedas < 0:
							jog.moedas = 0
						val[i] = ['-2', [1, 1, 0, 1]]
					else:
						jog.vida -= 2
						if jog.vida < 0:
							jog.vida = 0
						val[i] = ['-2', [1, 0, 0, 1]]
			elif 3 in val_cartas:
				for i, jog in enumerate(jogs):
					if self.valor == 'moedas':
						jog.moedas -= 1
						if jog.moedas < 0:
							jog.moedas = 0
						val[i] = ['-1', [1, 1, 0, 1]]
					else:
						jog.vida -= 1
						if jog.vida < 0:
							jog.vida = 0
						val[i] = ['-1', [1, 0, 0, 1]]
		else:
			if self.valor == 'moedas':
				a = max([i.moedas for i in jogs])
				if 5 in val_cartas:
					for i, jog in enumerate(jogs):
						if jog.moedas == a:
							jog.moedas -= 3
							if jog.moedas < 0:
								jog.moedas = 0
							val[i] = ['-3', [1, 1, 0, 1]]
				elif 4 in val_cartas:
					for i, jog in enumerate(jogs):
						if jog.moedas == a:
							jog.moedas -= 2
							if jog.moedas < 0:
								jog.moedas = 0
							val[i] = ['-2', [1, 1, 0, 1]]
				elif 3 in val_cartas:
					for i, jog in enumerate(jogs):
						if jog.moedas == a:
							jog.moedas -= 1
							if jog.moedas < 0:
								jog.moedas = 0
							val[i] = ['-1', [1, 1, 0, 1]]
			else:
				a = max([i.vida for i in jogs])
				if 5 in val_cartas:
					for i, jog in enumerate(jogs):
						if jog.vida == a:
							jog.vida -= 3
							if jog.vida < 0:
								jog.vida = 0
							val[i] = ['-3', [1, 0, 0, 1]]
				elif 4 in val_cartas:
					for i, jog in enumerate(jogs):
						if jog.vida == a:
							jog.vida -= 2
							if jog.vida < 0:
								jog.vida = 0
							val[i] = ['-2', [1, 0, 0, 1]]
				elif 3 in val_cartas:
					for i, jog in enumerate(jogs):
						if jog.vida == a:
							jog.vida -= 1
							if jog.vida < 0:
								jog.vida = 0
							val[i] = ['-1', [1, 0, 0, 1]]
		return ('', val, False)


class Chefe():
	def __init__(self, nome, vida, dano, imagem, hab):
		self.nome = nome
		self.vida = vida
		self.dano = dano
		self.tipo = 'Chefe'
		self.imagem = imagem
		self.escuro = True
		self.hab = hab

	def resolver(self):
		CHEFE_DICT_CARTAS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, 'espada': 5, 'chave': 0, 'boladecristal': 0, 'tocha': 0}
		danos = [['', [0, 0, 0, 0]]]*5
		morto = False

		if 4 in self.hab:
			if self.nome == 'Múmia':
				CHEFE_DICT_CARTAS['tocha'] = 5
			elif self.nome == 'Vampiro':
				CHEFE_DICT_CARTAS['tocha'] = 3
		if 6 in self.hab:
			CHEFE_DICT_CARTAS['boladecristal'] = 5

		val_cartas = sorted([sum(CHEFE_DICT_CARTAS[i]
								 for i in j.ultima) for j in jogs])

		if 8 in self.hab:
			self.dano = -val_cartas[-1] if val_cartas[-1] < 5 else -5

		if sum(val_cartas) >= self.vida[len(jogs)]:
			morto = True
			if 5 in self.hab:
				moedas_bau_chefe = sorted(
					[max(DICT_CARTAS[i] if i != 'espada' else 0 for i in j.ultima) for j in jogs])
				for i, jog in enumerate(jogs):
					if max(DICT_CARTAS[i] for i in jog.ultima) == moedas_bau_chefe[-1]:
						jog.moedas += self.bau1//moedas_bau_chefe.count(
							moedas_bau_chefe[-1])
						if jog.moedas > 20:
							jog.moedas = 20
						danos[i] = [
							self.bau1//moedas_bau_chefe.count(moedas_bau_chefe[-1]), [1, 1, 0, 1]]
		else:
			for i, jog in enumerate(jogs):
				if 2 not in self.hab:
					if sum(CHEFE_DICT_CARTAS[j] for j in jog.ultima) == val_cartas[0]:
						if 11 in self.hab:
							if 'tocha' in jog.ultima:
								continue
						jog.vida += self.dano
						danos[i] = [str(self.dano), [1, 0, 0, 1]]
						if jog.vida < 0:
							jog.vida = 0
						if 9 in self.hab:
							jog.moedas -= val_cartas[-1] if val_cartas[-1] < 5 else 5
							if jog.moedas < 0:
								jog.moedas = 0
				else:
					if max(CHEFE_DICT_CARTAS[i] for i in jog.ultima) == val_cartas[-1] if val_cartas[-1] < 5 else 5:
						jog.vida += self.dano
						danos[i] = [str(self.dano), [1, 0, 0, 1]]
						if jog.vida < 0:
							jog.vida = 0

			if 1 in self.hab:
				val_cartas = [i for i in val_cartas if i != val_cartas[0]]
				for i, p in enumerate(jogs):
					if min(CHEFE_DICT_CARTAS[i] for i in jog.ultima) == val_cartas[0]:
						jog.vida += self.dano
						danos[i] = [str(self.dano), [1, 0, 0, 1]]
						if jog.vida < 0:
							jog.vida = 0

		return (str(sum(val_cartas)), danos, morto)


jogs = []
def players(quant_jogs, escolha):
	guerreiro = Personagem('Guerreiro', 10, 2, 'cartas/personagens/guerreiro.png', ['1', '2', '3', '4', '5'])
	mago = Personagem('Mago', 9, 1, 'cartas/personagens/mago.png', ['1', '2', '3', '4', '5', 'boladecristal', 'boladecristal'])
	cavaleiro = Personagem('Cavaleiro', 9, 1, 'cartas/personagens/cavaleiro.png', ['1', '2', '3', '4', '5', 'espada'])
	exploradora = Personagem('Exploradora', 8, 3, 'cartas/personagens/exploradora.png', ['1', '2', '3', '4', '5', 'tocha'])
	ladra = Personagem('Ladra', 8, 2, 'cartas/personagens/ladra.png', ['1', '2', '3', '4', '5', 'chave'])
	pers = {'guerreiro': guerreiro, 'mago': mago, 'ladra': ladra, 'exploradora': exploradora, 'cavaleiro': cavaleiro}

	jogs.clear()

	if escolha != 'aleatorio':
		jogs.append(pers.pop(escolha))
	for i in range(quant_jogs-len(jogs)):
		jogs.append(pers.pop(random.choice(list(pers.keys()))))


masmorras = []
def gerador_masmorras():
	# gerar salas
	aboboda00 = Aboboda('tocha', 'boladecristal', 'chave', 'espada', {'vida': 1}, 'cartas/salas/aboboda0.png')  # 3
	aboboda01 = copy.deepcopy(aboboda00)
	aboboda02 = copy.deepcopy(aboboda00)
	aboboda10 = Aboboda({'moedas': 1}, {'moedas': 2}, {'vida': 1}, {'moedas': 3}, {'vida': 2}, 'cartas/salas/aboboda1.png')  # 2
	aboboda11 = copy.deepcopy(aboboda10)

	monstro00 = Monstro('Cobra', {2: 8, 3: 8, 4: 10, 5: 13}, -3, 'cartas/salas/cobra.png')
	monstro10 = Monstro('Zumbi', {2: 11, 3: 11, 4: 14, 5: 18}, -1, 'cartas/salas/zumbi.png')
	monstro20 = Monstro('Esqueleto', {2: 11, 3: 11, 4: 14, 5: 18}, -3, 'cartas/salas/esqueleto.png')
	monstro30 = Monstro('Cubo gelatinoso', {2: 14, 3: 14, 4: 18, 5: 23}, -1, 'cartas/salas/cubo.png')
	monstro40 = Monstro('Troll', {2: 14, 3: 14, 4: 18, 5: 23}, -2, 'cartas/salas/troll.png')  # 2
	monstro41 = copy.deepcopy(monstro10)
	monstro50 = Monstro('Dragão', {2: 14, 3: 14, 4: 18, 5: 23}, -3, 'cartas/salas/dragao.png')  # 2
	monstro51 = copy.deepcopy(monstro30)
	monstro60 = Monstro('Goblin', {2: 11, 3: 11, 4: 14, 5: 18}, -2, 'cartas/salas/goblin.png')  # 2
	monstro61 = copy.deepcopy(monstro40)

	tesouro00 = Tesouro(1, 0, 'cartas/salas/tesouro0.png')
	tesouro10 = Tesouro(2, 0, 'cartas/salas/tesouro1.png')
	tesouro20 = Tesouro(3, 0, 'cartas/salas/tesouro2.png')
	tesouro30 = Tesouro(4, 0, 'cartas/salas/tesouro3.png')
	tesouro40 = Tesouro(2, 1, 'cartas/salas/tesouro4.png')  # 2
	tesouro41 = copy.deepcopy(tesouro40)
	tesouro50 = Tesouro(3, 2, 'cartas/salas/tesouro5.png')  # 2
	tesouro51 = copy.deepcopy(tesouro50)
	tesouro60 = Tesouro(4, 2, 'cartas/salas/tesouro6.png')  # 2
	tesouro61 = copy.deepcopy(tesouro60)

	armadilha00 = Armadilha('Armadilha de imã', 'mais', 'moedas', {5: -3, 4: -2, 3: -1}, 'cartas/salas/armadilha0.png')  # 2
	armadilha01 = copy.deepcopy(armadilha00)
	armadilha10 = Armadilha('Armadilha de pedra', 'mais', 'vida', {5: -3, 4: -2, 3: -1}, 'cartas/salas/armadilha1.png')
	armadilha20 = Armadilha('Armadilha de estacas', 'todos', 'vida', {3: -1, 2: -2, 1: '/2'}, 'cartas/salas/armadilha2.png')
	armadilha30 = Armadilha('Armadilha de lava', 'todos', 'moedas', {3: -1, 2: -2, 1: '/2'}, 'cartas/salas/armadilha3.png')

	salas = [
		monstro00, monstro10, monstro20, monstro30, monstro40, monstro41, monstro50, monstro51, monstro60, monstro61,
		armadilha00, armadilha01, armadilha10, armadilha20, armadilha30,
		aboboda00, aboboda01, aboboda02, aboboda10, aboboda11,
		tesouro00, tesouro10, tesouro20, tesouro30, tesouro40, tesouro41, tesouro50, tesouro51, tesouro60, tesouro61
	]

	# gerar chefes
	matilha_de_lobos = 	  Chefe('Matilha de Lobos', {2: 14, 3: 14, 4: 14, 5: 18}, -3, 'cartas/chefes/matilha_de_lobos.jpg', [11, 0])
	megadragao = 		  Chefe('Megadragão', {2: 16, 3: 16, 4: 23, 5: 29}, -4, 'cartas/chefes/megadragao.jpg', [5, 0])
	medusa = 			  Chefe('Medusa', {2: 12, 3: 12, 4: 14, 5: 20}, -10, 'cartas/chefes/medusa.jpg', [10, 0])
	minotauro =			  Chefe('Minotauro', {2: 11, 3: 11, 4: 15, 5: 19}, -4, 'cartas/chefes/minotauro.jpg', [2, 0])
	coletor_de_impostos = Chefe('Coletor de impostos', {2: 14, 3: 14, 4: 18, 5: 23}, -4, 'cartas/chefes/coletor_de_impostos.jpg', [9, 0])
	golem = 			  Chefe('Golem', {2: 14, 3: 14, 4: 18, 5: 23}, 0, 'cartas/chefes/golem.jpg', [3, 8])
	necromante = 		  Chefe('Necromante', {2: 12, 3: 12, 4: 15, 5: 19}, -2, 'cartas/chefes/necromante.jpg', [7, 1])
	vampiro = 			  Chefe('Vampiro', {2: 14, 3: 14, 4: 18, 5: 23}, -3, 'cartas/chefes/vampiro.jpg', [4, 1])
	esfinge = 			  Chefe('Esfinge', {2: 14, 3: 14, 4: 18, 5: 23}, -4, 'cartas/chefes/esfinge.jpg', [6, 0])
	mumia = 			  Chefe('Múmia', {2: 13, 3: 13, 4: 18, 5: 23}, -4, 'cartas/chefes/mumia.jpg', [4, 0])
	hidra = 			  Chefe('Hídra', {2: 8, 3: 8, 4: 10, 5: 13}, -2, 'cartas/chefes/hidra.jpg', [12, 0])

	chefes = [matilha_de_lobos, hidra, mumia, vampiro, necromante, coletor_de_impostos, golem, megadragao, medusa, esfinge, minotauro]

	# gerar masmorra
	random.shuffle(salas)
	for i in range(6):
		salas.pop()
	for i in range(12):
		salas[i].escuro = True
	random.shuffle(salas)
	salas.extend([random.choice(chefes)])

	masmorras.clear()
	for i in range(0, 25, 5):
		masmorras.append(salas[i:i+5])
