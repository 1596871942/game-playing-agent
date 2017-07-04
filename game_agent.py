"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def custom_score(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    #For this one we'll keep it basic, and value moves that try to improve our choices while limiting the enemy's,
    #but favoring ours.
    return float(abs(len(game.get_legal_moves(player))*2 - len(game.get_legal_moves(game.get_opponent(player)))))
    raise NotImplementedError


def custom_score_2(game, player):
    #This heuristic values moves near the center of the board against those toward the edges.
    #While this is an imperfect guideline, odds ought to be that moves toward the center afford
    #more opportunities than those against  the walls. We'll employ a little taxicab geometry to achieve this.
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    ourMoves = len(game.get_legal_moves(player))
    enemyMoves = len(game.get_legal_moves(game.get_opponent(player)))
    centerY, centerX = int(game.height / 2), int(game.width / 2)
    ourY, ourX = game.get_player_location(player)
    theirY, theirX = game.get_player_location(game.get_opponent(player))
    ourDistance = abs(ourY - centerY) + abs(ourX - centerX)
    theirDistance = abs(theirY - centerY) + abs(theirX - centerX)
    #Now let's put this on a scale from -1 to 1 (good position shouldn't be better than being ahead a move) and return it
    return float(theirDistance - ourDistance) / 10

    raise NotImplementedError


def custom_score_3(game, player):
    #This heuristic I call "burn the ships", in the sense of motivating an army to fight because there is no way home.
    #We're giving additional weight to the number of moves the enemy has, and forechecking like the Pittsburgh Penguins :)
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    return float(abs(len(game.get_legal_moves(player)) - 2*len(game.get_legal_moves(game.get_opponent(player)))));
    raise NotImplementedError


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



def minimax_score(game,player):
    #Put in helper function despite being basic to meet requirements that self.score() be used

    # check to see if the game is over:
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    return float(len(game.get_legal_moves(player)));

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """
    def __init__(self, search_depth=3, score_fn=minimax_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
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

    def minPattern(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        legalMoves = game.get_legal_moves();
        if not legalMoves:
            return game.utility(self)
        if depth <= 0:
            return self.score(game,self)
        score = float("inf")
        for move in legalMoves:
            nextPly = game.forecast_move(move)
            score = min(score, self.maxPattern(nextPly, depth-1))
        return score

    def maxPattern(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        legalMoves = game.get_legal_moves();
        if not legalMoves:
            return game.utility(self)
        if depth <= 0:
            return self.score(game,self)
        score = float("-inf")
        for move in legalMoves:
            nextPly = game.forecast_move(move)
            score = max(score, self.minPattern(nextPly, depth-1))
        return score

    def minimax(self, game, depth, isMax=True):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        legalMoves = game.get_legal_moves();
        if not legalMoves:
            return game.utility(self)
        # if depth == 1:
        #     return self.score(game,self)
        startScore = float("-inf")
        useMove = (-1,-1)
        score = None
        for move in legalMoves:
            nextPly = game.forecast_move(move)
            score = self.minPattern(nextPly, depth-1)
            if score > startScore:
                startScore = score
                score, useMove = score, move
        return useMove
        raise NotImplementedError


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """
    def score(game,player):
        if game.is_loser(player):
            return float("-inf")

        if game.is_winner(player):
            return float("inf")
        return float(len(game.get_legal_moves(player)));

    def get_move(self, game, time_left):
        # TODO: finish this function!
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        useMove = (-1, -1)
        depth = 1
        try:
            while True:
                useMove = self.alphabeta(game, depth, alpha=float("-inf"), beta=float("inf"))
                depth+=1
        except SearchTimeout:
            pass
        # Return the best move from the last completed search iteration
        return useMove
        raise NotImplementedError

    def minPattern(self, game, depth,alpha,beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        legalMoves = game.get_legal_moves();
        if depth <= 0 or not legalMoves:
            return self.score(game,self)
        score = float("inf")
        for move in legalMoves:
            nextPly = game.forecast_move(move)
            score = min(score, self.maxPattern(nextPly, depth-1,alpha,beta))
            if score <= alpha:
                return score
            beta = min(beta,score)
        return score

    def maxPattern(self, game, depth,alpha,beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        legalMoves = game.get_legal_moves();
        if depth <= 0 or not legalMoves:
            return self.score(game,self)
        score = float("-inf")
        for move in legalMoves:
            nextPly = game.forecast_move(move)
            score = max(score, self.minPattern(nextPly, depth-1,alpha,beta))
            if score >= beta:
                return score
            alpha = max(alpha,score)
        return score

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
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
        legalMoves = game.get_legal_moves();
        if not legalMoves:
            return (-1,-1)
        startScore = float("-inf")
        useMove = (-1,-1)
        score = None
        for move in legalMoves:
            nextPly = game.forecast_move(move)
            score = self.minPattern(nextPly, depth-1,alpha,beta)
            if score >= startScore:
                startScore = score
                useMove = move
            alpha = max(alpha,score)
        return useMove
        raise NotImplementedError
