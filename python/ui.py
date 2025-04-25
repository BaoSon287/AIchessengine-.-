import pygame
import chess

WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8
WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
HIGHLIGHT = (186, 202, 68)
big_font = None
small_font = None

PIECE_IMAGES = {}
PIECES = ['p', 'r', 'n', 'b', 'q', 'k', 'p1', 'r1', 'n1', 'b1', 'q1', 'k1']
for piece in PIECES:
    try:
        PIECE_IMAGES[piece] = pygame.image.load(f'assets/{piece}.png')
        PIECE_IMAGES[piece] = pygame.transform.scale(PIECE_IMAGES[piece], (SQUARE_SIZE, SQUARE_SIZE))
    except pygame.error:
        print(f"Không thể load ảnh cho quân {piece}")

def draw_board(screen, flip=False, last_move_from=None, last_move_to=None):
    # Khởi tạo font để vẽ các chỉ số
    font = pygame.font.SysFont(None, 30)

    # Thanh trắng bên trái (cho các số 1-8) và dưới (cho a-h)
    BAR_WIDTH = 30  # Chiều rộng của thanh bên trái
    BAR_HEIGHT = 30  # Chiều cao của thanh phía dưới
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, BAR_WIDTH, HEIGHT + BAR_HEIGHT))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, HEIGHT, WIDTH + BAR_WIDTH, BAR_HEIGHT))

    # Vẽ các ô của bàn cờ, dịch chuyển sang phải để nhường chỗ cho thanh trắng bên trái
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
                    color = "#ADD8E6"

            if last_move_to is not None:
                to_rank = chess.square_rank(last_move_to)
                to_file = chess.square_file(last_move_to)
                to_row = 7 - to_rank if not flip else to_rank
                to_col = to_file if not flip else 7 - to_file
                if row == to_row and col == to_col:
                    color = "#ADD8E6"

            pygame.draw.rect(screen, color, pygame.Rect(BAR_WIDTH + col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Vẽ các chỉ số 1-8 (hàng) trên thanh trắng bên trái
    # Vẽ các chỉ số 1-8 (hàng) trên thanh trắng bên trái
    for row in range(8):
        # Tính toán hàng hiển thị dựa trên flip
        display_row = 7 - row if flip else row
        # Tính toán vị trí y để căn giữa ô
        y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        # Rank được hiển thị từ 8 (top) xuống 1 (bottom) khi flip=True
        rank = str(8 - row if flip else row + 1)
        text = font.render(rank, True, (255, 0, 0))
        screen.blit(text, (BAR_WIDTH // 2 - text.get_width() // 2, y - text.get_height() // 2))
    # Vẽ các chỉ số a-h (cột) trên thanh trắng phía dưới
    for col in range(8):
        # Tính toán cột hiển thị dựa trên flip
        display_col = 7 - col if flip else col
        # Tính toán vị trí x để căn giữa ô
        x = BAR_WIDTH + col * SQUARE_SIZE + SQUARE_SIZE // 2
        # File được hiển thị từ h (left) đến a (right) khi flip=True
        file = chr(ord('a') + display_col)  # Sửa lại để hiển thị đúng thứ tự
        text = font.render(file, True, (255, 0, 0))
        screen.blit(text, (x - text.get_width() // 2, HEIGHT + BAR_HEIGHT // 2 - text.get_height() // 2))
def draw_pieces(screen, board, flip=False):
    BAR_WIDTH = 30  # Để dịch chuyển các quân cờ sang phải
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
                screen.blit(PIECE_IMAGES[key], (BAR_WIDTH + col * SQUARE_SIZE, row * SQUARE_SIZE))

def highlight_moves(screen, board, from_square, flip=False):
    BAR_WIDTH = 30
    overlay_color = (144, 238, 144, 100)

    overlay = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    overlay.fill(overlay_color)

    for move in board.legal_moves:
        if move.from_square == from_square:
            to_rank = chess.square_rank(move.to_square)
            to_file = chess.square_file(move.to_square)
            row = 7 - to_rank if not flip else to_rank
            col = to_file if not flip else 7 - to_file

            screen.blit(overlay, (BAR_WIDTH + col * SQUARE_SIZE, row * SQUARE_SIZE))

def draw_promotion_choices(screen, color):
    BAR_WIDTH = 30
    options = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
    names = ['q', 'r', 'b', 'n']

    if color == chess.WHITE:
        names = [n + '1' for n in names]
    center_x = BAR_WIDTH + 300  # Dịch chuyển sang phải
    center_y = 300
    for i, name in enumerate(names):
        rect = pygame.Rect(center_x - 150 + i * 75, center_y - 75, 75, 75)
        pygame.draw.rect(screen, (200, 200, 200), rect)
        screen.blit(PIECE_IMAGES[name], (center_x - 150 + i * 75, center_y - 75))

def draw_game_over(screen, board, big_font, small_font):
    BAR_WIDTH = 30
    BAR_HEIGHT = 30
    outcome = board.outcome()
    if outcome is None:
        return

    if outcome.winner is None:
        result_text = "Hòa!"
        image_path = "assets/draw.png"
    elif outcome.winner:
        result_text = "Trắng thắng!"
        image_path = "assets/win.png"
    else:
        result_text = "Đen thắng!"
        image_path = "assets/loss.png"

    # Lớp phủ nền mờ
    overlay = pygame.Surface((WIDTH + BAR_WIDTH, HEIGHT + BAR_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # Hiển thị ảnh minh họa kết quả
    try:
        result_image = pygame.image.load(image_path).convert_alpha()
        result_image = pygame.transform.scale(result_image, (150, 150))
        image_rect = result_image.get_rect(center=((WIDTH + BAR_WIDTH) // 2, HEIGHT // 2 - 120))
        screen.blit(result_image, image_rect)
    except Exception as e:
        print(f"Lỗi khi tải ảnh {image_path}: {e}")

    # Hiển thị thông báo kết quả
    text_surface = big_font.render(result_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=((WIDTH + BAR_WIDTH) // 2, HEIGHT // 2 + 10))
    screen.blit(text_surface, text_rect)

    # Vẽ nút "Chơi lại"
    button_rect = pygame.Rect((WIDTH + BAR_WIDTH) // 2 - 80, HEIGHT // 2 + 70, 160, 50)
    pygame.draw.rect(screen, (70, 130, 180), button_rect, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), button_rect, 2, border_radius=10)

    button_text = small_font.render("Chơi lại", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)

    return button_rect

def get_promotion_choice(pos, color):
    BAR_WIDTH = 30
    x, y = pos
    center_x = BAR_WIDTH + 300
    center_y = 300
    if center_y - 75 <= y <= center_y and center_x - 150 <= x <= center_x + 150:
        index = (x - (center_x - 150)) // 75
        options = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
        return options[index]
    return None