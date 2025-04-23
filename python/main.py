import pygame
from ui import draw_board, draw_pieces, highlight_moves
from game import Game
import chess

if __name__ == "__main__":
    WIDTH, HEIGHT = 600, 600
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")

    font = pygame.font.SysFont(None, 48)
    text1 = font.render("Button 1: AI play White", True, (255, 255, 255))
    text2 = font.render("Button 2: AI play Black", True, (255, 255, 255))
    
    background_img = pygame.image.load("assets/background.jpg")
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    while True:
        waiting = True
        ai_color = None
        while waiting:
            screen.blit(background_img, (0, 0)) 
            screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 + 10))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        ai_color = chess.WHITE
                        waiting = False
                    elif event.key == pygame.K_2:
                        ai_color = chess.BLACK
                        waiting = False

        flip = ai_color == chess.WHITE
        game = Game(ai_color=ai_color, flip=flip)
        if game.board.turn == game.ai_color:
            game.ai_thinking = True
            game.ai_move_time = pygame.time.get_ticks()

        running = True
        while running and game.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    running = False
                else:
                    game.handle_event(event)

            screen.fill((0, 0, 0))
            draw_board(screen, flip,last_move_from=game.last_move_from, last_move_to=game.last_move_to)
            if game.selected_square is not None and game.history_index == len(game.board.move_stack):
                highlight_moves(screen, game.view_board, game.selected_square, flip)
            draw_pieces(screen, game.view_board, flip)


            game.update_ai_move()

            if game.history_index < len(game.board.move_stack):
                pygame.display.set_caption(f"Chess Game - Xem lại bước {game.history_index}/{len(game.board.move_stack)}")
            else:
                pygame.display.set_caption("Chess Game")

            pygame.display.flip()
            game.clock.tick(60)
