"""Continuous question viewport backed by the regular ExamUI renderers."""

from collections import OrderedDict

import pygame


class ExamDocument:
    def __init__(self):
        self.offset = 0
        self.limit = 0
        self.focus = None
        self.tops = []
        self.heights = []
        self.anchors = []
        self.cache = OrderedDict()

    def frame(self, exam, index):
        question = exam.exam['questions'][index]
        qid = question['id']
        signature = (repr(exam.answers.get(qid)), repr(exam.order_inputs.get(qid)),
                     exam.match_pending, exam.gap_focus if self.focus == index else -1,
                     exam._audio_error)
        cached = self.cache.get(index)
        if cached and cached[0] == signature:
            self.cache.move_to_end(index)
            return cached[1:]
        surface, actions, anchor = exam._render_document_question(question, index)
        self.cache[index] = signature, surface, actions, anchor
        self.cache.move_to_end(index)
        if len(self.cache) > 8:
            self.cache.popitem(last=False)
        return surface, actions, anchor

    def scroll(self, exam, offset):
        self.offset = max(0, min(self.limit, int(offset)))
        if self.tops:
            index = next((i for i, top in enumerate(self.tops)
                          if top + self.heights[i] + 12 > self.offset), len(self.tops) - 1)
            if exam.index != index:
                self.focus = None
                exam.index = index
                exam._sync_nav_page(index)

    def jump(self, exam, index):
        index = max(0, min(len(exam.exam['questions']) - 1, index))
        if self.tops:
            self.offset = min(self.limit, self.tops[index] + self.anchors[index])
        self.select(exam, index)

    def passage_index(self, exam):
        questions = exam.exam['questions']
        for index in range(exam.index, -1, -1):
            if 'fixed_passage' in questions[index]:
                return index if questions[index]['fixed_passage'].strip() else None
        return None

    def go_to_passage(self, exam):
        index = self.passage_index(exam)
        if index is not None and self.tops:
            self.focus = None
            self.scroll(exam, self.tops[index])

    def select(self, exam, index):
        if self.focus != index:
            exam.gap_focus = 0
        self.focus = exam.index = index
        exam._sync_nav_page(index)

    def draw(self, exam, surface):
        area = exam.read_area.copy()
        if not self.tops:
            height = 0
            for index in range(len(exam.exam['questions'])):
                block, _, anchor = self.frame(exam, index)
                self.tops.append(height)
                self.heights.append(block.get_height())
                self.anchors.append(anchor)
                height += block.get_height() + 12
            self.limit = max(0, height - area.height)
        old_clip = surface.get_clip()
        surface.set_clip(area.clip(old_clip))
        try:
            for index, (top, height) in enumerate(zip(self.tops, self.heights)):
                y = area.y + top - self.offset
                if y + height <= area.y or y >= area.bottom:
                    continue
                block, actions, _ = self.frame(exam, index)
                rect = pygame.Rect(area.x + 8, y, block.get_width(), height)
                surface.blit(block, rect)
                if index == exam.index:
                    pygame.draw.rect(surface, (51, 110, 211), rect, 2, border_radius=7)
                for hit, action in actions:
                    visible = hit.move(rect.x, y).clip(area)
                    if visible:
                        exam.buttons.append((visible, lambda i=index, fn=action: self._act(exam, i, fn)))
        finally:
            surface.set_clip(old_clip)
        track = pygame.Rect(area.right - 5, area.y, 5, area.height)
        exam.draw_scrollbar(surface, 'body', track, area.height, self.offset, self.limit)

    def _act(self, exam, index, action):
        self.select(exam, index)
        action()
