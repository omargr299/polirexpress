import GUI

loop = True

def finish(e):
    global loop
    loop = False
wnd = GUI.App("Test", finish=finish, resizable=True)
while loop:
    rect,frame = wnd.cam.read()
    if rect:
        wnd.camaras.imagen.update_frame(frame)
    else:
        wnd.camaras.imagen.set_default()
    wnd.update_cams()
    wnd.update_window()
