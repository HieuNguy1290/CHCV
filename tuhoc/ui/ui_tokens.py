"""Shared visual values for the TuHoc Tk desktop interface."""
from collections.abc import Mapping

_BASE_COLORS = {
    'primary':'#2F7A50', 'primary_dark':'#1F5A3A', 'primary_hover':'#286A45',
    'primary_pressed':'#1F5A3A', 'disabled':'#DDE7DE', 'disabled_text':'#4F6056',
    'text':'#1F3A2B', 'text_muted':'#5B6B60', 'muted':'#5B6B60',
    'border':'#DDE7DE', 'background':'#F8FAF5', 'surface':'#FFFFFF',
    'tint':'#E8F2E9', 'accent':'#FFE58B', 'studying':'#FFF3C4',
    'danger':'#A52D24', 'error':'#A52D24', 'success':'#286A45',
    'warning':'#774710', 'info':'#275B85', 'focus':'#275B85',
    'primary_text':'#2F7A50', 'progress_track':'#E8F2E9',
}
COLORS = _BASE_COLORS.copy()
APPEARANCE_NAMES = {
    'forest': 'Xanh lá',
    'ocean': 'Xanh biển',
    'plum': 'Tím mận',
    'dark': 'Tối',
}
_APPEARANCE_OVERRIDES = {
    'forest': {},
    'ocean': {
        'primary': '#205C91', 'primary_dark': '#16446D', 'primary_hover': '#194F7E',
        'text': '#1C3349', 'text_muted': '#4E6375', 'border': '#D7E3F0',
        'background': '#F3F8FD', 'tint': '#E3EFFA', 'focus': '#1C6495',
    },
    'plum': {
        'primary': '#75456F', 'primary_dark': '#563050', 'primary_hover': '#663B60',
        'text': '#40293D', 'text_muted': '#6B5367', 'border': '#EADCE8',
        'background': '#FCF6FA', 'tint': '#F3E7F2', 'focus': '#78456F',
    },
    'dark': {
        'primary': '#345F94', 'primary_dark': '#254674', 'primary_hover': '#3C69A0',
        'primary_text': '#A9CDFF', 'background': '#111820', 'surface': '#1C2733',
        'tint': '#283A4C', 'border': '#52677B', 'text': '#EBF1F8',
        'text_muted': '#B6C5D4', 'disabled': '#293746', 'disabled_text': '#AEBBC8',
        'studying': '#493B26', 'focus': '#A9CDFF', 'info': '#A9CDFF',
        'danger': '#FFADA7', 'error': '#FFADA7', 'warning': '#FFD28B', 'success': '#98DCB4',
    },
}


def appearance_colors(name):
    if not isinstance(name, str):
        name = 'forest'
    palette = {**_BASE_COLORS, **_APPEARANCE_OVERRIDES.get(name, {})}
    if 'primary_text' not in _APPEARANCE_OVERRIDES.get(name, {}):
        palette['primary_text'] = palette['primary']
    palette['progress_track'] = palette['primary_text'] if name == 'dark' else palette['tint']
    palette['primary_pressed'] = palette['primary_dark']
    palette['muted'] = palette['text_muted']
    return palette


def set_appearance(name):
    COLORS.update(appearance_colors(name))
SIZES = {'caption':11,'body':13,'subtitle':16,'title':20,'display':30}
SPACING = (4,8,12,16,24,32)
RADIUS = {'small':8,'normal':14,'large':20}
ELEVATION = {'flat':0,'raised':2,'overlay':5}
DURATION = {'fast':150,'normal':190,'slow':230}
FONT_FAMILY = 'Segoe UI'
FONT_SCALES = {'small':.9,'medium':1.,'large':1.17}
_scale = FONT_SCALES['medium']


def set_font_scale(choice):
    global _scale
    _scale = FONT_SCALES.get(choice,FONT_SCALES['medium'])


def font_at(size, style='normal'):
    return (FONT_FAMILY,max(1,round(int(size)*_scale)),style)


def font(role, bold=False):
    return font_at(SIZES[role],'bold' if bold else 'normal')


class LegacyFonts(Mapping):
    """Lazy compatibility view so existing consumers see the active text size."""
    roles = {'page':('title',True),'card':('subtitle',True),
             'body':('body',False),'small':('caption',False)}

    def __getitem__(self, key):
        return font(*self.roles[key])

    def __iter__(self):
        return iter(self.roles)

    def __len__(self):
        return len(self.roles)


def contrast_ratio(a,b):
    def luminance(color):
        channels=[int(color[i:i+2],16)/255 for i in (1,3,5)]
        linear=[value/12.92 if value<=.04045 else ((value+.055)/1.055)**2.4 for value in channels]
        return sum(component*weight for component,weight in zip(linear,(.2126,.7152,.0722)))
    lo,hi=sorted((luminance(a),luminance(b)))
    return (hi+.05)/(lo+.05)
