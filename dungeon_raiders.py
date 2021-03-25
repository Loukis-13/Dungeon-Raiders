import random,copy

class Personagens():
  def __init__(self,nome,vida,moedas,imagem,cartas):
    self.nome=nome
    self.vida=vida
    self.moedas=moedas
    self.imagem=imagem
    self.cartas=cartas
    self.ultima=''   

  def jogar(self, tipo):
    while True:
      x=random.choice(self.cartas)
      if (x=='chave' and tipo!='Tesouro') or (x=='espada' and tipo!='Monstro'):
        continue
      if x=='tocha' or x=='boladecristal':
        continue
      break
    self.ultima=x
    self.cartas.remove(x)

  def chefe_jogar(self, hab):
    while True:
      x=random.choice(self.cartas)
      if 3 in hab and x=='espada':
        continue
      if 7 in hab and x=='boladecristal':
        continue
      break
    self.ultima=[x,'0']
    self.cartas.remove(x)

    self.cartas+=['0','0','0']
    while True:
      x=random.choice(self.cartas)
      if 3 in hab and x=='espada':
        continue
      if 7 in hab and x=='boladecristal':
        continue
      break
    self.ultima[1]=x
    self.cartas.remove(x)

  def redefinir(self):
    for i in ['1','2','3','4','5']:
      if i in self.cartas:
        self.cartas.remove(i)
    self.cartas=['1','2','3','4','5']+self.cartas

  def __repr__(self):
    return (
    self.nome+'\n'+
    f'Vida: {self.vida}  Moedas: {self.moedas}\n'+
    f'cartas: {self.cartas}\n')

dic_cartas={'1':1, '2':2, '3':3, '4':4, '5':5, 'espada':5, 'chave':5, 'boladecristal':0, 'tocha':0}

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
    val=[['',[0,0,0,0]]]*5

    for ii,i in enumerate(jogs):
      if dic_cartas[i.ultima]==1:
        if isinstance(self.item1, str):
          i.cartas+=[self.item1]
          val[ii]=[self.item1,[1,1,1,1]]
        else:
          i.moedas+=1
          val[ii]=['+1',[1,1,0,1]]
          if i.moedas>20: i.moedas=20
      elif dic_cartas[i.ultima]==2:
        if isinstance(self.item2, str):
          i.cartas+=[self.item2]
          val[ii]=[self.item2,[1,1,1,1]]
        else:
          i.moedas+=2
          val[ii]=['+2',[1,1,0,1]]
          if i.moedas>20: i.moedas=20
      elif dic_cartas[i.ultima]==3:
        if isinstance(self.item3, str):
          i.cartas+=[self.item3]
          val[ii]=[self.item3,[1,1,1,1]]
        else:
          i.vida+=1
          val[ii]=['+1',[1,0,0,1]]
          if i.vida>10: i.vida=10
      elif dic_cartas[i.ultima]==4:
        if isinstance(self.item4, str):
          i.cartas+=[self.item4]
          val[ii]=[self.item4,[1,1,1,1]]
        else:
          i.moedas+=3
          val[ii]=['+3',[1,1,0,1]]
          if i.moedas>20: i.moedas=20
      elif dic_cartas[i.ultima]==5:
        if isinstance(self.item2, str):
          i.vida+=1
          val[ii]=['+1',[1,0,0,1]]
          if i.vida>10: i.vida=10
        else:
          i.vida+=2
          val[ii]=['+2',[1,0,0,1]]
          if i.vida>10: i.vida=10
    return ('',val,False)

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
    self.escuro=False

  def resolver(self):
    y=sorted([dic_cartas[i.ultima] for i in jogs])
    danos=[['',[0,0,0,0]]]*5
    morto=False

    #dois jogadores
    if len(jogs)==2:
      if y[0]==y[1]:
        return ('? ? ?', danos, morto)

    if sum(y)<self.vida[len(jogs)]:
      for i,j in enumerate(jogs):
        if dic_cartas[j.ultima]==y[0]:
          j.vida+=self.dano 
          danos[i]=[str(self.dano),[1,0,0,1]]
          if j.vida<0: j.vida=0
    else:
      morto=True
    return (str(sum(y)), danos, morto)

  def __str__(self):
    return (
    self.nome+'\n'+
    f'Vida: {self.vida}  Dano: {self.dano}\n')

class Tesouro():
  def __init__(self,bau1,bau2,imagem):
    self.bau1=bau1
    self.bau2=bau2
    self.imagem=imagem
    self.tipo='Tesouro'
    self.escuro=False

  def resolver(self):
    y=sorted([dic_cartas[i.ultima] for i in jogs])
    din=[['',[0,0,0,0]]]*5

    for i,j in enumerate(jogs):
      if dic_cartas[j.ultima]==y[-1]:
        x=self.bau1//y.count(y[-1])
        j.moedas+=x
        if j.moedas>20:j.moedas=20
        din[i]=[f'+{x}',[1,1,0,1]]
        
    if self.bau2:
      y=[i for i in y if i!=y[-1]]
      if len(y)==0:
        return ('',din,False)
      for i,j in enumerate(jogs):
        if dic_cartas[j.ultima]==y[-1]:
          x=self.bau2//y.count(y[-1])
          j.moedas+=x
          if j.moedas>20: j.moedas=20
          din[i]=[f'+{x}',[1,1,0,1]]
    return ('',din,False)

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
    val=[['',[0,0,0,0]]]*5

    if self.afeto=='todos':
      if 1 in y:
        for i,j in enumerate(jogs):
          if self.valor=='moedas':
            j.moedas//=2    
            val[i]=['/2',[1,1,0,1]]
          else:
            j.vida//=2
            val[i]=['/2',[1,0,0,1]]
      elif 2 in y:
        for i,j in enumerate(jogs):
          if self.valor=='moedas':
            j.moedas-=2
            if j.moedas<0: j.moedas=0
            val[i]=['-2',[1,1,0,1]]
          else:
            j.vida-=2
            if j.vida<0: j.vida=0
            val[i]=['-2',[1,0,0,1]]
      elif 3 in y:
        for i,j in enumerate(jogs):
          if self.valor=='moedas':
            j.moedas-=1
            if j.moedas<0: j.moedas=0
            val[i]=['-1',[1,1,0,1]]
          else:
            j.vida-=1
            if j.vida<0: j.vida=0
            val[i]=['-1',[1,0,0,1]]
    else:
      if self.valor=='moedas':
        a=max([i.moedas for i in jogs])
        if 5 in y:
          for ii,i in enumerate(jogs):
            if i.moedas==a:
              i.moedas-=3
              if i.moedas<0: i.moedas=0
              val[ii]=['-3',[1,1,0,1]]
        elif 4 in y:
          for ii,i in enumerate(jogs):
            if i.moedas==a:
              i.moedas-=2
              if i.moedas<0: i.moedas=0
              val[ii]=['-2',[1,1,0,1]]
        elif 3 in y:
          for ii,i in enumerate(jogs):
            if i.moedas==a:
              i.moedas-=1
              if i.moedas<0: i.moedas=0
              val[ii]=['-1',[1,1,0,1]]
      else:
        a=max([i.vida for i in jogs])
        if 5 in y:
          for ii,i in enumerate(jogs):
            if i.vida==a:
              i.vida-=3
              if i.vida<0: i.vida=0
              val[ii]=['-3',[1,0,0,1]]
        elif 4 in y:
          for ii,i in enumerate(jogs):
            if i.vida==a:
              i.vida-=2
              if i.vida<0: i.vida=0
              val[ii]=['-2',[1,0,0,1]]
        elif 3 in y:
          for ii,i in enumerate(jogs):
            if i.vida==a:
              i.vida-=1
              if i.vida<0: i.vida=0
              val[ii]=['-1',[1,0,0,1]]
    return ('',val,False)

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
  def __init__(self,nome,vida,dano,imagem,hab):
    self.nome=nome
    self.vida=vida
    self.dano=dano
    self.tipo='Chefe'
    self.imagem=imagem
    self.escuro=True
    self.hab=hab

  def resolver(self):
    chefe_dic_cartas={'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, 'espada':5, 'chave':0, 'boladecristal':0, 'tocha':0}
    danos=[['',[0,0,0,0]]]*5
    morto=False   

    if 4 in self.hab:
      if self.nome=='Múmia':
        chefe_dic_cartas['tocha']=5
      elif self.nome=='Vampiro':
        chefe_dic_cartas['tocha']=3
    if 6 in self.hab:
      chefe_dic_cartas['boladecristal']=5

    y=sorted([sum(chefe_dic_cartas[i] for i in j.ultima) for j in jogs])

    if 8 in self.hab:
      self.dano=-y[-1] if y[-1]<5 else -5

    if sum(y)>=self.vida[len(jogs)]:
      morto=True
      if 5 in self.hab:
        dic_cartas['espada']=0
        yy=sorted([max(dic_cartas[i] for i in j.ultima) for j in jogs])
        for ii,j in enumerate(jogs):
          if max(dic_cartas[i] for i in j.ultima)==yy[-1]:
            j.moedas+=self.bau1//yy.count(yy[-1])
            if j.moedas>20:j.moedas=20
            danos[ii]=[self.bau1//yy.count(yy[-1]),[1,1,0,1]]
        dic_cartas['espada']=5
    else:
      for ii,j in enumerate(jogs):
        if 2 not in self.hab:     
          if sum(chefe_dic_cartas[i] for i in j.ultima)==y[0]:
            if 11 in self.hab:
              if 'tocha' in j.ultima:
                continue
            j.vida+=self.dano 
            danos[ii]=[str(self.dano),[1,0,0,1]]
            if j.vida<0: j.vida=0
            if 9 in self.hab:
              j.moedas-=y[-1] if y[-1]<5 else 5
              if j.moedas<0: j.moedas=0
        else:
          if max(chefe_dic_cartas[i] for i in j.ultima)==y[-1] if y[-1]<5 else 5:
            j.vida+=self.dano 
            danos[ii]=[str(self.dano),[1,0,0,1]]
            if j.vida<0: j.vida=0
    
      if 1 in self.hab:
        y=[i for i in y if i!=y[0]]
        for ii,p in enumerate(jogs):
          if min(chefe_dic_cartas[i] for i in j.ultima)==y[0]:
            j.vida+=self.dano
            danos[ii]=[str(self.dano),[1,0,0,1]]
            if j.vida<0: j.vida=0

    return (str(sum(y)), danos, morto)

  def __str__(self):
    return(
    self.nome+'\n'+
    f'Vida: {self.vida[len(jogs)]}  Dano: {self.dano}\n'+
    str(self.habilidade1)+
    str(self.habilidade2))

jogs=[]
def players(qjog, escolha):
  guerreiro=Personagens('Guerreiro',10,2,'cartas/personagens/guerreiro.png',['1','2','3','4','5'])
  mago=Personagens('Mago',9,1,'cartas/personagens/mago.png',['1','2','3','4','5','boladecristal','boladecristal'])
  cavaleiro=Personagens('Cavaleiro',9,1,'cartas/personagens/cavaleiro.png',['1','2','3','4','5','espada'])
  exploradora=Personagens('Exploradora',8,3,'cartas/personagens/exploradora.png',['1','2','3','4','5','tocha'])
  ladra=Personagens('Ladra',8,2,'cartas/personagens/ladra.png',['1','2','3','4','5','chave'])
  pers={'guerreiro':guerreiro, 'mago':mago, 'ladra':ladra, 'exploradora':exploradora, 'cavaleiro':cavaleiro}
  
  jogs.clear()

  if escolha!='aleatorio':
    jogs.append(pers.pop(escolha))
  for i in range(qjog-len(jogs)):
    jogs.append(pers.pop(random.choice(list(pers.keys()))))

salas=[]
chefes=[]
def gerar_salas():
  aboboda00=Aboboda('tocha','boladecristal','chave','espada',{'vida':1},'cartas/salas/aboboda0.png')#3
  aboboda01=copy.deepcopy(aboboda00)
  aboboda02=copy.deepcopy(aboboda00)
  aboboda10=Aboboda({'moedas':1},{'moedas':2},{'vida':1},{'moedas':3},{'vida':2},'cartas/salas/aboboda1.png')#2
  aboboda11=copy.deepcopy(aboboda10)

  monstro00=Monstro('Cobra',{2:8,3:8,4:10,5:13},-3,'cartas/salas/cobra.png')
  monstro10=Monstro('Zumbi',{2:11,3:11,4:14,5:18},-1,'cartas/salas/zumbi.png')
  monstro20=Monstro('Esqueleto',{2:11,3:11,4:14,5:18},-3,'cartas/salas/esqueleto.png')
  monstro30=Monstro('Cubo gelatinoso',{2:14,3:14,4:18,5:23},-1,'cartas/salas/cubo.png')
  monstro40=Monstro('Troll',{2:14,3:14,4:18,5:23},-2,'cartas/salas/troll.png')#2
  monstro41=copy.deepcopy(monstro10)
  monstro50=Monstro('Dragão',{2:14,3:14,4:18,5:23},-3,'cartas/salas/dragao.png')#2
  monstro51=copy.deepcopy(monstro30)
  monstro60=Monstro('Goblin',{2:11,3:11,4:14,5:18},-2,'cartas/salas/goblin.png')#2
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

  salas[:]=[monstro00,monstro10,monstro20,monstro30,monstro40,monstro41,monstro50,monstro51,monstro60,monstro61,
  armadilha00,armadilha01,armadilha10,armadilha20,armadilha30,
  aboboda00,aboboda01,aboboda02,aboboda10,aboboda11,
  tesouro00,tesouro10,tesouro20,tesouro30,tesouro40,tesouro41,tesouro50,tesouro51,tesouro60,tesouro61]

  matilha_de_lobos=     Chefe('Matilha de Lobos',{2:14,3:14,4:14,5:18},-3,'cartas/chefes/matilha_de_lobos.png',[11,0])
  megadragao=           Chefe('Megadragão',{2:16,3:16,4:23,5:29},-4,'cartas/chefes/megadragao.png',[5,0])
  medusa=               Chefe('Medusa',{2:12,3:12,4:14,5:20},-10,'cartas/chefes/medusa.png',[10,0])
  minotauro=            Chefe('Minotauro',{2:11,3:11,4:15,5:19},-4,'cartas/chefes/minotauro.png',[2,0])
  coletor_de_impostos=  Chefe('Coletor de impostos',{2:14,3:14,4:18,5:23},-4,'cartas/chefes/coletor_de_impostos.png',[9,0])
  golem=                Chefe('Golem',{2:14,3:14,4:18,5:23},0,'cartas/chefes/golem.png',[3,8])
  necromante=           Chefe('Necromante',{2:12,3:12,4:15,5:19},-2,'cartas/chefes/necromante.png',[7,1])
  vampiro=              Chefe('Vampiro',{2:14,3:14,4:18,5:23},-3,'cartas/chefes/vampiro.png',[4,1])
  esfinge=              Chefe('Esfinge',{2:14,3:14,4:18,5:23},-4,'cartas/chefes/esfinge.png',[6,0])
  mumia=                Chefe('Múmia',{2:13,3:13,4:18,5:23},-4,'cartas/chefes/mumia.png',[4,0])
  hidra=                Chefe('Hídra',{2:8,3:8,4:10,5:13},-2,'cartas/chefes/hidra.png',[12,0])

  chefes[:]=[matilha_de_lobos, hidra, mumia, vampiro, necromante, coletor_de_impostos, golem, megadragao, medusa, esfinge, minotauro]

masmorras=[]
def gerador_masmorras():
  random.shuffle(salas)
  for i in range(6):
    salas.pop()  
  for i in range(12):
    salas[i].escuro=True
  random.shuffle(salas)
  salas.extend([random.choice(chefes)])

  masmorras[:]=[salas[i:i+5] for i in range(0,25,5)]