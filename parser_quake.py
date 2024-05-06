import json
with open("Quake.txt", "r") as quaker:
    texto = quaker.readlines()
jogos=0
vetorFinal = []
def montador(jogo, soma, dicionarioKV):
    
    jogo = {"game":"{}".format(jogo),
            "status":{
                "total_kills":"{}".format(soma),
                "players":[
                ]
                }
            }
    for chave in dicionarioKV.keys():
        jogo["status"]["players"].append({"nome":chave,"kills":dicionarioKV[chave]})
    vetorFinal.append(jogo)
    

for linha in texto:
    #inicio do game
    if "InitGame:" in linha:
        jogos+=1
        dicionarioAux = {}
        soma = 0
    if "ClientUserinfoChanged" in linha:
        nome = linha[linha.find('n\\')+2:linha.find('\\t')]
        if nome not in dicionarioAux.keys():
            dicionarioAux[nome] = 0

    #kill detectada
    if "Kill:" in linha:
        soma += 1
        splitado = linha.split(":")
        killed = splitado[-1].strip().split(" killed ")
        killer = killed[0] #selecionando palavra antes de killed - o que matou
        dead = killed[1][:killed[1].find(" by")] #selecionando palavra apos killed - o que foi morto
        
        if killer == "<world>" or killer == dead: #checa se foi suic ou se foi morto pelo ambiente
            dicionarioAux[dead] -= 1 #se ja existe no dicionario, subtrai 1
        else:
            dicionarioAux[killer] += 1 #se ja existe no dicionario, adiciona 1
        
    if "ShutdownGame:" in linha:
        montador(jogos,soma, dicionarioAux) #jogo acabou, mandar infos para funcao

print(vetorFinal)

with open("resultado_parser.json", "w") as arquivo_json:
    # Escrever o vetor no arquivo JSON
    json.dump(vetorFinal, arquivo_json)