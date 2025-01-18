from PyQt6.QtWidgets import QApplication
from UI import ChessBoard

if __name__ == '__main__':
    app = QApplication([])
    window = ChessBoard()
    window.show()
    app.exec()
