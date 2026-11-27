# Participantes: Lucas Macedo Dos Santos | RA 2019229
# Juan Ferreira Honória Pedroza | RA 2032428
# João Celso da Silva Nogueira dos santos | RA 2031553
# Raissa Kaori Kawakami | RA 2040357


def inserirVertice(grafo: dict, vertice: str):
    if vertice in grafo["vertices"]:
        print("Vértice já existe.")
        return

    grafo["vertices"].append(vertice)
    print("Vértice adicionado.")


def apagarVertice(grafo: dict, vertice: str):
    if vertice not in grafo["vertices"]:
        print("Vértice não existe.")
        return

    grafo["vertices"].remove(vertice)

    grafo["arestas"] = [
        aresta for aresta in grafo["arestas"]
        if aresta[0] != vertice and aresta[1] != vertice
    ]

    print("Vértice removido com sucesso.")


def inserirAresta(grafo: dict, verticeEntrada: str,
                  verticeSaida: str, direcional: bool, peso: float):
    if verticeEntrada not in grafo["vertices"]:
        inserirVertice(grafo, verticeEntrada)

    if verticeSaida not in grafo["vertices"]:
        inserirVertice(grafo, verticeSaida)

    if peso < 0:
        print("O peso não pode ser negativo.")
        return

    for origem, destino, peso_existente in grafo["arestas"]:
        if (origem == verticeEntrada and destino == verticeSaida) or (
            not direcional and origem == verticeSaida and destino == verticeEntrada
        ):
            print("Aresta já existe.")
            return

    grafo["arestas"].append([verticeEntrada, verticeSaida, peso])
    print("Aresta adicionada com sucesso!")


def apagarAresta(grafo: dict, verticeSaida: str,
                 verticeEntrada: str, direcional: bool):
    if verticeSaida not in grafo["vertices"] or verticeEntrada not in grafo["vertices"]:
        print("Um ou ambos os vértices não existem.")
        return

    removido = False
    for aresta in grafo["arestas"]:
        origem, destino, peso = aresta
        if (origem == verticeSaida and destino == verticeEntrada) or (
            not direcional and origem == verticeEntrada and destino == verticeSaida
        ):
            grafo["arestas"].remove(aresta)
            removido = True
            break

    if removido:
        print("Aresta removida com sucesso.")
    else:
        print("Aresta não existe.")


def obterVizinhos(grafo: dict, vertice: str, direcional: bool):
    if vertice not in grafo["vertices"]:
        return None

    vizinhos = []
    for origem, destino, peso in grafo["arestas"]:
        if origem == vertice:
            if destino not in vizinhos:
                vizinhos.append(destino)
        if not direcional and destino == vertice:
            if origem not in vizinhos:
                vizinhos.append(origem)

    return vizinhos


def existeAresta(grafo: dict, origem: str,
                 destino: str, direcional: bool):
    if origem not in grafo["vertices"] or destino not in grafo["vertices"]:
        return False

    for origem_aresta, destino_aresta, peso in grafo["arestas"]:
        if origem_aresta == origem and destino_aresta == destino:
            return True
        if not direcional and origem_aresta == destino and destino_aresta == origem:
            return True

    return False


def percurso_valido(grafo: dict, percurso, direcional: bool):
    if not percurso:
        print("Não adicionou um percurso.")
        return False

    for vertice in percurso:
        if vertice not in grafo["vertices"]:
            print(f"O vértice {vertice} não existe.")
            return False

    if len(percurso) == 1:
        print("Percurso válido de um único vértice.")
        return True

    for i in range(len(percurso) - 1):
        atual = percurso[i]
        proximo = percurso[i + 1]

        if not existeAresta(grafo, atual, proximo, direcional):
            print(f"Não existe aresta de {atual} para {proximo}.")
            return False

    print("Percurso válido.")
    return True


def grau_vertices(grafo: dict, direcional: bool):
    graus = {}

    for vertice in grafo["vertices"]:
        graus[vertice] = {"in": 0, "out": 0, "total": 0}

    for origem, destino, peso in grafo["arestas"]:
        if origem in graus:
            graus[origem]["out"] += 1
        if destino in graus:
            graus[destino]["in"] += 1
        if not direcional:
            if origem in graus:
                graus[origem]["in"] += 1
            if destino in graus:
                graus[destino]["out"] += 1

    for vertice in graus:
        if not direcional:
            vizinhos = obterVizinhos(grafo, vertice, direcional)
            graus[vertice]["out"] = len(vizinhos)
            graus[vertice]["in"] = len(vizinhos)
            graus[vertice]["total"] = len(vizinhos)
        else:
            graus[vertice]["total"] = (
                graus[vertice]["in"] + graus[vertice]["out"]
            )

    for vertice, grau in graus.items():
        print(
            f"{vertice}: entrada = {grau['in']}, "
            f"saída = {grau['out']}, total = {grau['total']}"
        )


def listarVizinhos(grafo: dict, vertice: str, direcional: bool):
    vizinhos = obterVizinhos(grafo, vertice, direcional)

    if vizinhos is None:
        print("Vértice não existe.")
    else:
        print(f"Vizinhos de {vertice}: {vizinhos}")


def exibirgrafo(grafo: dict):
    if not grafo["vertices"] and not grafo["arestas"]:
        print("Grafo vazio.")
        return

    print("Vértices:", grafo["vertices"])
    print("Arestas (origem, destino, peso):", grafo["arestas"])


grafo = {"vertices": [], "arestas": []}

direcional = int(input(
    "O grafo é direcional?\n1. Sim\n2. Não\n"
)) == 1



def menor_caminho(grafo: dict, inicio: str, destino: str):

    if inicio not in grafo["vertices"]:
        print("Vértice inicial não existe.")
        return

    if destino not in grafo["vertices"]:
        print("Vértice de destino não existe.")
        return

    fila = [inicio]
    visitados = [inicio]

    caminhos = {inicio: None}

    while fila:

        vertice = fila.pop(0)

        if vertice == destino:

            caminho = []
            atual = destino

            while atual is not None:
                caminho.append(atual)
                atual = caminhos[atual]

            caminho.reverse()

            print("Menor caminho:", " -> ".join(caminho))
            print("Quantidade de arestas:", len(caminho) - 1)

            return caminho

        for vizinho in obterVizinhos(grafo, vertice, direcional):

            if vizinho not in visitados:

                visitados.append(vizinho)
                fila.append(vizinho)

                caminhos[vizinho] = vertice

    print("Não existe caminho entre esses vértices.")
    return None

def busca_largura(grafo: dict, inicio: str):

    if inicio not in grafo["vertices"]:
        print("Vértice inicial não existe.")
        return

    fila = [inicio]
    visitados = []

    while fila:

        vertice = fila.pop(0)

        if vertice not in visitados:
            visitados.append(vertice)

            for vizinho in obterVizinhos(grafo, vertice, direcional):

                if vizinho not in fila and vizinho not in visitados:
                    fila.append(vizinho)

    print("Ordem de visita:", visitados)
    return visitados


def encontraCiclos(grafo: dict):
    visitados = []

    for inicio in grafo["vertices"]:
        if inicio not in visitados:
            fila = [(inicio, None)]

            while fila:
                vertice, pai = fila.pop(0)

                if vertice not in visitados:
                    visitados.append(vertice)

                    for vizinho in obterVizinhos(grafo, vertice, False):

                        if vizinho not in visitados:
                            fila.append((vizinho, vertice))

                        elif vizinho != pai:
                            print("Temos um ciclo")

def busca_profundidade(grafo: dict, inicio: str):
    if inicio not in grafo["vertices"]:
        print("Vértice inicial não existe.")
        return

    pilha = [inicio]
    visitados = []

    while pilha:
        vertice = pilha.pop()

        if vertice not in visitados:
            visitados.append(vertice)

            for vizinho in obterVizinhos(grafo, vertice, direcional):

                if vizinho not in pilha and vizinho not in visitados:
                    pilha.append(vizinho)

    print("Ordem de visita:", visitados)
    return visitados

def encontra_ciclos_dfs(grafo: dict, direcional: bool):
    if direcional:
        estado = {v: 0 for v in grafo["vertices"]}

        def dfs_dir(vertice):
            estado[vertice] = 1
            for vizinho in obterVizinhos(grafo, vertice, True):
                if estado[vizinho] == 1:
                    return True
                if estado[vizinho] == 0 and dfs_dir(vizinho):
                    return True
            estado[vertice] = 2
            return False

        for v in grafo["vertices"]:
            if estado[v] == 0:
                if dfs_dir(v):
                    print("O grafo possui ciclo.")
                    return True

        print("O grafo não possui ciclo.")
        return False

    else:
        visitados = []

        def dfs_nao_dir(vertice, pai):
            visitados.append(vertice)
            for vizinho in obterVizinhos(grafo, vertice, False):
                if vizinho not in visitados:
                    if dfs_nao_dir(vizinho, vertice):
                        return True
                elif vizinho != pai:
                    return True
            return False

        for v in grafo["vertices"]:
            if v not in visitados:
                if dfs_nao_dir(v, None):
                    print("O grafo possui ciclo.")
                    return True

        print("O grafo não possui ciclo.")
        return False


def obterPeso(grafo: dict, origem: str, destino: str, direcional: bool):
    for origem_aresta, destino_aresta, peso in grafo["arestas"]:
        if origem_aresta == origem and destino_aresta == destino:
            return peso
        if not direcional and origem_aresta == destino and destino_aresta == origem:
            return peso
    return None


def dijkstra(grafo: dict, inicio: str, destino: str, direcional: bool):
    if inicio not in grafo["vertices"]:
        print("Vértice inicial não existe.")
        return None

    if destino not in grafo["vertices"]:
        print("Vértice de destino não existe.")
        return None

    distancias = {vertice: float("inf") for vertice in grafo["vertices"]}
    anteriores = {vertice: None for vertice in grafo["vertices"]}
    nao_visitados = grafo["vertices"].copy()
    distancias[inicio] = 0

    while nao_visitados:
        atual = min(nao_visitados, key=lambda vertice: distancias[vertice])

        if distancias[atual] == float("inf"):
            break

        nao_visitados.remove(atual)

        if atual == destino:
            break

        for vizinho in obterVizinhos(grafo, atual, direcional):
            if vizinho in nao_visitados:
                peso = obterPeso(grafo, atual, vizinho, direcional)
                nova_distancia = distancias[atual] + peso

                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    anteriores[vizinho] = atual

    if distancias[destino] == float("inf"):
        print("Não existe caminho entre esses vértices.")
        return None

    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = anteriores[atual]

    caminho.reverse()
    print("Menor caminho:", " -> ".join(caminho))
    print("Custo total:", distancias[destino])
    return caminho, distancias[destino]


while True:
    try:
        opc = int(input(
            "\nDigite uma opção:\n"
            "1. Inserir vértice\n"
            "2. Remover vértice\n"
            "3. Inserir aresta\n"
            "4. Remover aresta\n"
            "5. Calcular grau dos vértices\n"
            "6. Verificar se existe uma aresta\n"
            "7. Listar vizinhos\n"
            "8. Verificar percurso\n"
            "9. Exibir grafo\n"
            "10. Menor caminho de um vértice para outro\n"
            "11. Busca em largura\n"
            "12. Verificar se o grafo possui ciclos\n"
            "13. Busca em profundidade\n"
            "14. Verificar se o grafo possui ciclos usando DFS\n"
            "15. Menor caminho usando Dijkstra\n"
            "0. Sair\n"
        ))
    except ValueError:
        print("Digite um número válido.")
        continue

    match opc:
        case 0:
            break

        case 1:
            vertice = input("Nome do vértice: ")
            inserirVertice(grafo, vertice)

        case 2:
            vertice = input("Vértice a remover: ")
            apagarVertice(grafo, vertice)

        case 3:
            exibirgrafo(grafo)
            origem = input("De qual vértice sai a aresta? ")
            destino = input("Para qual vértice vai a aresta? ")
            try:
                peso = float(input("Peso da aresta: "))
                inserirAresta(grafo, origem, destino, direcional, peso)
            except ValueError:
                print("Digite um peso numérico válido.")

        case 4:
            exibirgrafo(grafo)
            origem = input("De qual vértice sai a aresta? ")
            destino = input("Para qual vértice vai a aresta? ")
            apagarAresta(grafo, origem, destino, direcional)

        case 5:
            grau_vertices(grafo, direcional)

        case 6:
            origem = input("Vértice de origem: ")
            destino = input("Vértice de destino: ")

            if existeAresta(grafo, origem, destino, direcional):
                print("Existe uma aresta entre os vértices.")
            else:
                print("Não existe uma aresta entre os vértices.")

        case 7:
            vertice = input("Vértice para listar os vizinhos: ")
            listarVizinhos(grafo, vertice, direcional)

        case 8:
            entrada = input(
                "Digite o percurso separado por vírgulas "
                "(ex.: V1,V2,V5): "
            )
            percurso = [
                v.strip() for v in entrada.split(",") if v.strip()
            ]
            percurso_valido(grafo, percurso, direcional)

        case 9:
            exibirgrafo(grafo)
        
        case 10:
            print("Vértices disponíveis:", grafo["vertices"])
            inicio = input("Insira o vertice inicial: ")
            destino = input("insira o vertice de destino: ")
            menor_caminho(grafo, inicio, destino)

        case 11:
            print("Vértices disponíveis:", grafo["vertices"])
            inicio = input("Insira o vértice inicial: ")
            busca_largura(grafo, inicio)
        
        case 12:    
            encontraCiclos(grafo)
            
        case 13:
            print("Vértices disponíveis:", grafo["vertices"])
            inicio = input("Insira o vértice inicial: ")
            busca_profundidade(grafo, inicio)

        case 14:
            encontra_ciclos_dfs(grafo, direcional)

        case 15:
            print("Vértices disponíveis:", grafo["vertices"])
            inicio = input("Vértice inicial: ")
            destino = input("Vértice de destino: ")
            dijkstra(grafo, inicio, destino, direcional)

        case _:
            print("Opção inválida.")
