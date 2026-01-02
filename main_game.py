import random
from kivy.app import App
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.animation import Animation
from kivymd.uix.dialog import MDDialog
from kivy.core.audio import SoundLoader
from kivymd.uix.button import MDFlatButton
from kivy.uix.screenmanager import Screen, ScreenManager

class MenuScreen(Screen):
        
    def play_start_sound(self):
        app = App.get_running_app()
        if hasattr(app, "start_sound") and app.start_sound:
            app.start_sound.play()
        
class GameScreen(Screen):

    def play_box_sound(self):
        app = App.get_running_app()
        if hasattr(app, "box_sound") and app.box_sound:
            app.box_sound.play()

    def play_back_sound(self):
        app = App.get_running_app()
        if hasattr(app, "back_sound") and app.back_sound:
            app.back_sound.play()

    def trophy_pos(self):
        self.box1_position=.2
        self.box2_position=.5
        self.box3_position=.8
        choices = [self.box1_position,self.box2_position, self.box3_position]
        self.selected_trophy_pos = random.choice(choices)
        self.ids.cup.pos_hint = {'center_x':self.selected_trophy_pos, 'center_y':.54}
        self.ids.cup.parent.do_layout()
        
    def on_enter(self):
        self.trophy_pos()
        for b in (self.ids.box1,self.ids.box2,self.ids.box3):
            b.opacity=1
            b.disabled=False
        self.ids.cup.opacity=0
              
    def fade (self,*widgets):
        for w in widgets:
            w.disabled = True
            Animation(opacity=0, duration=2.5).start(w)

    def unfade (self,widget):
        Animation(opacity=1, duration=.5).start(widget)

    def dialog_call(self,dt):
        close_btn=MDFlatButton(text=self.restart_btn_txt,on_release=self.on_restart)
        self.box=MDDialog(title=self.restart_title,text="Any Bug?\nWait for updates.",size_hint=(.9,None),height="160dp",buttons=[close_btn],auto_dismiss=False)
        self.box.open()

    def on_restart(self,*args):
        self.box.dismiss()
        self.trophy_pos()
        for b in (self.ids.box1,self.ids.box2,self.ids.box3):
            b.opacity=1
            b.disabled=False
        self.ids.cup.opacity=0
        app = App.get_running_app()
        if hasattr(app, "restart_sound") and app.restart_sound:
            app.restart_sound.play()
    
    def clock_restart(self, obj):
        self.start=Clock.schedule_once(obj,3)

    def cancel_restart(self):
        if hasattr (self, "start") and self.start:
            self.start.cancel()


    def check_box_select(self,widget):
        if self.selected_trophy_pos==widget:
            self.restart_title="Nice Guess!"
            self.restart_btn_txt="Play Again"
        else:
            self.restart_title="So Close!"
            self.restart_btn_txt="Try Again"

class GuessTheBoxApp(MDApp):
    def build(self):
        pass

    def on_start(self):
        self.start_sound=SoundLoader.load("start_sound.ogg")
        self.bg = SoundLoader.load("gamebg_sound.ogg")
        self.box_sound = SoundLoader.load("box_select.wav")
        self.restart_sound = SoundLoader.load("restart_sound.wav")
        self.back_sound = SoundLoader.load("back_sound.wav")
        self.start_bg()
        self.root.ids.unmute.disabled=True
        self.root.ids.unmute.opacity=0
    
    def start_bg(self):
        if self.bg:
            self.bg.loop = True
            self.bg.volume = 0.4
            self.bg.play()
  
GuessTheBoxApp().run()