
INFINITEPLUS = 10000
INFINITENEGATIVE = -10000
class Artificial_Computation:
    def __init__(self, gameState):
        "we receive a game state, so we can generate our minimax function according to the actual board state."
        self.gameState = gameState

    def minimax(self, node, depth, maximizingPlayer):
        if(depth == 0 or node.isTerminalNode()):
            return self.getHeuristicValue()

        if(maximizingPlayer):
            bestValue = INFINITENEGATIVE
            for child in node:
                v = self.minimax(child, depth - 1, False)
                bestValue = max(v, bestValue)
            return bestValue
        else:                 # minimizing player
            bestValue = INFINITEPLUS
            for child in node:
                v = self.minimax(child, depth - 1, True)
                bestValue = min(bestValue, v)
            return bestValue

    def getHeuristicValue(self):
        return self.gameState.getScore()

    def setHeuristicValue(self):
        pass 
    
    def getTest(self):
        pass
