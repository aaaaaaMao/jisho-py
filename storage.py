import sqlite3
from sqlite3 import Error

class Word(object):
    def __init__(self):
        self.conn = None
        _default_database= r'words.db'

        self._createConnection(_default_database)
        self._ceateTable()

    def _createConnection(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
        except Error:
            raise Exception('Failed to connect: {}, error: {}'.format(db_file, Error))

    def _ceateTable(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS words (
            id integer PRIMARY KEY,
            kana text NOT NULL,
            kanji text,
            detail text
        );
        '''
        index_sql = '''
        CREATE INDEX IF NOT EXISTS idx_words ON words (
            kana,
            kanji
        )
        '''
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            cursor.execute(index_sql)

    def save(self, kana, kanji, detail):
        sql = '''
        INSERT INTO words(kana,kanji,detail)
              VALUES(?,?,?) 
        '''
        if not kana:
            raise Exception('Empty kana !')

        if len(self.search(kana)) is not 0:
            raise Exception('{} already in storage'.format(kana))

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(sql, (kana, kanji, detail))
            return cursor.lastrowid

    def search(self, word):
        sql = '''
        SELECT * FROM words WHERE kana=? OR kanji=?
        '''
        if not word:
            raise Exception('Empty word !')

        with self.conn:
            self.conn.row_factory = sqlite3.Row
            cursor = self.conn.cursor()
            cursor.execute(sql, (word, word))

            return cursor.fetchall()
