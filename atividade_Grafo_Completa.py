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
                  verticeSaida: str, direcional: bool):
    if verticeEntrada not in grafo["vertices"]:
        inserirVertice(grafo, verticeEntrada)

    if verticeSaida not in grafo["vertices"]:
        inserirVertice(grafo, verticeSaida)

    aresta = [verticeEntrada, verticeSaida]
    aresta_inversa = [verticeSaida, verticeEntrada]

    if aresta in grafo["arestas"] or (not direcional and aresta_inversa in grafo["arestas"]):
        print("Aresta já existe.")
        return

    grafo["arestas"].append(aresta)
    print("Aresta adicionada com sucesso!")


def apagarAresta(grafo: dict, verticeSaida: str,
                 verticeEntrada: str, direcional: bool):
    if verticeSaida not in grafo["vertices"] or verticeEntrada not in grafo["vertices"]:
        print("Um ou ambos os vértices não existem.")
        return

    aresta = [verticeSaida, verticeEntrada]
    aresta_inversa = [verticeEntrada, verticeSaida]

    removido = False
    if aresta in grafo["arestas"]:
        grafo["arestas"].remove(aresta)
        removido = True
    elif not direcional and aresta_inversa in grafo["arestas"]:
        grafo["arestas"].remove(aresta_inversa)
        removido = True

    if removido:
        print("Aresta removida com sucesso.")
    else:
        print("Aresta não existe.")


def obterVizinhos(grafo: dict, vertice: str, direcional: bool):
    if vertice not in grafo["vertices"]:
        return None

    vizinhos = []
    for origem, destino in grafo["arestas"]:
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

    for origem_aresta, destino_aresta in grafo["arestas"]:
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

    for origem, destino in grafo["arestas"]:
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
    print("Arestas:", grafo["arestas"])


grafo = {"vertices": [], "arestas": []}

direcional = int(input(
    "O grafo é direcional?\n1. Sim\n2. Não\n"
)) == 1



def menor_caminho(grafo: dict, inicio: str, destino: str):

    # Verifica se os vértices existem
    if inicio not in grafo["vertices"]:
        print("Vértice inicial não existe.")
        return

    if destino not in grafo["vertices"]:
        print("Vértice de destino não existe.")
        return

    # Estruturas utilizadas pelo BFS
    fila = [inicio]
    visitados = [inicio]

    # Guarda o antecessor de cada vértice
    caminhos = {inicio: None}

    while fila:

        vertice = fila.pop(0)

        # Verifica se encontramos o destino
        if vertice == destino:

            caminho = []
            atual = destino

            # Reconstrói o caminho
            while atual is not None:
                caminho.append(atual)
                atual = caminhos[atual]

            caminho.reverse()

            print("Menor caminho:", " -> ".join(caminho))
            print("Quantidade de arestas:", len(caminho) - 1)

            return caminho

        # Obtém os vizinhos do vértice atual
        for vizinho in obterVizinhos(grafo, vertice, direcional):

            if vizinho not in visitados:

                visitados.append(vizinho)
                fila.append(vizinho)

                caminhos[vizinho] = vertice

    print("Não existe caminho entre esses vértices.")
    return None


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
            inserirAresta(
                grafo, origem, destino, direcional
            )

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
            print("Vértices disponíveis:", list(grafo.keys()))
            inicio = input("Insira o vertice inicial: ")
            destino = input("insira o vertice de destino: ")
            menor_caminho(grafo, inicio, destino)

        case _:
            print("Opção inválida.")