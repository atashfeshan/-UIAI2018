import numpy as np


def make_board(array):
     t = np.array(array)
     t = np.round(t)
     t[...,0] += 7
     t[...,1] += 4
     t = np.array(t, dtype=int)
     board = np.zeros((15, 9),dtype=np.bool)
     board[t[..., 0],t[..., 1]] = 1
     return board.flatten()
