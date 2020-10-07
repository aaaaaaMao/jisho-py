import sys
import json

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QLineEdit,
    QListView, QLabel, QMessageBox
)
from PyQt5.QtCore import QStringListModel, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

from search import search_keyword
from storage import Word

class SearchThread(QThread):
    
    trigger = pyqtSignal(list)

    def __init__(self, keyword):
        super(SearchThread, self).__init__()
        self.keyword = keyword
    
    def run(self):
        result = search_keyword(self.keyword)
        self.trigger.emit(result)

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

        self.search_thread = None

        self.initUI()
        self.initWordStorage()

    def initUI(self):

        search_widget = self.initSearchWidget()
        content_widget = self.initContentWidget()

        main_layout = QVBoxLayout()
        main_layout.addWidget(search_widget)
        main_layout.addWidget(content_widget)

        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 7)

        self.setLayout(main_layout)

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
        self.search_box.setEnabled(False)
        self.search_thread = SearchThread(self.search_box.text())
        self.search_thread.start()
        self.search_thread.trigger.connect(self.display)
    
    def display(self, result):
        try:
            self.content_list = result
            if len(self.content_list) == 0:
                raise Exception('Invalid keyword!')
            breif = []
            for item in self.content_list:
                if 'word' in item and 'reading' in item:
                    content = item['word'] + ' ( ' + item['reading'] + ' ) '
                elif 'reading' in item:
                    content = item['reading']
                else:
                    continue
                breif.append(content)
            self.content_list_model.setStringList(breif)
            self.content_list_view.setModel(self.content_list_model)
        except Exception as e:
            print(e)
            self.errorMsg(str(e))
        finally:
            self.search_box.setEnabled(True)

    def showDetail(self, item):
        self.detail = self.content_list[item.row()]
        _detail = self.detail

        if 'word' in _detail and 'reading' in _detail:
            self.kana_label.setText(_detail['reading'])
            self.kanji_label.setText(_detail['word'])
        else:
            self.kana_label.setText('')
            self.kanji_label.setText(_detail['reading'])
        self.jlpt_label.setText(_detail['jlpt'])
        self.senses_list = _detail['senses']
        self.senses_list_model.setStringList(self.senses_list)
        self.senses_list_view.setModel(self.senses_list_model)
        return

    def cleanSearchBox(self):
        self.search_box.setText('')
        self.content_list = []
        self.content_list_model.setStringList(self.content_list)
        self.content_list_view.setModel(self.content_list_model)
        
        self.detail = None
        self.kana_label.setText('')
        self.kanji_label.setText('')
        self.jlpt_label.setText('')
        self.senses_list = []
        self.senses_list_model.setStringList(self.senses_list)
        self.senses_list_view.setModel(self.senses_list_model)

    def addToMyDictionary(self):

        if not self.kana_label.text():
            self.errorMsg('Empty word!')
            return

        reply = QMessageBox.question(
            self,
            'Message',
            'Add this word to local dictionary?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.wordStorage.save(
                    self.kana_label.text(),
                    self.kanji_label.text(),
                    json.dumps(self.detail)
                )
            except Exception as e:
                print(e)
                self.errorMsg('Failed add word!')
            print('Yes')
        else:
            print('No')
        return

    def initWordStorage(self):
        self.wordStorage = Word()

    def errorMsg(self, msg):
        QMessageBox.warning(
        self,
        'Warning',
        msg
        )

def main():

    app = QApplication(sys.argv)

    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    