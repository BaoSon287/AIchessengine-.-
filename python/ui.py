import pygame
import chess

WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8
WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
HIGHLIGHT = (186, 202, 68)

PIECE_IMAGES = {}
PIECES = ['p', 'r', 'n', 'b', 'q', 'k', 'p1', 'r1', 'n1', 'b1', 'q1', 'k1']
for piece in PIECES:
    try:
        PIECE_IMAGES[piece] = pygame.image.load(f'assets/{piece}.png')
        PIECE_IMAGES[piece] = pygame.transform.scale(PIECE_IMAGES[piece], (SQUARE_SIZE, SQUARE_SIZE))
    except pygame.error:
        print(f"Không thể load ảnh cho quân {piece}")

def draw_board(screen, flip=False, last_move_from=None, last_move_to=None):
    for row in range(8):
        for col in range(8):
            r = 7 - row if flip else row
            c = 7 - col if flip else col
            color = WHITE if (r + c) % 2 == 0 else BROWN

            # Nếu là ô liên quan đến nước đi cuối
            if last_move_from is not None:
                from_rank = chess.square_rank(last_move_from)
                from_file = chess.square_file(last_move_from)
                from_row = 7 - from_rank if not flip else from_rank
                from_col = from_file if not flip else 7 - from_file
                if row == from_row and col == from_col:
                    color = "#f7ecb5"

            if last_move_to is not None:
                to_rank = chess.square_rank(last_move_to)
                to_file = chess.square_file(last_move_to)
                to_row = 7 - to_rank if not flip else to_rank
                to_col = to_file if not flip else 7 - to_file
                if row == to_row and col == to_col:
                    color = "#f7ecb5"

            pygame.draw.rect(screen, color, pygame.Rect(col * 75, row * 75, 75, 75))


def draw_pieces(screen, board, flip=False):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            row = 7 - rank if not flip else rank
            col = file if not flip else 7 - file

            symbol = piece.symbol()
            key = symbol.lower() if piece.color == chess.BLACK else symbol.lower() + "1"

            if key in PIECE_IMAGES:
                screen.blit(PIECE_IMAGES[key], (col * SQUARE_SIZE, row * SQUARE_SIZE))



def highlight_moves(screen, board, from_square, flip=False):
    overlay_color = (144, 238, 144, 100)

    overlay = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    overlay.fill(overlay_color)

    for move in board.legal_moves:
        if move.from_square == from_square:
            to_rank = chess.square_rank(move.to_square)
            to_file = chess.square_file(move.to_square)
            row = 7 - to_rank if not flip else to_rank
            col = to_file if not flip else 7 - to_file

            screen.blit(overlay, (col * SQUARE_SIZE, row * SQUARE_SIZE))


        
def draw_promotion_choices(screen, color):
    options = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
    names = ['q', 'r', 'b', 'n']
    if color == chess.WHITE:
        names = [n + '1' for n in names]

    for i, name in enumerate(names):
        rect = pygame.Rect(i * 75 + 150, 225, 75, 75)
        pygame.draw.rect(screen, (200, 200, 200), rect)
        screen.blit(PIECE_IMAGES[name], (i * 75 + 150, 225))
def get_promotion_choice(pos, color):
    x, y = pos
    if 225 <= y <= 300 and 150 <= x <= 450:
        index = (x - 150) // 75
        options = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
        return options[index]
    return None
