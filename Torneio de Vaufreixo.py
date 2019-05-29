from itertools import product
import pandas as pd
import random
import os
#retorna o numero de linhas de um arquivo / recebe o nome do arquivo
def numerodeLinhas(nome):
    return sum(1 for line in open(nome+".txt"))
#Retorna os dados iniciais de Ducan
def preencherDucan():
    Ducan = [numerodeLinhas("entrada"), 0, 0]
    return Ducan
#retorna uma informacao especifica do arquivo / recebe a linha e a coluna da informacao
def retornarDadosArquivo(Linha, Coluna):
    with open("entrada.txt") as f:
        i = 0
        for line in f:
            if(i == Linha-1):
                return int(line.split()[Coluna-1])
            i += 1
    f.close()
    return -1
#retorna as combinacoes possiveis de justas dado o numero de participantes
def Combinacoes():
    comb = []
    genComb = product([0,1], repeat = retornarDadosArquivo(1,1))
    for subset in genComb:
        comb.append(subset)
    return comb
#Gera cada justa / recebe a combinacao especifica de quem ganha, recebe o estado de Ducan, recebe os Adv
def GerarJusta(Comb, Ducan, Adversarios):
    justa = []
    jus = []
    duc = Ducan
    adv = Adversarios
    cont = 0    
    for j in adv:
        if(Comb[cont] == 0):
            jus.append(j[0])
            jus.append(int(j[1])+1)
            jus.append(j[2])
            justa.append(jus)
        else:
            duc[0] = duc[0]
            duc[1] = duc[1]+1
            duc[2] = int(duc[2])+int(j[2])
            jus.append(j[0])
            jus.append(int(j[1]))
            jus.append(j[2])
            justa.append(jus)
        jus = []
        cont+=1
    cont = 0
    justa.append(duc)
    return justa
#Verifica a posicao em que Ducan ficou na Justa / Recebe Justa
def VerificarPosicaoNaJusta(justa, k):
    duc = justa[len(justa)-1]
    j = -1
    for i in justa:
        if(i[0]!=len(justa)-1):
            if(i[1]>duc[1]):            #se o adversario tem mais pontos que Ducan            
                if(duc[0]<i[0]):        #se Ducan esta em posicao melhor que o adversario
                    x = duc[0]
                    duc[0] = i[0]
                    i[0] = x
            elif(duc[1] > i[1]):        # se ducan esta melhor que adversario
                if(duc[0] > i[0]):      #se ducan esta em posicao pior que o adversario
                    x = duc[0]
                    duc[0] = i[0]
                    i[0] = x
            elif(i[1] == duc[1]):
                if(k[j] == 0):
                    if(duc[0]< i[0]):
                        x = duc[0]
                        duc[0] = i[0]
                        i[0] = x
                else:
                    if(duc[0] > i[0]):
                        x = duc[0]
                        duc[0] = i[0]
                        i[0] = x
        j+=1
    return [duc[0], duc[2]]
#Define o esforco inicial para verificar qual o menor esforco necessario
def esforcoinicial():
    esf = 0
    for line in open("entrada.txt"):
            esf += int(line.split()[1])
    return esf
#Compara os resultados de cada Justa tentando descobrir o de menor esforco
def compararresultados(esforcototal, comb):
    j=-1
    for i in comb:
        situacao = VerificarPosicaoNaJusta(GerarJusta(i,preencherDucan(), preencherAdversarios()),i)
        if(situacao[1] < esforcototal):
          if(situacao[0]<=retornarDadosArquivo(1,2)):
            esforcototal = situacao[1]
            j+=1
    if(j==-1):
      return j
    return esforcototal
#Ordenacao dos adversarios por pontos e indexados
def OrdenarAdversarios(adv, Adversarios):
  j= 0
  col1 = []
  col2 = []
  col3 = []
  for i in adv:
    col1.append(j)
    j+=1
    col2.append(i[0])
    col3.append(i[1])    
  advi = pd.DataFrame({'col2' : col2,'col3' : col3})        
  advi = advi.sort_values(by = ['col2'])
  aux = advi.values
  j = 1
  for i in aux:
    Adversarios.append([j, i[0], i[1]])
    j+=1
  return Adversarios
#Retorna uma lista de Adiversarios preenchidos os dados obtidos do arquivo
def preencherAdversarios():
    with open("entrada.txt") as f:
        Adversarios = []
        adv = []
        i = 0
        for line in f:
          if(i!=0):
            adv.append([line.split()[0],line.split()[1]])
          i+=1
    return OrdenarAdversarios(adv, Adversarios)
def gerarEntradas(num):
  arquivo = open('entrada.txt', 'w')
  N = num;
  K = random.randint(1,N)
  arquivo.write(str(N)+" "+str(K))
  for x in range(N):
    arquivo.write("\n")
    arquivo.write(str(random.randint(0,N))+" "+str(random.randint(0,N*2)))
    
    

#main
if __name__ =="__main__":
  justasTestes = (2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 1000, 10000, 100000)
  for i in justasTestes:
    gerarEntradas(i)
    print(compararresultados(esforcoinicial(),Combinacoes()))
