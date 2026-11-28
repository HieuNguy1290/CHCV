"""Presentation-only lesson map; existing learning and DB APIs remain authoritative."""
from tuhoc.ui.ui_tokens import COLORS as TOKEN_COLORS, font_at
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
import math
from tuhoc.ui.theme_config import UI_COLORS as C
from tuhoc.ui.ui_components import Card, Chip, ProgressBar, Tooltip, Toast, bind_hover
from tuhoc.lessons.lesson_display_names import display_name
from tuhoc.ui.ui_keys import GRID_MOVES, keyboard_button


class _TopicScrollIndicator(tk.Canvas):
    """Slim draggable indicator for the topic strip's horizontal viewport."""

    def __init__(self,parent,topics):
        super().__init__(parent,height=14,highlightthickness=0,bg=C['background'],
                         cursor='hand2',takefocus=True)
        self.topics=topics
        self.first,self.last=0.0,1.0
        self.grab_offset=None
        self.track=self.create_line(0,7,0,7,width=3,capstyle='round')
        self.thumb=self.create_line(0,7,0,7,width=5,capstyle='round')
        self.bind('<Configure>',self._paint)
        self.bind('<Button-1>',self._press)
        self.bind('<B1-Motion>',self._drag)
        self.bind('<ButtonRelease-1>',self._release)
        for event in ('<Enter>','<Leave>','<FocusIn>','<FocusOut>'):
            self.bind(event,self._paint)
        self.bind('<Left>',lambda _e:self._step(-1))
        self.bind('<Right>',lambda _e:self._step(1))

    def set(self,first,last):
        self.first,self.last=float(first),float(last)
        if self.last-self.first>=0.99999:
            self.grab_offset=None
            self.pack_forget()
            return
        if not self.winfo_manager():
            self.pack(fill='x',pady=(1,0))
        self._paint()

    def _geometry(self):
        width=max(1,self.winfo_width()-16)
        visible=min(1.0,self.last-self.first)
        thumb_width=min(width,max(38,width*visible))
        travel=width-thumb_width
        left=8+travel*min(1.0,self.first/max(1e-8,1-visible))
        return width,thumb_width,travel,left

    def _paint(self,event=None):
        if not self.winfo_manager():
            return
        width,thumb_width,_,left=self._geometry()
        inside=0<=self.winfo_pointerx()-self.winfo_rootx()<self.winfo_width() and (
            0<=self.winfo_pointery()-self.winfo_rooty()<self.winfo_height())
        active=self.grab_offset is not None or inside or self.focus_get() is self
        base=self.winfo_rgb(C['background'])
        accent=self.winfo_rgb(C['primary_text'])
        def blend(opacity):
            return '#{:02x}{:02x}{:02x}'.format(*[round((a+(b-a)*opacity)/257) for a,b in zip(base,accent)])
        self.coords(self.track,8,7,8+width,7)
        self.coords(self.thumb,left,7,left+thumb_width,7)
        self.itemconfigure(self.track,fill=blend(.16))
        self.itemconfigure(self.thumb,fill=blend(.87 if active else .60))

    def _press(self,event):
        self.focus_set()
        _,width,_,left=self._geometry()
        self.grab_offset=event.x-left if left<=event.x<=left+width else width/2
        self._drag(event)
        return 'break'

    def _drag(self,event):
        if self.grab_offset is not None:
            _,_,travel,_=self._geometry()
            if travel>0:
                fraction=max(0,min(1,(event.x-8-self.grab_offset)/travel))
                self.topics.xview_moveto(fraction*(1-self.last+self.first))
            self._paint()
        return 'break'

    def _release(self,_event):
        self.grab_offset=None
        self._paint()

    def _step(self,direction):
        self.topics.xview_scroll(direction,'units')
        return 'break'


class LessonMap:
    def __init__(self, app, map_mode=False):
        self.app=app; self.map_mode=map_mode; self.jobs=[]; self._level_animation=0; self._tip=None; self._tip_job=None
        self.themes=list(app._themes())
        self.theme=getattr(app,'_lesson_map_theme',None)
        if self.theme not in [x[0] for x in self.themes]: self.theme=self.themes[0][0] if self.themes else None
        self.level=getattr(app,'_lesson_map_level',1)
        self.body=app.layout('Bản đồ Level' if map_mode else 'Bài học')
        self.body.bind('<Destroy>',self._destroy,add='+')
        self.build()

    def _destroy(self,event):
        if event.widget is self.body:
            for job in self.jobs:
                try:self.app.after_cancel(job)
                except (tk.TclError,RuntimeError):pass
            self.jobs.clear()

    def later(self,ms,fn):
        def wrapped():
            if self.body.winfo_exists():fn()
        if getattr(self.app,'reduce_motion',False):
            wrapped()
        else:
            self.jobs.append(self.app.after(ms,wrapped))

    def label(self,parent,text,size=11,bold=False,fg=None,bg=None,**kw):
        return tk.Label(parent,text=text,font=font_at(size,'bold' if bold else 'normal'),bg=bg or parent.cget('bg'),fg=fg or C['text'],**kw)

    def build(self):
        if not self.theme:return
        title_lbl=next((c for c in self.body.winfo_children() if isinstance(c,tk.Label)),None)
        if title_lbl is not None:
            title_fg=str(title_lbl.cget('fg'));title_bg=str(title_lbl.cget('bg'))
            title_lbl.configure(fg=title_bg)
        head=tk.Frame(self.body,bg=C['background']);head.pack(fill='x',pady=(0,12))
        topic_lbl=self.label(head,'Chủ đề · Topics',13,True,fg=C['background']);topic_lbl.pack(side='left')
        self._topic_picker=ttk.Combobox(head,values=[title for _,title,_,_ in self.themes],
                                       state='readonly',width=26)
        self._topic_picker.pack(side='right')
        self._topic_picker.bind('<<ComboboxSelected>>',
                                self._select_topic)
        strip=tk.Frame(self.body,bg=C['background']);strip.pack(fill='x',pady=(0,12))
        cv=tk.Canvas(strip,height=56,bg=C['background'],highlightthickness=0,xscrollincrement=0)
        bar=_TopicScrollIndicator(strip,cv)
        cv.configure(xscrollcommand=bar.set)
        cv.pack(fill='x');inner=tk.Frame(cv,bg=C['background']);window=cv.create_window((0,0),window=inner,anchor='nw')
        inner.bind('<Configure>',lambda _e:cv.configure(scrollregion=cv.bbox('all')))
        self._topic_canvas=cv
        topic_chips=[]
        chip_sizes=[]
        for code,title,icon,color in self.themes:
            selected=code==self.theme
            base_bg=C['primary'] if selected else C['tint']
            base_fg='white' if selected else C['text']
            # A fixed-size slot isolates this chip from its neighbours.
            slot=tk.Frame(inner,bg=C['background'])
            chip=Chip(slot,text=f'{icon}  {title}',bg=base_bg,fg=base_fg,
                      cursor='hand2',takefocus=1)
            chip.configure(bd=0,relief='flat',highlightthickness=2,highlightcolor=C['focus'])
            slot.pack_propagate(False)
            slot.pack(side='left',padx=(0,4))
            chip_sizes.append((slot,chip))
            chip._hover_active=False
            chip._code=code
            chip._target=(base_bg,base_fg)
            chip.configure(bg=C['background'],fg=C['background'])
            topic_chips.append(chip)
            chip.bind('<Button-1>',lambda e,t=code:self.change_theme(t))
            chip.bind('<Return>',lambda e,t=code:self.change_theme(t))
            chip.bind('<space>',lambda e,t=code:self.change_theme(t))
            wheels=('<MouseWheel>','<Shift-MouseWheel>','<Button-4>','<Button-5>')
            for widget in (slot,chip):
                for sequence in wheels:
                    widget.bind(sequence,self._scroll_topics,add='+')
            # The same topic strip appears in both Lessons and Level Map.
            # Keep the active topic visibly selected while hovering others.
            def topic_hover(active, widget=chip, tcode=code):
                try:
                    if not widget.winfo_exists(): return
                    # Selection is read live so changing topic never rebuilds the strip.
                    is_selected=(tcode==self.theme)
                    normal_bg=C['primary'] if is_selected else C['tint']
                    normal_fg='white' if is_selected else C['text']
                    widget.configure(
                        bg=(C['primary_hover'] if is_selected else C['tint']) if active else normal_bg,
                        fg='white' if is_selected else (C['primary_text'] if active else normal_fg),
                        relief='flat', bd=0)
                    widget._hover_active=active
                    # Only the chip moves; its fixed slot never changes size.
                    widget.place_configure(y=6 if active else 12)
                except tk.TclError:
                    pass
            # Hover region is the fixed union of the rest/raised chip area.
            chip._hover_fn=topic_hover
            chip.bind('<FocusIn>',lambda _e,w=chip:self._reveal_topic(w),add='+')
            chip.bind('<FocusIn>',lambda e,fn=topic_hover:fn(True),add='+')
            chip.bind('<FocusOut>',lambda e,fn=topic_hover:fn(False),add='+')
        self.body.update_idletasks()
        for slot,chip in chip_sizes:
            width,height=chip.winfo_reqwidth(),chip.winfo_reqheight()
            slot_h=max(56,height+18)
            slot.configure(width=width+4,height=slot_h)
            chip.place(x=2,y=12,width=width,height=height)
            bind_hover(slot,chip._hover_fn,inset=(0,6,0,max(0,slot_h-(12+height))))
        cv.configure(height=max((slot.winfo_reqheight() for slot,_ in chip_sizes),default=56))
        for sequence in ('<MouseWheel>','<Shift-MouseWheel>','<Button-4>','<Button-5>'):
            cv.bind(sequence,self._scroll_topics,add='+')
        self._chips=topic_chips
        self._sync_topic_picker()
        cv.after_idle(self._sync_topic_picker)
        columns=tk.Frame(self.body,bg=C['background']);columns.pack(fill='both',expand=True)
        columns.grid_columnconfigure(0,weight=1);columns.grid_columnconfigure(1,minsize=400)
        left=tk.Frame(columns,bg=C['background']);left.grid(row=0,column=0,sticky='nsew',padx=(0,16))
        right=Card(columns);right.grid(row=0,column=1,sticky='nsew')
        self.grid_holder=left;self.details=right
        self._field_final=(right.cget('bg'),right.cget('highlightbackground'))
        right.configure(bg=C['background'],highlightbackground=C['background'])
        level_lbl=self.label(left,'Chọn Level · Select a level',14,True,fg=C['background']);level_lbl.pack(anchor='w',pady=(0,8))
        self._level_lbl=level_lbl
        self.level_grid=tk.Frame(left,bg=C['background']);self.level_grid.pack(fill='both',expand=True)
        foot_lbl=self.label(left,'Công Cha Nghĩa Mẹ. Con mãi khắc ghi.',10,fg=C['background']);foot_lbl.pack(anchor='w',pady=6)
        self._foot_lbl=foot_lbl
        # Intro choreography (ms): topic text -> +100 chips -> +150 level text ->
        # +100 level cards slide (50 apart) -> +150 lesson field -> +100 lesson
        # text -> +100 lesson rows slide (100 apart).
        bg0=C['background'];FADE=100
        t=0
        if title_lbl is not None:
            self.fade_text(title_lbl,title_fg,title_bg,t,FADE);t+=FADE+100
            self.fade_text(topic_lbl,C['text'],bg0,t,FADE);t+=FADE+100
        t=self.animate_topics(topic_chips,t)+150
        self.fade_text(level_lbl,C['text'],bg0,t,FADE);t+=FADE
        self.fade_field(self.details,t,FADE);t+=FADE
        text_start=t;t+=FADE+100
        cards_end=self.draw_levels(delay=t)
        rows_end=self.draw_detail(intro=(text_start,t))
        self.fade_text(foot_lbl,C['muted'],bg0,max(cards_end,rows_end)+100,FADE)
        self.body.bind('<Left>',lambda e:self.move(-1),add='+')
        self.body.bind('<Right>',lambda e:self.move(1),add='+')
        self.body.bind('<Up>',lambda e:self.move(-5),add='+')
        self.body.bind('<Down>',lambda e:self.move(5),add='+')
        self.body.bind('<Return>',lambda e:self.select(self.level),add='+')
        self.body.bind('<Escape>',lambda e:self.app.home(),add='+')

    def _scroll_topics(self,event):
        canvas=self._topic_canvas
        first,last=canvas.xview()
        if last-first>=1:
            return None
        direction=-1 if getattr(event,'num',None)==4 or event.delta>0 else 1
        canvas.xview_scroll(direction,'units')
        return 'break'

    def _reveal_topic(self,chip):
        canvas=self._topic_canvas
        bounds=canvas.bbox('all')
        if not bounds or canvas.winfo_width()<=1:
            return
        edge=canvas.canvasx(0)
        left=chip.master.winfo_x()
        right=left+chip.master.winfo_width()
        width=canvas.winfo_width()
        if left<edge:
            canvas.xview_moveto(left/max(1,bounds[2]))
        elif right>edge+width:
            canvas.xview_moveto(max(0,right-width)/max(1,bounds[2]))

    def _sync_topic_picker(self):
        for index,chip in enumerate(self._chips):
            if chip._code==self.theme:
                self._topic_picker.current(index)
                self._reveal_topic(chip)
                break

    def _select_topic(self,_event):
        index=self._topic_picker.current()
        if index>=0:
            self.change_theme(self.themes[index][0])

    def fade_text(self,lbl,fg,bg,start,dur=240):
        steps=8
        lbl.configure(fg=bg)
        for i in range(steps+1):
            self.later(start+int(dur*i/steps),lambda w=lbl,f=i/steps:w.configure(fg=self._blend_color(bg,fg,f)) if w.winfo_exists() else None)

    def fade_field(self,widget,start,dur=240):
        steps=8;bg=C['background']
        fill,edge=self._field_final
        widget.configure(bg=bg,highlightbackground=bg)
        for i in range(steps+1):
            self.later(start+int(dur*i/steps),lambda w=widget,f=i/steps:w.configure(bg=self._blend_color(bg,fill,f),highlightbackground=self._blend_color(bg,edge,f)) if w.winfo_exists() else None)

    def animate_topics(self, chips, delay=0):
        # Each topic fades in only as its single travelling wave reaches it.
        # Animate the original widget, without copies or repeated bounce cycles.
        offsets=(0, -2, -5, -8, -5, -2, 0)
        steps=len(offsets)-1
        background=C['background']
        for index, chip in enumerate(chips):
            target_bg,target_fg=chip._target
            chip.configure(bg=background, fg=background)
            for frame, offset in enumerate(offsets):
                fraction=frame/steps
                def update(widget=chip, dy=offset, t=fraction,
                           bg=target_bg, fg=target_fg):
                    if not widget.winfo_exists(): return
                    if not widget._hover_active:
                        widget.configure(
                            bg=self._blend_color(background,bg,t),
                            fg=self._blend_color(background,fg,t))
                    # Wave and hover share the same fixed coordinate system.
                    widget.place_configure(y=(6 if widget._hover_active else 12+dy))
                self.later(delay+min(index,5)*60+frame*38,update)
        return delay+min(max(0,len(chips)-1),5)*60+steps*38

    def _blend_color(self, start, end, fraction):
        # Tk resolves both named colors (e.g. white) and hexadecimal colors.
        first = self.body.winfo_rgb(start)
        last = self.body.winfo_rgb(end)
        fraction = max(0.0, min(1.0, fraction))
        rgb = [round((x + (y - x) * fraction) / 257) for x, y in zip(first, last)]
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    def animate_levels(self, cards, generation, delay=0):
        # Each card slides in from the left while fading from 0% to 100%.
        background=C['background']
        steps=9;dist=28
        for card, base, n, thickness in cards:
            card.configure(bg=background,highlightbackground=background)
            for child in card.winfo_children():
                if isinstance(child,tk.Label):
                    child.configure(bg=background,fg=background)
        for index, (card, base, n, thickness) in enumerate(cards):
            for step in range(steps+1):
                t=step/steps;ease=1-(1-t)**2
                def update(widget=card, target=base, num=n, thick=thickness,
                           t=t, ease=ease, token=generation, last=(step==steps)):
                    if token!=self._level_animation or not widget.winfo_exists():return
                    if last:widget._ready=True
                    if getattr(widget,'_hover',False):return
                    fill=self._blend_color(background,target,t)
                    outline=self._blend_color(background,self._edge(num),t)
                    widget.configure(bg=fill,highlightbackground=outline,highlightthickness=thick)
                    widget.place_configure(x=-round(dist*(1-ease)))
                    for child in widget.winfo_children():
                        if isinstance(child,tk.Label):
                            child.configure(bg=fill,fg=self._blend_color(background,child._fade_fg,t))
                self.later(delay+index*50+step*25,update)
        return delay+max(0,len(cards)-1)*50+steps*25

    def status(self,level):
        sid=self.app.student['id'];code=self.theme
        done=bool(self.app.db.lesson_completed(sid,f'{code}_{level}'))
        unlocked=bool(self.app.learning.unlocked(sid,code,level))
        return ('Done' if done else 'Current' if unlocked else 'Locked'),done,unlocked

    def _edge(self,n):
        done,unlocked=self._info[n]
        return C['primary'] if n==self.level else '#C99A24' if unlocked and not done else C['border']

    def _tip_hide(self):
        if self._tip_job:
            try:self.app.after_cancel(self._tip_job)
            except (tk.TclError,RuntimeError):pass
            self._tip_job=None
        if self._tip is not None:
            try:self._tip.destroy()
            except tk.TclError:pass
            self._tip=None

    def _tip_show(self,n):
        # Delayed tip placed beside the pointer (never under it), driven by the
        # same stable hover state, so it cannot trigger Enter/Leave loops.
        self._tip_hide()
        if self._info[n][1]:return
        def go():
            self._tip_job=None
            card,_=self._cards[n]
            if not card.winfo_exists() or not getattr(card,'_hover',False):return
            x,y=card.winfo_pointerxy()
            tip=tk.Toplevel(card);tip.wm_overrideredirect(True);tip.geometry(f'+{x+16}+{y+22}')
            tk.Label(tip,text='Cần hoàn thành level trước để mở khóa.',bg=C['surface'],fg=C['text'],padx=8,pady=5).pack()
            self._tip=tip
        self._tip_job=self.app.after(350,go)

    def _level_hover(self,n,active):
        card,base=self._cards[n]
        if not card.winfo_exists() or not getattr(card,'_ready',False):return
        card._hover=active
        if active:self._tip_show(n)
        else:self._tip_hide()
        color=C['tint'] if active else base
        card.configure(bg=color,highlightbackground=C['primary'] if active else self._edge(n))
        for child in card.winfo_children():child.configure(bg=color)
        # Zoom: only the card grows inside its fixed slot; the grid never reflows.
        if active:
            card.lift()
            card.place_configure(x=-5,y=-5,relwidth=1,relheight=1,width=10,height=10)
        else:
            card.place_configure(x=0,y=0,relwidth=1,relheight=1,width=0,height=0)

    def draw_levels(self,animate=True,delay=0):
        self._level_animation+=1
        generation=self._level_animation
        cards=[];self._cards={};self._info={};self._titles=[]
        for w in self.level_grid.winfo_children():w.destroy()
        maximum=self.app._max_level(self.theme)
        if self.level>maximum or self.level<1 or not self.app.learning.unlocked(self.app.student['id'],self.theme,self.level):
            self.level=next((n for n in range(1,maximum+1) if self.app.learning.unlocked(self.app.student['id'],self.theme,n) and not self.app.db.lesson_completed(self.app.student['id'],f'{self.theme}_{n}')),1)
        for col in range(5):self.level_grid.grid_columnconfigure(col,weight=1)
        for n in range(1,maximum+1):
            text,done,unlocked=self.status(n)
            bg=C['tint'] if done else C['studying'] if unlocked else C['disabled']
            edge=C['primary'] if n==self.level else '#C99A24' if unlocked and not done else C['border']
            slot=tk.Frame(self.level_grid,bg=C['background'],width=10)
            slot.grid(row=(n-1)//5,column=(n-1)%5,padx=5,pady=5,sticky='nsew')
            card=tk.Frame(self.level_grid,bg=bg,highlightbackground=edge,highlightthickness=2,
                          highlightcolor=C['focus'],takefocus=True,cursor='hand2')
            card._ready=False
            self._cards[n]=(card,bg);self._info[n]=(done,unlocked)
            cards.append((card,bg,n,2))
            title_lbl=self.label(card,display_name(self.app.curriculum.data_dir, 'level', self.theme, n),13,True,bg=bg)
            title_lbl.pack(pady=(13,5))
            self._titles.append((slot,title_lbl))
            self.label(card,text,9,bg=bg).pack()
            self.label(card,'100%' if done else '0%',9,fg=C['muted'],bg=bg).pack(pady=(5,0))
            card.configure(bg=C['background'],highlightbackground=C['background'])
            for child in card.winfo_children():
                child._fade_fg=child.cget('fg')
                child.configure(bg=C['background'],fg=C['background'])
            card.place(in_=slot,x=-28,y=0,relwidth=1,relheight=1)
            for widget in [card,*card.winfo_children()]:
                widget.bind('<Button-1>',lambda e,k=n:self.select(k))
            def focus_level(event,origin=n):
                target=max(1,min(maximum,origin+GRID_MOVES[event.keysym]))
                self._cards[target][0].focus_set()
                return 'break'
            for key in GRID_MOVES:
                card.bind('<'+key+'>',focus_level)
            def activate(_event,level=n):
                self.select(level)
                return 'break'
            card.bind('<Return>',activate)
            card.bind('<space>',activate)
            bind_hover(card,lambda a,k=n:self._level_hover(k,a),region=slot,also=(slot,))
        self.body.update_idletasks()
        for (slot,_title),(card,*_rest) in zip(self._titles,cards):
            slot.configure(height=card.winfo_reqheight()+9)
        end=self.animate_levels(cards,generation,delay)
        # Fit names once, while the cards are still at 0% opacity.
        self.body.update_idletasks()
        self.fit_titles()
        if not getattr(self,'_fit_bound',False):
            self._fit_bound=True;self._fit_job=None;self._fit_w=self.level_grid.winfo_width()
            self.level_grid.bind('<Configure>',self._refit,add='+')
        return end

    def fit_titles(self):
        fonts=getattr(self,'_fonts',None)
        if fonts is None:fonts=self._fonts={}
        for slot,lbl in self._titles:
            try:
                avail=slot.winfo_width()-20
                if avail<40:continue
                text=lbl.cget('text')
                for size in range(13,7,-1):
                    f=fonts.get(size) or fonts.setdefault(size,tkfont.Font(family='Segoe UI',size=size,weight='bold'))
                    if f.measure(text)<=avail:break
                if getattr(lbl,'_size',None)!=size:
                    lbl._size=size;lbl.configure(font=('Segoe UI',size,'bold'))
            except tk.TclError:pass

    def _refit(self,e):
        # Debounced: only re-fit after the window width has settled.
        if e.width==self._fit_w:return
        self._fit_w=e.width
        if self._fit_job:
            try:self.app.after_cancel(self._fit_job)
            except (tk.TclError,RuntimeError):pass
        self._fit_job=self.app.after(200,lambda:self.body.winfo_exists() and self.fit_titles())

    def change_theme(self,code):
        # Keep the page and the topic strip; only levels and lessons replay their flow.
        if code==self.theme:return
        self.app._lesson_map_theme=code;self.app._lesson_map_level=1
        self.theme=code;self.level=1
        self._sync_topic_picker()
        for chip in self._chips:
            if not chip.winfo_exists():continue
            selected=chip._code==code
            chip.configure(bg=C['primary'] if selected else C['tint'],fg='white' if selected else C['text'])
            if chip._hover_active:chip._hover_fn(True)
        self._play_level_flow()

    def _play_level_flow(self):
        for job in self.jobs:
            try:self.app.after_cancel(job)
            except (tk.TclError,RuntimeError):pass
        self.jobs.clear()
        self._tip_hide()
        bg0=C['background'];FADE=240
        # Hide the old panels before anything can repaint.
        for w in self.details.winfo_children():w.destroy()
        self.details.configure(bg=bg0,highlightbackground=bg0)
        self._level_lbl.configure(fg=bg0);self._foot_lbl.configure(fg=bg0)
        t=0
        self.fade_text(self._level_lbl,C['text'],bg0,t,FADE)
        self.fade_field(self.details,t,FADE)
        text_start=t;t+=FADE+100
        cards_end=self.draw_levels(delay=t)
        rows_end=self.draw_detail(intro=(text_start,t))
        self.fade_text(self._foot_lbl,C['muted'],bg0,max(cards_end,rows_end)+100,FADE)

    def move(self,delta):
        self.select(max(1,min(self.app._max_level(self.theme),self.level+delta)))

    def select(self,n):
        if not self.app.learning.unlocked(self.app.student['id'],self.theme,n):
            Toast(self.app,'Level đang khóa');return
        morph=getattr(self.app,'morph',None)
        animate=morph is not None and n!=self.level
        if animate:
            morph.begin(self._cards[n][0],'level-detail',f'Level {n}')
        self.level=n;self.app._lesson_map_level=n;self.app._lesson_map_theme=self.theme
        # Restyle in place: no widget rebuild, no re-fade, no flicker.
        for k,(card,base) in self._cards.items():
            if not getattr(card,'_hover',False):
                card.configure(highlightbackground=self._edge(k))
        self.draw_detail()
        if animate:
            morph.arrive('level-detail',self.details)

    def open_lesson(self,lesson,mode,anchor=None):
        self.app._lesson_map_theme=self.theme;self.app._lesson_map_level=self.level
        self.app._selected_lesson=lesson
        if hasattr(self,'_lesson_list_canvas'):
            self.app._lesson_list_scroll=(self.theme,self.level,self._lesson_list_canvas.yview()[0])
        morph=getattr(self.app,'morph',None)
        if morph and mode=='lesson':
            morph.begin(anchor,'lesson-heading',f'Lesson {lesson}')
        action=self.app.level_lesson if mode=='lesson' else self.app.level_quiz
        action(self.theme,self.level)

    def _lesson_total(self,theme,level):
        try:return max(1,int(self.app._lesson_count(theme,level)))
        except Exception:return 10

    def draw_detail(self,intro=None):
        """intro=(text_start,rows_start) in ms plays the entrance; None shows instantly."""
        for w in self.details.winfo_children():w.destroy()
        content=tk.Frame(self.details,bg=C['surface'])
        title=next((x[1] for x in self.themes if x[0]==self.theme),self.theme)
        head1=self.label(content,f"{display_name(self.app.curriculum.data_dir, 'level', self.theme, self.level)} · {title}",16,True,bg=C['surface'],wraplength=355)
        head1.pack(anchor='w')
        head2=self.label(content,'Góc học tập!',10,fg=C['muted'],bg=C['surface'])
        head2.pack(anchor='w',pady=(4,12))
        canvas=tk.Canvas(content,bg=C['surface'],highlightthickness=0,width=360,height=410)
        self._lesson_list_canvas=canvas
        canvas.pack(fill='both',expand=True,side='left')
        bar=tk.Scrollbar(content,orient='vertical',command=canvas.yview);bar.pack(side='right',fill='y')
        canvas.configure(yscrollcommand=bar.set)
        list_frame=tk.Frame(canvas,bg=C['surface']);canvas.create_window((0,0),window=list_frame,anchor='nw')
        offset=getattr(self.app,'_lesson_list_scroll',None)
        def update_region(_event):
            nonlocal offset
            canvas.configure(scrollregion=canvas.bbox('all'))
            if offset and offset[:2]==(self.theme,self.level):
                canvas.yview_moveto(offset[2])
                offset=None
        list_frame.bind('<Configure>',update_region)
        completed=self.app.db.lesson_completed(self.app.student['id'],f'{self.theme}_{self.level}')
        unlocked=self.app.learning.unlocked(self.app.student['id'],self.theme,self.level)
        items=[]
        lesson_total=self._lesson_total(self.theme,self.level)
        for i in range(1,lesson_total+1):
            slot=tk.Frame(list_frame,bg=C['surface'],width=10)
            slot.pack(fill='x',pady=3,padx=(0,6))
            row=tk.Frame(list_frame,bg=C['surface'],highlightthickness=1,highlightbackground=C['border'],padx=9,pady=7)
            accent=tk.Frame(row,bg=C['surface'],width=4);accent.place(x=0,y=0,relheight=1)
            # Legacy completion is tracked at theme/level granularity, not by lesson index.
            status='Xong' if completed else 'Đang học' if unlocked else 'Chưa mở'
            self.label(row,display_name(self.app.curriculum.data_dir, 'lesson', self.theme, self.level, i),11,True,bg=C['surface']).pack(anchor='w')
            self.label(row,status,9,fg=C['muted'],bg=C['surface']).pack(anchor='w')
            actions=tk.Frame(row,bg=C['surface']);actions.pack(fill='x',pady=(5,0))
            for mode,text in [('lesson','Học'),('quiz','Bài tập')]:
                b=tk.Button(actions,text=text,font=font_at(10, 'bold'),bg=C['surface'] if mode=='lesson' else C['primary'],fg=C['primary_text'] if mode=='lesson' else 'white',relief='solid',bd=1,padx=12,pady=5,cursor='hand2' if unlocked else 'arrow',state='normal' if unlocked else 'disabled',command=lambda k=i,m=mode,w=row:self.open_lesson(k,m,w))
                b.pack(side='left',padx=(0,8))
                keyboard_button(b)
                b.configure(highlightcolor=C['focus'])
                if unlocked:
                    base=C['surface'] if mode=='lesson' else C['primary']
                    over=C['tint'] if mode=='lesson' else C['primary_hover']
                    b.bind('<Enter>',lambda e,w=b,color=over:w.configure(bg=color),add='+')
                    b.bind('<Leave>',lambda e,w=b,color=base:w.configure(bg=color),add='+')
                    b.bind('<FocusIn>',lambda e,w=b,color=over:w.configure(bg=color),add='+')
                    b.bind('<FocusOut>',lambda e,w=b,color=base:w.configure(bg=color),add='+')
                else:Tooltip(b,'Level chưa mở khóa')
            def hover_row(_event, active, holder=row, accent=accent):
                try:
                    if not holder.winfo_exists() or not holder.place_info():return
                    color=C['tint'] if active else C['surface']
                    # Shift right 4px by moving the row inside its fixed slot.
                    holder.place_configure(x=4 if active else 0)
                    holder.configure(bg=color,highlightbackground=C['primary'] if active else C['border'])
                    for child in holder.winfo_children():
                        if child is accent:
                            child.configure(bg=C['primary'] if active else C['surface'])
                        elif isinstance(child,(tk.Label,tk.Frame)):
                            child.configure(bg=color)
                except tk.TclError: pass
            bind_hover(row,lambda a,fn=hover_row:fn(None,a),region=slot,also=(slot,))
            row.lesson_morph_key=f'lesson-row:{i}'
            items.append((row,slot))
        self.body.update_idletasks()
        for row,slot in items:
            slot.configure(width=row.winfo_reqwidth()+4,height=row.winfo_reqheight())
        def put(row,slot,x):
            if row.winfo_exists() and slot.winfo_exists():
                row.place(in_=slot,x=x,y=0,relheight=1,relwidth=1,width=-4)
                morph=getattr(self.app,'morph',None)
                if morph and x==0:
                    morph.arrive(row.lesson_morph_key,row)
        if intro is None:
            content.pack(fill='both',expand=True)
            for row,slot in items:put(row,slot,0)
            return
        text_start,rows_start=intro
        def show():
            if content.winfo_exists():content.pack(fill='both',expand=True)
        self.later(text_start,show)
        self.fade_text(head1,C['text'],'white',text_start)
        self.fade_text(head2,C['muted'],'white',text_start)
        # Rows slide in from the left edge of the field, 100 ms apart.
        steps=8;dist=60
        for index,(row,slot) in enumerate(items):
            for step in range(steps+1):
                t=step/steps;x=-round(dist*(1-(1-(1-t)**2)))
                self.later(rows_start+index*100+step*25,lambda r=row,sl=slot,x=x:put(r,sl,x))
        return rows_start+max(0,len(items)-1)*100+steps*25
