
# encoding=UTF-8

import itertools
import datetime as dt
from hashlib import sha1
from Queue import PriorityQueue
import numpy as np
import copy 
from pygame.locals import *
import random
from sys import stdout


def find_zero_pos(board):
	n = len(board)
	for i in range(n):
		for j in range(n):
			if board[i][j] == 0:
				return (i,j)
	return -1,-1

def move_pos(spot,i):
	spotx, spoty = spot
	if i == 0:
		return spotx,spoty+1
	elif i == 1:
		return spotx, spoty-1
	elif i == 2:
		return spotx-1, spoty
	elif i == 3:
		return spotx+1, spoty

def position_legal(spot, board):
	n = len(board)
	spotx,spoty = spot 
	if spotx >= n or spotx <0 or spoty >=n or spoty < 0:
		return False 
	else:
		return True

def feasible_state(board):
	feasible_state_ = []
	spotx,spoty = find_zero_pos(board)
	for i in range(4):
		new_pos = move_pos((spotx,spoty),i)
		if position_legal(new_pos,board):
			basic_board = copy.deepcopy(board)
			temp = basic_board[new_pos[0]][new_pos[1]]
			basic_board[new_pos[0]][new_pos[1]] = basic_board[spotx][spoty]
			basic_board[spotx][spoty] = temp
			feasible_state_.append(basic_board)
	return feasible_state_


def board_is_goal(board):
	global goal
	if hash_board(board) == hash_board(goal):
		return True
	else:
		return False

def find_pos(board, num):
	n = len(board)
	for i in range(n):
		for j in range(n):
			if board[i][j] == num:
				return (i, j)

def manhattan(spot1,spot2):
	return abs(spot1[0] - spot2[0]) + abs(spot1[1] - spot2[1])

def manhattan_distance(board):
	n = len(board)
	count = 0
	for num in range(n*n):
		spotx, spoty = find_pos(board, num)
		goalx, goaly = find_pos(goal, num)
		count += manhattan((spotx, spoty), (goalx, goaly))
	return count

def misplaced(board):
	count = 0
	n = len(board)
	for i in range(n):
		for j in range(n):
			if board[i][j] != goal[i][j]:
				count += 1
	return count 


def a_star(board, heuristic):
	cur_state = [board, 0, []]
	q = PriorityQueue()
	q.put((0,cur_state))
	visited = []
	iterations = 0	

	def estimate_cost(state): return state[1] + heuristic(state[0])
	def queue_entry(state): return (estimate_cost(state), state)
	while not q.empty():
		#iterations += 1
		#if iterations % 1000 == 0:
		#	print("iterations: ", iterations)
		cur_board, cost, movement  = q.get()[1]
		if board_is_goal(cur_board):
			queue_size = q.qsize()
			return [cost, iterations, queue_size, movement]
		visited.append(hash_board(cur_board))
		for move in feasible_state(cur_board):
			if hash_board(move) not in visited:
				pos = find_zero_pos(move)
				cur_state = [move, cost + 1, movement + [pos]]
				q.put(queue_entry(cur_state))


def iddfs(board):
	iterations = 0
	for depth in itertools.count():
		cur_state = [board, 0, []]
		q = []
		q.append(cur_state)
		visited = {}
		while len(q) != 0:
			#iterations += 1
			#if iterations % 1000 == 0:
			#	print("iterations : ",iterations)
			cur_board, cost, movement = q.pop(0)
			if board_is_goal(cur_board):
			    queue_size = len(q)
			    return [cost, iterations, queue_size, movement]
			visited[hash_board(cur_board)] = cost

			if cost < depth:
				for move in feasible_state(cur_board):
					if hash_board(move) not in visited:
						spot = find_zero_pos(move)
						cur_state = [move, cost + 1, movement + [spot]]
						q.append(cur_state)


def bfs(board):
	cur_state = [board, 0, []]
	q = []
	q.append(cur_state)
	visited = []
	iterations = 0
	while len(q) != 0:
		#iterations += 1
		#if iterations % 1000 == 0:
		#	print("iterations: ", iterations)
		cur_board, cost, movement = q.pop(0)
		if board_is_goal(cur_board):
			queue_size = len(q)
			return [cost, iterations, queue_size, movement]
		visited.append(hash_board(cur_board))
		for new_board in feasible_state(cur_board):
			if hash_board(new_board) not in visited:
				spot = find_zero_pos(new_board)
				cur_state = [new_board, cost+1, movement + [spot]]
				q.append(cur_state)

def hash_board(board):
	board = np.array(board)
	return sha1(board).hexdigest()

def solve(algorithm, board, heuristic = None):

	ans = algorithm(board, heuristic) if heuristic else algorithm(board)
	result = {}
	return ans[2],ans[1]

def is_legal(move, zero):
	for i in range(4):
		if move == move_pos(zero, i):
			return True
	return False


def check_ans(board, movement):
	board_ = copy.deepcopy(board)
	boards = []
	boards.append(board_)
	for move in movement:
		zerox,zeroy = find_zero_pos(board_)
		if is_legal(move, (zerox,zeroy)):
			spotx, spoty = move
			temp = board_[spotx][spoty]
			board_[spotx][spoty] = board_[zerox][zeroy]
			board_[zerox][zeroy] = temp
			boards.append(board_)
		else:
			return False
	#draw_board()
	if hash_board(goal) == hash_board(board_):
		print("correct")
		return True
	else:
		print("wrong")
		return False

def draw_board(board):
	n = len(board)
	for i in range(n):
		for j in range(n):
			temp = board[i][j]
			print(temp),
		print(" ")
	print(" ")


def shuffle_puzzle(board):
	board_ = copy.deepcopy(board)
	for i in range(1000):
		states = feasible_state(board_)
		n = len(states)
		temp = random.randint(0,n-1)
		board_ = states[temp]
	return board_

def run_timed(algorithm, board, heuristic = None):
  # Write a dot to stdout every twenty thousand iterations.

  start = dt.datetime.now()
  result = algorithm(board, heuristic) if heuristic else algorithm(board)
  end = dt.datetime.now()

  # Add approximate time elapsed as datetime.timedelta to result object.
  result.append(end - start)
  return result

def print_result(result):
    global boardG
    print(" " + "✓" if check_ans(boardG,result[3]) else "✕")
    stats = [("Execution time",     result[-1]),
           ("Path cost to goal",  "{} moves".format(result[0])),
           ("Iterations",         result[1]),
           ("Queue size at goal", result[2])]

    for s in stats:
        print("    * {:<20} {:<20}".format(s[0] + ":", str(s[1])))
    print("")

def main():
    global goal,boardG
    goal = [[1,2,3],[4,5,6],[7,8,0]]
    #boardG = [[1,2,3],[4,5,6],[7,0,8]]
    boardG = [[7,2,4],[5,0,6],[8,3,1]]
    #board = shuffle_puzzle(goal)
    print("  a) Uninformed breadth-first search")
    print_result(run_timed(bfs, boardG))

    print("  b) Iterative deepening depth-first search")
    print_result(run_timed(iddfs, boardG))

    print("  c I) A* search using number of misplaced tiles heuristic")
    print_result(run_timed(a_star, boardG, misplaced))

    print("  c II) A* search using sum of manhattan distances heuristic")
    print_result(run_timed(a_star, boardG, manhattan_distance))


if __name__ == "__main__":
	main()