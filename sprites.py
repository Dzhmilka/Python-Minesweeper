import random

import pygame
from settings import *

# types list
# "." -> unknown
# "X" -> mine
# "C" -> clue
# "/" -> empty

class Interface:
    def __init__(self, board_surface):
        board_surface.blit(self.image, (self.x, self.y))

class Tile:
    def __init__(self, x, y, image, type, revealed=False, flagged=False):
        self.x, self.y = x * TILESIZE, y * TILESIZE
        self.image = image
        self.type = type
        self.revealed = revealed
        self.flagged = flagged
        self.is_pressed = False

    def draw(self, board_surface):
        if self.flagged:
            board_surface.blit(tile_flag, (self.x, self.y))
        elif self.revealed:
            board_surface.blit(self.image, (self.x, self.y))
        elif self.is_pressed: 
            board_surface.blit(tile_empty, (self.x, self.y))
        else:
            board_surface.blit(tile_unknown, (self.x, self.y))


class Board:
    def __init__(self):
        self.board_surface = pygame.Surface((WIDTH, HEIGHT))
        self.board_list = [[Tile(col, row, tile_empty, ".") for col in range(COLS)] for row in range(ROWS)]
        self.place_mines()
        self.place_clues()
        self.dug = []
        self.start_time = None 
        self.is_smile_pressed = False
        self.current_smile_image = ind_faces[0]
        self.total_elapsed_time = 0

    def start_timer(self):
        self.start_time = pygame.time.get_ticks()

    def stop_timer(self):
        if self.start_time is not None:
            # Update total_elapsed_time when stopping the timer
            self.total_elapsed_time += (pygame.time.get_ticks() - self.start_time) // 1000
        self.start_time = None

    def get_elapsed_time(self):
        if self.start_time is not None:
            elapsed_time = pygame.time.get_ticks() - self.start_time
            return min(elapsed_time // 1000, 999)
        return min(self.total_elapsed_time, 999)
    
    def place_mines(self):
        for _ in range(AMOUNT_MINES):
            while True:
                x = random.randint(0, ROWS-1)
                y = random.randint(0, COLS-1)

                if self.board_list[x][y].type == ".":
                    self.board_list[x][y].image = tile_mine
                    self.board_list[x][y].type = "X"
                    break

    def place_clues(self):
        for x in range(ROWS):
            for y in range(COLS):
                if self.board_list[x][y].type != "X":
                    total_mines = self.check_neighbours(x, y)
                    if total_mines > 0:
                        self.board_list[x][y].image = tile_numbers[total_mines-1]
                        self.board_list[x][y].type = "C"


    @staticmethod
    def is_inside(x, y):
        return 0 <= x < ROWS and 0 <= y < COLS

    def check_neighbours(self, x, y):
        total_mines = 0
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                neighbour_x = x + x_offset
                neighbour_y = y + y_offset
                if self.is_inside(neighbour_x, neighbour_y) and self.board_list[neighbour_x][neighbour_y].type == "X":
                    total_mines += 1

        return total_mines

    def check_flags(self, x, y):
        total_flags = 0
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                neighbour_x = x + x_offset
                neighbour_y = y + y_offset
                if self.is_inside(neighbour_x, neighbour_y) and self.board_list[neighbour_x][neighbour_y].flagged:
                    total_flags += 1
        return total_flags

    def mine_counter(self):
        mine_counter = AMOUNT_MINES
        for row in self.board_list:
            for tile in row:
                if tile.flagged:
                    mine_counter = mine_counter - 1
        return min(mine_counter, 999)
    
    def get_digit_images(self, value):
        if value < 0:
            return [ind_numbers[0], ind_numbers[0], ind_numbers[0]]  # Display three zeros for negative values
        elif value < 10:
            return [ind_numbers[0], ind_numbers[0], ind_numbers[value]]
        else:
            # Display three digits, e.g., for mine_counter = 012
            digit1 = value // 100 % 10
            digit2 = value // 10 % 10
            digit3 = value % 10
            return [ind_numbers[digit1], ind_numbers[digit2], ind_numbers[digit3]]

    def draw(self, screen):
        self.board_surface.fill(BGCOLOR)

        topleft_border_rect = topleft_border.get_rect()
        topleft_border_rect.topleft = (0, 0)
        self.board_surface.blit(topleft_border, topleft_border_rect)

        topright_border_rect = topright_border.get_rect()
        topright_border_rect.topright = (WIDTH, 0)
        self.board_surface.blit(topright_border, topright_border_rect)
        
        long_left_border = pygame.transform.scale(leftright_border, (leftright_border.get_width(), ind_numbers[0].get_height() + 14))
        long_left_border_rect = long_left_border.get_rect()
        long_left_border_rect.topleft = (0, topleft_border_rect.bottom)
        self.board_surface.blit(long_left_border, long_left_border_rect)

        long_right_border = pygame.transform.scale(leftright_border, (leftright_border.get_width(), ind_numbers[0].get_height() + 14))
        long_right_border_rect = long_right_border.get_rect()
        long_right_border_rect.topleft = (topright_border_rect.left, topright_border_rect.bottom)
        self.board_surface.blit(long_right_border, long_right_border_rect)

        middleleft_border_rect = middleleft_border.get_rect()
        middleleft_border_rect.topleft = (0, long_left_border_rect.bottom)
        self.board_surface.blit(middleleft_border, middleleft_border_rect)

        smile_image = self.current_smile_image
        smile_width = smile_image.get_width()
        smile_height = smile_image.get_height()
        smile_x = (WIDTH - smile_width) // 2
        smile_y = topleft_border_rect.bottom + (middleleft_border_rect.top - topleft_border_rect.bottom - smile_height) // 2
        self.smile_rect = pygame.Rect(smile_x, smile_y, ind_faces[0].get_width(), ind_faces[0].get_height())

        # Draw the smile image
        self.board_surface.blit(smile_image, (smile_x, smile_y))

        mine_counter_images = self.get_digit_images(self.mine_counter())
        start_x_mine_counter = long_left_border_rect.right + 12
        # Draw the mine counter images at the desired position
        for _, image in enumerate(mine_counter_images):
            rect = image.get_rect()
            rect.topleft = (start_x_mine_counter, topleft_border_rect.bottom + 7)  # Adjust the position as needed
            start_x_mine_counter += rect.width
            self.board_surface.blit(image, rect)

        timer_images = self.get_digit_images(self.get_elapsed_time())
        timer_width = sum(image.get_rect().width for image in timer_images)
        # Draw the timer images starting from the rightmost position
        start_x_timer = long_right_border_rect.left - 12 - timer_width  # Adjusted position
        for _, image in enumerate(timer_images):
            rect = image.get_rect()
            rect.topleft = (start_x_timer, topleft_border_rect.bottom + 7)  # Adjusted position
            start_x_timer += rect.width  # Adjusted position
            self.board_surface.blit(image, rect)

        for row in self.board_list:
            left_border_rect = leftright_border.get_rect()
            left_border_rect.topleft = (row[0].x, row[0].y + topbottom_border.get_height() * 2 + ind_numbers[0].get_height() + 14)
            self.board_surface.blit(leftright_border, left_border_rect)

            for tile in row:
                # Adjust the drawing position by the width of the left border
                tile.x = tile.x + leftright_border.get_width()
                tile.y = tile.y + topbottom_border.get_height() * 2 + ind_numbers[0].get_height() + 14
                tile.draw(self.board_surface)
                tile.x -= leftright_border.get_width()  # Reset the x-coordinate for logical consistency
                tile.y = tile.y - topbottom_border.get_height() * 2 - ind_numbers[0].get_height() - 14

            right_border_rect = leftright_border.get_rect()
            right_border_rect.topleft = (row[-1].x + TILESIZE + leftright_border.get_width(), row[-1].y + topbottom_border.get_height() * 2 + ind_numbers[0].get_height() + 14)
            self.board_surface.blit(leftright_border, right_border_rect)
        # Draw bottom left corner after all tiles in the row
        bottom_left_rect = bottomleft_border.get_rect()
        bottom_left_rect.topleft = (row[0].x, row[-1].y + TILESIZE + topbottom_border.get_height() * 2 + ind_numbers[0].get_height() + 14)
        self.board_surface.blit(bottomleft_border, bottom_left_rect)

        # Draw bottom borders for each column
        for col in range(len(row)):
            top_border_rect = topbottom_border.get_rect()
            top_border_rect.topleft = (self.board_list[0][col].x + topleft_border.get_width(), self.board_list[0][col].y)
            self.board_surface.blit(topbottom_border, top_border_rect)

            middle_border_rect = topbottom_border.get_rect()
            middle_border_rect.topleft = (self.board_list[0][col].x + topleft_border.get_width(), self.board_list[0][col].y + topbottom_border.get_height() + ind_numbers[0].get_height() + 14)
            self.board_surface.blit(topbottom_border, middle_border_rect)

            bottom_border_rect = topbottom_border.get_rect()
            bottom_border_rect.topleft = (self.board_list[0][col].x + bottomleft_border.get_width(), self.board_list[-1][col].y + TILESIZE + topbottom_border.get_height() * 2 + ind_numbers[0].get_height() + 14)
            self.board_surface.blit(topbottom_border, bottom_border_rect)

        middleright_border_rect = middleright_border.get_rect()
        middleright_border_rect.topleft = (topright_border_rect.left, long_right_border_rect.bottom)
        self.board_surface.blit(middleright_border, middleright_border_rect)

        # Draw bottom right corner after all bottom borders
        bottom_right_rect = bottomright_border.get_rect()
        bottom_right_rect.topleft = (row[-1].x + TILESIZE + leftright_border.get_width(), row[-1].y + TILESIZE + topbottom_border.get_height() * 2 + ind_numbers[0].get_height() + 14)
        self.board_surface.blit(bottomright_border, bottom_right_rect)

        screen.blit(self.board_surface, (0, 0))

    def reveal_empty_around(self, x, y):
        self.board_list[x][y].is_pressed = True
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                neighbour_x = x + x_offset
                neighbour_y = y + y_offset
                if self.is_inside(neighbour_x, neighbour_y) and \
                        not self.board_list[neighbour_x][neighbour_y].revealed and \
                        not self.board_list[neighbour_x][neighbour_y].flagged:
                    self.board_list[neighbour_x][neighbour_y].is_pressed = True

    def dig(self, x, y):
        if self.board_list[x][y].flagged:
            return True
        self.dug.append((x, y))
        if self.board_list[x][y].type == "X":
            self.board_list[x][y].revealed = True
            self.board_list[x][y].image = tile_exploded
            return False
        elif self.board_list[x][y].type == "C":
            if self.board_list[x][y].revealed == True and self.check_flags(x, y) == self.check_neighbours(x, y):
                for x_offset in range(-1, 2):
                    for y_offset in range(-1, 2):
                        neighbour_x = x + x_offset
                        neighbour_y = y + y_offset
                        if self.is_inside(neighbour_x, neighbour_y):
                            if self.board_list[neighbour_x][neighbour_y].type == "X" and self.board_list[neighbour_x][neighbour_y].flagged:
                                continue
                            elif self.board_list[neighbour_x][neighbour_y].type == "X":
                                self.board_list[neighbour_x][neighbour_y].revealed = True
                                self.board_list[neighbour_x][neighbour_y].image = tile_exploded
                                return False
                            elif self.board_list[neighbour_x][neighbour_y].type == ".":
                                for row in range(max(0, x-1), min(ROWS-1, x+1) + 1):
                                    for col in range(max(0, y-1), min(COLS-1, y+1) + 1):
                                        if (row, col) not in self.dug and not self.board_list[row][col].flagged:
                                            if self.dig(row, col) == False:
                                                return False
                                return True
                            else: 
                                self.dug.append((neighbour_x, neighbour_y))
                                self.board_list[neighbour_x][neighbour_y].revealed = True
                return True
            elif self.board_list[x][y].revealed == True and self.check_flags(x, y) != self.check_neighbours(x, y):
                return True
            self.board_list[x][y].revealed = True
            return True

        self.board_list[x][y].revealed = True

        for row in range(max(0, x-1), min(ROWS-1, x+1) + 1):
            for col in range(max(0, y-1), min(COLS-1, y+1) + 1):
                if (row, col) not in self.dug:
                    self.dig(row, col)
        return True

    def display_board(self):
        for row in self.board_list:
            print(row)
        print()