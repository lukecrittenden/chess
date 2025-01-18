from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout
from PyQt6.QtGui import QColor, QPalette, QIcon, QPixmap, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import Qt, QEvent
from typing import Optional, List, Dict

class ClickableLabel(QLabel):
    def __init__(self, row: int, column: int, parent: 'ChessBoard', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row: int = row
        self.column: int = column
        self.parent: 'ChessBoard' = parent
        self.defaultColor: QColor = QColor(Qt.GlobalColor.white) if (row + column) % 2 == 0 else QColor(Qt.GlobalColor.darkGray)
        self.setAutoFillBackground(True)
        self.updateBackgroundColor(self.defaultColor)

    def mousePressEvent(self, event: QEvent) -> None:
        self.parent.labelClicked(self)

    def updateBackgroundColor(self, color: QColor) -> None:
        palette: QPalette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, color)
        self.setPalette(palette)

class ChessBoard(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Chess")
        self.setWindowIcon(QIcon("images/black_pawn.svg"))

        self.initUI()
        self.setupBoard()
        self.drawPieces()
        self.previousLabel: Optional[ClickableLabel] = None
        self.selectedPiece: Optional[str] = None
        self.selectedLabel: Optional[ClickableLabel] = None

    def initUI(self) -> None:
        self.grid: QGridLayout = QGridLayout()
        self.setLayout(self.grid)

        for row in range(8):
            for column in range(8):
                label: ClickableLabel = ClickableLabel(row, column, self)
                label.setFixedSize(50, 50)
                self.grid.addWidget(label, row, column)

    def setupBoard(self) -> None:
        self.board: List[List[Optional[str]]] = [
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            [None for _ in range(8)], [None for _ in range(8)], [None for _ in range(8)], [None for _ in range(8)],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        ]

    def drawPieces(self) -> None:
        pieceImages: Dict[str, str] = {
            'R': 'images/white_rook.svg', 'N': 'images/white_knight.svg', 'B': 'images/white_bishop.svg', 'Q': 'images/white_queen.svg', 'K': 'images/white_king.svg', 'P': 'images/white_pawn.svg',
            'r': 'images/black_rook.svg', 'n': 'images/black_knight.svg', 'b': 'images/black_bishop.svg', 'q': 'images/black_queen.svg', 'k': 'images/black_king.svg', 'p': 'images/black_pawn.svg'
        }

        for row in range(8):
            for column in range(8):
                piece: Optional[str] = self.board[row][column]
                label: ClickableLabel = self.grid.itemAtPosition(row, column).widget()
                if piece:
                    svgRenderer: QSvgRenderer = QSvgRenderer(pieceImages[piece])
                    pixmap: QPixmap = QPixmap(50, 50)
                    pixmap.fill(Qt.GlobalColor.transparent)
                    painter: QPainter = QPainter(pixmap)
                    svgRenderer.render(painter)
                    painter.end()
                    label.setPixmap(pixmap)
                else:
                    label.clear()

    def labelClicked(self, label: ClickableLabel) -> None:
        if self.selectedPiece:
            self.movePiece(label)
        else:
            self.selectPiece(label)

    def selectPiece(self, label: ClickableLabel) -> None:
        row, column = label.row, label.column
        piece: Optional[str] = self.board[row][column]
        if piece:
            self.selectedPiece = piece
            self.selectedLabel = label
            label.updateBackgroundColor(QColor(Qt.GlobalColor.gray))

    def movePiece(self, label: ClickableLabel) -> None:
        if label != self.selectedLabel:
            targetRow, targetColumn = label.row, label.column
            self.board[targetRow][targetColumn] = self.selectedPiece
            self.board[self.selectedLabel.row][self.selectedLabel.column] = None
            self.selectedLabel.updateBackgroundColor(self.selectedLabel.defaultColor)
            self.selectedPiece = None
            self.selectedLabel = None
            self.drawPieces()
