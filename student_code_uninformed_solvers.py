
from solver import *
import queue
class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        # Gamestate(self, state, depth, movableToReachThisState)
        if self.currentState.state == self.victoryCondition:
            self.visited[self.currentState] = True
            return True
        if self.currentState not in self.visited:
            self.visited[self.currentState] = True
            return self.currentState.state == self.victoryCondition
        # expand the whole tree by depth
        # expand children of current node

        if not self.currentState.children and self.gm.getMovables():
            # get all movables
            for movables in self.gm.getMovables():
                # make move to one of children
                self.gm.makeMove(movables)
                # get GameState of children
                new_state_tuple = self.gm.getGameState()
                new_GameState = GameState(new_state_tuple, self.currentState.depth+1, movables)
                if new_GameState not in self.visited:
                    new_GameState.parent = self.currentState
                    self.currentState.children.append(new_GameState)
                self.gm.reverseMove(movables)
        move = False
        # traverse
        # nextChildToVisit (int): index of the next GameState node in 'children' list of expand
        if self.currentState.nextChildToVisit < len(self.currentState.children):
        # state (object): a hashable object that denotes a specific game state, such as a Tuple of Tuples
            for x in range(self.currentState.nextChildToVisit, len(self.currentState.children)):
                if self.currentState.children[x] not in self.visited:
                    self.currentState.nextChildToVisit = x
                    self.visited[self.currentState.children[x]] = True
                    self.gm.makeMove(self.currentState.children[x].requiredMovable)
                    self.currentState = self.currentState.children[x]
                    print(self.currentState.state)
                    move = True
                    break
                if move and self.currentState.state == self.victoryCondition:
                    return True
                elif move and self.currentState.state != self.victoryCondition:
                    return self.solveOneStep()

                # reverse move to parent
        else:
            if self.currentState.requiredMovable:
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                return self.solveOneStep()
            else:
                return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        #self.queue = queue.Queue()
        #self.moves_to_child = dict()
    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.


            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            self.visited[self.currentState] = True
            return True
        depth = self.currentState.depth
        while True:
            next_node = self.solveOneStep_helper(depth)
            if next_node:
                if self.currentState.state == self.victoryCondition:
                    return True
                else:
                    depth += 1
            else:
                return False
    def solveOneStep_helper(self,depth):
        # expand in one depth
        if self.currentState.depth == depth:
            if depth == 0 or self.currentState not in self.visited and not self.currentState.children:
                for movables in self.gm.getMovables():
                    self.gm.makeMove(movables)
                    new_GameState = GameState(self.gm.getGameState(), self.currentState.depth+1, movables)
                    if new_GameState not in self.visited:
                        new_GameState.parent = self.currentState
                        self.currentState.children.append(new_GameState)
                    self.gm.reverseMove(movables)
            if self.currentState.state == self.victoryCondition:
                self.visited[self.currentState] = True
                return True
            elif self.currentState not in self.visited:
                self.visited[self.currentState] = True
                return self.currentState.state == self.victoryCondition
            else:
                if self.currentState.depth == 0:
                    return True
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                return self.solveOneStep_helper(depth)
        # search children
        elif self.currentState.depth < depth:

            if self.currentState.nextChildToVisit < len(self.currentState.children):
                new_GameState = self.currentState.children[self.currentState.nextChildToVisit]
                self.currentState.nextChildToVisit += 1

                self.gm.makeMove(new_GameState.requiredMovable)
                self.currentState = new_GameState
                return self.solveOneStep_helper(depth)
            elif self.currentState.nextChildToVisit == len(self.currentState.children):
                # if all children searched, initial searching list
                self.currentState.nextChildToVisit = 0
                if self.currentState.depth == 0:
                    return True
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent

                return self.solveOneStep_helper(depth)
        # return to parent
        elif self.currentState.depth > depth:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return self.solveOneStep_helper(depth)

