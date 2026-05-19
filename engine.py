def generate_pairings(players):
    """
    Motor Suíço Simplificado (Algoritmo de Emparceiramento v1)
    
    players: lista de tuplas (id, name, rating, points)
    Retorna uma lista de pares: [(player1, player2), ...]
    """
    if len(players) < 2:
        return []

    # Aqui vamos usar grafos no futuro (networkx) para garantir que 
    # as pessoas não joguem duas vezes contra as mesmas.
    # Por agora, nesta v1, vamos parear os jogadores adjacentes 
    # (que já chegam ordenados por pontos do Banco de Dados).
    
    pairings = []
    unpaired = players.copy()
    
    while len(unpaired) >= 2:
        p1 = unpaired.pop(0)
        p2 = unpaired.pop(0)
        pairings.append((p1, p2))
        
    # Lidar com BYE (jogador ímpar que fica sobrando na rodada)
    if unpaired:
        bye = unpaired.pop(0)
        pairings.append((bye, None)) # None significa que ele não tem adversário (BYE)
        
    return pairings
