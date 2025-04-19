from game import Agent
from game import Directions
import random

class DumbAgent(Agent):
    "An agent that goes East until it can't."
    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        print("Location: ", state.getPacmanPosition())
        print("Actions available: ", state.getLegalPacmanActions())
        if Directions.EAST in state.getLegalPacmanActions():
            print("Going East.")
            return Directions.EAST
        else:
            print("Stopping.")
            return Directions.STOP
class RandomAgent(Agent):
    "An agent that chooses a legal action randomly."
    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        legal = state.getLegalPacmanActions()
        if legal:
            action = random.choice(legal)
            print("Going", action)
            return action
        else:
            print("Stopping.")
            return Directions.STOP
class BetterRandomAgent(Agent):
    "An agent that chooses a legal action randomly."
    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        import random
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        if legal:
            action = random.choice(legal)
            print("Going", action)
            return action
        else:
            print("Stopping.")
            return Directions.STOP
class ReflexAgent(Agent):
    "An agent that chooses actions to eat food pellets if possible."
    def getAction(self, state):
        legals = state.getLegalPacmanActions()
        legals.pop()
        for legal in legals:
            successor = state.generatePacmanSuccessor(legal)
            if Directions.STOP in legals:
                legals.remove(Directions.STOP)
            if successor.getNumFood() < state.getNumFood():
                return legal
        return random.choice(legals)