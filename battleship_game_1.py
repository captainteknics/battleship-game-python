import random

class EnhancedBattleshipGame:
    def __init__(self, grid_size=10):
        # Initialize the game with a default grid size of 10x10
        self.grid_size = grid_size
        # Create grids for the player and the computer, filled with '-' indicating empty space
        self.player_grid = [['-' for _ in range(grid_size)] for _ in range(grid_size)]
        self.computer_grid = [['-' for _ in range(grid_size)] for _ in range(grid_size)]
        # Grid to keep track of player's guesses
        self.player_guesses = [['-' for _ in range(grid_size)] for _ in range(grid_size)]
        # Predefined ship sizes
        self.ship_sizes = [5, 4, 3, 3, 2]

    def print_grid(self, grid):
        # Print the current state of a grid
        for row in grid:
            print(' '.join(row))
        print()

    def place_ships_randomly(self, grid):
        # Place ships randomly on the specified grid
        for ship_size in self.ship_sizes:
            placed = False
            while not placed:
                orientation = random.choice(['H', 'V'])  # Choose horizontal or vertical orientation
                row, col = self.random_ship_position(ship_size, orientation)
                if self.check_free_space(grid, row, col, ship_size, orientation):
                    self.place_ship(grid, row, col, ship_size, orientation)
                    placed = True

    def random_ship_position(self, ship_size, orientation):
        # Generate a random position for the ship
        if orientation == 'H':
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - ship_size)
        else:
            row = random.randint(0, self.grid_size - ship_size)
            col = random.randint(0, self.grid_size - 1)
        return row, col

    def check_free_space(self, grid, row, col, ship_size, orientation):
        # Check if there is enough free space to place the ship
        if orientation == 'H':
            return all(grid[row][col+i] == '-' for i in range(ship_size))
        else:
            return all(grid[row+i][col] == '-' for i in range(ship_size))

    def place_ship(self, grid, row, col, ship_size, orientation):
        # Place the ship on the grid
        if orientation == 'H':
            for i in range(ship_size):
                grid[row][col+i] = 'S'
        else:
            for i in range(ship_size):
                grid[row+i][col] = 'S'

    def player_turn(self):
        # Handle the player's turn
        valid_guess = False
        while not valid_guess:
            try:
                guess = input("Enter your guess (e.g., '5,3'): ")
                row, col = map(int, guess.split(','))  # Convert input into row and column
                if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
                    if self.player_guesses[row][col] == '-':
                        valid_guess = True
                        self.check_hit_or_miss(row, col, self.computer_grid, self.player_guesses)
                    else:
                        print("You've already guessed that location.")
                else:
                    print("Invalid coordinates. Please guess within the grid.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter coordinates like 'row,col'.")

    def computer_turn(self):
        # Handle the computer's turn
        row, col = self.random_ship_position(1, 'H')
        while self.player_grid[row][col] != '-':
            row, col = self.random_ship_position(1, 'H')
        self.check_hit_or_miss(row, col, self.player_grid, self.computer_grid)

    def check_hit_or_miss(self, row, col, target_grid, guess_grid):
        # Check if the guess is a hit or a miss
        if target_grid[row][col] == 'S':
            print("Hit!")
            guess_grid[row][col] = 'X'  # Mark hit with 'X'
        else:
            print("Miss.")
            guess_grid[row][col] = 'O'  # Mark miss with 'O'

    def check_game_over(self, grid):
        # Check if the game is over (i.e., all ships are sunk)
        for row in grid:
            if 'S' in row:
                return False
        return True

    def start_game(self):
        # Start the game
        print("Welcome to Battleship!")
        self.place_ships_randomly(self.computer_grid)
        self.place_ships_randomly(self.player_grid)

        game_over = False
        while not game_over:
            print("\nYour guesses:")
            self.print_grid(self.player_guesses)

            print("Your turn:")
            self.player_turn()

            if self.check_game_over(self.computer_grid):
                print("Congratulations! You've sunk all the computer's ships!")
                break

            print("Computer's turn:")
            self.computer_turn()

            if self.check_game_over(self.player_grid):
                print("Game over! The computer has sunk all your ships!")
                break

# Create and start the game
game = EnhancedBattleshipGame()
game.start_game()
