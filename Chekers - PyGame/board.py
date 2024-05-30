import os
import queue
import time
import pygame
import json

# Chekers - Projekat: Algoritmi i strukture podataka
# Autor: Milan Sazdov SV21-2023, GitHub: MilanSazdov
# Maj. 2024

# inicijalizacija prozora same igre
board_width = 800
board_height = 800

white = (255, 50, 20)
black = (0, 0, 0)

square_size = board_width // 8

green = (118, 150, 86)
bez = (238, 238, 210)

gray = (128, 128, 128)

clock = pygame.time.Clock()
fps = 60
screen = pygame.display.set_mode((board_width, board_height))

pygame.font.init()
font = pygame.font.SysFont('Arial', 24)


class Figure:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.queen = False

    def move_figure(self, row, col):
        self.row = row
        self.col = col

    def make_queen(self):
        self.queen = True

    def draw_fig(self):
        if self.color == white:
            pygame.draw.circle(screen, white,
                               (self.col * square_size + square_size // 2, self.row * square_size + square_size // 2),
                               30)
            if self.queen:
                pygame.draw.circle(screen, (0, 40, 20), (
                    self.col * square_size + square_size // 2, self.row * square_size + square_size // 2), 15, 5)
                pygame.draw.circle(screen, (0, 100, 255), (
                    self.col * square_size + square_size // 2, self.row * square_size + square_size // 2), 20, 5,
                                   5, 5)
        else:
            pygame.draw.circle(screen, black,
                               (self.col * square_size + square_size // 2, self.row * square_size + square_size // 2),
                               30)
            if self.queen:
                pygame.draw.circle(screen, (160, 255, 24), (
                    self.col * square_size + square_size // 2, self.row * square_size + square_size // 2), 15, 5)
                pygame.draw.circle(screen, (0, 100, 255), (
                    self.col * square_size + square_size // 2, self.row * square_size + square_size // 2), 20, 5,
                                   5, 5)


class Board:
    def __init__(self):
        self.board = []
        self.white_figures = 12
        self.black_figures = 12
        self.white_queens = 0
        self.black_queens = 0
        self.create_board()
        self.selected_fig = None
        self.que = queue.Queue()  # queue koji nam sluzi za pretragu hash mape svih mogucih poteza uracunato sa skokovima
        self.valid_moves_hash = {}  # hash mapa za storovanje validnih poteza

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                if col % 2 == ((row + 1) % 2):
                    pygame.draw.rect(screen, bez, (col * square_size, row * square_size, square_size, square_size))
                else:
                    pygame.draw.rect(screen, green, (col * square_size, row * square_size, square_size, square_size))

        for row in range(8):
            for col in range(8):
                figure = self.get_figure(row, col)
                if figure is not None:
                    figure.draw_fig()
        if self.selected_fig is not None:
            for d in self.get_valid_moves(self.selected_fig):
                row, col = d["move"]
                pygame.draw.circle(screen, gray,
                                   (col * square_size + square_size // 2, row * square_size + square_size // 2), 15)

    def create_board(self):
        for row in range(8):
            self.board.append([])
            for col in range(8):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Figure(white, row, col))
                    elif row > 4:
                        self.board[row].append(Figure(black, row, col))
                    else:
                        self.board[row].append(None)
                else:
                    self.board[row].append(None)

    def get_figure(self, row, col):
        return self.board[row][col]

    # ovde moze da stoji i nereseno umesto ova poslednja dva ako nema mogucih poteza
    def winner(self):
        if self.white_figures <= 0:
            return 'black'
        elif self.black_figures <= 0:
            return 'white'
        elif not self.has_valid_moves(white):
            return 'black'
        elif not self.has_valid_moves(black):
            return 'white'
        else:
            return None

    # moguci potezi za igraca
    def has_valid_moves(self, player_color):
        for row in range(8):
            for col in range(8):
                figure = self.get_figure(row, col)
                if figure is not None and figure.color == player_color:
                    if self.get_valid_moves(figure):
                        return True
        return False

    def search_binary_tree(self, figure, row, col, visited_t, path_t, hash_map_of_av_moves):
        visited = visited_t.copy()
        path = path_t.copy()

        if figure.color == black or figure.queen:
            if row > 0 and col > 0:
                if self.get_figure(row - 1, col - 1) is None or self.get_figure(row - 1, col - 1).color == figure.color:
                    pass
                else:
                    if col > 1 and row > 1:
                        if self.get_figure(row - 2, col - 2) is None:
                            if (row - 1, col - 1) in visited:
                                pass
                            else:
                                path.append((row - 2, col - 2))
                                visited.append((row - 1, col - 1))
                                hash_map_of_av_moves.append({"move": (row - 2, col - 2), "skipped": visited.copy()})
                                call_move = figure, row - 2, col - 2, visited.copy(), path.copy(), hash_map_of_av_moves
                                self.que.put(call_move)
                                path.pop()
                                visited.pop()
            if row > 0 and col < 7:
                if self.get_figure(row - 1, col + 1) is None or self.get_figure(row - 1, col + 1).color == figure.color:
                    pass
                else:
                    if col < 6 and row > 1:
                        if (row - 1, col + 1) in visited:
                            pass
                        else:
                            if self.get_figure(row - 2, col + 2) is None:
                                path.append((row - 2, col + 2))
                                visited.append((row - 1, col + 1))
                                hash_map_of_av_moves.append({"move": (row - 2, col + 2), "skipped": visited.copy()})
                                call_move = figure, row - 2, col + 2, visited.copy(), path.copy(), hash_map_of_av_moves
                                self.que.put(call_move)
                                path.pop()
                                visited.pop()
        if figure.color == white or figure.queen:
            if row < 7 and col > 0:
                if self.get_figure(row + 1, col - 1) is None or self.get_figure(row + 1, col - 1).color == figure.color:
                    pass
                else:
                    if col > 1 and row < 6:
                        if (row + 1, col - 1) in visited:
                            pass
                        else:
                            if self.get_figure(row + 2, col - 2) is None:
                                path.append((row + 2, col - 2))
                                visited.append((row + 1, col - 1))
                                hash_map_of_av_moves.append({"move": (row + 2, col - 2), "skipped": visited.copy()})
                                call_move = figure, row + 2, col - 2, visited.copy(), path.copy(), hash_map_of_av_moves
                                self.que.put(call_move)
                                path.pop()
                                visited.pop()
            if row < 7 and col < 7:
                if self.get_figure(row + 1, col + 1) is None or self.get_figure(row + 1, col + 1).color == figure.color:
                    pass
                else:
                    if col < 6 and row < 6:
                        if (row + 1, col + 1) in visited:
                            pass
                        else:
                            if self.get_figure(row + 2, col + 2) is None:
                                path.append((row + 2, col + 2))
                                visited.append((row + 1, col + 1))
                                hash_map_of_av_moves.append({"move": (row + 2, col + 2), "skipped": visited.copy()})
                                call_move = figure, row + 2, col + 2, visited.copy(), path.copy(), hash_map_of_av_moves
                                self.que.put(call_move)
                                path.pop()
                                visited.pop()
        while self.que.qsize() > 0:
            e = self.que.get()
            figure, row, col, visited, path, hash_map_of_av_moves = e
            self.search_binary_tree(figure, row, col, visited, path, hash_map_of_av_moves)

    def get_valid_moves(self, figure):
        hash_key = (figure.row, figure.col, figure.color, figure.queen)
        if hash_key in self.valid_moves_hash:
            return self.valid_moves_hash[hash_key]

        hash_map_of_av_moves = []  # lista svih mogucih hash mapa gde je (row, col) kljuc a vrednost je lista svih skipped
        # moglo je i da to bude dictionary ali je ovako bilo lakse za implementaciju
        # jedine razlika bi bila umesto append koristili bi smo update ili extend
        # i sto ce onda kljucevi biti tuple a ne lista
        # vremenska slozenost ostaje ista
        row = figure.row
        col = figure.col
        if figure.color == black or figure.queen:
            if row > 0 and col > 0:
                if self.get_figure(row - 1, col - 1) is None:
                    hash_map_of_av_moves.append({"move": (row - 1, col - 1), "skipped": []})
            if row > 0 and col < 7:
                if self.get_figure(row - 1, col + 1) is None:
                    hash_map_of_av_moves.append({"move": (row - 1, col + 1), "skipped": []})
        if figure.color == white or figure.queen:
            if row < 7 and col > 0:
                if self.get_figure(row + 1, col - 1) is None:
                    hash_map_of_av_moves.append({"move": (row + 1, col - 1), "skipped": []})
            if row < 7 and col < 7:
                if self.get_figure(row + 1, col + 1) is None:
                    hash_map_of_av_moves.append({"move": (row + 1, col + 1), "skipped": []})

        self.search_binary_tree(figure, row, col, [], [], hash_map_of_av_moves)

        self.valid_moves_hash[hash_key] = hash_map_of_av_moves

        return hash_map_of_av_moves

    # brisemo figure iz visestrukih skokova
    def remove_skipped(self, positions):
        for pos in positions:
            row, col = pos
            pygame.draw.rect(screen, (255, 150, 20), (col * square_size, row * square_size, square_size, square_size),
                             10)
            self.board[row][col] = None
            if player_turn == white:
                self.black_figures -= 1
            else:
                self.white_figures -= 1

    def move_figure_board(self, figure, new_row, new_col):
        old_col = figure.col
        old_row = figure.row
        self.board[new_row][new_col] = self.board[old_row][old_col]
        self.board[old_row][old_col] = None
        figure.move_figure(new_row, new_col)
        if new_row == 0 or new_row == 7:
            figure.make_queen()
            if player_turn == white:
                self.white_queens += 1
            else:
                self.black_queens += 1
        self.valid_moves_hash.clear()  # Brisemo hash jer se potez desio

    def add_glowing_effect(self, player_turn):
        glow_color = (255, 165, 0)
        for row in range(8):
            for col in range(8):
                figure = self.get_figure(row, col)
                if figure is not None and figure.color == player_turn:
                    valid_moves = self.get_valid_moves(figure)
                    if len(valid_moves) > 0:
                        pygame.draw.circle(screen, glow_color,
                                           (col * square_size + square_size // 2, row * square_size + square_size // 2),
                                           28, 5)

    def add_green_glowing_effect(self):
        if self.selected_fig:
            row, col = self.selected_fig.row, self.selected_fig.col
            pygame.draw.circle(screen, (0, 255, 0),
                               (col * square_size + square_size // 2, row * square_size + square_size // 2), 35, 5)

    def select_fig(self, row, col, player_turn):
        if self.selected_fig is not None:
            hash_map_of_av_moves = self.get_valid_moves(self.selected_fig)
            i = len(hash_map_of_av_moves) - 1
            while i >= 0:
                if (row, col) == hash_map_of_av_moves[i]["move"]:
                    self.move_figure_board(self.selected_fig, row, col)
                    if len(hash_map_of_av_moves[i]["skipped"]) > 0:
                        self.remove_skipped(hash_map_of_av_moves[i]["skipped"])
                    self.selected_fig = None
                    return True
                i -= 1
            self.selected_fig = None

        if self.selected_fig is None:
            figure = self.get_figure(row, col)
            if figure is not None and figure.color == player_turn:
                self.selected_fig = figure
        return False

    # broj figura koje trenutno ne mogu biti pojedene
    def get_number_of_safe_figures(self, player_color):

        opponent_color = white if player_color == black else black

        threatened_positions = set()

        for row in range(8):
            for col in range(8):
                figure = self.get_figure(row, col)
                if figure and figure.color == opponent_color:
                    for move in self.get_valid_moves(figure):
                        if move['skipped']:
                            threatened_positions.add((move['move'][0], move['move'][1]))
                            threatened_positions.update(move['skipped'])

        safe_figures = 0
        safe_queens = 0

        for row in range(8):
            for col in range(8):
                figure = self.get_figure(row, col)
                if figure and figure.color == player_color:
                    if (row, col) not in threatened_positions:
                        if figure.queen:
                            safe_queens += 1
                        else:
                            safe_figures += 1

        return safe_figures, safe_queens

    def get_number_of_moveable_figures(self, player_color):
        moveable_figures = 0
        moveable_queens = 0
        for row in range(8):
            for col in range(8):
                figure = self.get_figure(row, col)
                if figure and figure.color == player_color:
                    moves = self.get_valid_moves(figure)
                    non_capturing_moves = [move for move in moves if not move['skipped']]
                    if non_capturing_moves:
                        if figure.queen:
                            moveable_queens += 1
                        else:
                            moveable_figures += 1

        return moveable_figures, moveable_queens

    def get_number_of_loner_figures(self, player_color):
        loner_figures = 0
        loner_queens = 0

        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for row in range(8):
            for col in range(8):
                figure = self.get_figure(row, col)
                if figure and figure.color == player_color:
                    is_loner = True

                    # proveravamo sve susede
                    for dr, dc in directions:
                        adjacent_row, adjacent_col = row + dr, col + dc

                        if 0 <= adjacent_row < 8 and 0 <= adjacent_col < 8:
                            adjacent_figure = self.get_figure(adjacent_row, adjacent_col)
                            if adjacent_figure:
                                is_loner = False
                                break

                    if is_loner:
                        if figure.queen:
                            loner_queens += 1
                        else:
                            loner_figures += 1

        return loner_figures, loner_queens

    def get_figure_stats(self, player_color):
        opponent_color = white if player_color == black else black
        threatened_positions = set()
        safe_figures, safe_queens = 0, 0
        moveable_figures, moveable_queens = 0, 0
        loner_figures, loner_queens = 0, 0
        total_captures = 0
        total_queen_captures = 0  # Dodajemo promenljivu za hvatanje kraljica
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        promotion_row_black = 0
        promotion_row_white = 7
        unoccupied_promotion_black, unoccupied_promotion_white = 0, 0

        for row in range(8):
            for col in range(8):
                figure = self.get_figure(row, col)
                if figure and figure.color == opponent_color:
                    for move in self.get_valid_moves(figure):
                        if move['skipped']:
                            threatened_positions.add((move['move'][0], move['move'][1]))
                            threatened_positions.update(move['skipped'])

        for row in range(8):
            for col in range(8):
                figure = self.get_figure(row, col)
                if figure and figure.color == player_color:
                    # da li je figurica sigurna
                    if (row, col) not in threatened_positions:
                        if figure.queen:
                            safe_queens += 1
                        else:
                            safe_figures += 1

                    # da li je figurica movable (bez uzimanja)
                    moves = self.get_valid_moves(figure)
                    non_capturing_moves = []
                    for move in moves:
                        if move['skipped']:
                            for skipped_pos in move['skipped']:
                                skipped_figure = self.get_figure(skipped_pos[0], skipped_pos[1])
                                if skipped_figure.queen:
                                    total_queen_captures += 1
                                else:
                                    total_captures += 1
                        else:
                            non_capturing_moves.append(move)

                    if non_capturing_moves:
                        if figure.queen:
                            moveable_queens += 1
                        else:
                            moveable_figures += 1

                    # da li je figurica loner
                    is_loner = True
                    for dr, dc in directions:
                        adjacent_row, adjacent_col = row + dr, col + dc
                        if 0 <= adjacent_row < 8 and 0 <= adjacent_col < 8:
                            adjacent_figure = self.get_figure(adjacent_row, adjacent_col)
                            if adjacent_figure:
                                is_loner = False
                                break
                    if is_loner:
                        if figure.queen:
                            loner_queens += 1
                        else:
                            loner_figures += 1

        defender_figures, defender_queens = self.get_number_of_defender_figures(player_color)
        centrally_positioned_figures, centrally_positioned_queens = self.get_number_of_centrally_positioned_figures(
            player_color)

        return {
            "safe_figures": safe_figures,
            "safe_queens": safe_queens,
            "moveable_figures": moveable_figures,
            "moveable_queens": moveable_queens,
            "loner_figures": loner_figures,
            "loner_queens": loner_queens,
            "unoccupied_promotion_black": unoccupied_promotion_black,
            "unoccupied_promotion_white": unoccupied_promotion_white,
            "total_captures": total_captures,
            "total_queen_captures": total_queen_captures,
            "defender_figures": defender_figures,
            "defender_queens": defender_queens,
            "centrally_positioned_figures": centrally_positioned_figures,
            "centrally_positioned_queens": centrally_positioned_queens
        }

    # broj slobodnih polja na liniji promocije
    def get_number_of_unoccupied_fields_on_promotion_line(self):
        promotion_row_black = 0  # crni promovise na redu 0
        promotion_row_white = 7  # beli promovise na redu 0
        unoccupied_promotion_black = 0
        unoccupied_promotion_white = 0

        # Gledamo promociju za crnog
        for col in range(8):
            if self.board[promotion_row_black][col] is None:
                unoccupied_promotion_black += 1

        # Gledamo promociju za belog
        for col in range(8):
            if self.board[promotion_row_white][col] is None:
                unoccupied_promotion_white += 1

        return unoccupied_promotion_black, unoccupied_promotion_white

    # broj figura koje se nalaze u dva najniza reda
    def get_number_of_defender_figures(self, player_color):
        defender_figures = 0
        defender_queens = 0

        # Skorz donja 2 reda predstavljaju odbranu
        if player_color == white:
            rows_to_check = [0, 1]
        else:
            rows_to_check = [6, 7]

        for row in rows_to_check:
            for col in range(8):
                figure = self.get_figure(row, col)
                if figure is not None and figure.color == player_color:
                    if figure.queen:
                        defender_queens += 1
                    else:
                        defender_figures += 1

        return defender_figures, defender_queens

    # broj figurica koje su smestene na osam centralnih polja
    def get_number_of_centrally_positioned_figures(self, player_color):
        central_positions = [(3, 2), (3, 3), (3, 4), (4, 2), (4, 3), (4, 4)]
        centrally_positioned_figures = 0
        centrally_positioned_queens = 0

        for row, col in central_positions:
            figure = self.get_figure(row, col)
            if figure is not None and figure.color == player_color:
                if figure.queen:
                    centrally_positioned_queens += 1
                else:
                    centrally_positioned_figures += 1

        return centrally_positioned_figures, centrally_positioned_queens

    def evaluate_board(self, figure_stats):
        score = 0

        score += (figure_stats['safe_figures'] * 1.3)
        score += (figure_stats['safe_queens'] * 3.3)
        score += (figure_stats['moveable_figures'] * 1.15)
        score += (figure_stats['moveable_queens'] * 3.15)
        score += (figure_stats['loner_figures'] * -1.5)
        score += (figure_stats['loner_queens'] * -3.5)
        score += (figure_stats['defender_figures'] * 1.35)
        score += (figure_stats['defender_queens'] * 3.35)
        score += (figure_stats['centrally_positioned_figures'] * 1.25)
        score += (figure_stats['centrally_positioned_queens'] * 3.25)

        score += (figure_stats['total_captures'] * 27.5)
        score += (figure_stats['total_queen_captures'] * 33.5)

        if player_turn == white:
            score += (figure_stats[
                          'unoccupied_promotion_white'] * 0.5)
            score -= (figure_stats[
                          'unoccupied_promotion_black'] * 0.5)
        else:
            score += (figure_stats['unoccupied_promotion_black'] * 0.5)
            score -= (figure_stats['unoccupied_promotion_white'] * 0.5)

        return score

    def apply_best_move(self, move):
        figure = self.get_figure(move["figure_row"], move["figure_col"])
        if figure is None:
            raise ValueError("Figure not found at the specified location.")
        self.move_figure_board(figure, move["move"][0], move["move"][1])
        if "skipped" in move:
            self.remove_skipped(move["skipped"])

    def clone(self):
        new_board = Board()
        new_board.board = [[self.clone_figure(fig) for fig in row] for row in self.board]
        new_board.white_figures = self.white_figures
        new_board.black_figures = self.black_figures
        new_board.white_queens = self.white_queens
        new_board.black_queens = self.black_queens
        return new_board

    def clone_figure(self, figure):
        if figure is None:
            return None
        new_figure = Figure(figure.color, figure.row, figure.col)
        new_figure.queen = figure.queen
        return new_figure


class GameState:
    def __init__(self, board, move=None, depth=0, score=0):
        self.board = board
        self.move = move
        self.depth = depth
        self.score = score
        self.children = []

    # pravljenje stabla igre
    def generate_children(self, maximizingPlayer):
        player_color = white if maximizingPlayer else black
        for row in range(8):
            for col in range(8):
                figure = self.board.get_figure(row, col)
                if figure is not None and figure.color == player_color:
                    valid_moves = self.board.get_valid_moves(figure)
                    # sortiramo poteze tako da prilikom pretrage forsiramo visetruko izmanje koje je uvek bolje
                    valid_moves.sort(key=lambda x: len(x['skipped']), reverse=True)

                    for move in valid_moves:
                        new_board = self.board.clone()
                        new_figure = new_board.get_figure(figure.row, figure.col)
                        new_board.move_figure_board(new_figure, move["move"][0], move["move"][1])
                        if move["skipped"]:
                            new_board.remove_skipped(move["skipped"])
                        child = GameState(new_board, {
                            "figure_row": figure.row,
                            "figure_col": figure.col,
                            "move": move["move"],
                            "skipped": move.get("skipped", [])
                        }, self.depth + 1)
                        self.children.append(child)
                        if self.depth < max_depth:
                            child.generate_children(not maximizingPlayer)

    # evaluacija stanja, + score je pogotdnost za belog, - score je pogodnost za crnog
    def evaluate(self):

        white_stats = self.board.get_figure_stats(white)
        black_stats = self.board.get_figure_stats(black)

        white_score = self.board.evaluate_board(white_stats)
        black_score = self.board.evaluate_board(black_stats)

        self.score = white_score - black_score


# minimax algoritam za alpha beta rezovima koji ima tajmer sa secenje (ako udjemo u veliku dubinu)
def minimax_with_timeout(node, depth, alpha, beta, maximizingPlayer, start_time, time_limit=3.0):
    if time.time() - start_time > time_limit:
        # ako nekim slucajem odemo preko vremena, prekidamo pretragu i vracamo trenutni score (score koji je u trenutnom vremenskom pronalazenju najbolji)
        raise TimeoutError("Minimax search timed out")
    if depth == 0 or node.board.winner() is not None:
        node.evaluate()
        return node.score

    if maximizingPlayer:
        maxEval = float('-inf')
        for child in node.children:
            eval = minimax_with_timeout(child, depth - 1, alpha, beta, False, start_time, time_limit)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        node.score = maxEval
        return maxEval
    else:
        minEval = float('inf')
        for child in node.children:
            eval = minimax_with_timeout(child, depth - 1, alpha, beta, True, start_time, time_limit)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        node.score = minEval
        return minEval


# animacija za potez figure (Napomena: kod visetrukog uzimanja on ide direktno na polje koje mu je najbolje, animacija ne ide cik - cak nego ide pravolinijski)
# iz razloga sto bi to dosta usporilo vreme, jer bi morali svako dijagonalno polje od skipped da postavimo figuru
# i da je uklonimo sa prethodnog polja (sto pogorsava vreme) koje je trenutno prioriet
# a i nije bio funkcionalni zahtev u samom projektu
def animate_move(board, figure, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    steps = 20
    for step in range(steps + 1):
        row = start_row + (end_row - start_row) * step / steps
        col = start_col + (end_col - start_col) * step / steps
        board.draw_board()
        pygame.draw.circle(screen, figure.color,
                           (int(col * square_size + square_size // 2), int(row * square_size + square_size // 2)), 30)
        pygame.display.flip()
        time.sleep(0.02)


def change_player_turn(player_turn):
    return black if player_turn == white else white


def display_depth(depth):
    text_surface = font.render(f"Depth: {depth}", True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))


# odlucivanje koju dubinu pretrage koristiti
# varijabilna dubina
def get_search_depth(board):
    all_moves = []
    capture_moves = []

    for row in range(8):
        for col in range(8):
            figure = board.get_figure(row, col)
            if figure and figure.color == white:
                valid_moves = board.get_valid_moves(figure)
                all_moves.extend(valid_moves)
                capture_moves.extend([m for m in valid_moves if m['skipped']])

    total_moves = len(all_moves)
    total_captures = len(capture_moves)

    if total_captures > 0:
        return 5 if total_captures > 3 else 4
    elif total_moves > 30:
        return 3
    elif total_moves > 15:
        return 4
    elif total_moves > 8:
        return 4
    elif total_moves < 4:
        return 5
    else:
        return 3

def handle_timeout(best_move):
    if best_move:
        print("Applying best move found before timeout:", best_move)
        board.apply_best_move(best_move)
    else:
        print("No valid move found before timeout.")

def read_hash_map_from_file(file_name):
    if not os.path.exists(file_name):
        return {}

    try:
        with open(file_name, 'r') as file:
            data = file.read().strip()
            if not data:
                return {}
            return json.loads(data)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def write_hash_map_to_file(file_name, hash_map):
    with open(file_name, 'w') as file:
        json.dump(hash_map, file)

def generate_board_string(board):
    board_string = ""
    for row in board.board:
        for figure in row:
            if figure is None:
                board_string += "0"
            elif figure.color == white:
                board_string += "W" if figure.queen else "w"
            else:
                board_string += "B" if figure.queen else "b"
    return board_string


# inicijalizacija igre
board = Board()
depth_levels = [3, 4, 5]
depth_index = 0
depth = depth_levels[depth_index]
max_depth = depth

player_turn = black
start = True

# ucitavanje hash mape iz fajla
hash_map_file = "evaluations.txt"
evaluations_hash_map = read_hash_map_from_file(hash_map_file)

# glavna petlja -> igra
while start:
    board.draw_board()
    board.add_glowing_effect(player_turn)
    board.add_green_glowing_effect()
    display_depth(depth)

    winner = board.winner()
    if winner:
        print(f"The winner is: {winner}")
        break

    if player_turn == white:  # kompjuter igra belog
        print("Computer's turn.")
        depth = get_search_depth(board)
        start_time = time.time()

        root = GameState(board.clone())
        board_string = generate_board_string(board)
        best_move = None

        if board_string in evaluations_hash_map:
            best_move = evaluations_hash_map[board_string]
            print("Using hash map for best move.")
            figure = board.get_figure(best_move["figure_row"], best_move["figure_col"])
            start_pos = (figure.row, figure.col)
            end_pos = best_move["move"]
            animate_move(board, figure, start_pos, end_pos)
            board.apply_best_move(best_move)
            player_turn = change_player_turn(player_turn)
        else:
            root.generate_children(True)

            best_score = minimax_with_timeout(root, depth, float('-inf'), float('inf'), True, start_time)
            turn_duration = time.time() - start_time
            for child in root.children:
                if child.score == best_score:
                    best_move = child.move
                    break

            if best_move:
                figure = board.get_figure(best_move["figure_row"], best_move["figure_col"])
                start_pos = (figure.row, figure.col)
                end_pos = best_move["move"]

                # pusti animaciju za potez / kod unakrsnog skoka je malo konfuzna
                animate_move(board, figure, start_pos, end_pos)

                # odigraj najbolji potez
                board.apply_best_move(best_move)
                player_turn = change_player_turn(player_turn)
                print("Move applied successfully:", best_move)
                print(f"Turn duration: {turn_duration:.3f} seconds")

                evaluations_hash_map[board_string] = best_move
                write_hash_map_to_file(hash_map_file, evaluations_hash_map)
                print("Best move saved to hash map.")

            else:
                print("No valid move was selected.")



    else:  # moj potez (covek)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                row = y // square_size
                col = x // square_size
                move_success = board.select_fig(row, col, player_turn)
                if move_success:
                    player_turn = change_player_turn(player_turn)
                    print("Player move successful.")

    clock.tick(fps)
    pygame.display.flip()

'''
hash implementacija za validne poteze:
- dodali smo hahs mapu koja čuva već izračunate validne poteze za svaku figuru. Kada se sledeći put zatraži validan potez za istu figuru na istoj poziciji, rezultati se jednostavno uzimaju iz keša umesto da se ponovo računaju
- svaki put kada se figura pomeri svi potezi figure moraju ponovo da se racunaju sto moze biti sporo i skupo vremenski
- zbog toga se hash brise samo kada se figura pomeri, to znaci da ce validni potezi biti ponovo izracunati samo kada je to zaista potrebno, smanjujemo broj nepotrebnih racunanja i ubrzava se odlucivanje tokom gameplay-a
...
'''