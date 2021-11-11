from Board import Field
from Const import Const


class TUIController:
    def __init__(self, board):
        self.board = board

    # for translation of the move notation
    def letter(self,col):
        return chr(97+col)
    def digit(self,col):
        return ord(col)-97

    def print_board(self):
        moves_counter, possible_moves = self.board.count_moves()
        captures_counter, possible_captures = self.board.count_captures()
        print(f"\nMove: {'white' if self.board.get_turn() else 'black'}")
        print(f"Legal moves: {moves_counter}")
        if possible_moves:
            for move in possible_moves:
                start_row,start_col,end_row,end_col = move
                print(f"{self.letter(start_col)}{start_row+1}->{self.letter(end_col)}{end_row+1}", end=" ")
            print()
        print(f"Legal captures: {captures_counter}")
        if possible_captures:
            for capture in possible_captures:
                start_row,start_col,end_row,end_col = capture
                print(f"{self.letter(start_col)}{start_row+1}->{self.letter(end_col)}{end_row+1}", end=" ")
            print()
        print(f"Moves until draw: {self.board.get_draw()}/{Const.DRAW+1}")
        translation = {Field.white : "w",
                       Field.white_king : "W",
                       Field.black : "b",
                       Field.black_king : "B",
                       Field.empty : "_",
                       Field.out_of_play : "_"}
        print(f"  {''.join([f' {chr(i)} ' for i in range(ord('a'),ord('h')+1)])}")
        for index,row in enumerate(reversed(self.board.get_board())):
            print(f"{Const.ROW-index} {''.join([f'[{translation[Field[square.name]]}]' for square in row])} {Const.ROW-index}")

        print(f"  {''.join([f' {chr(i)} ' for i in range(ord('a'),ord('h')+1)])}")

    def play(self):
        running = True
        while running:
            self.print_board()
            print("Input moves as a combination of letter and digit, e.g. a3 or f4.")
            start = input("Start: ")
            if len(start)==2 and start[0] in "abcdefgh" and start[1] in "12345678":
                start_row = int(start[1])-1
                start_col = self.digit((start[0]))
            else:
                input("Wrong syntax. Press ENTER to continue...")
                continue

            if self.board.can_capture():
                status, message = self.board.can_capture(start_row,start_col)
                if status:
                    print("Possible destinations:")
                    for destination in message:
                        row, col = destination
                        print(f"{self.letter(col)}{row+1}", end=" ")
                    print()
                else:
                    input(f"{message} Press ENTER to continue...")
                    continue
            if self.board.can_move():
                status, message = self.board.can_move(start_row, start_col)
                if status:
                    print("Possible destinations:")
                    for destination in message:
                        row, col = destination
                        print(f"{self.letter(col)}{row+1}", end=" ")
                    print()
                else:
                    input(f"{message} Press ENTER to continue...")
                    continue
            end = input("End: ")
            if len(end)==2 and end[0] in "abcdefgh" and end[1] in "12345678":      
                end_row = int(end[1])-1
                end_col = self.digit((end[0]))
            else:
                input("Wrong syntax. Press ENTER to continue...")
                continue

            if not self.board.move(start_row,start_col,end_row,end_col):
                input("This move isn't legal. Press ENTER to continue...")
                continue
            if self.board.is_end():
                print(f"End of the game. {'Black' if self.board.get_turn() else 'White'} won!")
                running = False

