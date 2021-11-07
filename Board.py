from enum import Enum

# constants
ROW = 8
COL = 8
DRAW = 39

class Field(Enum):
    white = 1
    white_king = 2
    black = 3
    black_king = 4
    empty = 0
    out_of_play = -1

class Board:
    __board = [[Field.empty for _ in range(8)] for _ in range(8)] # [row][col]
    __white_turn = True # move indicator
    __draw = 0 # draw indicator
    def __init__(self):
        self.__board = [[Field.empty for _ in range(8)] for _ in range(8)] # [row][col]
        self.__board[0][1::2] = [Field.black]*4
        self.__board[1][0::2] = [Field.black]*4
        self.__board[2][1::2] = [Field.black]*4
        self.__board[5][0::2] = [Field.white]*4
        self.__board[6][1::2] = [Field.white]*4
        self.__board[7][0::2] = [Field.white]*4

    def print_board(self):
        moves_counter, possible_moves = self.count_all_moves()
        captures_counter, possible_captures = self.count_all_captures()
        print(f"\nMove: {'white' if self.__white_turn else 'black'}")
        print(f"Legal moves: {moves_counter}")
        if possible_moves:
            print(", ".join(possible_moves))
        print(f"Legal captures: {captures_counter}")
        if possible_captures:
            print(", ".join(possible_captures))
        print(f"Moves until draw: {self.__draw}/{DRAW+1}")
        translation = {Field.white : "w",
                       Field.white_king : "W",
                       Field.black : "b",
                       Field.black_king : "B",
                       Field.empty : "_",
                       Field.out_of_play : " "}
        print(f"  {''.join([f' {i} ' for i in range(8)])}")
        for index,row in enumerate(self.__board):
            print(f"{index} {''.join([f'[{translation[square]}]' for square in row])}")
 
    def set_square(self,row,col,ch):
        self.__board[row][col] = ch

    
    def change_move(self):
        self.__white_turn = not self.__white_turn
    def add_to_draw(self):
        self.__draw += 1

    def get_board(self):
        return self.__board

    def get_square(self, row, col):
        if row < 0 or row > 7 or col < 0 or col > 7:
            return Field.out_of_play
        if not (row+col)%2:
            return Field.empty
        return self.__board[row][col]

    def get_draw(self):
        return self.__draw

    def get_white_move(self):
        return self.__white_turn 

    def is_enemy(self, row, col):
        if self.__white_turn:
            return self.get_square(row,col) in [Field.black, Field.black_king]
        else:
            return self.get_square(row,col) in [Field.white, Field.white_king]

    def is_friend(self, row, col):
        if self.__white_turn:
            return self.get_square(row,col) in [Field.white, Field.white_king]
        else:
            return self.get_square(row,col) in [Field.black, Field.black_king]

    def direction(self):
        return -1 if self.__white_turn else 1

    def can_capture_any(self):
        for row in range(ROW):
            for col in range(COL):
                if self.can_capture(row,col)[0]:
                    return True
        return False

    def can_capture(self, row, col):
        if not self.is_friend(row,col):
            return [False, "You can't capture with this piece."]
        
        possible_captures = []
        square = self.get_square(row,col)
        if square in [Field.white, Field.black]:
            for i in [-1,1]:
                if self.legal_capture(row, col, row+2*self.direction(), col+2*i):
                    possible_captures.append(f"{row+2*self.direction()}{col+2*i}")

        if square in [Field.white_king, Field.black_king]:
            for i in [-1,1]:
                for j in [-1,1]:
                    if self.legal_capture(row, col, row+2*i, col+2*j):
                        possible_captures.append(f"{row+2*i}{col+2*j}")
        if possible_captures:
            return [True, possible_captures]
        return [False, "You can't capture with this piece."]


    def legal_capture(self, start_row, start_col, end_row, end_col):
        if abs(end_col-start_col) != 2:
            return False
        
        start_square = self.get_square(start_row,start_col)
        end_square = self.get_square(end_row,end_col)
        row_between = (start_row+end_row)//2
        col_between = (start_col+end_col)//2
        if start_square in [Field.white, Field.black]:
            return end_square == Field.empty and end_row-start_row == 2*self.direction() and self.is_enemy(row_between,col_between)

        if start_square in [Field.white_king, Field.black_king]:
            return end_square == Field.empty and abs(end_row-start_row) == 2 and self.is_enemy(row_between,col_between)

    def can_move_any(self):
        for row in range(ROW):
            for col in range(COL):
                if self.can_move(row,col)[0]:
                    return True
        return False                


    def can_move(self,row,col):
        if not self.is_friend(row,col):
            return [False, "You can't move this piece."]
        possible_moves = []
        square = self.get_square(row,col)
        if square in [Field.white, Field.black]:
            for i in [-1,1]:
                if self.legal_move(row,col,row+self.direction(),col+i):
                    possible_moves.append(f"{row+self.direction()}{col+i}")
        
        if square in [Field.white_king, Field.black_king]:
            for i in [-1,1]:
                for j in [-1,1]:
                    if self.legal_move(row,col,row+i,col+j):
                        possible_moves.append(f"{row+i}{col+j}")
        if possible_moves:
            return [True, possible_moves]
        return [False, "You can't move this piece."]
    
    def legal_move(self,start_row,start_col,end_row,end_col):
        if self.can_capture_any():
            return False
        if abs(end_col-start_col) != 1:
            return False
        if self.can_capture(start_row,start_col)[0]:
            return False
        
        start_square = self.get_square(start_row,start_col)
        end_square = self.get_square(end_row,end_col)
        if start_square in [Field.white, Field.black]:
            return end_square == Field.empty and end_row-start_row == self.direction()
        if start_square in [Field.white_king, Field.black_king]:
            return end_square == Field.empty and abs(end_row-start_row) == 1
        return False    

    def count_all_captures(self):
        counter = 0
        all_captures = []
        if self.__white_turn:
            for row in range(ROW):
                for col in range(COL):
                    if self.get_square(row,col) in [Field.white, Field.white_king]:
                        to_counter, to_all_captures = self.count_captures(row,col)
                        counter += to_counter
                        all_captures += to_all_captures
        else:
            for row in range(ROW):
                for col in range(COL):
                    if self.get_square(row,col) in [Field.black, Field.black_king]:
                        to_counter, to_all_captures = self.count_captures(row,col)
                        counter += to_counter
                        all_captures += to_all_captures
        return counter, all_captures

    def count_captures(self, row, col):
        counter = 0
        all_captures = []
        square = self.get_square(row,col)

        if square in [Field.white, Field.black]:
            for i in [-1,1]:
                if self.legal_capture(row,col,row+2*self.direction(),col+2*i):
                    counter += 1
                    all_captures.append(f"{row}{col}->{row+2*self.direction()}{col+2*i}")
        if square in [Field.white_king, Field.black_king]:
            for i in [-1,1]:
                for j in [-1,1]:
                    if self.legal_capture(row,col,row+2*i,col+2*j):
                        counter += 1
                        all_captures.append(f"{row}{col}->{row+2*i}{col+2*j}")
        return counter, all_captures

    def count_all_moves(self):
        counter = 0
        all_moves = []
        if self.can_capture_any():
            return counter, all_moves
        if self.__white_turn:
            for row in range(ROW):
                for col in range(COL):
                    if self.get_square(row,col) in [Field.white, Field.white_king]:
                        to_counter, to_all_moves = self.count_moves(row,col)
                        counter += to_counter
                        all_moves += to_all_moves

        else:
            for row in range(ROW):
                for col in range(COL):
                    if self.get_square(row,col) in [Field.black, Field.black_king]:
                        to_counter, to_all_moves = self.count_moves(row,col)
                        counter += to_counter
                        all_moves += to_all_moves
        return counter, all_moves

    def count_moves(self,row,col):
        counter = 0
        all_moves = []
        square = self.get_square(row,col)

        if square in [Field.white, Field.black]:
            for i in [-1,1]:
                if self.legal_move(row,col,row+self.direction(),col+i):
                    counter += 1
                    all_moves.append(f"{row}{col}->{row+self.direction()}{col+i}")
        if square in [Field.white_king, Field.black_king]:
            for i in [-1,1]:
                for j in [-1,1]:
                    if self.legal_move(row,col,row+i,col+j):
                        counter +=1
                        all_moves.append(f"{row}{col}->{row+i}{col+j}")
        return counter, all_moves

    def promotion(self):
        self.__board[0][:] = [Field.white_king if piece == Field.white else piece for piece in self.__board[0][:]]
        self.__board[7][:] = [Field.black_king if piece == Field.black else piece for piece in self.__board[7][:]]



    def move(self, start_row,start_col,end_row,end_col):
        start_square = self.get_square(start_row,start_col)

        if self.get_square(start_row,start_col) in [Field.white, Field.black, Field.white_king, Field.black_king]:
            if self.legal_capture(start_row,start_col,end_row,end_col):
                self.set_square(start_row,start_col,Field.empty)
                self.set_square((start_row+end_row)//2,(start_col+end_col)//2,Field.empty)
                self.set_square(end_row,end_col,start_square)

                if not self.can_capture(end_row,end_col)[0]:
                    self.change_move()
            elif self.legal_move(start_row,start_col,end_row,end_col):
                self.set_square(start_row,start_col,Field.empty)
                self.set_square(end_row,end_col,start_square)

                self.change_move()
                self.add_to_draw()
            else:
                return False
        else:
            return False
        self.promotion()
        return True

    def play(self):
        running = True
        while running:
            self.print_board()
            print("Input moves as a one two digit number that consist of row and column, respectively.")
            start = (input("Start: "))
            start_row = int(start[0])
            start_col = int(start[1])

            if self.can_capture_any():
                status, message = self.can_capture(start_row,start_col)
                if status:
                    print(f"Possible destinations: {', '.join(message)}")
                else:
                    input(f"{message} Press ENTER to continue...")
                    continue
            if self.can_move_any():
                status, message = self.can_move(start_row, start_col)
                if status:
                    print(f"Possible destinations: {', '.join(message)}")
                else:
                    input(f"{message} Press ENTER to continue...")
                    continue
            end = (input("End: "))
            end_row = int(end[0])
            end_col = int(end[1])
            if not self.move(start_row,start_col,end_row,end_col):
                input("This move isn't legal. Press ENTER to continue...")
            if self.is_end():
                print("End of the game.")
                running = False

    def is_draw(self):
        return self.__draw > DRAW

    def is_end(self):
        if self.is_draw():
            return True
        if self.can_move_any() or self.can_capture_any():
            return False
        return True

if __name__ == "__main__":
    b1 = Board()
    b1.play()




