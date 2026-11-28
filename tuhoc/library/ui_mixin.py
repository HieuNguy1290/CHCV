"""Pages for the shared reading and dictation library."""
import sqlite3
import tkinter as tk
from collections import Counter
from tkinter import messagebox

from tuhoc.library.dictation_view import open_dictation
from tuhoc.library.migrate_legacy import check_reading_source, migrate_legacy
from tuhoc.library.models import SUBJECTS, LibraryError
from tuhoc.library.reading_view import open_reading
from tuhoc.library.store import LibraryStore
from tuhoc.library.ui_editor import edit_text, edit_topic
from tuhoc.paths import PROJECT_ROOT
from tuhoc.ui.ui_tokens import COLORS, font_at


class LibraryMixin:
    def _library_error(self, error):
        messagebox.showerror(title='Thư viện của tôi', message=str(error), parent=self)

    def _library_subject(self):
        return 'tieng_viet' if self.lang == 'vi' else 'tieng_anh'

    def library_page(self, mode='read'):
        body = self.layout('Thư viện của tôi')
        store = LibraryStore(self.data_dir)
        try:
            topics = store.topics()
            counts = Counter(article['topic_id'] for article in store.texts())
        except LibraryError as exc:
            self._library_error(exc)
        else:
            self.action_button(body, '＋ Chủ đề mới', lambda: edit_topic(
                self, store, None, self._library_subject(), lambda topic: self.library_page(mode),
            )).pack(anchor='w', pady=(0, 10))
            if not topics:
                self.label(body, 'Tạo chủ đề đầu tiên để lưu bài đọc và bài chép chính tả.',
                           12).pack(anchor='w', pady=8)
            else:
                self._library_topic_cards(body, store, topics, counts, mode)
        footer = tk.Frame(body, bg=body.cget('bg'))
        footer.pack(fill='x', pady=14)
        self.action_button(footer, 'Nhập từ dữ liệu cũ',
                           lambda: self._library_import(store, mode)).pack(side='left', padx=(0, 10))
        legacy = self.legacy_reading_topics if mode == 'read' else self.legacy_dictation_page
        self.button(footer, 'Xem bản cũ', legacy).pack(side='left')
        return body

    def _library_topic_cards(self, body, store, topics, counts, mode):
        grid = tk.Frame(body, bg=body.cget('bg'))
        grid.pack(fill='x')
        columns = 2
        for column in range(columns):
            grid.columnconfigure(column, weight=1, uniform='library_topics')
        for index, topic in enumerate(topics):
            topic_id = topic['id']
            row, column = divmod(index, columns)
            card = tk.Frame(grid, bg=COLORS['surface'], padx=12, pady=12,
                            highlightbackground=COLORS['border'], highlightthickness=1)
            card.grid(row=row, column=column, padx=4, pady=4, sticky='nsew')
            self.label(card, f"{topic['icon']} {topic['name']}", 15, True).pack(anchor='w')
            tk.Frame(card, bg=topic['color'], height=3).pack(fill='x', pady=(3, 5))
            self.label(card, f"{SUBJECTS[topic['subject']]} · {counts[topic_id]} bài", 11,
                       color=COLORS['muted']).pack(anchor='w')
            self.button(card, 'Mở chủ đề', lambda key=topic_id: self.library_topic(key, mode)).pack(
                anchor='w', pady=(6, 4),
            )
            self.action_button(card, 'Sửa', lambda entry=topic: edit_topic(
                self, store, entry, entry['subject'], lambda saved: self.library_page(mode),
            )).pack(side='left')
            self.action_button(card, 'Xóa', lambda entry=topic: self._library_delete_topic(
                store, entry, mode,
            )).pack(side='left', padx=6)

    def _library_delete_topic(self, store, topic, mode):
        try:
            count = len(store.texts(topic['id']))
            detail = f' và {count} bài viết' if count else ''
            if messagebox.askyesno(title='Xóa chủ đề',
                                   message=f"Xóa chủ đề “{topic['name']}”{detail}?", parent=self):
                store.delete_topic(topic['id'], cascade=bool(count))
                self.library_page(mode)
        except LibraryError as exc:
            self._library_error(exc)

    def library_topic(self, topic_id, mode='read'):
        store = LibraryStore(self.data_dir)
        try:
            topics = store.topics()
            topic = next((entry for entry in topics if entry['id'] == topic_id), None)
            if topic is None:
                raise LibraryError('Không tìm thấy chủ đề.')
            articles = store.texts(topic_id)
            progress = {(record['text_id'], record['mode']): record
                        for record in self.db.library_progress(self.student['id'])} if self.student else {}
        except (LibraryError, sqlite3.Error) as exc:
            self._library_error(exc)
            return None
        body = self.layout(f"{topic['icon']} {topic['name']}")
        actions = tk.Frame(body, bg=body.cget('bg'))
        actions.pack(fill='x', pady=(0, 10))
        self.button(actions, '← Thư viện của tôi', lambda: self.library_page(mode)).pack(side='left')
        self.action_button(actions, '＋ Bài mới', lambda: edit_text(
            self, store, topics, topic_id, None, lambda article: self.library_article(article['id'], mode),
        )).pack(side='left', padx=8)
        if not articles:
            self.label(body, 'Chủ đề này chưa có bài viết.', 12).pack(anchor='w')
        for article in articles:
            text_id = article['id']
            row = tk.Frame(body, bg=COLORS['surface'], padx=12, pady=7)
            row.pack(fill='x', pady=4)
            reading = progress.get((text_id, 'read'))
            dictation = progress.get((text_id, 'dictation'))
            status = ['✓ Đã đọc' if reading and reading['passed'] else 'Chưa đọc']
            if dictation:
                status.append(f"Chép tốt nhất {dictation['best_score']:g}%")
            if article['audio']:
                status.append('🔊 Có âm thanh')
            name = f"{article['title']}\n{' · '.join(status)}"
            self.label(row, name, 12).pack(side='left', fill='x', expand=True)
            def open_article(key=text_id,anchor=row,title=article['title']):
                morph=getattr(self,'morph',None)
                if morph:
                    morph.begin(anchor,f'article:{key}',title)
                return self.library_article(key,mode)
            self.button(row, 'Mở bài', open_article).pack(side='right')
            morph=getattr(self,'morph',None)
            if morph:
                morph.arrive(f'library-row:{text_id}',row)
        return body

    def library_article(self, text_id, mode='read'):
        store = LibraryStore(self.data_dir)
        try:
            article = store.get_text(text_id)
            topics = store.topics()
        except LibraryError as exc:
            self._library_error(exc)
            return None
        topic_id = article['topic_id']
        body = self.layout(article['title'])
        heading=getattr(self,'_page_heading',None)
        morph=getattr(self,'morph',None)
        if morph:
            morph.arrive(f'article:{text_id}',heading)
        def back_to_topic():
            if morph:
                morph.begin(heading,f'library-row:{text_id}',article['title'])
            return self.library_topic(topic_id,mode)
        self.button(body, '← Về danh sách', back_to_topic).pack(anchor='w')
        self.label(body, f"{SUBJECTS[article['subject']]} · Mức độ {article['level']}", 11,
                   color=COLORS['muted']).pack(anchor='w', pady=8)
        if article['image']:
            try:
                self._library_image(body, store.resolve_media(article['image'], 'image'))
            except (LibraryError, OSError, ValueError) as exc:
                self._library_error(exc)
        actions = tk.Frame(body, bg=body.cget('bg'))
        actions.pack(anchor='w', pady=8)
        label = 'Chép chính tả' if mode == 'dictation' else 'Đọc'
        def practice():
            if morph:
                morph.begin(heading,f'practice:{text_id}',article['title'])
            return self.library_practice(text_id,mode)
        self.button(actions, label, practice).pack(side='left')
        if article['glossary']:
            self.label(body, 'Từ khó', 14, True).pack(anchor='w', pady=(14, 4))
            for item in article['glossary']:
                self.label(body, f"{item['word']} — {item['meaning']}", 12).pack(anchor='w')
        edit_actions = tk.Frame(body, bg=body.cget('bg'))
        edit_actions.pack(anchor='w', pady=12)
        self.action_button(edit_actions, 'Sửa bài', lambda: edit_text(
            self, store, topics, topic_id, article, lambda saved: self.library_article(saved['id'], mode),
        )).pack(side='left', padx=(0, 8))
        self.action_button(edit_actions, 'Xóa bài', lambda: self._library_delete_text(
            store, article, mode,
        )).pack(side='left')
        return body

    @staticmethod
    def _library_image(body, path):
        from PIL import Image, ImageTk

        with Image.open(path) as image:
            image.thumbnail((540, 310))
            photo = ImageTk.PhotoImage(image, master=body)
        widget = tk.Label(body, image=photo, bg=COLORS['surface'])
        widget.image = photo
        widget.pack(anchor='w', pady=8)

    def _library_delete_text(self, store, article, mode):
        if messagebox.askyesno(title='Xóa bài viết',
                               message=f"Xóa bài “{article['title']}”?", parent=self):
            try:
                store.delete_text(article['id'])
                self.library_topic(article['topic_id'], mode)
            except LibraryError as exc:
                self._library_error(exc)

    def library_practice(self, text_id, mode):
        store = LibraryStore(self.data_dir)
        try:
            article = store.get_text(text_id)
            topic_id = article['topic_id']

            def back():
                morph=getattr(self,'morph',None)
                page=getattr(self,'_library_reading_page',None)
                anchor=page.center if mode=='read' and page is not None else getattr(self,'_page_heading',None)
                if morph:
                    morph.begin(anchor,f'library-row:{text_id}',article['title'])
                return self.library_topic(topic_id, mode)

            if mode == 'read':
                return open_reading(self, store, article, back)
            articles = store.texts(topic_id)
            index = next((i for i, entry in enumerate(articles) if entry['id'] == text_id), None)
            if index is None:
                raise LibraryError('Không tìm thấy bài viết trong chủ đề.')
            next_article = None
            if index + 1 < len(articles):
                next_id = articles[index + 1]['id']

                def next_article():
                    return self.library_practice(next_id, 'dictation')

            return open_dictation(self, store, article, back, next_article)
        except (LibraryError, sqlite3.Error) as exc:
            self._library_error(exc)
            return None

    def _library_import(self, store, mode):
        subject = self._library_subject()
        path = PROJECT_ROOT / 'mon_hoc' / subject / 'dictation' / 'dap_an_chinh_ta.json'
        if subject == 'tieng_viet' and not path.is_file():
            path = self.data_dir / 'vi' / 'dictation' / path.name
        reading_errors = []
        reading_rows = self._levels('reading')
        try:
            check_reading_source(self.curriculum.data_dir / 'content_library' / 'level_reading.json')
            reading_errors = [error for error in self.curriculum.errors
                              if error.startswith(('reading:', 'reading,'))]
        except LibraryError as exc:
            reading_errors.append(str(exc))
            reading_rows = []
        try:
            summary = migrate_legacy(store, subject, dictation_file=path if path.is_file() else None,
                                     reading_rows=reading_rows, image_resolver=self.media_file)
        except LibraryError as exc:
            self._library_error(exc)
            return
        summary['skipped'] += sum(error.startswith('reading, dòng ') for error in reading_errors)
        summary['warnings'].extend(reading_errors)
        message = (f"{SUBJECTS[subject]} · Đã nhập {summary['imported']} bài, "
                   f"bỏ qua {summary['skipped']} bài.")
        if summary['warnings']:
            warnings = summary['warnings']
            message += '\n\n' + '\n'.join(warnings[:8])
            if len(warnings) > 8:
                message += f'\nCòn {len(warnings) - 8} thông báo.'
        messagebox.showinfo(title='Nhập từ dữ liệu cũ', message=message, parent=self)
        self.library_page(mode)
