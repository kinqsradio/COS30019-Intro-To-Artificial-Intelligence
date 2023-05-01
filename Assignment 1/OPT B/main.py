import pygame
import time
import math

from grid import Grid
from algorithm import Search

textFile = 'map.txt'
# 'RobotNav-test.txt'
# 'test.txt'

# Parse coordinates from text file
def parse_coordinates(text):
    text = text.strip('[]()\n')
    return tuple(map(int, text.split(',')))

# Reading from text file
def read_grid_setup(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        
        dimensions = parse_coordinates(lines[0])
        starting_location = parse_coordinates(lines[1])[::-1]
        goal_states = [parse_coordinates(goal.strip())[::-1] for goal in lines[2].split('|')]
        walls = [parse_coordinates(line) for line in lines[3:]]
        return dimensions, starting_location, goal_states, walls


#This execute function has bug  => fixed  
def execute_search(algorithm):
    start_time = time.time()
    result = search.search(algorithm=algorithm)
    end_time = time.time()
    duration = end_time - start_time
    
    # print("Execute Result:", result) # This is correct

    path = result.strip(";").split("; ") # Incorrect => Fixed
    
    # print("Execute path:", path)

    if not path or all(x.isspace() for x in path):
        path_output = "No Path Found"
    else:
        path_output = ', '.join(path)
        
    # print("Execute Path Output:", path_output)

    search_nodes = search.get_search_movement()
    return path, path_output, duration, search_nodes

# Reused render buttons function
def render_button(screen, rect, text):
    pygame.draw.rect(screen, white, rect)
    font = mediumFont
    button_text = font.render(text, True, black)
    text_rect = button_text.get_rect()
    text_rect.center = rect.center
    screen.blit(button_text, text_rect)

# Initialize
dimensions, starting_location, goal_states, walls = read_grid_setup(textFile)
rows, cols = dimensions

#Setting Up Pygame
cell_size = 40  # Define the size of each square cell
pygame.init()

# Set up display
cell_size = 40  # Define the size of each square cell
pygame.display.set_caption("Robot Navigation Assignment (Opt B)")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

#Fonts
smallFont = pygame.font.Font("OpenSans-Regular.ttf", 15)
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

# Set up
grid = Grid(rows, cols, cell_size, starting_location, goal_states, walls)
# print(goal_states)
search = Search(grid)

#Main
running = True
goals_found = []
while running:
    
    # Set the screen dimensions for the button choosing state
    button_width = 200
    button_height = 50
    width = 1280
    height = 720
    screen = pygame.display.set_mode((width, height))
    pathOutput = None
    
    choose = True
    while choose:
        #Reset to default
        path_drawn = False
        algorithm = None
        path = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                choose = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if DFSbutton.collidepoint(mouse_pos) and algorithm is None:
                    algorithm = 'dfs-r'
                    path, path_output, duration, search_nodes = execute_search(algorithm)
                    dimensions, starting_location, goal_states, walls = read_grid_setup(textFile)
                    # print(f'Result: {path_output}')
                    choose = False
                elif BFSbutton.collidepoint(mouse_pos) and algorithm is None:
                    algorithm = 'bfs'
                    path, path_output, duration, search_nodes = execute_search(algorithm)
                    dimensions, starting_location, goal_states, walls = read_grid_setup(textFile)
                    # print(f'Result: {path_output}')
                    choose = False
                elif DLSbutton.collidepoint(mouse_pos) and algorithm is None: #custom1
                    algorithm = 'cus1'
                    path, path_output, duration, search_nodes = execute_search(algorithm)
                    dimensions, starting_location, goal_states, walls = read_grid_setup(textFile)
                    # print(f'Result: {path_output}')
                    choose = False
                elif IDSbutton.collidepoint(mouse_pos) and algorithm is None: #custom1ext
                    algorithm = 'cus1_ext'
                    path, path_output, duration, search_nodes = execute_search(algorithm)
                    dimensions, starting_location, goal_states, walls = read_grid_setup(textFile)
                    # print(f'Result: {path_output}')
                    choose = False
                elif GBFSbutton.collidepoint(mouse_pos) and algorithm is None:
                    algorithm = 'gbfs'
                    path, path_output, duration, search_nodes = execute_search(algorithm)
                    dimensions, starting_location, goal_states, walls = read_grid_setup(textFile)
                    # print(f'Result: {path_output}')
                    choose = False
                elif Abutton.collidepoint(mouse_pos) and algorithm is None:
                    algorithm = 'a'
                    path, path_output, duration, search_nodes = execute_search(algorithm)
                    dimensions, starting_location, goal_states, walls = read_grid_setup(textFile)
                    # print(f'Result: {path_output}')
                    choose = False
                elif IDAbutton.collidepoint(mouse_pos) and algorithm is None: #custom2
                    algorithm = 'cus_2'
                    path, path_output, duration, search_nodes = execute_search(algorithm)
                    dimensions, starting_location, goal_states, walls = read_grid_setup(textFile)
                    # print(f'Result: {path_output}')
                    choose = False
                    
                #Updating Heurisitc
                elif Manbutton.collidepoint(mouse_pos) and algorithm is None: #manhantan
                    heuristic = 'manhattan'
                    search.update_heuristic(heuristic)
                    #print(heuristic)
                elif Chebutton.collidepoint(mouse_pos) and algorithm is None: #chebyshev
                    heuristic = 'chebyshev'
                    search.update_heuristic(heuristic)
                    #print(heuristic)
                elif Eubutton.collidepoint(mouse_pos) and algorithm is None: #euclidean
                    heuristic = 'euclidean'
                    search.update_heuristic(heuristic)
                    #print(heuristic)
                elif Qbutton.collidepoint(mouse_pos) and algorithm is None: #Quit
                    running = False
                    choose = False
        screen.fill(black)
        if algorithm is None:
            #print(f"Here is result array: {result}")
            # Draw title
            title = largeFont.render("Robot Navigation", True, white)
            titleRect = title.get_rect()
            titleRect.center = ((width / 2), 50)
            screen.blit(title, titleRect)
                
            # DFS
            DFSbutton = pygame.Rect((width // 8), (height // 2), button_width, button_height)
            render_button(screen, DFSbutton, "DFS")

            # BFS
            BFSbutton = pygame.Rect((width // 8 + button_width + 10), (height // 2), button_width, button_height)
            render_button(screen, BFSbutton, "BFS")
            
            # DLS
            DLSbutton = pygame.Rect((width // 8 + 2 * button_width + 20), (height // 2), button_width, button_height)
            render_button(screen, DLSbutton, "Custom 1")

            # IDS
            IDSbutton = pygame.Rect((width // 8 + 3 * button_width + 30), (height // 2), button_width, button_height)
            render_button(screen, IDSbutton, "Custom 1 Ext")

            # GBFS
            GBFSbutton = pygame.Rect((width // 8), (height // 2 + 60), button_width, button_height)
            render_button(screen, GBFSbutton, "GBFS")

            # A*
            Abutton = pygame.Rect((width // 8 + button_width + 10), (height // 2 + 60), button_width, button_height)
            render_button(screen, Abutton, "A*")

            # IDA*
            IDAbutton = pygame.Rect((width // 8 + 2 * button_width + 20), (height // 2 + 60), button_width, button_height)
            render_button(screen, IDAbutton, "Custom 2")
            
            # Quit
            Qbutton = pygame.Rect((width // 8 + 3 * button_width + 30), (height // 2 + 60), button_width, button_height)
            render_button(screen, Qbutton, "Quit")
            
            # Heuristic = manhattan
            Manbutton = pygame.Rect((width // 8), (height // 2 + 120), button_width, button_height)
            render_button(screen, Manbutton, "Manhanttan")
            
            # Heuristic = chebyshev
            Chebutton = pygame.Rect((width // 8 + button_width + 10), (height // 2 + 120), button_width, button_height)
            render_button(screen, Chebutton, "Chebyshev")
            
            # Heuristic = euclidean
            Eubutton = pygame.Rect((width // 8 + 2* button_width + 20), (height // 2 + 120), button_width, button_height)
            render_button(screen, Eubutton, "Euclidean")
            
                    
        pygame.display.flip()
    
    # Set the screen dimensions for visualisation
    width, height = cols * cell_size, rows * cell_size
    screen = pygame.display.set_mode((width, height))
    goal_index = 0

    while algorithm is not None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                algorithm = None

        screen.fill(black)

        if not path_drawn:
            # This is needed to handle more than 1 goals
            if goal_index < len(goal_states):
                grid.intial_state(screen)
                search_nodes = list(search_nodes)
                grid.draw_path(screen, path, search_nodes)
                path_drawn = True
                pygame.time.delay(5000)
                search_nodes_length = len(search_nodes)
                
                print(f"filename:main.py | search method:{algorithm} | number of searched nodes:{search_nodes_length}")
                print(f"Number/Length of searched nodes: {search_nodes_length}")
                
                if path is not None and path_output != 'No path found.':
                    current_position = grid.starting_location
                    
                    # Direction to cords
                    for direction in path:
                        move = None
                        if direction == 'up':
                            move = (-1, 0)
                        elif direction == 'down':
                            move = (1, 0)
                        elif direction == 'right':
                            move = (0, 1)
                        elif direction == 'left':
                            move = (0, -1)
                        if move:
                            current_position = (current_position[0] + move[0], current_position[1] + move[1])
                            
                    # print("Here is current pos: ",current_position)
                    found_goal = current_position
                    if found_goal in goal_states:
                        goals_found.append(found_goal)
                        goal_states.remove(found_goal)

                # Reset for the next goal state
                starting_location = grid.starting_location
                grid.goal_states = goal_states[goal_index:]  # Update the grid's goal states
                grid = Grid(rows, cols, cell_size, starting_location, grid.goal_states, walls)
                search = Search(grid)
                path_drawn = False
                search_nodes = []

                print(f'Goals found: {goals_found}')
                print(f'Result: {path_output}')
                print(f'Time taken: {duration}')

                # To handle some index might out of bound
                try:
                    path, path_output, duration, search_nodes = execute_search(algorithm)
                except IndexError as e:
                    algorithm = None
                else:
                    if path_output == 'No path found.':
                        goal_index += 1
                        starting_location = grid.starting_location
                        grid.goal_states = goal_states[goal_index:]  # Update the grid's goal states
                        grid = Grid(rows, cols, cell_size, starting_location, grid.goal_states, walls)
                        search = Search(grid)
                        path_drawn = False
                        search_nodes = []
            
            # Reset
            else:
                algorithm = None
                path = None
                neighbour_nodes = []
                search_nodes = []
                goals_found.clear()
                dimensions, starting_location, goal_states, walls = read_grid_setup(textFile)
                grid = Grid(rows, cols, cell_size, starting_location, goal_states, walls)
                search = Search(grid)

        pygame.display.flip()
        choose = True

pygame.quit()
