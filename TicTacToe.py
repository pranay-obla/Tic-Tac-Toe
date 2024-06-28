from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

class TicTacToeApp(App):
    def build(self):
        self.current_player = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.scores = {'X': 0, 'O': 0}

        main_layout = BoxLayout(orientation='vertical')
        self.info_label = Label(text=f"Player {self.current_player}'s turn", font_size=32, size_hint=(1, 0.1))
        main_layout.add_widget(self.info_label)

        self.grid = GridLayout(cols=3)
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                button = Button(font_size=32, on_press=lambda btn, x=i, y=j: self.on_button_press(btn, x, y))
                self.grid.add_widget(button)
                self.buttons[i][j] = button

        main_layout.add_widget(self.grid)

        self.score_label = Label(text=self.get_score_text(), font_size=32, size_hint=(1, 0.1))
        main_layout.add_widget(self.score_label)

        restart_button = Button(text='Restart Game', font_size=32, size_hint=(1, 0.2), on_press=self.reset_board)
        main_layout.add_widget(restart_button)

        return main_layout

    def on_button_press(self, button, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            button.text = self.current_player
            if self.check_winner(self.current_player):
                self.scores[self.current_player] += 1
                self.show_popup(f"Player {self.current_player} wins!")
                self.update_score()
                self.reset_board(reset_scores=False)
            elif self.is_board_full():
                self.show_popup("It's a draw!")
                self.reset_board(reset_scores=False)
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.info_label.text = f"Player {self.current_player}'s turn"

    def check_winner(self, player):
        for i in range(3):
            if all([self.board[i][j] == player for j in range(3)]) or all([self.board[j][i] == player for j in range(3)]):
                return True
        if all([self.board[i][i] == player for i in range(3)]) or all([self.board[i][2 - i] == player for i in range(3)]):
            return True
        return False

    def is_board_full(self):
        return all(cell != ' ' for row in self.board for cell in row)

    def reset_board(self, reset_scores=True):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].text = ' '
        self.info_label.text = f"Player {self.current_player}'s turn"
        if reset_scores:
            self.scores = {'X': 0, 'O': 0}
            self.update_score()

    def update_score(self):
        self.score_label.text = self.get_score_text()

    def get_score_text(self):
        return f"Scores - X: {self.scores['X']}  O: {self.scores['O']}"

    def show_popup(self, message):
        popup = Popup(title='Game Over', content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()

if __name__ == "__main__":
    TicTacToeApp().run()
