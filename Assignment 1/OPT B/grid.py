import pygame

class Grid:
    def __init__(self, rows, cols, cell_size, starting_location, goal_states, walls):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.starting_location = starting_location
        self.goal_states = goal_states
        self.walls = walls

    # Drawing Initial States (MAP/Grid)
    def intial_state(self, screen):
        rects = []
        for i in range(self.rows):
            for j in range(self.cols):
                color = (255, 255, 255)  # White background
                if (i, j) == self.starting_location:
                    color = (255, 0, 0)  # Red (starting location)
                elif (i, j) in self.goal_states:
                    color = (0, 255, 0)  # Green (goal states)

                rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, color, rect)
                rects.append(rect)

        # Draw walls
        for wall in self.walls:
            x, y, width, height = wall
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size, width * self.cell_size, height * self.cell_size)
            pygame.draw.rect(screen, (192, 192, 192), rect)
            rects.append(rect)

        # Draw grid lines on top of everything
        for i in range(self.rows):
            for j in range(self.cols):
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
                rects.append(rect)

        return rects

                                
    # Draw path + Visualize
    def draw_path(self, screen, path, search_nodes, delay=100, nodes_per_iteration=10):
        rects = self.intial_state(screen)
        pygame.display.update(rects)

        # I don't know why but search nodes are extremely hard to optimize may be there is a large amount of searched nodes
        # Draw Searched Nodes
        visited_nodes = set()
        search_node_surface = pygame.Surface((self.cols * self.cell_size, self.rows * self.cell_size), pygame.SRCALPHA)

        while search_nodes:
            updated_rects = []

            chunk, search_nodes = search_nodes[:nodes_per_iteration], search_nodes[nodes_per_iteration:]

            for node in chunk:
                if node in visited_nodes:
                    continue

                visited_nodes.add(node)

                vx, vy = node
                rect = pygame.Rect(vy * self.cell_size, vx * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(search_node_surface, (0, 255, 255), rect)
                updated_rects.append(rect)

            screen.blit(search_node_surface, (0, 0))
            pygame.display.update(updated_rects)
            pygame.time.delay(delay)
        
        # Reset
        rects = self.intial_state(screen)
        pygame.display.update(rects)

        # Start Drawing Path
        current_position = self.starting_location
        
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
                rect = pygame.Rect(current_position[1] * self.cell_size, current_position[0] * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (255, 255, 0), rect)
                pygame.display.update([rect])
                pygame.time.delay(delay)