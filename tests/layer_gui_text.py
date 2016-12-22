
import pygooey
import pygame as pg

pg.init()
screen = pg.display.set_mode((600,400))
screen_rect = screen.get_rect()
done = False
widgets = []

def textbox_callback(id, final):
    print('enter pressed, textbox contains {}'.format(final))
    
def alternative_callback(id, final):
    print('alternative textbox contains {}'.format(final))
    
def button_callback():
    print('button pressed, textbox contains {}'.format(entry.final))

#see all settings help(pygooey.TextBox.__init__)
entry_settings = {
    "inactive_on_enter" : False,
    'active':False
}
entry = pygooey.TextBox(rect=(70,100,150,30), command=textbox_callback, **entry_settings)
widgets.append(entry)
entry2 = pygooey.TextBox(rect=(70,200,150,30), command=alternative_callback, **entry_settings)
widgets.append(entry2)

#see all settings help(pygooey.Button.__init__)
btn_settings = {
    "clicked_font_color" : (0,0,0),
    "hover_font_color"   : (205,195, 100),
    'font'               : pg.font.Font(None,16),
    'font_color'         : (255,255,255),
    'border_color'       : (0,0,0),
}
btn = pygooey.Button(rect=(10,10,105,25), command=button_callback, text='OK', **btn_settings)
widgets.append(btn)

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        for w in widgets:
            w.get_event(event)
    for w in widgets:
        w.update()
        w.draw(screen)
    pg.display.update()
