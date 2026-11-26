"""Custom decks and word editing in Storage (SQLite in memory)."""
import ast
import sqlite3
import time
import unittest
from pathlib import Path


def load_storage():
    """Import Storage; fall back to extracting the class when tkinter is unavailable."""
    try:
        from tuhoc.app.main import Storage
        return Storage
    except Exception:
        source = Path(__file__).resolve().parents[1].joinpath('tuhoc/app/main.py').read_text(encoding='utf-8')
        tree = ast.parse(source)
        node = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Storage')
        namespace = {'sqlite3': sqlite3, 'time': time, 'DB': ':memory:'}
        import json, os, sys, hashlib, datetime
        namespace.update(json=json, os=os, sys=sys, hashlib=hashlib, datetime=datetime, Path=Path)
        exec(compile(ast.Module([node], []), 'Storage', 'exec'), namespace)
        return namespace['Storage']


class DeckTests(unittest.TestCase):
    def setUp(self):
        self.db = load_storage()(':memory:')
        self.sid = 1

    def word_id(self, word):
        return self.db.conn.execute('SELECT id FROM vocabulary WHERE student_id=? AND word=?', (self.sid, word)).fetchone()['id']

    def test_create_deck_lists_when_empty_and_blocks_duplicates(self):
        deck = self.db.create_custom_deck(self.sid, '  Màu   sắc ', 'vi')
        self.assertEqual(deck['source_title'], 'Màu sắc')
        groups = self.db.vocabulary_groups(self.sid)
        self.assertEqual([(g['source_type'], g['source_title'], g['total'], g['lang']) for g in groups],
                         [('custom', 'Màu sắc', 0, 'vi')])
        with self.assertRaises(ValueError):
            self.db.create_custom_deck(self.sid, 'màu sắc', 'vi')      # case-insensitive
        with self.assertRaises(ValueError):
            self.db.create_custom_deck(self.sid, '   ', 'en')

    def test_add_new_and_existing_words_and_remove(self):
        deck = self.db.create_custom_deck(self.sid, 'Fruits', 'en')
        self.db.save_word_in_source(self.sid, 'apple', 'quả táo', 'lesson', 'fruit', 1, 'x')   # other deck
        apple = self.word_id('apple')
        self.assertEqual(self.db.add_words_to_deck(self.sid, deck, [apple]), 1)
        self.assertEqual(self.db.add_words_to_deck(self.sid, deck, [apple]), 0)                # no duplicate link
        self.db.save_word_in_source(self.sid, 'pear', 'quả lê', 'custom', '', 0, 'Fruits')
        words = self.db.words_in_source(self.sid, 'custom', '', 0, 'Fruits')
        self.assertEqual([w['word'] for w in words], ['apple', 'pear'])
        group = next(g for g in self.db.vocabulary_groups(self.sid) if g['source_title'] == 'Fruits')
        self.assertEqual(group['total'], 2)

        self.db.remove_word_from_deck(self.sid, deck, apple)
        self.assertEqual([w['word'] for w in self.db.words_in_source(self.sid, 'custom', '', 0, 'Fruits')], ['pear'])
        # still in library and in the other deck
        self.assertEqual(len(self.db.words_in_source(self.sid, 'lesson', 'fruit', 1, 'x')), 1)
        self.assertIsNotNone(self.word_id('apple'))

    def test_add_ignores_unknown_ids(self):
        deck = self.db.create_custom_deck(self.sid, 'D', 'en')
        self.assertEqual(self.db.add_words_to_deck(self.sid, deck, [999]), 0)

    def test_update_word_both_languages_keeps_schedule(self):
        self.db.save_word_in_source(self.sid, 'aple', 'quả táo', 'manual', lang='en')
        self.db.save_word_in_source(self.sid, 'con mèo', '', 'manual', lang='vi')
        en, vi = self.word_id('aple'), self.word_id('con mèo')
        self.db.review(self.sid, en, 'good')
        before = dict(self.db.conn.execute('SELECT * FROM vocabulary WHERE id=?', (en,)).fetchone())
        self.db.update_word(self.sid, en, 'apple', 'quả táo đỏ')
        after = dict(self.db.conn.execute('SELECT * FROM vocabulary WHERE id=?', (en,)).fetchone())
        self.assertEqual((after['word'], after['meaning']), ('apple', 'quả táo đỏ'))
        for key in ('due_at', 'interval_days', 'repetitions', 'lapses'):
            self.assertEqual(before[key], after[key])
        self.db.update_word(self.sid, vi, 'con mèo', 'loài vật nuôi trong nhà')         # fill an empty meaning
        self.db.update_word(self.sid, vi, 'con mèo nhà', 'loài vật nuôi trong nhà')     # and rename it
        row = self.db.conn.execute('SELECT * FROM vocabulary WHERE id=?', (vi,)).fetchone()
        self.assertEqual((row['word'], row['meaning'], row['lang']), ('con mèo nhà', 'loài vật nuôi trong nhà', 'vi'))

    def test_update_word_rejects_empty_duplicate_unknown(self):
        self.db.save_word_in_source(self.sid, 'cat', 'mèo', 'manual')
        self.db.save_word_in_source(self.sid, 'dog', 'chó', 'manual')
        cat = self.word_id('cat')
        with self.assertRaises(ValueError):
            self.db.update_word(self.sid, cat, '   ', 'x')
        with self.assertRaises(ValueError):
            self.db.update_word(self.sid, cat, '[VI] ', 'x')                # legacy prefix with no text
        with self.assertRaises(ValueError):
            self.db.update_word(self.sid, cat, 'dog', 'x')
        with self.assertRaises(ValueError):
            self.db.update_word(self.sid, 999, 'bird', 'x')
        self.assertEqual(self.db.conn.execute('SELECT word FROM vocabulary WHERE id=?', (cat,)).fetchone()[0], 'cat')

    def test_delete_custom_deck_removes_deck_not_words(self):
        deck = self.db.create_custom_deck(self.sid, 'Tmp', 'en')
        self.db.save_word_in_source(self.sid, 'sun', 'mặt trời', 'custom', '', 0, 'Tmp')
        self.db.rename_deck(self.sid, deck, 'Tên khác')
        self.db.delete_deck(self.sid, deck)
        self.assertEqual(self.db.vocabulary_groups(self.sid), [])
        self.assertIsNotNone(self.word_id('sun'))                    # kept as an unclassified word
        self.assertIsNone(self.db.deck_custom_name(self.sid, deck))


class ImageColumnTests(unittest.TestCase):
    def test_pictures_saved_updated_removed_and_tracked(self):
        db = load_storage()(':memory:')
        db.save_word_in_source(1, 'apple', '', 'manual', lang='en', word_image='w.png', meaning_image='m.jpg')
        row = db.conn.execute('SELECT * FROM vocabulary').fetchone()
        self.assertEqual((row['word_image'], row['meaning_image'], row['meaning']), ('w.png', 'm.jpg', ''))
        self.assertTrue(db.image_in_use('w.png'))
        self.assertFalse(db.image_in_use('other.png'))
        self.assertFalse(db.image_in_use(''))
        db.update_word(1, row['id'], 'apple', 'quả táo')                      # None keeps both pictures
        again = db.conn.execute('SELECT * FROM vocabulary').fetchone()
        self.assertEqual((again['word_image'], again['meaning_image'], again['meaning']), ('w.png', 'm.jpg', 'quả táo'))
        db.update_word(1, row['id'], 'apple', 'quả táo', word_image='', meaning_image='new.png')
        last = db.conn.execute('SELECT * FROM vocabulary').fetchone()
        self.assertEqual((last['word_image'], last['meaning_image']), ('', 'new.png'))
        self.assertFalse(db.image_in_use('w.png'))

    def test_database_that_already_has_lang_gets_picture_columns(self):
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / 'tuhoc.db')
            con = sqlite3.connect(path)
            con.execute("""CREATE TABLE vocabulary (id INTEGER PRIMARY KEY, student_id INTEGER NOT NULL, word TEXT NOT NULL,
                meaning TEXT NOT NULL, due_at REAL NOT NULL, interval_days INTEGER NOT NULL DEFAULT 0,
                repetitions INTEGER NOT NULL DEFAULT 0, lapses INTEGER NOT NULL DEFAULT 0,
                lang TEXT NOT NULL DEFAULT 'en', UNIQUE(student_id, lang, word))""")
            con.execute("INSERT INTO vocabulary VALUES(1,1,'cat','mèo',1.0,2,3,0,'en')")
            con.commit()
            con.close()
            db = load_storage()(path)
            row = db.conn.execute('SELECT * FROM vocabulary').fetchone()
            self.assertEqual((row['word'], row['word_image'], row['meaning_image'], row['repetitions']), ('cat', '', '', 3))
            db.conn.close()
            load_storage()(path).conn.close()                                # reopening is harmless

    def test_legacy_prefixed_database_ends_with_lang_and_picture_columns(self):
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / 'tuhoc.db')
            MigrationTests().make_legacy(path)
            db = load_storage()(path)
            columns = {r['name'] for r in db.conn.execute('PRAGMA table_info(vocabulary)')}
            self.assertTrue({'lang', 'word_image', 'meaning_image'} <= columns)
            db.conn.close()

class LangColumnTests(unittest.TestCase):
    def test_same_word_in_both_languages_and_legacy_prefix(self):
        db = load_storage()(':memory:')
        db.save_word_in_source(1, 'co', 'to cold', 'manual', lang='en')
        db.save_word_in_source(1, '[VI] co', 'thu nhỏ lại', 'manual')           # old callers still send the prefix
        rows = db.conn.execute('SELECT word,lang FROM vocabulary ORDER BY lang').fetchall()
        self.assertEqual([(r['word'], r['lang']) for r in rows], [('co', 'en'), ('co', 'vi')])
        self.assertEqual([r['lang'] for r in db.words(1, lang='vi')], ['vi'])
        self.assertEqual(len(db.words(1)), 2)
        db.save_word_in_source(1, 'co', 'again', 'manual', lang='en')              # same language: no duplicate
        self.assertEqual(len(db.words(1)), 2)
        db.save_word(1, '   ', '')                                                  # blank words are ignored
        self.assertEqual(len(db.words(1)), 2)


class MigrationTests(unittest.TestCase):
    LEGACY = '''
        CREATE TABLE vocabulary (id INTEGER PRIMARY KEY, student_id INTEGER NOT NULL, word TEXT NOT NULL,
            meaning TEXT NOT NULL, due_at REAL NOT NULL, interval_days INTEGER NOT NULL DEFAULT 0,
            repetitions INTEGER NOT NULL DEFAULT 0, lapses INTEGER NOT NULL DEFAULT 0, UNIQUE(student_id, word));
        CREATE TABLE reviews (id INTEGER PRIMARY KEY, student_id INTEGER NOT NULL, vocabulary_id INTEGER NOT NULL,
            rating TEXT NOT NULL, reviewed_at REAL NOT NULL);
        CREATE TABLE vocabulary_sources (student_id INTEGER NOT NULL, vocabulary_id INTEGER NOT NULL,
            source_type TEXT NOT NULL, theme TEXT NOT NULL DEFAULT '', level INTEGER NOT NULL DEFAULT 0,
            source_title TEXT NOT NULL DEFAULT '', PRIMARY KEY(student_id, vocabulary_id, source_type, theme, level, source_title));
    '''

    def make_legacy(self, path):
        con = sqlite3.connect(path)
        con.executescript(self.LEGACY)
        con.executemany('INSERT INTO vocabulary VALUES(?,?,?,?,?,?,?,?)', [
            (1, 1, '[VI] con mèo', '', 100.0, 2, 3, 1),
            (2, 1, 'cat', 'mèo', 200.0, 4, 5, 0),
            (3, 1, 'co', 'cold', 300.0, 1, 1, 0),
            (4, 1, '[VI] co', 'co lại', 400.0, 1, 2, 0),
            (7, 2, '[VI] xin chào', 'hello', 500.0, 8, 9, 2)])
        con.executemany('INSERT INTO reviews(student_id,vocabulary_id,rating,reviewed_at) VALUES(?,?,?,?)',
                        [(1, 2, 'good', 1.0), (1, 4, 'hard', 2.0)])
        con.executemany('INSERT INTO vocabulary_sources VALUES(?,?,?,?,?,?)',
                        [(1, 1, 'lesson', 'animals', 1, 'x'), (1, 4, 'manual', '', 0, '')])
        con.commit()
        con.close()

    def test_old_database_is_migrated_once_with_backup(self):
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / 'tuhoc.db')
            self.make_legacy(path)
            db = load_storage()(path)
            rows = {r['id']: dict(r) for r in db.conn.execute('SELECT * FROM vocabulary')}
            self.assertEqual({i: (r['word'], r['lang']) for i, r in rows.items()},
                             {1: ('con mèo', 'vi'), 2: ('cat', 'en'), 3: ('co', 'en'), 4: ('co', 'vi'), 7: ('xin chào', 'vi')})
            self.assertEqual((rows[1]['due_at'], rows[1]['interval_days'], rows[1]['repetitions'], rows[1]['lapses']), (100.0, 2, 3, 1))
            self.assertEqual(rows[7]['student_id'], 2)
            self.assertEqual([(r['vocabulary_id'], r['rating']) for r in db.conn.execute('SELECT * FROM reviews ORDER BY id')],
                             [(2, 'good'), (4, 'hard')])
            self.assertEqual(len(db.conn.execute('SELECT * FROM vocabulary_sources').fetchall()), 2)
            self.assertEqual([g['total'] for g in db.vocabulary_groups(1)], [1, 1])
            backup = Path(path + '.before-lang.bak')
            self.assertTrue(backup.is_file())
            old = sqlite3.connect(str(backup))
            self.assertEqual(old.execute("SELECT word FROM vocabulary WHERE id=1").fetchone()[0], '[VI] con mèo')
            old.close()
            db.conn.close()

            again = load_storage()(path)                                   # reopening changes nothing
            self.assertEqual(again.conn.execute('SELECT COUNT(*) FROM vocabulary').fetchone()[0], 5)
            self.assertEqual(again.conn.execute("SELECT word FROM vocabulary WHERE id=1").fetchone()[0], 'con mèo')
            again.conn.close()

    def test_failed_migration_rolls_back_completely(self):
        import tempfile
        Storage = load_storage()
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / 'tuhoc.db')
            self.make_legacy(path)
            original = Storage.split_word_lang

            def explode(word, lang=None):
                if word == 'cat':
                    raise RuntimeError('boom')
                return original(word, lang)

            Storage.split_word_lang = staticmethod(explode)
            try:
                with self.assertRaises(RuntimeError):
                    Storage(path)
            finally:
                Storage.split_word_lang = staticmethod(original)
            con = sqlite3.connect(path)
            columns = [r[1] for r in con.execute('PRAGMA table_info(vocabulary)')]
            tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            words = sorted(r[0] for r in con.execute('SELECT word FROM vocabulary'))
            con.close()
            self.assertNotIn('lang', columns)
            self.assertNotIn('vocabulary_legacy', tables)
            self.assertEqual(words, ['[VI] co', '[VI] con mèo', '[VI] xin chào', 'cat', 'co'])
            Storage(path).conn.close()                                     # and the next start migrates fine

    def test_double_prefix_only_loses_one_marker(self):
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / 'tuhoc.db')
            con = sqlite3.connect(path)
            con.executescript(self.LEGACY)
            con.executemany('INSERT INTO vocabulary VALUES(?,?,?,?,?,?,?,?)', [
                (1, 1, '[VI] mèo', '', 1.0, 0, 0, 0), (2, 1, '[VI] [VI] mèo', '', 1.0, 0, 0, 0)])
            con.commit()
            con.close()
            # Only the first marker is removed, so both rows stay distinct and nothing is lost.
            db = load_storage()(path)
            self.assertEqual(sorted(r['word'] for r in db.conn.execute('SELECT word FROM vocabulary')), ['[VI] mèo', 'mèo'])
            db.conn.close()


if __name__ == '__main__':
    unittest.main()
