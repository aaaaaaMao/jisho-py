import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, 
    QVBoxLayout, QHBoxLayout, QLineEdit, 
    QListView, QLabel, QMessageBox
)
from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QFont, QIcon

from search import search_keyword

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Jisho')
        _width = 800
        _height = 600
        self.resize(_width, _height)
        self.move(300, 300)

        self.search_box = QLineEdit()
        self.clean_btn = QPushButton('clean', self)

        self.search_box.returnPressed.connect(self.search)
        self.clean_btn.clicked.connect(self.cleanSearchBox)

        self.content_list_view = QListView()
        self.content_list_model = QStringListModel()
        self.content_list = []
        self.content_list_model.setStringList(self.content_list)
        self.content_list_view.setModel(self.content_list_model)
        self.content_list_view.clicked.connect(self.showDetail)

        self.kana_label = QLabel()
        self.kanji_label = QLabel()
        self.kanji_label.setFont(QFont('bold', 32))
        self.jlpt_label = QLabel()
        self.add_btn = QPushButton('+', self)
        self.add_btn.resize(self.add_btn.sizeHint())
        self.add_btn.clicked.connect(self.addToMyDictionary)

        self.senses_list_view = QListView()
        self.senses_list_model = QStringListModel()
        self.senses_list = []
        self.senses_list_model.setStringList(self.senses_list)
        self.senses_list_view.setModel(self.senses_list_model)

        self.setWindowIcon(QIcon('logo.png'))

        self.initUI()

    def initUI(self):

        search_widget = self.initSearchWidget()
        content_widget = self.initContentWidget()

        main_layout = QVBoxLayout()
        main_layout.addWidget(search_widget)
        main_layout.addWidget(content_widget)

        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 7)

        self.setLayout(main_layout)

        self.show()

    def initSearchWidget(self):
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.clean_btn)
        search_layout.setStretch(0, 9)
        search_layout.setStretch(1, 1)
        search_widget = QWidget()
        search_widget.setLayout(search_layout)
        return search_widget
    
    def initContentWidget(self):
        content_layout = QHBoxLayout()
        content_layout.addWidget(self.content_list_view)
        content_layout.addWidget(self.initDetailWidget())
        content_layout.setStretch(0, 1)
        content_layout.setStretch(1, 2)
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        return content_widget

    def initDetailWidget(self):
        detail_layout = QVBoxLayout()
        detail_layout.addWidget(self.initUpperDetailWidget())
        detail_layout.addWidget(self.senses_list_view)
        detail_layout.setStretch(0, 2)
        detail_layout.setStretch(1, 10)
        detail_widget = QWidget()
        detail_widget.setLayout(detail_layout)
        return detail_widget
    
    def initUpperDetailWidget(self):
        layout = QVBoxLayout()
        layout.addWidget(self.kana_label)
        layout.addWidget(self.kanji_label)

        sub_layout = QHBoxLayout()
        sub_layout.addWidget(self.jlpt_label)
        sub_layout.addWidget(self.add_btn)
        sub_layout.setStretch(0, 14)
        sub_layout.setStretch(1, 1)
        sub_widget = QWidget()
        sub_widget.setLayout(sub_layout)

        layout.addWidget(sub_widget)
        layout.setStretch(0, 1)
        layout.setStretch(1, 48)
        layout.setStretch(2, 1)
        wiget = QWidget()
        wiget.setLayout(layout)
        return wiget


    def search(self):
        self.content_list = search_keyword(self.search_box.text())
        breif = []
        for item in self.content_list:
            content = item['word'] + ' ( ' + item['reading'] + ' ) '
            breif.append(content)

        self.content_list_model.setStringList(breif)
        self.content_list_view.setModel(self.content_list_model)

    def showDetail(self, item):
        detail = self.content_list[item.row()]
        # QMessageBox.information(self, 'test', detail)
        self.kana_label.setText(detail['reading'])
        self.kanji_label.setText(detail['word'])
        self.jlpt_label.setText(detail['jlpt'])
        self.senses_list = detail['senses']
        self.senses_list_model.setStringList(self.senses_list)
        self.senses_list_view.setModel(self.senses_list_model)
        return

    def cleanSearchBox(self):
        self.search_box.setText('')
        self.content_list = []
        self.content_list_model.setStringList(self.content_list)
        self.content_list_view.setModel(self.content_list_model)
        
        self.kana_label.setText('')
        self.kanji_label.setText('')
        self.jlpt_label.setText('')
        self.senses_list = []
        self.senses_list_model.setStringList(self.senses_list)
        self.senses_list_view.setModel(self.senses_list_model)

    def addToMyDictionary(self):
        reply = QMessageBox.question(
            self,
            'Message',
            'Add this word to local dictionary?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            print('Yes')
        else:
            print('No')
        return


def main():

    app = QApplication(sys.argv)

    window = Window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    