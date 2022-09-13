import tkinter as tk

# --------------------- DEFAULT CONTROL VALUES ---------------------
flags = {"flag_f1_nr": False,
         "flag_edit": True,
         "flag_view": False,
         "flag_undoTrackAnchors": False,
         "flag_clearTrackAnchors": False,
         "flag_addTurnNumber": False,
         "flag_shift": False
         }

nodes = []

validNodePoints = []

for x in range(50, 1200 + 1, 25):
    for y in range(100, 701, 25):
        validNodePoints.append([x, y])


# --------------------- FUNCTIONS ---------------------
def keypress(event):
    global flags
    global prevKey
    if event.keysym == "Shift_L" and flags["flag_edit"]:
        flags["flag_shift"] = True
    elif event.keysym != prevKey or (event.keysym in ['u', 'U', 'c', 'C'] and len(nodes) > 0):
        print("pressed", event.keysym)

        if event.char in ['v', 'V']:
            flags = {"flag_f1_nr": flags["flag_f1_nr"],
                     "flag_edit": False,
                     "flag_view": True,
                     "flag_undoTrackAnchors": False,
                     "flag_clearTrackAnchors": False,
                     "flag_addTurnNumber": False,
                     "flag_shift": False
                     }
            print("FLAG VIEW")
            viewbutton()
        elif event.char in ['e', 'E']:
            flags = {"flag_f1_nr": flags["flag_f1_nr"],
                     "flag_edit": True,
                     "flag_view": False,
                     "flag_undoTrackAnchors": False,
                     "flag_clearTrackAnchors": False,
                     "flag_addTurnNumber": False,
                     "flag_shift": False
                     }
            print("FLAG EDIT")
            editbutton()
        elif event.char in ['c', 'C']:
            flags = {"flag_f1_nr": flags["flag_f1_nr"],
                     "flag_edit": False,
                     "flag_view": False,
                     "flag_undoTrackAnchors": False,
                     "flag_clearTrackAnchors": True,
                     "flag_addTurnNumber": False,
                     "flag_shift": False
                     }
            print("FLAG CLEAR")
            clearbutton()
        elif event.char in ['t', 'T']:
            flags = {"flag_f1_nr": flags["flag_f1_nr"],
                     "flag_edit": False,
                     "flag_view": False,
                     "flag_undoTrackAnchors": False,
                     "flag_clearTrackAnchors": False,
                     "flag_addTurnNumber": True,
                     "flag_shift": False
                     }
            print("FLAG TURN")
            turnbutton()
        elif event.char in ['u', 'U', '\x1a']:
            flags = {"flag_f1_nr": flags["flag_f1_nr"],
                     "flag_edit": False,
                     "flag_view": False,
                     "flag_undoTrackAnchors": True,
                     "flag_clearTrackAnchors": False,
                     "flag_addTurnNumber": False,
                     "flag_shift": False
                     }
            print("FLAG UNDO")
            undobutton()

    prevKey = event.keysym


def createcircle(self, xorig, yorig, r, **kwargs):
    return self.create_oval(xorig - r, yorig - r, xorig + r, yorig + r, **kwargs)


tk.Canvas.create_circle = createcircle


def leftclick(event):
    cursorPosition = [event.x, event.y]
    if 100 < event.y < 700 \
            and 50 < event.x < 1150 \
            and flags["flag_edit"]:

        nearDist = 1000
        nearestNode = [0, 0]

        for node in validNodePoints:
            dist = abs(node[0] - cursorPosition[0]) + abs(node[1] - cursorPosition[1])
            # print(node, curPos, dist)
            if dist < nearDist:
                nearDist = dist
                nearestNode = node

        print("clicked at", event.x, event.y, "nearest node is:", nearestNode)

        if flags["flag_shift"] and len(nodes) > 0 and nearestNode in nodes:
            print("REMOVE NODE AT:", nearestNode)
            canvas.create_circle(nearestNode[0], nearestNode[1], 12, fill="white", outline="white")
            nodes.remove(nearestNode)
            print("CURRENT NODES:", nodes)
        elif nearestNode not in nodes and not flags["flag_shift"]:
            print("ADD NODE AT:", nearestNode)
            nodes.append(nearestNode)
            print("CURRENT NODES:", nodes)
            canvas.create_circle(nearestNode[0], nearestNode[1], 12, fill="black")

        # flags["flag_shift"] = False


def viewbutton():
    global flags
    if not flags["flag_view"]:
        print("CLICKED VIEW BUTTON")
        flags = {"flag_f1_nr": flags["flag_f1_nr"],
                 "flag_edit": False,
                 "flag_view": True,
                 "flag_undoTrackAnchors": False,
                 "flag_clearTrackAnchors": False,
                 "flag_addTurnNumber": False,
                 "flag_shift": False
                 }
        print("FLAG VIEW")


def update():
    # print(flags["flag_shift"])
    if flags["flag_shift"]:
        for node in nodes:
            canvas.create_circle(node[0], node[1], 12, fill="red", outline="red")
    else:
        for node in nodes:
            canvas.create_circle(node[0], node[1], 12, fill="black", outline="black")

    flags["flag_shift"] = False

    setmode()
    root.after(50, update)


def editbutton():
    global flags
    if not flags["flag_edit"]:
        print("CLICKED EDIT BUTTON")
        flags = {"flag_f1_nr": flags["flag_f1_nr"],
                 "flag_edit": True,
                 "flag_view": False,
                 "flag_undoTrackAnchors": False,
                 "flag_clearTrackAnchors": False,
                 "flag_addTurnNumber": False,
                 "flag_shift": False
                 }
        print("FLAG EDIT")


def undobutton():
    global flags
    if len(nodes) > 0:
        print("CLICKED UNDO BUTTON")
        flags = {"flag_f1_nr": flags["flag_f1_nr"],
                 "flag_edit": False,
                 "flag_view": False,
                 "flag_undoTrackAnchors": True,
                 "flag_clearTrackAnchors": False,
                 "flag_addTurnNumber": False,
                 "flag_shift": False
                 }
        print("FLAG UNDO")

        canvas.create_circle(nodes[-1][0], nodes[-1][1], 15, fill="white", outline="white")
        nodes.pop()

        print("RESETTING FLAGS")
        flags = {"flag_f1_nr": flags["flag_f1_nr"],
                 "flag_edit": True,
                 "flag_view": False,
                 "flag_undoTrackAnchors": False,
                 "flag_clearTrackAnchors": False,
                 "flag_addTurnNumber": False,
                 "flag_shift": False
                 }
    else:
        print("NO NODES TO UNDO")
        print("RESETTING FLAGS")
        flags = {"flag_f1_nr": flags["flag_f1_nr"],
                 "flag_edit": True,
                 "flag_view": False,
                 "flag_undoTrackAnchors": False,
                 "flag_clearTrackAnchors": False,
                 "flag_addTurnNumber": False,
                 "flag_shift": False
                 }


def turnbutton():
    print("CLICKED TURN BUTTON")
    global flags
    flags = {"flag_f1_nr": flags["flag_f1_nr"],
             "flag_edit": False,
             "flag_view": False,
             "flag_undoTrackAnchors": False,
             "flag_clearTrackAnchors": False,
             "flag_addTurnNumber": True,
             "flag_shift": False
             }
    print("FLAG TURN")


def clearbutton():
    global nodes
    global flags
    if len(nodes) > 0:
        print("CLICKED CLEAR BUTTON")
        flags = {"flag_f1_nr": flags["flag_f1_nr"],
                 "flag_edit": False,
                 "flag_view": False,
                 "flag_undoTrackAnchors": False,
                 "flag_clearTrackAnchors": True,
                 "flag_addTurnNumber": False,
                 "flag_shift": False
                 }
        print("FLAG CLEAR")

        for node in nodes:
            canvas.create_circle(node[0], node[1], 12, fill="white", outline="white")

        nodes = []

        print("RESETTING FLAGS")
        flags = {"flag_f1_nr": flags["flag_f1_nr"],
                 "flag_edit": True,
                 "flag_view": False,
                 "flag_undoTrackAnchors": False,
                 "flag_clearTrackAnchors": False,
                 "flag_addTurnNumber": False,
                 "flag_shift": False
                 }
    else:
        print("NO NODES TO CLEAR")
        print("RESETTING FLAGS")
        flags = {"flag_f1_nr": flags["flag_f1_nr"],
                 "flag_edit": True,
                 "flag_view": False,
                 "flag_undoTrackAnchors": False,
                 "flag_clearTrackAnchors": False,
                 "flag_addTurnNumber": False,
                 "flag_shift": False
                 }


def setmode():
    for key, value in flags.items():
        if value:
            flagMode.set(f"MODE:\n{key[5:]}")


def motion(event):
    global cursorPos
    cursorPosition = [event.x, event.y]
    nearDist = 1000
    nearestNode = [0, 0]

    for node in validNodePoints:
        dist = abs(node[0] - cursorPosition[0]) + abs(node[1] - cursorPosition[1])
        # print(node, curPos, dist)
        if dist < nearDist:
            nearDist = dist
            nearestNode = node

    cursorPos.set("Cursor pos: " + str(nearestNode[0]) + ", " + str(nearestNode[1]))


# --------------------- PROGRAM WINDOW ---------------------
root = tk.Tk()
root.title("Circuit Map Builder - Python remake")

prevKey = ''
root.bind("<Key>", keypress)
root.bind("<Button-1>", leftclick)
root.bind('<Motion>', motion)

# --------------------- GUI WINDOW DIMENSIONS ---------------------
canvas = tk.Canvas(root, width=1280, height=720)
canvas.grid(columnspan=100, rowspan=100)
canvas.configure(background="white")

# --------------------- BUTTON LAYOUT ---------------------
flagMode = tk.StringVar()
cursorPos = tk.StringVar()
f1_nr_text = tk.StringVar()

flagMode.set("MODE:\nEdit")
cursorPos.set("Cursor pos: 0, 0")
f1_nr_text.set("F1")

mode = tk.Label(root, textvariable=flagMode, width=16, height=2)
curPos = tk.Label(root, textvariable=cursorPos, width=23, height=1)
view = tk.Button(root, text="View", width=6, height=1, command=lambda: viewbutton())
edit = tk.Button(root, text="Edit", width=6, height=1, command=lambda: editbutton())
undoTrackAnchors = tk.Button(root, text="Undo Track Anchors", width=18, height=1, command=lambda: undobutton())
clearTrackAnchors = tk.Button(root, text="Clear Track Anchors", width=18, height=1, command=lambda: clearbutton())
addTurnNumber = tk.Button(root, text="Add Turn Number", width=15, height=1, command=lambda: turnbutton())
f1_nr = tk.OptionMenu(root, f1_nr_text, "F1", "NR")

mode.grid(column=30, row=1)
view.grid(column=40, row=1)
edit.grid(column=50, row=1)
undoTrackAnchors.grid(column=60, row=1)
clearTrackAnchors.grid(column=70, row=1)
addTurnNumber.grid(column=80, row=1)
f1_nr.grid(column=85, row=1)
curPos.grid(column=90, row=90)

root.after(50, update)

root.mainloop()
