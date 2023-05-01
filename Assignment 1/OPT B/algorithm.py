import math

class Search:
    def __init__(self, grid):
        self.grid = grid
        self.visited = set()
        self.search_movement = []
        self.path = []
        self.heuristicFunction = "manhattan"
        
    def get_visited_nodes(self):
        return self.visited
    
    def get_search_movement(self):
        return self.search_movement

    '''Reuse Function'''    
    def is_valid_move(self, position):
        row, col = position

        # Check if the position is outside the bounds of the grid
        if row < 0 or row >= self.grid.rows or col < 0 or col >= self.grid.cols:
            return False

        # Check if the position is inside a wall
        for wall in self.grid.walls:
            x, y, width, height = wall
            if col >= x and col < x + width and row >= y and row < y + height:
                return False

        return True

    def get_neighbors(self, position):
        row, col = position
        neighbors = [
            (row - 1, col),  # up
            (row, col - 1),  # left
            (row + 1, col),  # down
            (row, col + 1),  # right
        ]

        valid_neighbors = []
        for neighbor in neighbors:
            if self.is_valid_move(neighbor):
                # print("Here is the current Neighbor: ", neighbor)
                valid_neighbors.append(neighbor)

        return valid_neighbors

    '''Possible Heuristic Function'''
    
    def update_heuristic(self, new_heuristic):
        if new_heuristic in ["manhattan", "chebyshev", "euclidean"]:
            self.heuristicFunction = new_heuristic
            #print("New heuristic: ", self.heuristicFunction)
    
    def heuristic(self, position, goal):
        #print("Current heurisitic: ", self.heuristicFunction)
        if self.heuristicFunction == "manhattan":
            return self.manhattan_distance(position, goal)
        elif self.heuristicFunction == "chebyshev":
            return self.chebyshev(position, goal)
        elif self.heuristicFunction == "euclidean":
            return self.euclidean(position, goal)
        else:
            raise ValueError("Invalid heuristic function specified.")    
        
    # h(n) heuristic
    # Mahattan = |x1-x2| + |y1-y2|
    def manhattan_distance(self, position, goal): # <---------- Recommended
        x = abs(position[0] - goal[0])
        y = abs(position[1] - goal[1])
        return x + y
    
    # h(n) heuristic
    # Chebyshev = max(|x1 - x2|, |y1 - y2|)
    def chebyshev(self, position, goal):
        x = abs(position[0] - goal[0])
        y = abs(position[1] - goal[1])
        return max(x, y)

    
    # h(n) heuristic
    # Euclidean sqrt((x2 - x1)^2 + (y2 - y1)^2)
    def euclidean(self, position, goal):
        x = (position[0] - goal[0]) ** 2
        y = (position[1] - goal[1]) ** 2
        return math.sqrt(x + y)
    
    '''End Reuse Function'''


    '''Any search algo will be written below this'''

    '''DFS sample code:
    Reference:
    https://www.educative.io/answers/how-to-implement-depth-first-search-in-python
    '''
    #Note: DFS using LIFO
    
    # Recursive method    
    def dfs(self, position, path, stack=None):
        if stack is None:
            stack = []    
            
        if position in self.grid.goal_states:
            self.path = path
            # print("Here is DFS SELF PATH:", self.path)
            return True

        # print(position)
        self.visited.add(position)
        # print(self.visited)
        self.search_movement.append(position)

        for neighbor in self.get_neighbors(position):
            direction = (neighbor[0] - position[0], neighbor[1] - position[1])
            direction_map = {(-1, 0): 'up', (0, -1): 'left', (1, 0): 'down',  (0, 1): 'right'}
            move_direction = direction_map[direction]
            if neighbor not in self.visited:
                stack.append(neighbor)
                if self.dfs(neighbor, path + [move_direction], stack):
                    return True
                stack.pop()
        self.visited.remove(position)
        return False
    
    '''BFS sample code:
    Reference:
    https://favtutor.com/blogs/breadth-first-search-python
    '''
    # Note: BFS using FIFO
    def bfs(self):
        start = self.grid.starting_location
        queue = [(start, [])]  # Each element in the queue is a tuple containing a position and the path to that position

        while queue:
            position, path = queue.pop(0)  # FIFO
            
            # print("BFS Position:", position)

            self.search_movement.append(position)     
                   
            if position in self.grid.goal_states:
                return '; '.join(path) + ';'
        
            if position not in self.visited:
                self.visited.add(position)

                for neighbor in self.get_neighbors(position):
                    direction = (neighbor[0] - position[0], neighbor[1] - position[1])
                    direction_map = {(-1, 0): 'up', (0, -1): 'left', (1, 0): 'down',  (0, 1): 'right'}
                    move_direction = direction_map[direction]
                    queue.append((neighbor, path + [move_direction]))  # Enqueue the neighbor with its path
                    # print("BFS Path:", path)
                
        return "No path found."
    
    '''
    Reference:
    http://www.sfu.ca/~arashr/warren.pdf
    '''
    
    # Greedy Best First
    # f(n) = h(n)
    def greedy_best_first(self):
        start = self.grid.starting_location
        goal_states = self.grid.goal_states

        open_list = [(start, 0, [])]
        closed_list = set()

        while open_list:
            if not goal_states:
                return "No goals left to find."
            
            open_list.sort(key=lambda x: min(self.heuristic(x[0], goal) for goal in goal_states))  # Sort by heuristic (min cost to goal)
            position, cost, path = open_list.pop(0)
            self.search_movement.append(position)
                        
            if position in goal_states:
                return '; '.join(path) + ';'
            
            closed_list.add(position)
            self.visited.add(position)
                        
            for neighbor in self.get_neighbors(position):
                if neighbor not in closed_list:
                    direction = (neighbor[0] - position[0], neighbor[1] - position[1])
                    direction_map = {(-1, 0): 'up', (0, -1): 'left', (1, 0): 'down',  (0, 1): 'right'}
                    move_direction = direction_map[direction]
                    neighbor_cost = cost + 1
                    existing_neighbor = [entry for entry in open_list if entry[0] == neighbor]
                    if not existing_neighbor:
                        open_list.append((neighbor, neighbor_cost, path + [move_direction]))     
                             
        return "No path found."

    
    # A*            
    def a_star(self):
        start = self.grid.starting_location
        goal = self.grid.goal_states[0]

        open_list = [(start, 0, [])]
        closed_list = set()

        while open_list:
            open_list.sort(key=lambda x: x[1] + self.heuristic(x[0], goal))  # Sort by total cost (cost so far + heuristic)
            position, cost, path = open_list.pop(0)
            self.search_movement.append(position)

            if position == goal:
                return '; '.join(path) + ';'
            
            closed_list.add(position)
            self.visited.add(position)

            for neighbor in self.get_neighbors(position):
                if neighbor not in closed_list:
                    direction = (neighbor[0] - position[0], neighbor[1] - position[1])
                    direction_map = {(-1, 0): 'up', (0, -1): 'left', (1, 0): 'down',  (0, 1): 'right'}
                    move_direction = direction_map[direction]
                    neighbor_cost = cost + 1

                    existing_neighbor = [entry for entry in open_list if entry[0] == neighbor]
                    if not existing_neighbor or existing_neighbor[0][1] > neighbor_cost:
                        open_list.append((neighbor, neighbor_cost, path + [move_direction]))
                        
        return "No path found."
        
    
    '''
    Custom 1 - Uninform Search
    I'm using Dept Limit Search but I also extended it to Iterative Deepening Search 
    where it will performs multiple Depth Limit Search
    '''
    '''
    References:
    https://www.geeksforgeeks.org/iterative-deepening-searchids-iterative-deepening-depth-first-searchiddfs/
    '''
    #Depth limit search (DLS)
    def cus_1(self, position, goal, maxDepth, path):
        if position in goal:
            self.path = path
            return True
        
        self.visited.add(position)
        self.search_movement.append(position)

        if maxDepth <= len(path):
            return False
        
        for neighbor in self.get_neighbors(position):
            direction = (neighbor[0] - position[0], neighbor[1] - position[1])
            direction_map = {(-1, 0): 'up', (0, -1): 'left', (1, 0): 'down',  (0, 1): 'right'}
            move_direction = direction_map[direction]

            if neighbor not in self.visited:
                next_path = path.copy()
                next_path.append(move_direction)
                if self.cus_1(neighbor, goal, maxDepth, next_path):
                    return True
        self.visited.remove(position)
        
        return False
    
    #Iterative Deepening Search (IDS)
    def cus_1ext(self, position, goal, maxDepth, path):
        for i in range(maxDepth):
            self.visited = set()  #This always needs to be reset because it needs to perform multiple DLS  search!
            if self.cus_1(position, goal, i, path):
                return True
            
        return False
    
    '''
    Custom 2 - Informed Search
    IDA* Search
    '''
    def cus_2(self):
        def search(position, cost, heuristic, path, threshold):
            f = cost + heuristic
            if f > threshold:
                return f, None
            
            if position in self.grid.goal_states:
                return f, path
            
            minimum = float("inf")
            
            self.visited.add(position)
            self.search_movement.append(position)
            
            for neighbor in self.get_neighbors(position):
                if neighbor not in self.visited:
                    direction = (neighbor[0] - position[0], neighbor[1] - position[1])
                    direction_map = {(-1, 0): 'up', (0, -1): 'left', (1, 0): 'down',  (0, 1): 'right'}
                    move_direction = direction_map[direction]
                    self.visited.add(neighbor)
                    new_cost = cost + 1
                    new_heuristic = self.heuristic(neighbor, self.grid.goal_states[0])
                    next_threshold, result = search(neighbor, new_cost, new_heuristic, path + [move_direction], threshold)
                    self.visited.remove(neighbor)
                    
                    if result is not None:
                        return next_threshold, result
                    
                    minimum = min(minimum, next_threshold)
                    
            return minimum, None

        start = self.grid.starting_location
        goal = self.grid.goal_states[0]
        threshold = self.heuristic(start, goal)

        while True:
            threshold, result = search(start, 0, threshold, [], threshold)
            if result is not None:
                return '; '.join(result) + ';'
            if threshold == float("inf"):
                return "No path found."


    def search(self, algorithm='dfs'):
        if algorithm == 'dfs-r':
            if self.dfs(self.grid.starting_location, [], []):
                return '; '.join(self.path) + ';'
            else:
                return "No path found."
            
        elif algorithm == 'dfs-r':
            return self.dfs()
        elif algorithm == 'bfs':
            return self.bfs()
        elif algorithm == 'gbfs':
            return self.greedy_best_first()
        elif algorithm == 'a':
            return self.a_star()
        elif algorithm == 'cus1':
            if self.cus_1(self.grid.starting_location, self.grid.goal_states, 10000000, []): # Initialize depth is 10000000
                return '; '.join(self.path) + ';'
            else:
                return "No path found"
            
        elif algorithm == 'cus1_ext':
            if self.cus_1ext(self.grid.starting_location, self.grid.goal_states, 10000000, []): # Initialize depth is 10000000
                return '; '.join(self.path) + ';'
            else:
                return "No path found"
        elif algorithm == "cus_2":
            return self.cus_2()