#!/usr/bin/python
import sys, xbmc
from kodipopcorntime.utils import xbmcItem
from kodipopcorntime.logging import log, LOGLEVEL

__addon__ = sys.modules['__main__'].__addon__

class TorrentPlayer(xbmc.Player):
    def onPlayBackStarted(self):
        log('(Torrent Player) onPlayBackStarted')

    def onPlayBackResumed(self):
        log('(Torrent Player) onPlayBackResumed')
        self._overlay.close()

    def onPlayBackPaused(self):
        log('(Torrent Player) onPlayBackPaused')
        self._overlay.open()

    def onPlayBackStopped(self):
        log('(Torrent Player) Stop playback')
        self._overlay.close()

    def onPlayBackSeek(self):
        log('(Torrent Player) onPlayBackSeek')
        self.pause()

    def playTorrentFile(self, mediaSettings, magnet, item, subtitleURL=None):

        log('(Torrent Player) Start the playback', LOGLEVEL.INFO)
        self.play(f"plugin://plugin.video.torrest/play_magnet?magnet={magnet}", xbmcItem(**item))

        if subtitleURL:
            log('(Torrent Player) Add subtitle to the playback')
            self.setSubtitles(subtitleURL)
