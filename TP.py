from itertools import product

#retorna o numero de linhas de um arquivo / recebe o nome do arquivo
def numerodeLinhas(nome):
    return sum(1 for line in open(nome+".txt"))

#Retorna os dados iniciais de Ducan
def preencherDucan():
    Ducan = [numerodeLinhas("entrada"), 0, 0]
    return Ducan

#Retorna uma lista de Adiversarios preenchidos os dados obtidos do arquivo
def preencherAdversarios():
    with open("entrada.txt") as f:
        i = 0
        Adversarios = []
        for line in f:
            if(i!=0):
                Adversarios.append([i,line.split()[0],line.split()[1]])
            i+=1
    f.close()
    return Adversarios

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
    justa.append(duc)
    return justa

#Verifica a posicao em que Ducan ficou na Justa / Recebe Justa
def VerificarPosicaoNaJusta(justa):
    duc = justa[len(justa)-1]
    pos = -1
    esforco = -1
    for i in justa:
        if(i[1]>=duc[1]):
            if(duc[0]<i[0]):
                x = duc[0]
                duc[0] = i[0]
                i[0] = x
                pos = duc[0]        
                esforco = duc[2]
                
        if(duc[1]> i[1]):
            if(duc[0] > i[0]):
                x = duc[0]
                duc[0] = i[0]
                i[0] = x  
                pos = duc[0]        
                esforco = duc[2]

    return [pos, esforco]

#Define o esforco inicial para verificar qual o menor esforco necessario
def esforcoinicial():
    esf = 0
    for line in open("entrada.txt"):
            esf += int(line.split()[1])
    return esf

#Compara os resultados de cada Justa tentando descobrir o de menor esforco
def compararresultados(esforcototal):
    for i in comb:
        situacao = VerificarPosicaoNaJusta(GerarJusta(i,preencherDucan(), Adversarios))
        if(situacao[0]<=retornarDadosArquivo(1,2)):    
            if(situacao[1] < esforcototal):
                esforcototal = situacao[1]
    return esforcototal

#main
if __name__ =="__main__":
    Ducan = preencherDucan()
    Adversarios = preencherAdversarios()
    comb = Combinacoes()
    esforcototal = esforcoinicial()
    esforcototal = compararresultados(esforcototal)    
    print(esforcototal)
    print("esperado = 12")


