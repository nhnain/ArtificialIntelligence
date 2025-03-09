# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

class Superstate:
    def __init__(self,state,prev,action,priority = 0) -> None:
        self.state = state
        self.prev = prev
        self.move_from_prev = action
        self.priority = priority

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    #print("Start:", problem.getStartState())
    #print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    #print("Start's successors:", problem.getSuccessors(problem.getStartState()))


    my_stack = util.Stack()
    init_state = problem.getStartState()
    init_superstate = Superstate(init_state,None,None)
    #return []
    visited_list = []
    my_stack.push(init_superstate)
    while (my_stack.isEmpty() == False):
        current_superstate = my_stack.pop()
        if problem.isGoalState(current_superstate.state):
            visited_list += [current_superstate]
            re_solution = []
            runner_superstate = current_superstate
            while runner_superstate.state != init_superstate.state :
                re_solution = [runner_superstate.move_from_prev]+re_solution
                runner_superstate = runner_superstate.prev
            return re_solution
        else :
            if current_superstate not in visited_list:
                visited_list+=[current_superstate]
                successors = problem.getSuccessors(current_superstate.state)
                for successor in list(successors):
                    successors_superstate = Superstate(successor[0],current_superstate,successor[1],successor[2])
                    for i,each in enumerate(visited_list):
                        if successors_superstate.state == visited_list[i].state:
                            break
                        if i == len(visited_list)-1:
                            my_stack.push(successors_superstate)
    return visited_list
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    my_queue = util.Queue()
    init_state = problem.getStartState()
    init_superstate = Superstate(init_state,None,None)
    visited_list = [init_superstate]
    my_queue.push(init_superstate)
    while (my_queue.isEmpty() == False):
        current_superstate = my_queue.pop()
        if problem.isGoalState(current_superstate.state):
            re_solution = []
            runner_superstate = current_superstate
            while runner_superstate.state != init_superstate.state :
                re_solution = [runner_superstate.move_from_prev]+re_solution
                runner_superstate = runner_superstate.prev
            return re_solution
        else :                
            successors = problem.getSuccessors(current_superstate.state)
            for successor in list(successors):
                successors_superstate = Superstate(successor[0],current_superstate,successor[1],successor[2])
                for i,each in enumerate(visited_list):
                    if successors_superstate.state == visited_list[i].state:
                        break
                    if i == len(visited_list)-1:
                        visited_list += [successors_superstate]
                        my_queue.push(successors_superstate)
                    
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    visited_list = []
    my_prioqueue = util.PriorityQueue()
    my_prioqueue.push(Superstate(problem.getStartState(), None, None), 0)
    while (my_prioqueue.isEmpty() == False):
        current_superstate = my_prioqueue.pop()
        if problem.isGoalState(current_superstate.state) is True:
            re_solution = []
            while current_superstate.move_from_prev is not None:
                re_solution = [current_superstate.move_from_prev] + re_solution
                current_superstate = current_superstate.prev
            return re_solution
        if current_superstate.state not in visited_list:
            visited_list += [current_superstate.state]
            for successor in problem.getSuccessors(current_superstate.state):
                my_prioqueue.push(Superstate(successor[0], current_superstate, successor[1], successor[2]+current_superstate.priority),successor[2]+current_superstate.priority)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited_list = []
    my_prioqueue = util.PriorityQueue()
    init_state = problem.getStartState()
    my_prioqueue.push(Superstate(init_state, None, None,heuristic(init_state, problem)),heuristic(init_state, problem))
    while (my_prioqueue.isEmpty() == False ):
        current_superstate = my_prioqueue.pop()
        if problem.isGoalState(current_superstate.state) is True:
            re_solution = []
            while current_superstate.move_from_prev is not None:
                re_solution =[current_superstate.move_from_prev] + re_solution
                current_superstate = current_superstate.prev
            return re_solution
        if current_superstate.state not in visited_list:
            visited_list += [current_superstate.state]
            for successor in problem.getSuccessors(current_superstate.state):
                my_prioqueue.push(Superstate(successor[0], current_superstate, successor[1], successor[2]+current_superstate.priority),successor[2]+current_superstate.priority+heuristic(successor[0], problem))
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
