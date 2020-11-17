import random,copy

class Personagens():
  def __init__(self,nome,vida,moedas,imagem,cartas):
    self.nome=nome
    self.vida=vida
    self.moedas=moedas
    self.imagem=imagem
    self.cartas=cartas
    self.vivo=True
    self.ultima=''   
    self.z=['1','2','3','4','5']

  def jogar(self):    
    x=random.choice(self.z)
    self.ultima=(x)
    self.cartas.remove(x)
    self.z.remove(x)

  def redefinir(self):
    for i in ['1','2','3','4','5']:
      if i in self.cartas:
        self.cartas.remove(i)
    self.cartas=['1','2','3','4','5']+self.cartas
    self.z=['1','2','3','4','5']

  def __repr__(self):
    return (
    self.nome+'\n'+
    f'Vida: {self.vida}  Moedas: {self.moedas}\n'+
    f'cartas: {self.cartas}\n')

dic_cartas={'1':1, '2':2, '3':3, '4':4, '5':5, 'espada':5, 'chave':5}

class Aboboda():
  def __init__(self,item1,item2,item3,item4,item5,imagem):
    self.item1=item1
    self.item2=item2
    self.item3=item3
    self.item4=item4
    self.item5=item5
    self.imagem=imagem
    self.tipo='Abóboda'
    self.escuro=False

  def resolver(self):
    y=sorted([dic_cartas[i.ultima] for i in jogs])

    for i in jogs:
      if dic_cartas[i.ultima]==1:
        if isinstance(self.item1, str):
          i.cartas+=[self.item1]
        else:
          i.moedas+=1
          if i.moedas>20: i.moedas=20
      elif dic_cartas[i.ultima]==2:
        if isinstance(self.item2, str):
          i.cartas+=[self.item2]
        else:
          i.moedas+=2
          if i.moedas>20: i.moedas=20
      elif dic_cartas[i.ultima]==3:
        if isinstance(self.item3, str):
          i.cartas+=[self.item3]
        else:
          i.vida+=1
          if i.vida>10: i.vida=10
      elif dic_cartas[i.ultima]==4:
        if isinstance(self.item4, str):
          i.cartas+=[self.item4]
        else:
          i.moedas+=3
          if i.moedas>20: i.moedas=20
      elif dic_cartas[i.ultima]==5:
        if isinstance(self.item2, str):
          i.vida+=1
          if i.vida>10: i.vida=10
        else:
          i.vida+=2
          if i.vida>10: i.vida=10
    return ''

  def __str__(self):
    return(
    self.tipo+'\n'+
    f'Itens: {self.item1}, {self.item2}, {self.item3}, {self.item4}, {self.item5}\n')

class Monstro():
  def __init__(self,nome,vida,dano,imagem):
    self.nome=nome
    self.vida=vida
    self.dano=dano
    self.imagem=imagem
    self.tipo='Monstro'
    self.vivo=True
    self.escuro=False

  def resolver(self):
    y=sorted([dic_cartas[i.ultima] for i in jogs])
    nomes=[]

    #dois jogadores
    if len(jogs)==2:
      if y[0]==y[1]:
        return 'Monstro confuso\nEle recua'

    if sum(y)>=self.vida and len(jogs)>2:
      return 'monstro derrotado'
    else:
      for i in jogs:
        if dic_cartas[i.ultima]==y[0]:
          nomes+=[i.nome]
          i.vida+=self.dano 
          if i.vida<0: i.vida=0
      return 'monstro continua vivo\nEle ataca: '+', '.join(nomes)   

  def __str__(self):
    return (
    self.nome+'\n'+
    f'Vida: {self.vida}  Dano: {self.dano}\n')

plural=lambda n: 0 if n==1 else 1
s  = ["","s"]
es = ["","es"]
m  = ["","m"]
ser= ["é","são"]

class Tesouro():
  def __init__(self,bau1,bau2,imagem):
    self.bau1=bau1
    self.bau2=bau2
    self.imagem=imagem
    self.tipo='Tesouro'
    self.escuro=False

  def resolver(self):
    y=sorted([dic_cartas[i.ultima] for i in jogs])
    nomes=[]

    for i in jogs:
      if dic_cartas[i.ultima]==y[-1]:
        i.moedas+=self.bau1//y.count(y[-1])
        if i.moedas>20:i.moedas=20
        nomes+=[i.nome]
    x=f'Jogador{es[plural(len(nomes))]} '+', '.join(nomes)+f' pega{m[plural(len(nomes))]} o baú 1'
    
    nomes=[]
    if self.bau2:
      a=y[-1]
      while a in y:
        y.remove(a)
      if len(y)==0:
        x+='\nNinguém pega o baú 2'
        return x
      for i in jogs:
        if dic_cartas[i.ultima]==y[-1]:
          i.moedas+=self.bau2//y.count(y[-1])
          if i.moedas>20: i.moedas=20
          nomes+=[i.nome]
      x+=f'\nJogador{es[plural(len(nomes))]} '+', '.join(nomes)+f' pega{m[plural(len(nomes))]} o baú 2'
    return x

  def __str__(self):
    x=''
    x+=self.tipo+'\n'
    x+=f'Baú 1: {self.bau1} moeda{s[plural(self.bau1)]}\n'
    if self.bau2:
      x+=f'Baú 2: {self.bau2} moeda{s[plural(self.bau2)]}\n'
    return x

class Armadilha():
  def __init__(self,nome,afeto,valor,quant,imagem):
    self.nome=nome
    self.afeto=afeto
    self.valor=valor
    self.quant=quant
    self.imagem=imagem
    self.tipo='Armadilha'
    self.escuro=False

  def resolver(self):
    y=sorted([dic_cartas[i.ultima] for i in jogs])
    nomes=[]

    if self.afeto=='todos':
      if 1 in y:
        for i in jogs:
          if self.valor=='moedas':
            i.moedas//=2            
          else:
            i.vida//=2
      elif 2 in y:
        for i in jogs:
          if self.valor=='moedas':
            i.moedas-=2
            if i.moedas<0: i.moedas=0
          else:
            i.vida-=2
            if i.vida<0: i.vida=0
      elif 3 in y:
        for i in jogs:
          if self.valor=='moedas':
            i.moedas-=1
            if i.moedas<0: i.moedas=0
          else:
            i.vida-=1
            if i.vida<0: i.vida=0
      return 'todos perdem '+self.valor
    else:
      if self.valor=='moedas':
        a=max([i.moedas for i in jogs])
        if 5 in y:
          for i in jogs:
            if i.moedas==a:
              i.moedas-=3
              if i.moedas<0: i.moedas=0
              nomes+=[i.nome]
        elif 4 in y:
          for i in jogs:
            if i.moedas==a:
              i.moedas-=2
              if i.moedas<0: i.moedas=0
              nomes+=[i.nome]
        elif 3 in y:
          for i in jogs:
            if i.moedas==a:
              i.moedas-=1
              if i.moedas<0: i.moedas=0
              nomes+=[i.nome]
      else:
        a=max([i.vida for i in jogs])
        if 5 in y:
          for i in jogs:
            if i.vida==a:
              i.vida-=3
              if i.vida<0: i.vida=0
              nomes+=[i.nome]
        elif 4 in y:
          for i in jogs:
            if i.vida==a:
              i.vida-=2
              if i.vida<0: i.vida=0
              nomes+=[i.nome]
        elif 3 in y:
          for i in jogs:
            if i.vida==a:
              i.vida-=1
              if i.vida<0: i.vida=0
              nomes+=[i.nome]
      return f'Jogador{es[plural(len(nomes))]} '+ ', '.join(nomes) +f' {ser[plural(len(nomes))]} afetado{s[plural(len(nomes))]}'

  def __str__(self):
    x=''
    x+=self.nome+'\n'
    if self.afeto=='todos':
      x+=f'Afeta todos: {self.valor}\n'
    else:
      x+=f'Afeta quem tem  mais: {self.valor}\n'
    x+=str(self.quant).strip('{}')+'\n'
    return x

class Chefe():
  def __init__(self,nome,vida,dano,imagem,hab1,hab2):
    self.nome=nome
    self.vida=vida
    self.dano=dano
    self.tipo='Chefe'
    self.imagem=imagem
    self.escuro=True
    self.vivo=True
    self.hab1=hab1
    self.hab2=hab2

  def resolver(self):
    y=sorted([dic_cartas[i.ultima] for i in jogs])
    nomes=[]

    if sum(y)>=self.vida:
      return f'{self.nome} derrotado'
    else:
      for i in jogs:
        if dic_cartas[i.ultima]==y[0]:
          nomes+=[i.nome]
          i.vida+=self.dano 
          if i.vida<0: i.vida=0
      return f'{self.nome} continua vivo\nEle ataca: '+', '.join(nomes)   

  def __str__(self):
    return(
    self.nome+'\n'+
    f'Vida: {self.vida}  Dano: {self.dano}\n'+
    str(self.habilidade1)+
    str(self.habilidade2))

qjog=0
jogs=['']
def players(qjog):
    global jogs

    guerreiro=Personagens('Guerreiro',10,2,'cartas/personagens/guerreiro.png',['1','2','3','4','5'])
    mago=Personagens('Mago',9,1,'cartas/personagens/mago.png',['1','2','3','4','5','boladecristal','boladecristal'])
    cavaleiro=Personagens('Cavaleiro',9,1,'cartas/personagens/cavaleiro.png',['1','2','3','4','5','espada'])
    exploradora=Personagens('Exploradora',8,3,'cartas/personagens/exploradora.png',['1','2','3','4','5','tocha'])
    ladra=Personagens('Ladra',8,2,'cartas/personagens/ladra.png',['1','2','3','4','5','chave'])
    pers=[guerreiro,mago,ladra,exploradora,cavaleiro]

    jogs=[jogs[0]]+['','','','']
    jogs=jogs[:qjog]

    if jogs[0]!='aleatorio':
        if jogs[0]=='mago':
            jogs[0]=mago
            pers.remove(mago)
        elif jogs[0]=='guerreiro':
            jogs[0]=guerreiro
            pers.remove(guerreiro)
        elif jogs[0]=='ladra':
            jogs[0]=ladra
            pers.remove(ladra)
        elif jogs[0]=='exploradora':
            jogs[0]=exploradora
            pers.remove(exploradora)
        elif jogs[0]=='cavaleiro':
            jogs[0]=cavaleiro
            pers.remove(cavaleiro)
        for i in range(1,qjog):
            y=random.choice(pers)
            jogs[i]=y
            pers.remove(y)
    else:
        for i in range(qjog):
            y=random.choice(pers)
            jogs[i]=y
            pers.remove(y)  
    return jogs 

salas=[]
chefes=[]
def gerar_salas(qjog):
  aboboda00=Aboboda('tocha','boladecristal','chave','espada',{'vida':1},'cartas/salas/aboboda0.png')#3
  aboboda01=copy.deepcopy(aboboda00)
  aboboda02=copy.deepcopy(aboboda00)
  aboboda10=Aboboda({'moedas':1},{'moedas':2},{'vida':1},{'moedas':3},{'vida':2},'cartas/salas/aboboda1.png')#2
  aboboda11=copy.deepcopy(aboboda10)

  monstro00=Monstro('Cobra',{2:8,3:8,4:10,5:13}[qjog],-3,'cartas/salas/cobra.png')
  monstro10=Monstro('Zumbi',{2:11,3:11,4:14,5:18}[qjog],-1,'cartas/salas/zumbi.png')
  monstro20=Monstro('Esqueleto',{2:11,3:11,4:14,5:18}[qjog],-3,'cartas/salas/esqueleto.png')
  monstro30=Monstro('Cubo gelatinoso',{2:14,3:14,4:18,5:23}[qjog],-1,'cartas/salas/cubo.png')
  monstro40=Monstro('Troll',{2:14,3:14,4:18,5:23}[qjog],-2,'cartas/salas/troll.png')#2
  monstro41=copy.deepcopy(monstro10)
  monstro50=Monstro('Dragão',{2:14,3:14,4:18,5:23}[qjog],-3,'cartas/salas/dragao.png')#2
  monstro51=copy.deepcopy(monstro30)
  monstro60=Monstro('Goblin',{2:11,3:11,4:14,5:18}[qjog],-2,'cartas/salas/goblin.png')#2
  monstro61=copy.deepcopy(monstro40)

  tesouro00=Tesouro(1,0,'cartas/salas/tesouro0.png')
  tesouro10=Tesouro(2,0,'cartas/salas/tesouro1.png')
  tesouro20=Tesouro(3,0,'cartas/salas/tesouro2.png')
  tesouro30=Tesouro(4,0,'cartas/salas/tesouro3.png')
  tesouro40=Tesouro(2,1,'cartas/salas/tesouro4.png')#2
  tesouro41=copy.deepcopy(tesouro40)
  tesouro50=Tesouro(3,2,'cartas/salas/tesouro5.png')#2
  tesouro51=copy.deepcopy(tesouro50)
  tesouro60=Tesouro(4,2,'cartas/salas/tesouro6.png')#2
  tesouro61=copy.deepcopy(tesouro60)

  armadilha00=Armadilha('Armadilha de imã','mais','moedas',{5:-3,4:-2,3:-1},'cartas/salas/armadilha0.png')#2
  armadilha01=copy.deepcopy(armadilha00)
  armadilha10=Armadilha('Armadilha de pedra','mais','vida',{5:-3,4:-2,3:-1},'cartas/salas/armadilha1.png')
  armadilha20=Armadilha('Armadilha de estacas','todos','vida',{3:-1,2:-2,1:'/2'},'cartas/salas/armadilha2.png')
  armadilha30=Armadilha('Armadilha de lava','todos','moedas',{3:-1,2:-2,1:'/2'},'cartas/salas/armadilha3.png')

  global salas
  salas=[monstro00,monstro10,monstro20,monstro30,monstro40,monstro41,monstro50,monstro51,monstro60,monstro61,
  armadilha00,armadilha01,armadilha10,armadilha20,armadilha30,
  aboboda00,aboboda01,aboboda02,aboboda10,aboboda11,
  tesouro00,tesouro10,tesouro20,tesouro30,tesouro40,tesouro41,tesouro50,tesouro51,tesouro60,tesouro61]

  matilha_de_lobos=     Chefe('Matilha de Lobos',{2:14,3:14,4:14,5:18}[qjog],-3,'cartas/chefes/matilha_de_lobos.png',11,0)
  megadragao=           Chefe('Megadragão',{2:16,3:16,4:23,5:29}[qjog],-4,'cartas/chefes/megadragao.png',5,0)
  medusa=               Chefe('Medusa',{2:12,3:12,4:14,5:20}[qjog],-10,'cartas/chefes/medusa.png',10,0)
  minotauro=            Chefe('Minotauro',{2:11,3:11,4:15,5:19}[qjog],-4,'cartas/chefes/minotauro.png',2,0)
  coletor_de_impostos=  Chefe('Coletor de impostos',{2:14,3:14,4:18,5:23}[qjog],-4,'cartas/chefes/coletor_de_impostos.png',9,0)
  golem=                Chefe('Golem',{2:14,3:14,4:18,5:23}[qjog],0,'cartas/chefes/golem.png',2,8)
  necromante=           Chefe('Necromante',{2:12,3:12,4:15,5:19}[qjog],-2,'cartas/chefes/necromante.png',7,1)
  vampiro=              Chefe('Vampiro',{2:14,3:14,4:18,5:23}[qjog],-3,'cartas/chefes/vampiro.png',4,1)
  esfinge=              Chefe('Esfinge',{2:14,3:14,4:18,5:23}[qjog],-4,'cartas/chefes/esfinge.png',6,0)
  mumia=                Chefe('Múmia',{2:13,3:13,4:18,5:23}[qjog],-4,'cartas/chefes/mumia.png',4,0)
  hidra=                Chefe('Hídra',{2:8,3:8,4:10,5:13}[qjog],-2,'cartas/chefes/hidra.png',12,0)

  global chefes
  chefes=[matilha_de_lobos, hidra, mumia, vampiro, necromante, coletor_de_impostos, golem, megadragao, medusa, esfinge, minotauro]

masmorras=['']*5
def gerador_masmorras():
  global salas, masmorras, chefes
  random.shuffle(salas)
  for i in range(6):
    salas.remove(random.choice(salas))  
  random.shuffle(salas)
  x=[]
  for i in range(12):
    x+=[random.choice(salas)]
    salas.remove(x[-1])
  for i in x:
    i.escuro=True
  salas+=x
  random.shuffle(salas)
  salas+=[random.choice(chefes)]
  masmorras[0]=salas[:5]
  masmorras[1]=salas[5:10]
  masmorras[2]=salas[10:15]
  masmorras[3]=salas[15:20]
  masmorras[4]=salas[20:25]