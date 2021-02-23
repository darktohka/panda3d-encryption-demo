from panda3d.core import Multifile, VirtualFileSystem, Filename, TextNode, loadPrcFileData
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.ShowBase import ShowBase
import hmac, webbrowser

loadPrcFileData('', 'window-title Encryption Demo')

class App(ShowBase):
    PW = "PASSWORD"

    def __init__(self):
        ShowBase.__init__(self)
        self.mount_multifile()

        self.current_credits = True

        self.bg = OnscreenImage('/phase_1/bg.jpg')
        self.bg.reparentTo(render2d)

        scale = 0.33

        self.gift = OnscreenImage('/phase_1/gift.jpg')
        self.gift.reparentTo(aspect2d)
        self.gift.setScale(scale, 1, scale * 1.77)
        self.gift.setPos(0.8, 0, 0)
        self.gift.hide()

        self.title = DirectLabel(self.a2dTopCenter, relief=None, text_align=TextNode.ACenter, color=(0.6, 0.6, 0.6, 0.6), pos=(0, 0, -0.15), scale=0.15, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text='Can you guess the password?')
        self.title.setTransparency(True)

        self.label = DirectLabel(aspect2d, relief=None, text_align=TextNode.ACenter, pos=(0, 0, 0.2), scale=0.1, text='')
        self.label.setTransparency(True)

        self.entry = DirectEntry(aspect2d, text_align=TextNode.ACenter, scale=0.1, pos=(-0, 0, 0), width=15, focus=1)
        self.button = DirectButton(self.entry, text_align=TextNode.ACenter, pos=(0, 0, -2), text='Submit', command=self.attempt_decryption)

        self.credits = DirectButton(base.a2dBottomLeft, relief=None, text_align=TextNode.ALeft, text='C', scale=0.08, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), pos=(0.05, 0, 0.05), command=self.open_credits)

        self.entry.bind(DGG.ACCEPT, self.attempt_decryption)

        self.music = self.loader.loadMusic('/phase_1/audio/dweller.ogg')

        self.playMusic(self.music, looping=True, volume=0.1)
        self.play_animation()

    def play_animation(self):
        Sequence(
            self.bg.scaleInterval(7, 1.1, 1, blendType='easeInOut'),
            self.bg.scaleInterval(7, 1, 1.1, blendType='easeInOut'),
        ).loop()

    def open_credits(self):
        if self.current_credits:
            webbrowser.open('https://www.instagram.com/p/BgmTyb6l8VB')
        else:
            webbrowser.open('https://halleylabs.com')

        self.current_credits = not self.current_credits

    def mount_multifile(self):
        mf = Multifile()
        mf.open_read(Filename.from_os_specific('phase_1.ef'))
        mf.set_encryption_flag(True)
        mf.set_encryption_password(self.PW)

        if not VirtualFileSystem.get_global_ptr().mount(mf, Filename('/'), 0):
            raise Exception('Multifile could not be mounted.')

    def attempt_decryption(self, *args):
        attempt = self.entry.get(plain=True)

        if hmac.compare_digest(attempt, self.PW):
            self.title['text'] = 'CONGRATULATIONS!!!'
            self.title['text_fg'] = (0, 1, 0, 1)
            self.title['text_shadow'] = (0, 0.3, 0, 1)

            self.label['text_fg'] = (1, 0.5, 0, 1)
            self.label['text_shadow'] = (0.3, 0.3, 0, 1)
            self.label['text'] = "You've cracked the multifile password!!!\n\nWas it a lucky guess?\n\nIn any case, here's a special picture of a subwoofer."
            self.label['text_wordwrap'] = 15
            self.label.setPos(-0.3, 0, 0.25)

            self.entry.destroy()
            self.playSfx(self.loader.loadSfx('/phase_1/audio/congrats.ogg'), volume=0.5)
            self.gift.show()
        else:
            self.label['text'] = 'Incorrect password!'
            self.label['text_fg'] = (1, 0, 0, 1)
            self.label['text_shadow'] = (0.3, 0, 0, 1)
            self.entry['focus'] = True

            self.playSfx(self.loader.loadSfx('/phase_1/audio/error.ogg'))

app = App()
app.run()
