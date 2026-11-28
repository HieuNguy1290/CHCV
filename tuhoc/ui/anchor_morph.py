"""Shared-element transitions between Tk pages without capturing the screen."""

import time
import tkinter as tk

from tuhoc.ui.ui_motion import smoothstep
from tuhoc.ui.ui_tokens import COLORS, font_at


class AnchorMorph:
    def __init__(self, root):
        self.root = root
        self.pending = None
        self.layer = None
        self.job = None

    def _bounds(self, widget):
        if widget is None or not widget.winfo_exists() or not widget.winfo_ismapped():
            return None
        return (widget.winfo_rootx()-self.root.winfo_rootx(),
                widget.winfo_rooty()-self.root.winfo_rooty(),
                widget.winfo_width(), widget.winfo_height())

    def begin(self, widget, destination, text):
        self.stop()
        self.pending = None
        if getattr(self.root, 'reduce_motion', False) or widget is None:
            return
        try:
            bounds = self._bounds(widget)
            if bounds and bounds[2]>1 and bounds[3]>1:
                self.pending = destination,bounds,text,time.monotonic()
        except tk.TclError:
            pass

    def arrive(self, key, widget):
        pending = self.pending
        if pending is not None and pending[0] == key:
            self.pending = None
            if not getattr(self.root, 'reduce_motion', False) and time.monotonic()-pending[3] < 12:
                self.stop()
                self.job = self.root.after_idle(lambda:self._animate(pending[1], widget, pending[2]))

    def has_pending(self):
        if self.pending is not None and time.monotonic()-self.pending[3]>=12:
            self.pending = None
        return self.pending is not None

    def stop(self):
        if self.job is not None:
            try:self.root.after_cancel(self.job)
            except tk.TclError:pass
            self.job = None
        if self.layer is not None:
            try:self.layer.destroy()
            except tk.TclError:pass
            self.layer = None

    def _animate(self, start, widget, text):
        self.job = None
        try:
            target = self._bounds(widget)
        except tk.TclError:
            return
        if not target or getattr(self.root, 'reduce_motion', False):
            return
        width,height = self.root.winfo_width(),self.root.winfo_height()
        if not all(0 <= rect[0] < width and 0 <= rect[1] < height for rect in (start,target)):
            return
        self.layer = tk.Canvas(self.root,bg=COLORS['tint'],highlightthickness=1,
                               highlightbackground=COLORS['focus'],takefocus=False)
        label = self.layer.create_text(0,0,text=text,fill=COLORS['text'],font=font_at(15,'bold'))
        started = time.monotonic()
        def frame():
            if not widget.winfo_exists() or (self.root.winfo_width(),self.root.winfo_height()) != (width,height):
                self.stop()
                return
            elapsed = (time.monotonic()-started)/.22
            if elapsed>=1:
                self.stop()
                return
            x,y,w,h = [round(a+(b-a)*smoothstep(elapsed)) for a,b in zip(start,target)]
            # Keep the flying layer confined to the client area.
            w,h = min(w,width-x),min(h,height-y)
            self.layer.place(x=x,y=y,width=w,height=h)
            self.layer.tk.call('raise',self.layer._w)
            self.layer.coords(label,w/2,h/2)
            self.layer.itemconfigure(label,width=max(1,w-8))
            self.job = self.root.after(16,frame)
        frame()
