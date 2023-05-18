from state.functions import open_texture


class Resources:
    background = open_texture("resources/images/background.png")
    text_logo = open_texture("resources/images/logo.png")
    play_btn = open_texture("resources/images/play.png")
    go_back_btn = open_texture("resources/images/go-back.png")
    settings_btn = open_texture("resources/images/settings.png")
    settings_back = open_texture("resources/images/settings_background.png")
    note = open_texture("resources/images/note.png")
    no_note = open_texture("resources/images/no_note.png")
    double_note = open_texture("resources/images/double_note.png")
    no_double_note = open_texture("resources/images/no_double_note.png")
    windowed = open_texture("resources/images/windowed.png")
    fullscreen = open_texture("resources/images/fullscreen.png")
    solo_play = open_texture("resources/images/soloplay.png")
    map = open_texture("resources/images/map.png")
    walkcolor1r = open_texture("resources/images/walkcolor1.png")
    walkcolor2r = open_texture("resources/images/walkcolor2.png")
    walkcolor3r = open_texture("resources/images/walkcolor3.png")
    walkcolor4r = open_texture("resources/images/walkcolor4.png")
    walkcolor1l = open_texture("resources/images/walkcolor1.png", True, False)
    walkcolor2l = open_texture("resources/images/walkcolor2.png", True, False)
    walkcolor3l = open_texture("resources/images/walkcolor3.png", True, False)
    walkcolor4l = open_texture("resources/images/walkcolor4.png", True, False)
    walkcolor0r = open_texture("resources/images/idle.png")
    walkcolor0l = open_texture("resources/images/idle.png", True, False)
    animation = {
        "1l": walkcolor1l,
        "2l": walkcolor2l,
        "3l": walkcolor3l,
        "4l": walkcolor4l,
        "1r": walkcolor1r,
        "2r": walkcolor2r,
        "3r": walkcolor3r,
        "4r": walkcolor4r,
        "0r": walkcolor0r,
        "0l": walkcolor0l,
    }

    cls_list = ["archer", "assassin", "magician", "marksman", "spearsman", "swordsman", "darkmage", "glasscannon", "ninja", "priest"]
    classes = [open_texture(f"resources/classes/{cls}.png") for cls in cls_list]
