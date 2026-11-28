"""Shared Tk components with antialiased shapes for curved edges."""
from tuhoc.ui.ui_tokens import DURATION, RADIUS, font_at
import sys
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from tuhoc.ui.theme_config import UI_COLORS

_SHAPE_SCALE = 4


def _shape_layer(width, height):
    return Image.new('RGBA', (width * _SHAPE_SCALE, height * _SHAPE_SCALE))


def _shape_photo(canvas, layer, width, height):
    image = layer.resize((width, height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image, master=canvas)


def rounded_rect(canvas,x1,y1,x2,y2,r=16,fill='white',outline='',**kw):
    r=max(0,min(r,(x2-x1)/2,(y2-y1)/2))
    points=[x1+r,y1,x2-r,y1,x2,y1,x2,y1+r,x2,y2-r,x2,y2,x2-r,y2,x1+r,y2,x1,y2,x1,y2-r,x1,y1+r,x1,y1]
    return canvas.create_polygon(points,smooth=True,splinesteps=12,fill=fill,outline=outline,**kw)

class RoundedButton(tk.Canvas):
    def __init__(self,parent,text,command=None,variant='primary',width=160,height=44,
                 *,disabled=False,loading=False,icon=None,tooltip=None,**kw):
        width,height=max(44,width),max(44,height)
        options=dict(width=width,height=height,highlightthickness=2,
                     highlightbackground=UI_COLORS['border'],takefocus=1,cursor='hand2')
        options.update(kw)
        super().__init__(parent,**options)
        self.command=command
        self.text=text
        self.icon=icon
        self.disabled=disabled
        self.loading=loading
        self.variant=variant
        self._spinner=None
        self._frame=0
        self._colors={'primary':UI_COLORS['primary'],'outline':UI_COLORS['surface'],
                      'ghost':UI_COLORS['background']}
        self._shape_size = width, height
        self._shape_fill = None
        self._shape = self.create_image(0, 0, anchor='nw')
        self._label=self.create_text(width/2,height/2,font=font_at(12,'bold'))
        self.bind('<Button-1>',self._click)
        self.bind('<Return>',self._click)
        self.bind('<space>',self._click)
        self.bind('<FocusIn>',lambda _e:self.configure(highlightbackground=UI_COLORS['focus']))
        self.bind('<FocusOut>',lambda _e:self.configure(highlightbackground=UI_COLORS['border']))
        self.bind('<Destroy>',self._dispose,add='+')
        if tooltip:
            self.tooltip=Tooltip(self,tooltip)
        self.set_state(disabled=disabled,loading=loading)

    def _click(self,event):
        if event.keysym=='??':
            self.focus_set()
        self.invoke()
        return 'break'

    def invoke(self):
        if not self.disabled and not self.loading and self.command:
            return self.command()

    def _dispose(self,event=None):
        if self._spinner is not None:
            self.after_cancel(self._spinner)
            self._spinner=None

    def _render(self):
        blocked=self.disabled or self.loading
        icons=('◐','◓','◑','◒')
        icon=icons[self._frame%len(icons)] if self.loading else self.icon
        fill = UI_COLORS['disabled'] if blocked else self._colors[self.variant]
        if fill != self._shape_fill:
            width, height = self._shape_size
            scale = _SHAPE_SCALE
            layer = _shape_layer(width, height)
            ImageDraw.Draw(layer).rounded_rectangle(
                (2 * scale, 2 * scale, (width - 2) * scale - 1, (height - 2) * scale - 1),
                radius=RADIUS['normal'] * scale, fill=fill,
                outline=UI_COLORS['border'] if self.variant == 'outline' else None, width=scale)
            self._shape_image = _shape_photo(self, layer, width, height)
            self.itemconfigure(self._shape, image=self._shape_image)
            self._shape_fill = fill
        self.itemconfigure(self._label,text=f'{icon}  {self.text}' if icon else self.text,
                           fill=UI_COLORS['disabled_text'] if blocked else 'white'
                           if self.variant=='primary' else UI_COLORS['text'])

    def _next_frame(self):
        self._spinner=None
        if self.loading and self.winfo_exists():
            self._frame+=1
            self._render()
            self._spinner=self.after(DURATION['fast'],self._next_frame)

    def set_state(self,*,disabled=None,loading=None):
        if disabled is not None:self.disabled=bool(disabled)
        if loading is not None:self.loading=bool(loading)
        self._dispose()
        blocked=self.disabled or self.loading
        self.configure(takefocus=not blocked,cursor='' if blocked else 'hand2')
        self._render()
        if self.loading:
            self._spinner=self.after(DURATION['fast'],self._next_frame)


def bind_hover(root,on_change,inset=(0,0,0,0),region=None,also=()):
    """Hover by pointer position inside a stationary region of `root`.
    Child Enter/Leave events only trigger a re-check, so moving widgets or
    child boundaries never cause enter/leave flicker."""
    state={'on':False,'job':None}
    geo=region or root   # stationary widget that defines the hover area
    def check():
        state['job']=None
        try:
            if not root.winfo_exists() or not geo.winfo_exists():return
            x,y=root.winfo_pointerxy()
            l,t,r,b=inset
            x0=geo.winfo_rootx()+l;y0=geo.winfo_rooty()+t
            x1=geo.winfo_rootx()+geo.winfo_width()-r;y1=geo.winfo_rooty()+geo.winfo_height()-b
            inside=x0<=x<x1 and y0<=y<y1 and root.winfo_containing(x,y) is not None
            if inside!=state['on']:
                state['on']=inside;on_change(inside)
        except tk.TclError:pass
    def schedule(_e=None):
        if state['job'] is None:
            try:state['job']=root.after_idle(check)
            except tk.TclError:pass
    def walk(w):
        w.bind('<Enter>',schedule,add='+');w.bind('<Leave>',schedule,add='+')
        for c in w.winfo_children():walk(c)
    walk(root)
    for w in also:walk(w)
    return state

class Card(tk.Frame):
    def __init__(self,parent,**kw):super().__init__(parent,bg=UI_COLORS['surface'],highlightbackground=UI_COLORS['border'],highlightthickness=1,padx=16,pady=16,**kw)

class ProgressBar(tk.Canvas):
    def __init__(self,parent,value=0,width=200,height=14,**kw):
        super().__init__(parent,width=width,height=height,highlightthickness=0,**kw)
        self.value=value;self.draw(width,height)
    def draw(self,w,h):
        scale = _SHAPE_SCALE
        width, height = max(1, round(w)), max(1, round(h))
        layer = _shape_layer(width, height)
        draw = ImageDraw.Draw(layer)
        draw.rounded_rectangle((0, 0, width * scale - 1, height * scale - 1),
                               radius=height * scale / 2, fill=UI_COLORS['tint'])
        if self.value > 0:
            filled = min(width, max(height, width * self.value))
            draw.rounded_rectangle((0, 0, round(filled * scale) - 1, height * scale - 1),
                                   radius=height * scale / 2, fill=UI_COLORS['primary'])
        self._progress_image = _shape_photo(self, layer, width, height)
        self.delete('all')
        self.create_image(0, 0, anchor='nw', image=self._progress_image)

class ProgressRing(tk.Canvas):
    def __init__(self,parent,value=0,size=80,*,track=None,progress=None,text_color=None,
                 text_font=None,stroke=7,**kw):
        super().__init__(parent,width=size,height=size,highlightthickness=0,**kw)
        self.size = size
        self.stroke = stroke
        self.track = track or UI_COLORS['border']
        self.progress = progress or UI_COLORS['primary']
        self.text_color = text_color or UI_COLORS['text']
        self.text_font = text_font or font_at(12)
        self.draw(value)

    def draw(self, value):
        value = max(0, min(1, value))
        size = self.size
        scale = _SHAPE_SCALE
        inset = 3 * scale
        bounds = (inset, inset, size * scale - inset - 1, size * scale - inset - 1)
        layer = _shape_layer(size, size)
        draw = ImageDraw.Draw(layer)
        draw.ellipse(bounds, outline=self.track, width=self.stroke * scale)
        if value == 1:
            draw.ellipse(bounds, outline=self.progress, width=self.stroke * scale)
        elif value > 0:
            draw.arc(bounds, start=-90, end=-90 + value * 360,
                     fill=self.progress, width=self.stroke * scale)
        self._progress_image = _shape_photo(self, layer, size, size)
        self.delete('all')
        self.create_image(0, 0, anchor='nw', image=self._progress_image)
        self.create_text(size / 2, size / 2, text=f'{value:.0%}',
                         fill=self.text_color, font=self.text_font)

class Chip(tk.Label):
    def __init__(self,parent,text,**kw):
        opts=dict(bg=UI_COLORS['tint'],fg=UI_COLORS['text'],padx=12,pady=6,font=font_at(11));opts.update(kw)
        super().__init__(parent,text=text,**opts)

class Dialog(tk.Toplevel):
    def __init__(self,parent,title,message,*,primary='Đồng ý',secondary=None,
                 tone='info',safe=True):
        parent=parent.winfo_toplevel()
        super().__init__(parent,bg=UI_COLORS['surface'])
        self.title(title)
        self.transient(parent)
        self.resizable(False,False)
        self.result=False if secondary else True
        self._parent=parent
        self._previous_focus=parent.focus_get()
        frame=tk.Frame(self,bg=UI_COLORS['surface'],padx=22,pady=18)
        frame.pack(fill='both',expand=True)
        tk.Label(frame,text=title,fg=UI_COLORS.get(tone,UI_COLORS['text']),
                 bg=UI_COLORS['surface'],font=font_at(16,'bold'),
                 wraplength=460,justify='left').pack(anchor='w')
        tk.Label(frame,text=message,fg=UI_COLORS['text'],bg=UI_COLORS['surface'],
                 font=font_at(13),wraplength=460,justify='left').pack(anchor='w',pady=(10,15))
        row=tk.Frame(frame,bg=UI_COLORS['surface'])
        row.pack(fill='x')
        self.primary=RoundedButton(row,primary,lambda:self.close(True),width=128)
        self.primary.pack(side='right',padx=(8,0))
        self.secondary=None
        if secondary:
            self.secondary=RoundedButton(row,secondary,lambda:self.close(False),variant='outline',width=128)
            self.secondary.pack(side='right')
        safe_button=self.secondary if safe and self.secondary else self.primary
        self.bind('<Escape>',lambda _e:self.close(False))
        self.protocol('WM_DELETE_WINDOW',lambda:self.close(False))
        self.update_idletasks()
        x=parent.winfo_rootx()+(parent.winfo_width()-self.winfo_reqwidth())//2
        y=parent.winfo_rooty()+(parent.winfo_height()-self.winfo_reqheight())//2
        self.geometry(f'+{max(0,x)}+{max(0,y)}')
        self.wait_visibility()
        self._prior_grab=parent.grab_current()
        self.grab_set()
        safe_button.focus_set()

    def close(self,result):
        self.result=result
        self.grab_release()
        self.destroy()
        if self._prior_grab is not None and self._prior_grab.winfo_exists():
            self._prior_grab.grab_set()
        if self._previous_focus is not None and self._previous_focus.winfo_exists():
            self._previous_focus.focus_set()
        return 'break'

    def show(self):
        self.wait_window()
        return self.result


class ConfirmDialog(Dialog):
    def __init__(self,parent,title,message,*,safe=True):
        super().__init__(parent,title,message,primary='Có',secondary='Không',
                         tone='warning',safe=safe)


class EmptyState(tk.Frame):
    def __init__(self,parent,text,*,icon='○',action=None,background=None):
        bg=background or UI_COLORS['surface']
        super().__init__(parent,bg=bg,padx=14,pady=12)
        tk.Label(self,text=icon,bg=bg,fg=UI_COLORS['primary_text'],font=font_at(24,'bold')).pack()
        tk.Label(self,text=text,bg=bg,fg=UI_COLORS['muted'],font=font_at(13),
                 wraplength=460,justify='center').pack()
        if action:
            label,command=action
            RoundedButton(self,label,command,variant='outline').pack(pady=(8,0))


class LoadingState(tk.Frame):
    def __init__(self,parent,text='Đang tải…'):
        from tkinter import ttk

        super().__init__(parent,bg=UI_COLORS['surface'],padx=14,pady=12)
        tk.Label(self,text=text,bg=UI_COLORS['surface'],fg=UI_COLORS['text']).pack(anchor='w')
        self.progress=ttk.Progressbar(self,mode='indeterminate')
        self.progress.pack(fill='x',pady=(6,0))
        self._job=self.after(65,self._tick)
        self.bind('<Destroy>',self._stop,add='+')

    def _tick(self):
        self.progress.step()
        self._job=self.after(65,self._tick)

    def _stop(self,event):
        if event.widget is self:
            self.after_cancel(self._job)


class Badge(Chip):
    def __init__(self,parent,text,tone='success',**kw):
        super().__init__(parent,text,fg=UI_COLORS[tone],**kw)


class Toast:
    def __init__(self,root,text,duration=2500,action=None):
        self.root=root
        self.frame=tk.Frame(root,bg=UI_COLORS['text'])
        self.label=tk.Label(self.frame,text=text,bg=UI_COLORS['text'],fg='white',
                            padx=16,pady=10,wraplength=500,justify='left')
        self.label.pack(side='left')
        if action:
            caption,callback=action
            def run():
                self.close()
                callback()
            tk.Button(self.frame,text=caption,command=run,takefocus=True).pack(side='right',padx=8)
        self.frame.place(relx=.5,rely=.92,anchor='center')
        self.job=root.after(duration,self.close)
        self.frame.bind('<Destroy>',self._cancel,add='+')

    def _cancel(self,event):
        if event.widget is self.frame and self.job is not None:
            self.root.after_cancel(self.job)
            self.job=None

    def close(self):
        if self.job is not None:
            self.root.after_cancel(self.job)
            self.job=None
        self.frame.destroy()


def _tooltip_work_area(widget, x, y):
    if sys.platform == 'win32':
        import ctypes
        from ctypes import wintypes

        class MonitorInfo(ctypes.Structure):
            _fields_ = [('size', wintypes.DWORD), ('monitor', wintypes.RECT),
                        ('work', wintypes.RECT), ('flags', wintypes.DWORD)]

        user32 = ctypes.windll.user32
        monitor_from_point = user32.MonitorFromPoint
        monitor_from_point.argtypes = (wintypes.POINT, wintypes.DWORD)
        monitor_from_point.restype = wintypes.HMONITOR
        get_monitor_info = user32.GetMonitorInfoW
        get_monitor_info.argtypes = (wintypes.HMONITOR, ctypes.POINTER(MonitorInfo))
        get_monitor_info.restype = wintypes.BOOL
        info = MonitorInfo()
        info.size = ctypes.sizeof(info)
        monitor = monitor_from_point(wintypes.POINT(x, y), 2)  # Nearest monitor.
        if monitor and get_monitor_info(monitor, ctypes.byref(info)):
            rect = info.work
            return rect.left, rect.top, rect.right, rect.bottom
    left, top = widget.winfo_vrootx(), widget.winfo_vrooty()
    return left, top, left + widget.winfo_vrootwidth(), top + widget.winfo_vrootheight()


def _tooltip_position(anchor, size, area):
    x, y, anchor_width, anchor_height = anchor
    width, height = size
    left, top, right, bottom = area
    gap = 5
    if x + width > right:
        x += anchor_width - width
    below = y + anchor_height + gap
    above = y - height - gap
    preferred_y = above if below + height > bottom and above >= top else below
    return max(left, min(x, right - width)), max(top, min(preferred_y, bottom - height))


class Tooltip:
    def __init__(self,widget,text):
        self.widget=widget
        self.text=text
        self.tip=None
        self.job=None
        for event in ('<Enter>','<FocusIn>'):
            widget.bind(event,self.schedule,add='+')
        for event in ('<Leave>','<FocusOut>','<Destroy>'):
            widget.bind(event,self.hide,add='+')

    def schedule(self,event=None):
        self.hide()
        self.job=self.widget.after(350,self.show)

    def show(self,event=None):
        self.job=None
        if not self.widget.winfo_viewable():
            return
        x, y = self.widget.winfo_rootx(), self.widget.winfo_rooty()
        width, height = self.widget.winfo_width(), self.widget.winfo_height()
        area = _tooltip_work_area(self.widget, x + width // 2, y + height // 2)
        tip = self.tip = tk.Toplevel(self.widget)
        tip.withdraw()
        tip.wm_overrideredirect(True)
        tk.Label(tip, text=self.text, bg=UI_COLORS['text'], fg=UI_COLORS['background'],
                 padx=8, pady=5, wraplength=max(1, min(360, area[2] - area[0] - 16)),
                 justify='left').pack()
        tip.update_idletasks()
        if self.tip is not tip:
            return
        x, y = _tooltip_position((x, y, width, height),
                                 (tip.winfo_reqwidth(), tip.winfo_reqheight()), area)
        tip.geometry(f'+{x}+{y}')
        tip.deiconify()

    def hide(self,event=None):
        if self.job is not None:
            self.widget.after_cancel(self.job)
            self.job=None
        if self.tip:
            self.tip.destroy()
            self.tip=None
