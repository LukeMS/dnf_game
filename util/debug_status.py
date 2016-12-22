from tkinter import *

def view(creature):
    import types
    from mylib.data_tree import tk_tree_view

    dic = {}
    dic_keys = dir(creature)
    for att in dic_keys:
        if isinstance(getattr(creature, att), types.FunctionType):
            continue
        elif att[-2:] == "__":
            continue
        elif isinstance(getattr(type(creature), att, None), property):
            dic[att] = getattr(
                type(creature), att).__get__(creature, type(creature))
        else:
            dic[att] = getattr(creature, att, None)

    tk_tree_view(dic)


def input(game):
    """..."""
    master = Tk()
    e = Entry(master)
    e.pack()
    e.focus_set()

    def callback():
        """...

        print(game._scene.current_level[20, 22])
        print(game._scene.current_level.objects)
        """
        eval(e.get(), {"game": game})

    def setforth():
        """..."""
        x = e.get()
        e.delete(0, last=len(x) + 1)
        # e.insert(0, "new_value")
        e.select_to(len(e.get()))

    def makeentry(parent, caption, width=None, **options):
        """..."""
        Label(parent, text=caption).pack(side=LEFT)
        entry = Entry(parent, **options)
        if width:
            entry.config(width=width)
        entry.pack(side=LEFT)
        return entry

    b1 = Button(master, text="eval", width=10, command=callback)
    b1.pack()
    b2 = Button(master, text="clear", width=10, command=setforth)
    b2.pack()
    mainloop()


