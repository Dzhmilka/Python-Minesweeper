import pygame
import sys
from settings import *
from sprites import *


class GameBuilder:
    def __init__(self):
        self.game = Game()

    def build_board(self):
        self.game.board = Board()
        return self

    def build_display(self):
        self.game.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        return self

    def build_clock(self):
        self.game.clock = pygame.time.Clock()
        return self

    def get_game(self):
        return self.game

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.start_time = 0

    def new(self):
        self.board = Board()
        self.start_time = pygame.time.get_ticks()
        # self.board.display_board()

    def run(self):
        self.playing = True
        self.board.start_timer()
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
            pygame.display.flip()
        else:
            self.end_screen()

    def draw(self):
        self.board.draw(self.screen)
        pygame.display.flip()

    def check_win(self):
        for row in self.board.board_list:
            for tile in row:
                if tile.type != "X" and not tile.revealed:
                    return False
        return True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                my, mx = pygame.mouse.get_pos()
                if self.board.smile_rect.collidepoint(my, mx):
                    self.board.is_smile_pressed = True
                    self.board.current_smile_image = ind_faces[1]
                elif event.button == 1: self.board.current_smile_image = ind_faces[2]
                if my < 19: return
                if mx < topbottom_border.get_height() * 2 + ind_numbers[0].get_height() + 14: return

                mx = (mx - ind_numbers[0].get_height() - 14 - topbottom_border.get_height() * 2) // TILESIZE
                my = (my - leftright_border.get_width()) // TILESIZE

                try:
                    if event.button == 1:
                        if not self.board.board_list[mx][my].flagged:
                                if self.board.board_list[mx][my].type == "C" and self.board.board_list[mx][my].revealed:
                                    self.board.reveal_empty_around(mx, my)

                                self.board.board_list[mx][my].is_pressed = True

                    if event.button == 3:
                        if not self.board.board_list[mx][my].revealed:
                            self.board.board_list[mx][my].flagged = not self.board.board_list[mx][my].flagged
                            self.board.mine_counter()
                except IndexError:
                    continue

            if event.type == pygame.MOUSEBUTTONUP:
                my, mx = pygame.mouse.get_pos()
                if self.board.smile_rect.collidepoint(my, mx):
                    self.new()
                    self.run()
                    self.board.is_smile_pressed = False
                    self.board.current_smile_image = ind_faces[0]
                    return
                self.board.current_smile_image = ind_faces[0]
                for row in self.board.board_list:
                        for tile in row:
                            tile.is_pressed = False
                if my < 19: return
                if mx < topbottom_border.get_height() * 2 + ind_numbers[0].get_height() + 14: return
                mx = (mx - ind_numbers[0].get_height() - 14 - topbottom_border.get_height() * 2) // TILESIZE
                my = (my - leftright_border.get_width()) // TILESIZE
                if event.button == 1:
                    try:
                        if not self.board.board_list[mx][my].flagged:
                            # dig and check if exploded
                            if not self.board.dig(mx, my):
                                self.board.current_smile_image = ind_faces[4]
                                # explode
                                for row in self.board.board_list:
                                    for tile in row:
                                        if tile.flagged and tile.type != "X":
                                            tile.flagged = False
                                            tile.revealed = True
                                            tile.image = tile_not_mine
                                        elif tile.type == "X":
                                            tile.revealed = True
                                self.playing = False
                                return
                    except IndexError:
                        continue

                if self.check_win():
                    self.win = True
                    self.playing = False
                    self.board.current_smile_image = ind_faces[3]
                    for row in self.board.board_list:
                        for tile in row:
                            if not tile.revealed:
                                tile.flagged = True

    def end_screen(self):
        while True:
            self.board.stop_timer()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    my, mx = pygame.mouse.get_pos()
                    if self.board.smile_rect.collidepoint(my, mx):
                        self.board.is_smile_pressed = True
                        self.board.current_smile_image = ind_faces[1]

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.board.smile_rect.collidepoint(my, mx):
                        self.board.is_smile_pressed = False
                        self.board.current_smile_image = ind_faces[0]

                    my, mx = pygame.mouse.get_pos()
                    if self.board.smile_rect.collidepoint(my, mx):
                        self.new()
                        self.run()

            self.draw()


if __name__ == "__main__":
    game_builder = GameBuilder()
    game = game_builder.build_display().build_clock().build_board().get_game()

    while True:
        game.new()
        game.run()
