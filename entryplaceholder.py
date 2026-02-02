def onFocusIn(txtbox, placeholder, show):
    if txtbox.get() == placeholder:
        txtbox.delete(0, "end")
        txtbox.config(fg="black", show=show)


def onFocusOut(txtbox, placeholder):
    if txtbox.get() == "":
        txtbox.insert(0, placeholder)
        txtbox.config(fg="#777777", show="")


def changeOnFocus(txtbox, placeholder, show=""):
    txtbox.bind("<FocusIn>", lambda e: onFocusIn(
        txtbox, placeholder, show))
    txtbox.bind("<FocusOut>", lambda e: onFocusOut(
        txtbox, placeholder))
