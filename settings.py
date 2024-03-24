# COLORS (r, g, b)
import pygame
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (192, 192, 192)
GREEN = (0, 255, 0)
DARKGREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BGCOLOR = LIGHTGREY

# game settings
TILESIZE = 30
ROWS = 16
COLS = 16
AMOUNT_MINES = 30
FPS = 60
TITLE = "Minesweeper"

tile_numbers = []
for i in range(1, 9):
    tile_numbers.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", f"Tile{i}.png")), (TILESIZE, TILESIZE)))

numbers = pygame.image.load(os.path.join("assets", "numbers.png"))
image_width = numbers.get_width() // 10
image_height = numbers.get_height()
ind_numbers = []
for i in range(10):
    rect = pygame.Rect(i * image_width, 0, image_width, image_height)
    image = numbers.subsurface(rect)
    ind_numbers.append(pygame.transform.scale(image, (TILESIZE * 0.9, TILESIZE * 1.5)))

faces = pygame.image.load(os.path.join("assets", "faces.png"))
image_width = faces.get_width() // 5
image_height = faces.get_height()
ind_faces = []
for i in range(5):
    rect = pygame.Rect(i * image_width, 0, image_width, image_height)
    image = faces.subsurface(rect)
    ind_faces.append(pygame.transform.scale(image, (TILESIZE * 1.3, TILESIZE * 1.3)))

topbottom_border = pygame.transform.scale(pygame.image.load(os.path.join("assets/borders", "topbottom.png")), (TILESIZE, image_height - 8))
bottomleft_border = pygame.transform.scale(pygame.image.load(os.path.join("assets/borders", "bottomleft.png")), (image_width - 8, image_height - 8))
bottomright_border = pygame.transform.scale(pygame.image.load(os.path.join("assets/borders", "bottomright.png")), (image_width - 8, image_height - 8))
middleleft_border = pygame.transform.scale(pygame.image.load(os.path.join("assets/borders", "middleleft.png")), (image_width - 8, image_height - 8))
middleright_border = pygame.transform.scale(pygame.image.load(os.path.join("assets/borders", "middleright.png")), (image_width - 8, image_height - 8))
leftright_border = pygame.transform.scale(pygame.image.load(os.path.join("assets/borders", "leftright.png")), (image_width - 8, TILESIZE))
topleft_border = pygame.transform.scale(pygame.image.load(os.path.join("assets/borders", "topleft.png")), (image_width - 8, image_height - 8))
topright_border = pygame.transform.scale(pygame.image.load(os.path.join("assets/borders", "topright.png")), (image_width - 8, image_height - 8))

WIDTH = TILESIZE * COLS + leftright_border.get_width() * 2
HEIGHT = TILESIZE * ROWS + topbottom_border.get_height() * 3 + ind_numbers[0].get_height() + 14

tile_empty = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileEmpty.png")), (TILESIZE, TILESIZE))
tile_exploded = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileExploded.png")), (TILESIZE, TILESIZE))
tile_flag = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileFlag.png")), (TILESIZE, TILESIZE))
tile_mine = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileMine.png")), (TILESIZE, TILESIZE))
tile_unknown = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileUnknown.png")), (TILESIZE, TILESIZE))
tile_not_mine = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileNotMine.png")), (TILESIZE, TILESIZE))
