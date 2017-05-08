import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    #if player is None:
    #    player = game.active_player

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    player_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

    #xprint('custom_score', player_moves - 2 * opponent_moves, player)

    return float(player_moves - 2 * opponent_moves)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if player is None:
        player = self.active_player

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    player_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

    #xprint('custom_score', len(player_moves) - len(opponent_moves))

    return float(player_moves - opponent_moves)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if player is None:
        player = self.active_player

    return float(len(game.get_legal_moves(player)))

def xprint(*args):
    #print(args)
    #xprint( "XXX"+" ".join(map(str,args))+"XXX")
    return

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.testTrees = []

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            #xprint('no legal_moves left')
            return (-1, -1)

        scores = dict()
        for move in legal_moves:
            scores[move] = self.minvalue(game.forecast_move(move), depth-1)
        #xprint('scores', scores, max(scores, key=scores.get))
        return max(scores, key=scores.get)

    def maxvalue(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return game.utility(self)
            #return game.utility(game.active_player)
        if depth <= 0:
            return self.score(game, self)
        v = float("-inf")
        for move in legal_moves:
            board = game.forecast_move(move)
            v = max(v, self.minvalue(board, depth-1))

        return v

    def minvalue(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return game.utility(self)
            #return game.utility(game.active_player)
        if depth <= 0:
            return self.score(game, self)
        v = float("inf")
        for move in legal_moves:
            board = game.forecast_move(move)
            v = min(v, self.maxvalue(board, depth-1))

        return v

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left, tree=None):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # For testing purposes
        xprint('tree', tree)
        if tree:
            return self.alphabeta(None, 6, float("-inf"), float("inf"), tree)

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        depth = 1

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            while self.time_left() > self.TIMER_THRESHOLD:
                best_move = self.alphabeta(game, depth)
                depth += 1

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), tree=None):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        xprint('--------------------------------')
        xprint('tree', tree)
        #xprint('ALPHABETA game.active_player', game.active_player)
        temptree = None
        new_board = None
        if tree:
            legal_moves = range(0, len(tree))
        else:
            legal_moves = game.get_legal_moves()
        #xprint('ALPHABETA legal_moves', legal_moves)
        if not legal_moves:
            xprint('no legal_moves left')
            return (-1, -1)

        best_move = legal_moves[0]
        for move in legal_moves:
            if tree:
                temptree = tree[move]
            else:
                new_board = game.forecast_move(move)
            v = self.minvalue(new_board, depth-1, alpha, beta, temptree)
            #v, testTree = self.minvalue(new_board, depth-1, alpha, beta, temptree)
            if v >= beta:
                break
            if v > alpha:
                alpha = v
                best_move = move

        if tree:
            self.testTrees.append(testTree)
            return alpha
        return best_move

    def maxvalue(self, game, depth, alpha, beta, tree):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        xprint('--', 'depth', depth, 'tree', tree, 'MAXVALUE', alpha, beta)
        if tree or tree == 0:
            if not isinstance(tree, list):
                return tree
        else:
            if depth <= 0:
                return self.score(game, self)

        temptree = None
        new_board = None
        if tree:
            legal_moves = range(0, len(tree))
        else:
            legal_moves = game.get_legal_moves(self)
        #xprint('ALPHABETA MAXVALUE game.active_player', game.active_player, 'depth, alpha, beta', depth, alpha, beta, 'legal_moves', legal_moves)
        if not legal_moves:
            xprint('no legal_moves')
            return game.utility(self)
            #return game.utility(game.active_player)

        v = float("-inf")
        for move in legal_moves:
            if tree:
                temptree = tree[move]
            else:
                new_board = game.forecast_move(move)
            v = max(v, self.minvalue(new_board, depth-1, alpha, beta, temptree))
            #res, testTree = self.minvalue(new_board, depth-1, alpha, beta, temptree)
            #v = max(v, res)

            xprint('**', 'depth', depth, 'tree', tree, 'MAXVALUE result to max(minvalue)', v, 'for temptree ', temptree, 'v >= beta', v >= beta, 'alpha', alpha, 'beta', beta)
            if v >= beta:
                xprint('_______PRUNING tree', tree, ' after ', temptree)
                return v
            alpha = max(alpha, v)
            xprint('max(alpha, v)', alpha, beta)

        #return v, testTree
        return v

    def minvalue(self, game, depth, alpha, beta, tree):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        xprint('--', 'depth', depth, 'tree', tree, 'MINVALUE', alpha, beta)
        if tree or tree == 0:
            if not isinstance(tree, list):
                return tree
        else:
            if depth <= 0:
                return self.score(game, self)
        temptree = None
        new_board = None
        if tree:
            legal_moves = range(0, len(tree))
        else:
            legal_moves = game.get_legal_moves()
        #xprint('ALPHABETA MINVALUE game.active_player', game.active_player, 'depth, alpha, beta', depth, alpha, beta, 'legal_moves', legal_moves)
        if not legal_moves:
            xprint('no legal_moves')
            return game.utility(self)
            #return game.utility(game.active_player)

        v = float("inf")
        for move in legal_moves:
            if tree:
                temptree = tree[move]
            else:
                new_board = game.forecast_move(move)
            v = min(v, self.maxvalue(new_board, depth-1, alpha, beta, temptree))

            xprint('**', 'depth', depth, 'tree', tree, 'MINVALUE result to min(maxvalue)', v, 'for temptree ', temptree, 'v <= alpha', v <= alpha, 'alpha', alpha, 'beta', beta)
            if v <= alpha:
                xprint('_______PRUNING tree', tree, ' after ', temptree)
                return v
            beta = min(beta, v)
            xprint('min(beta, v)', alpha, beta)

        return v


# Testing alpha beta algo
# player = AlphaBetaPlayer()
# player.set_tree = tree
# root = player.get_move(None, lambda : 20, tree)
# print('TreeTest result', root)
tree = [
        [
            [
                [
                    [-1, 13],
                    [1, 6]
                ],
                [
                    [-16, 13],
                    [-13, -10]
                ]
            ],
            [
                [
                    [-4, 9],
                    [-20, -13]
                ],
                [
                    [-16, -13],
                    [-4, 11]
                ]
            ],
        ],
        [
            [
                [
                    [-14, -7],
                    [0, 19]
                ],
                [
                    [-14, -7],
                    [12, -15]
                ]
            ],
            [
                [
                    [2, -16],
                    [-13, 4]
                ],
                [
                    [2, -1],
                    [-5, -9]
                ]
            ]
        ]
    ]