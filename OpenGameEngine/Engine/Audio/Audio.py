import sounddevice as sd
import threading

class Audio:
    def __init__(self):
        self.source = None
        self.position = 0.0
        self.is_playing = False
        self.volume = 1.0

    def SetSource(self, source:tuple):
        self.source = source

    def SetVolume(self, volume:float):
        self.volume = volume
        
    def Play(self):
        if self.is_playing:
            return

        audio, rate = self.source
        start = int(self.position * len(audio))
        
        threading.Thread(target=self._play, args=(audio[start:], rate), daemon=True).start()
        self.is_playing = True

    def SetPosition(self, position:float):
        self.position = max(0.0, min(1.0, position))
        if self.is_playing:
            sd.stop()
            self.is_playing = False
            self.Play()

    def Stop(self):
        sd.stop()
        self.is_playing = False

    def _play(self, data, rate):
        if self.volume != 1.0:
            data = (data * self.volume).astype(data.dtype)
        try:
            sd.play(data, rate)
            sd.wait()
        finally:
            self.is_playing = False

    @property
    def IsPlaying(self):
        return self.is_playing
