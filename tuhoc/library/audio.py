"""Local audio playback and waveform decoding for dictation."""
import shutil
import subprocess
import sys
from array import array
from pathlib import Path


def speak_article(app, article, content=None):
    """Use the article's language for the application's speech callback."""
    former = app.lang
    app.lang = 'vi' if article['subject'] == 'tieng_viet' else 'en'
    try:
        app._speak(article['body'] if content is None else content)
    finally:
        app.lang = former


# Decode only a low-rate mono preview for lightweight waveform visualization.
_WAVE_CACHE = {}

def waveform_peaks(path, bars=320):
    """Return 0..1 peak levels derived from the real MP3/WAV waveform.

    The preview uses ffmpeg to decode the actual audio file to a mono PCM stream,
    then samples peak values per bar. The shaping keeps transients sharp so the UI
    looks closer to a modern editing/player waveform instead of rounded equalizer bars.
    """
    source = Path(path)
    stat = source.stat()
    key = (str(source.resolve()), stat.st_mtime_ns, stat.st_size, bars)
    if key in _WAVE_CACHE:
        return _WAVE_CACHE[key]
    ffmpeg = shutil.which('ffmpeg')
    if not ffmpeg:
        try:
            import imageio_ffmpeg
            ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        except (ImportError, OSError):
            return None
    command = [ffmpeg, '-nostdin', '-v', 'error', '-i', str(source), '-vn',
               '-ac', '1', '-ar', '1000', '-f', 's16le', '-acodec', 'pcm_s16le', 'pipe:1']
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=45, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0 or len(result.stdout) < 2:
        return None
    samples = array('h')
    samples.frombytes(result.stdout[:len(result.stdout) // 2 * 2])
    if not samples:
        return None
    size = len(samples)
    raw_peaks = []
    for index in range(bars):
        a = int(index * size / bars)
        b = max(a + 1, int((index + 1) * size / bars))
        chunk = samples[a:b]
        peak = max(abs(v) for v in chunk) / 32768
        raw_peaks.append(peak)
    if not raw_peaks:
        return None
    sorted_peaks = sorted(raw_peaks)
    ref = sorted_peaks[max(0, int(len(sorted_peaks) * 0.96) - 1)] or max(raw_peaks) or 1.0
    floor = min(raw_peaks)
    span = max(ref - floor, 1e-6)
    shaped = []
    for value in raw_peaks:
        normalized = max(0.0, min(1.0, (value - floor) / span))
        # Keep the waveform crisp: lower values remain visible but peaks stay sharp.
        shaped.append(max(0.06, normalized ** 1.18))
    if len(_WAVE_CACHE) > 25:
        _WAVE_CACHE.clear()
    _WAVE_CACHE[key] = shaped
    return shaped


class MP3Player:
    """Local audio playback with position, duration, pause and seek."""
    def __init__(self, *, allow_ogg=False):
        self.alias='tuhoc_dictation';self.active=False;self.paused=False
        self.allow_ogg = allow_ogg
        self._pygame=False;self._duration=0;self._offset=0;self._started=0

    def _mci(self, command, query=False):
        import ctypes
        buffer=ctypes.create_unicode_buffer(256) if query else None
        err=ctypes.windll.winmm.mciSendStringW(command,buffer,256 if query else 0,None)
        if err:
            text=ctypes.create_unicode_buffer(256)
            ctypes.windll.winmm.mciGetErrorStringW(err,text,256)
            raise RuntimeError(f'Lỗi phát MP3 ({err}): {text.value}')
        return buffer.value if query else ''

    def play(self,path):
        self.stop()
        path=Path(path).resolve()
        if not path.is_file():raise FileNotFoundError('Không tìm thấy file nghe: '+str(path))
        if sys.platform=='win32' and not (self.allow_ogg and path.suffix.lower() == '.ogg'):
            try:
                kind=' type mpegvideo' if path.suffix.lower()=='.mp3' else ''
                self._mci(f'open "{path}"{kind} alias {self.alias}')
                self.active=True
                self._mci(f'set {self.alias} time format milliseconds')
                self._duration=int(self._mci(f'status {self.alias} length',True))
                self._mci(f'play {self.alias} from 0')
            except Exception:
                self.stop();raise
        else:
            try:
                import pygame
            except ImportError as exc:raise RuntimeError('Cài pygame: pip install pygame') from exc
            if not pygame.mixer.get_init():pygame.mixer.init()
            pygame.mixer.music.load(str(path));pygame.mixer.music.play()
            self._pygame=True;self.active=True
            self._duration=0
            try:
                from mutagen import File
                metadata=File(path)
                if metadata is not None and metadata.info:
                    self._duration = int(metadata.info.length * 1000)
            except (ImportError,OSError,ValueError):pass
            self._offset=0
        self.paused=False

    def duration_ms(self):return max(0,self._duration)

    def position_ms(self):
        if not self.active:return 0
        if not self._pygame:
            try:return max(0,int(self._mci(f'status {self.alias} position',True)))
            except RuntimeError:return 0
        import pygame
        position=pygame.mixer.music.get_pos()
        return max(0,self._offset+(position if position>=0 else 0))

    def is_finished(self):
        if not self.active or self.paused:return False
        if not self._pygame:
            try:return self._mci(f'status {self.alias} mode',True).lower()=='stopped'
            except RuntimeError:return False
        import pygame
        return not pygame.mixer.music.get_busy()

    def pause(self):
        if not self.active or self.paused:return
        if not self._pygame:self._mci(f'pause {self.alias}')
        else:
            import pygame
            pygame.mixer.music.pause()
        self.paused=True

    def resume(self):
        if not self.active or not self.paused:return
        if not self._pygame:self._mci(f'resume {self.alias}')
        else:
            import pygame
            pygame.mixer.music.unpause()
        self.paused=False

    def seek(self,ms):
        if not self.active:return
        ms=max(0,min(int(ms),self._duration)) if self._duration else max(0,int(ms))
        if not self._pygame:
            self._mci(f'play {self.alias} from {ms}')
            if self.paused:self._mci(f'pause {self.alias}')
        else:
            import pygame
            pygame.mixer.music.play(start=ms/1000.)
            if self.paused:pygame.mixer.music.pause()
            self._offset=ms

    def stop(self):
        if not self.active:return
        if self._pygame:
            import pygame
            pygame.mixer.music.stop()
        elif sys.platform=='win32':
            try:self._mci(f'close {self.alias}')
            except RuntimeError:pass
        self.active=False;self.paused=False;self._pygame=False
