import numpy as np
import chess
import time
from joblib import dump, load
import dask


# Flatten any board into a single string
def flatten_board(x):
    return(str(x).replace(' ','').replace('\n',''))

# Encode any board to get its board state
def get_encoded_board(x):
    '''Must pass a flattened board'''
    num_squares = range(64)
    
    #Black Player Feature Vectors
    b_rook  = [1 if x[i]=='r' else 0 for i in num_squares]
    b_night = [1 if x[i]=='n' else 0 for i in num_squares]
    b_bish  = [1 if x[i]=='b' else 0 for i in num_squares]
    b_queen = [1 if x[i]=='q' else 0 for i in num_squares]
    b_king  = [1 if x[i]=='k' else 0 for i in num_squares]
    b_pawn  = [1 if x[i]=='p' else 0 for i in num_squares]
    b_value = [(sum(b_rook)*5 + sum(b_night)*3 + sum(b_bish)*3
           + sum(b_queen)*9 + sum(b_pawn)*1
          )]
    
    #White Player Feature Vectors
    w_rook  = [1 if x[i]=='R' else 0 for i in num_squares]
    w_night = [1 if x[i]=='N' else 0 for i in num_squares]
    w_bish  = [1 if x[i]=='B' else 0 for i in num_squares]
    w_queen = [1 if x[i]=='Q' else 0 for i in num_squares]
    w_king  = [1 if x[i]=='K' else 0 for i in num_squares]
    w_pawn  = [1 if x[i]=='P' else 0 for i in num_squares]
    w_value = [(sum(w_rook)*5 + sum(w_night)*3 + sum(w_bish)*3
           + sum(w_queen)*9 + sum(w_pawn)*1
          )]

    feature_list = (b_rook+b_night+b_bish+b_queen
                +b_king+b_pawn+w_rook+w_night+w_bish
                +w_queen+w_king+w_pawn+b_value+w_value)
    
    return(feature_list)

# Recursion
class Tree:
    """Base Class used to setup chess move tree"""
    def __init__(self, board):
        self.board = board
        self.children = []

    def addNode(self, obj):
        self.children.append(obj)


class Node:
    """Class used to add depth to Tree class"""
    def __init__(self, parent, board, move):
        self.parent = parent
        self.board = board
        self.previous_move = move
        self.children = []

    def addNode(self, obj):
        self.children.append(obj)

def build_tree(parent, level, max_level=1):
    """Builds a chess move tree out to max_level"""
    if level == max_level:
        return

    # Build up children nodes
    for move in parent.board.legal_moves:
        board_copy = parent.board.copy()
        board_copy.push(move)
        parent.addNode(Node(parent, board_copy, move))

    # Recursively add Nodes for each child
    for node in parent.children:
            build_tree(node, level+1, max_level=max_level)

def get_leaf(child, leaf_nodes, level):
    """After a Tree is built, this is used to get a reference 
    to the leaf nodes out to level"""
    if not child.children:
        leaf_nodes.append((child, level))
        return
    else:
        for child in child.children:
            get_leaf(child, leaf_nodes, level+1)  

def recommend_move(board=None, max_level=3):
    if not board:
        board = chess.Board() # Instantiate board - gone if used as method
        print("Creating a board")
    
    clf = load('filename.joblib') # load model
    
    
    root = Tree(board) # Create root
    build_tree(root, 0, max_level=max_level) # Build the tree

    child_dict = {} # Instantiate dictionary to hold references to leaf nodes
    for child in root.children:
        leaf_nodes = []
        get_leaf(child, leaf_nodes, 0)
        child_dict[str(child.previous_move)] = leaf_nodes

    predictions = {each:[] for each in child_dict.keys()}
    # Determine probabilities for each leaf
    for k,v in child_dict.items(): # k is 1 of the original moves, v is a list of (node, level)
        #print('got here')
        #print(k)
        my_move = False
        for game_state in v: # game_state means who's turn is it :P
            #print(game_state[1])
            if game_state[1] % 2 == 0:
                #print('My Move')
                my_move = True
            else:
                #print('Opponent Move')
                pass
            #print(game_state[0].board)
            # board should be k.board
            board_flat = flatten_board(game_state[0].board) # changed from board to k.board
            encode = np.array(get_encoded_board(board_flat)).reshape(1, -1)
            #probability = clf.predict(encode)[0]
            probability = clf.predict_proba(encode)[0]
            #print('PROBABILITY IS:')
            #print(probability)
            #print(probability)
            
            if my_move:
                predictions[k].append(probability[2]) # since its prob of white losing [0], make it black losign [2]
            elif not my_move:
                predictions[k].append(probability[0])
            
    move_list = list(predictions.keys())
    loss_sum = []
    for k,v in predictions.items():
        #loss_sum.append(np.average(np.array(v)))        
        loss_sum.append(np.min(np.array(v)))        
    
    loss_sum = np.array(loss_sum)
    #print('loss_sum', loss_sum)
    ###print(loss_sum)
    loss_sum_min = np.where(loss_sum == loss_sum.min())[0]
    #print('loss_sum_min', loss_sum_min)
    recommended_move_idx = np.random.choice(loss_sum_min)
    recommended_move = move_list[recommended_move_idx]
    return {'move': recommended_move, 'stats': {'moves_with_least_loss': len(loss_sum_min), 'num_predicted_moves': len(loss_sum)}}


