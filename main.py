

    @property
    def grid(self):
        # Properti untuk mendapatkan grid papan
        return self._grid

    def draw(self, screen):
        # Menggambar papan dan simbol pada layar
        for i in range(1, 3):
            pygame.draw.line(screen, self.line_color, (0, i * self.cell_size), (600, i * self.cell_size), 5)
            pygame.draw.line(screen, self.line_color, (i * self.cell_size, 0), (i * self.cell_size, 600), 5)

        for row in range(3):
            for col in range(3):
                if self._grid[row][col] != "":
                    # Menampilkan simbol 'X' atau 'O' dengan warna sesuai
                    color = (0, 128, 255) if self._grid[row][col] == "X" else (255, 0, 0)
                    text = self.font.render(self._grid[row][col], True, color)
                    screen.blit(text, (col * self.cell_size + 70, row * self.cell_size + 50))

    def mark_cell(self, row, col, player_symbol):
        # Tandai sel jika kosong dan kembalikan status
        if self._grid[row][col] == "":
            self._grid[row][col] = player_symbol
            return True
        return False

    def check_winner(self):
        # Periksa apakah ada pemenang berdasarkan baris, kolom, atau diagonal
        for row in self._grid:
            if row[0] == row[1] == row[2] != "":
                return row[0]
        for col in range(3):
            if self._grid[0][col] == self._grid[1][col] == self._grid[2][col] != "":
                return self._grid[0][col]
        if self._grid[0][0] == self._grid[1][1] == self._grid[2][2] != "":
            return self._grid[0][0]
        if self._grid[0][2] == self._grid[1][1] == self._grid[2][0] != "":
            return self._grid[0][2]
        return None

    def is_full(self):
        # Periksa apakah papan penuh (tidak ada sel kosong)
        return all(cell != "" for row in self._grid for cell in row)


# Kelas utama untuk mengelola permainan Tic Tac Toe
class Game:
    def __init__(self):
        # Inisialisasi game, termasuk tampilan, papan, dan pemain
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Tic Tac Blitz")
        self.board = Board()
        self.players = [Player("X"), AI("O")]
        self.current_player = 0
        self.running = True
        self.font = pygame.font.Font(None, 50)
        self.mode = None
        self.bg_color = (240, 240, 255)

        self.show_menu()  # Tampilkan menu utama

    def show_menu(self):
        # Menampilkan menu utama untuk memilih mode permainan
        while True:
            self.screen.fill(self.bg_color)
            title = self.font.render("Tic Tac Blitz", True, (0, 0, 255))
            self.screen.blit(title, (150, 50))

            mouse_pos = pygame.mouse.get_pos()

            # Efek hover pada tombol menu
            pvp_color = (200, 0, 0) if 150 <= mouse_pos[1] <= 200 else (0, 0, 0)
            pve_color = (200, 0, 0) if 250 <= mouse_pos[1] <= 300 else (0, 0, 0)
            exit_color = (200, 0, 0) if 350 <= mouse_pos[1] <= 400 else (0, 0, 0)

            pvp_button = self.font.render("1. Player vs Player", True, pvp_color)
            pve_button = self.font.render("2. Player vs AI", True, pve_color)
            exit_button = self.font.render("3. Exit", True, exit_color)

            self.screen.blit(pvp_button, (150, 150))
            self.screen.blit(pve_button, (150, 250))
            self.screen.blit(exit_button, (150, 350))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if 150 <= pos[1] <= 200:
                        self.mode = 'PVP'
                        return
                    elif 250 <= pos[1] <= 300:
                        self.mode = 'PVE'
                        return
                    elif 350 <= pos[1] <= 400:
                        pygame.quit()
                        sys.exit()

    def handle_click(self, pos):
        # Tangani klik pada papan permainan
        row = pos[1] // self.board.cell_size
        col = pos[0] // self.board.cell_size
        if self.board.mark_cell(row, col, self.players[self.current_player].symbol):
            winner = self.board.check_winner()
            if winner:
                self.display_message(f"Player {winner} wins!")
                self.running = False
            elif self.board.is_full():
                self.display_message("It's a Draw!")
                self.running = False
            self.current_player = 1 - self.current_player

    def display_message(self, message):
        # Tampilkan pesan akhir permainan (menang atau seri)
        text = self.font.render(message, True, (255, 0, 0))
        self.screen.fill((255, 255, 255))
        self.screen.blit(text, (150, 250))
        pygame.display.flip()
        pygame.time.wait(2000)
        self.reset_game()

    def reset_game(self):
        # Reset papan permainan untuk memulai permainan baru
        self.board = Board()
        self.current_player = 0
        self.running = True

    def run(self):
        # Jalankan loop utama permainan
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.mode == 'PVP':
                    self.handle_click(pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEBUTTONDOWN and self.mode == 'PVE':
                    self.handle_click(pygame.mouse.get_pos())
                    if self.current_player == 1:  # AI's turn
                        self.players[1].make_move(self.board)
                        winner = self.board.check_winner()
                        if winner:
                            self.display_message(f"Player {winner} wins!")
                            self.running = False
                        elif self.board.is_full():
                            self.display_message("It's a Draw!")
                            self.running = False
                        self.current_player = 0

            self.screen.fill(self.bg_color)
            self.board.draw(self.screen)
            pygame.display.flip()


if __name__ == "__main__":
    # Mulai permainan
    game = Game()
    game.run()
