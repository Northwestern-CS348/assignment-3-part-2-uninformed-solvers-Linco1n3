from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        pegs = []
        for peg_id in range(1, 4):

            listOfBindings = self.kb.kb_ask(parse_input('fact: (on ?disk peg' + str(peg_id) + ')'))
            if listOfBindings:
                id_list = []
                for bindings in listOfBindings:
                    #bindings_dict to match key and value
                    disk_id = int(bindings.bindings_dict['?disk'].replace('disk', ''))
                    id_list.append(disk_id)
                pegs.append(id_list)
            else:
                pegs.append([])

        pegs_tuples = []
        for disk_list in pegs:
            disk_list.sort()
            peg_tup = tuple(disk_list)
            # [(1,2,5), (), (3,4)]
            pegs_tuples.append(peg_tup)
        pegs_tuples = tuple(pegs_tuples)
        return pegs_tuples


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """

        ### Student code goes here
        movableQuery = self.produceMovableQuery()
        checkismatch = match(movable_statement, movableQuery.statement)

        # fact: (movable ?disk ?init ?target)
        if checkismatch:
            curr_disk = checkismatch['?disk']
            curr_init = checkismatch['?init']
            curr_target = checkismatch['?target']

            # retract facts supported by facts of curr_disk
            self.kb.kb_retract(parse_input('fact: (ontop ' + curr_disk + ' ' + curr_init + ')'))
            self.kb.kb_retract(parse_input('fact: (on ' + curr_disk + ' ' + curr_init + ')'))

            # check whether curr_disk is above another disk
            checkisabove = self.kb.kb_ask(parse_input('fact: (above ' + curr_disk + ' ?disk)'))
            if checkisabove:
                new_top = checkisabove[0].bindings_dict['?disk']
                self.kb.kb_retract(parse_input('fact: (above ' + curr_disk + ' ' + new_top + ')'))
                self.kb.kb_assert(parse_input('fact: (ontop ' + new_top + ' ' + curr_init + ')'))
            else:
                self.kb.kb_assert(parse_input('fact: (empty ' + curr_init + ')'))

            # check whether curr_target is empty
            checkisempty = self.kb.kb_ask(parse_input('fact: (empty ' + curr_target + ')'))
            if checkisempty:
                self.kb.kb_retract(parse_input('fact: (empty ' + curr_target + ')'))
                self.kb.kb_assert(parse_input('fact: (ontop ' + curr_disk + ' ' + curr_target + ')'))
                self.kb.kb_assert(parse_input('fact: (on ' + curr_disk + ' ' + curr_target + ')'))
            else:
                old_top = self.kb.kb_ask(parse_input('fact: (ontop ?disk ' + curr_target + ')'))[0].bindings_dict['?disk']
                self.kb.kb_retract(parse_input('fact: (ontop ' + old_top + ' ' + curr_target + ')'))
                self.kb.kb_assert(parse_input('fact: (on ' + curr_disk + ' ' + curr_target + ')'))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here

        listOfBindings = self.kb.kb_ask(parse_input('fact: (pos ?tile ?x ?y)'))
        tuples = ([-1 for _ in range(3)], [-1 for _ in range(3)], [-1 for _ in range(3)])
        for binding in listOfBindings:
            y_index = int(binding['?x'][3]) - 1

            if str(binding['?tile']) == 'empty':
                tuples[int(binding['?y'][3]) - 1][y_index] = -1
            else:
                tuples[int(binding['?y'][3])-1][y_index] = int(binding['?tile'][4])

        return tuple(tuple(k) for k in tuples)
    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        movableQuery = self.produceMovableQuery()
        checkismatch = match(movable_statement, movableQuery.statement)

        #fact: (movable ?piece ?initX ?initY ?targetX ?targetY)
        if checkismatch:
            tile = str(movable_statement.terms[0])
            initX = str(movable_statement.terms[1])
            initY = str(movable_statement.terms[2])
            targetX = str(movable_statement.terms[3])
            targetY = str(movable_statement.terms[4])

            self.kb.kb_retract(parse_input('fact: (pos empty ' + targetX + ' ' + targetY + ')'))
            self.kb.kb_retract(parse_input('fact: (pos ' + tile + ' ' + initX + ' ' + initY + ')'))

            self.kb.kb_assert(parse_input('fact: (pos empty ' + initX + ' ' + initY + ')'))
            self.kb.kb_assert(parse_input('fact: (pos ' + tile + ' ' + targetX + ' ' + targetY + ')'))
    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
