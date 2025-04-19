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
import networkx as nx
import matplotlib.pyplot as plt

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

def visualize_paths(graph, all_paths, optimal_path):
    pos = nx.spring_layout(graph)
    
    # Draw the full graph
    nx.draw(graph, pos, with_labels=True, node_color='lightgray', edge_color='gray', node_size=500, font_size=10)
    
    # Draw all paths in blue
    for path in all_paths:
        edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='blue', alpha=0.3, width=1)
    
    # Draw the optimal path in red
    optimal_edges = [(optimal_path[i], optimal_path[i+1]) for i in range(len(optimal_path)-1)]
    nx.draw_networkx_edges(graph, pos, edgelist=optimal_edges, edge_color='red', width=2.5)
    
    plt.title("All Paths (Blue) vs Optimal Path (Red)")
    plt.show()

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.
    Extract all paths explored and store them.
    """
    print("Start:", problem.getStartState())
    
    my_stack = util.Stack()
    init_state = problem.getStartState()
    init_superstate = Superstate(init_state, None, None)
    visited_list = []
    all_paths = []  # Store all paths
    my_stack.push((init_superstate, []))  # Stack stores (Superstate, Path taken)
    
    nodes_expanded = 0
    nodes = []
    edges = []
    costs = {}
    re_solution = []

    while not my_stack.isEmpty():
        current_superstate, current_path = my_stack.pop()
        nodes_expanded += 1
        nodes.append(current_superstate.state)
        costs[current_superstate.state] = current_superstate.priority
        
        new_path = current_path + [current_superstate.state]  # Update path

        if problem.isGoalState(current_superstate.state):
            all_paths.append(new_path)  # Store the entire path when goal is reached
            visited_list.append(current_superstate)
            re_solution = new_path  # Use the path of states as the solution
            runner_superstate = current_superstate
            while runner_superstate.state != init_superstate.state:
                edges.append((runner_superstate.prev.state, runner_superstate.state))
                runner_superstate = runner_superstate.prev
            print(f"Nodes expanded: {nodes_expanded}")
            print(f"Nodes: {nodes}")
            print(f"Edges: {edges}")
            print(f"Costs: {costs}")
            print(f"Optimal path: {re_solution}")
            visualize_paths(nx.DiGraph(edges), all_paths, re_solution)  # Use visualize_paths to visualize the search tree
            return re_solution
        else:
            if current_superstate not in visited_list:
                visited_list.append(current_superstate)
                successors = problem.getSuccessors(current_superstate.state)
                for successor in successors:
                    successor_superstate = Superstate(successor[0], current_superstate, successor[1], successor[2])
                    edges.append((current_superstate.state, successor[0]))
                    # Ensure successor state is not already visited
                    if all(s.state != successor_superstate.state for s in visited_list):
                        my_stack.push((successor_superstate, new_path))  # Pass updated path
    
    print(f"Nodes expanded: {nodes_expanded}")
    print(f"Nodes: {nodes}")
    print(f"Edges: {edges}")
    print(f"Costs: {costs}")
    print(f"All Paths: {all_paths}")
    visualize_paths(nx.DiGraph(edges), all_paths, re_solution)  # Use visualize_paths to visualize the search tree if no solution is found
    return visited_list, nodes_expanded, nodes, edges, costs

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    my_queue = util.Queue()
    init_state = problem.getStartState()
    init_superstate = Superstate(init_state, None, None)
    visited_list = [init_superstate]
    my_queue.push(init_superstate)
    nodes_expanded = 0
    nodes = []
    edges = []
    costs = {}
    all_paths = []  # Store all paths
    re_solution = []

    while not my_queue.isEmpty():
        current_superstate = my_queue.pop()
        nodes_expanded += 1
        nodes.append(current_superstate.state)
        costs[current_superstate.state] = current_superstate.priority
        if problem.isGoalState(current_superstate.state):
            re_solution = []
            runner_superstate = current_superstate
            while runner_superstate.state != init_superstate.state:
                re_solution = [runner_superstate.move_from_prev] + re_solution
                edges.append((runner_superstate.prev.state, runner_superstate.state))
                runner_superstate = runner_superstate.prev
            all_paths.append(re_solution)  # Store the entire path when goal is reached
            print(f"Nodes expanded: {nodes_expanded}")
            print(f"Nodes: {nodes}")
            print(f"Edges: {edges}")
            print(f"Costs: {costs}")
            print(f"Optimal path: {re_solution}")
            visualize_paths(nx.DiGraph(edges), all_paths, re_solution)  # Use visualize_paths to visualize the search tree
            return re_solution
        else:
            successors = problem.getSuccessors(current_superstate.state)
            for successor in successors:
                successors_superstate = Superstate(successor[0], current_superstate, successor[1], successor[2])
                edges.append((current_superstate.state, successor[0]))
                for i, each in enumerate(visited_list):
                    if successors_superstate.state == visited_list[i].state:
                        break
                    if i == len(visited_list) - 1:
                        visited_list.append(successors_superstate)
                        my_queue.push(successors_superstate)
    print(f"Nodes expanded: {nodes_expanded}")
    print(f"Nodes: {nodes}")
    print(f"Edges: {edges}")
    print(f"Costs: {costs}")
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    visited_list = []
    my_prioqueue = util.PriorityQueue()
    my_prioqueue.push(Superstate(problem.getStartState(), None, None), 0)
    nodes_expanded = 0
    nodes = []
    edges = []
    costs = {}
    all_paths = []  # Store all paths
    re_solution = []

    while not my_prioqueue.isEmpty():
        current_superstate, current_path = my_prioqueue.pop()
        nodes_expanded += 1
        nodes.append(current_superstate.state)
        costs[current_superstate.state] = current_superstate.priority
        new_path = current_path + [current_superstate.state]  # Update path
        if problem.isGoalState(current_superstate.state):
            re_solution = new_path
            while current_superstate.move_from_prev is not None:
                re_solution = [current_superstate.state] + re_solution
                edges.append((current_superstate.prev.state, current_superstate.state))
                current_superstate = current_superstate.prev
            all_paths.append(re_solution)  # Store the entire path when goal is reached
            print(f"Nodes expanded: {nodes_expanded}")
            print(f"Nodes: {nodes}")
            print(f"Edges: {edges}")
            print(f"Costs: {costs}")
            print(f"Optimal path: {re_solution}")
            visualize_paths(nx.DiGraph(edges), all_paths, re_solution)  # Use visualize_paths to visualize the search tree
            return re_solution
        if current_superstate.state not in visited_list:
            visited_list.append(current_superstate.state)
            for successor in problem.getSuccessors(current_superstate.state):
                successors_superstate = Superstate(successor[0], current_superstate, successor[1], successor[2] + current_superstate.priority)
                edges.append((current_superstate.state, successor[0]))
                my_prioqueue.push(successors_superstate, successor[2] + current_superstate.priority)
    print(f"Nodes expanded: {nodes_expanded}")
    print(f"Nodes: {nodes}")
    print(f"Edges: {edges}")
    print(f"Costs: {costs}")
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
