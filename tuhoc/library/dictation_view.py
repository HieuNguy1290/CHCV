"""Whole-article dictation with the existing audio controls and word feedback."""
import queue
import sqlite3
import threading
import tkinter as tk
from tkinter import messagebox

from tuhoc.lessons.dictation_vi import ModernAudioControls, WaveformSeek
from tuhoc.library.audio import MP3Player, speak_article, waveform_peaks
from tuhoc.library.dictation_check import check_dictation
from tuhoc.library.models import LibraryError
from tuhoc.ui.ui_tokens import COLORS, font_at


class AudioPanel(tk.Frame):
    def __init__(self, parent, app, path):
        super().__init__(parent, bg=COLORS['surface'], padx=14, pady=8)
        self.player = app.dictation_audio = MP3Player(allow_ogg=True)
        self.path = path
        self.repeat = 'once'
        self.controls = ModernAudioControls(self, lambda: self.skip(-5000), self.toggle,
                                            lambda: self.skip(5000), self.set_repeat)
        self.controls.pack(fill='x')
        self.wave = WaveformSeek(self, self.seek_fraction, bg=self.cget('bg'))
        self.wave.pack(fill='x')
        self.clock = app.label(self, '00:00 / 00:00', 10)
        self.clock.pack(anchor='e')
        self.peaks = queue.SimpleQueue()
        threading.Thread(target=self.load_waveform, daemon=True).start()
        self.waiting_for_wave = True
        self.job = self.after(150, self.tick)
        self.bind('<Destroy>', self.cleanup, add='+')

    def load_waveform(self):
        try:
            peaks = waveform_peaks(self.path)
        except (OSError, ValueError):
            peaks = None
        self.peaks.put(peaks)

    def play_if_stopped(self):
        if not self.player.active:
            self.player.play(self.path)

    def toggle(self):
        try:
            if not self.player.active:
                self.play_if_stopped()
            elif self.player.paused:
                self.player.resume()
            else:
                self.player.pause()
        except (OSError, RuntimeError, ValueError) as exc:
            messagebox.showerror(title='Không phát được âm thanh', message=str(exc), parent=self)
        self.sync_controls()

    def seek(self, position):
        try:
            self.play_if_stopped()
            self.player.seek(position())
        except (OSError, RuntimeError, ValueError) as exc:
            messagebox.showerror(title='Không tua được âm thanh', message=str(exc), parent=self)
        self.sync_controls()

    def skip(self, delta):
        self.seek(lambda: self.player.position_ms() + delta)

    def seek_fraction(self, fraction):
        self.seek(lambda: self.player.duration_ms() * fraction)

    def set_repeat(self, repeat):
        self.repeat = repeat
        self.sync_controls()

    def sync_controls(self):
        self.controls.set_state(self.player.active and not self.player.paused, self.repeat)

    @staticmethod
    def format_time(milliseconds):
        seconds = milliseconds // 1000
        return f'{seconds // 60:02d}:{seconds % 60:02d}'

    def tick(self):
        if self.waiting_for_wave:
            try:
                self.wave.set_peaks(self.peaks.get_nowait())
            except queue.Empty:
                pass
            else:
                self.waiting_for_wave = False
        if self.player.is_finished():
            if self.repeat == 'loop':
                try:
                    self.player.play(self.path)
                except (RuntimeError, OSError, ValueError) as exc:
                    messagebox.showerror(title='Không lặp được âm thanh', message=str(exc), parent=self)
            else:
                self.player.stop()
        position, duration = self.player.position_ms(), self.player.duration_ms()
        self.wave.set_progress(position, duration)
        self.clock.configure(text=f'{self.format_time(position)} / {self.format_time(duration)}')
        self.sync_controls()
        self.job = self.after(150, self.tick)

    def cleanup(self, event):
        if event.widget is self:
            self.after_cancel(self.job)
            self.player.stop()


def open_dictation(app, store, article, back, next_article=None):
    path = store.resolve_media(article['audio'], 'audio')
    body = app.layout(f"Chép chính tả · {article['title']}")
    app.label(body, 'Nghe và chép lại toàn bộ bài.', 12).pack(anchor='w', pady=(0, 8))
    if path:
        AudioPanel(body, app, path).pack(fill='x', pady=6)
    else:
        app.action_button(body, '🔊 Đọc bài bằng giọng máy',
                          lambda: speak_article(app, article)).pack(anchor='w', pady=6)
    app.label(body, 'Bài chép của em', 13, True).pack(anchor='w', pady=(10, 5))
    field = tk.Text(body, height=9, font=font_at(14), wrap='word', undo=True)
    field.pack(fill='x')
    feedback = tk.Frame(body, bg=body.cget('bg'))
    feedback.pack(fill='x', pady=8)
    settings = article['dictation']

    def check():
        entered = field.get('1.0', 'end-1c').strip()
        if not entered:
            messagebox.showwarning(title='Chưa có đáp án',
                                   message='Em hãy nghe và chép nội dung trước khi kiểm tra.', parent=app)
            return
        result = check_dictation(article['body'], entered, settings['accepted_variants'],
                                 settings['equivalences'])
        for widget in feedback.winfo_children():
            widget.destroy()
        score = result['score']
        app.label(feedback, f"Kết quả: {score:g}% · Đúng {result['matched']}/{result['total']} từ", 15,
                  True, color=COLORS['success' if result['passed'] else 'warning']).pack(anchor='w')
        if result['passed']:
            app.label(feedback, 'Chính xác! Em đã chép đúng toàn bộ từ và dấu.', 12).pack(anchor='w')
        else:
            app.label(feedback, 'Cần sửa (đáp án → bài em chép)', 12, True).pack(anchor='w')
            for issue in result['issues'][:20]:
                expected = issue['expected'] or '(không có)'
                written = issue['written'] or '(thiếu)'
                app.label(feedback, f'• {expected} → {written}', 11).pack(anchor='w')
            app.action_button(feedback, 'Xem đáp án gốc', lambda: messagebox.showinfo(
                title='Đáp án chính tả', message='\n\n'.join([article['body'], *settings['accepted_variants']]),
                parent=app,
            )).pack(anchor='w', pady=4)
        if app.student:
            try:
                app.db.save_library_result(app.student['id'], article['id'], 'dictation', score, result['passed'])
            except (LibraryError, sqlite3.Error) as exc:
                messagebox.showerror(title='Không lưu được tiến trình', message=str(exc), parent=app)

    actions = tk.Frame(body, bg=body.cget('bg'))
    actions.pack(anchor='w', pady=10)
    app.action_button(actions, '✓ Kiểm tra đáp án', check).pack(side='left', padx=(0, 6))
    app.button(actions, '← Về danh sách', back).pack(side='left', padx=(0, 6))
    if next_article:
        app.button(actions, 'Bài tiếp theo →', next_article).pack(side='left')
    return body
