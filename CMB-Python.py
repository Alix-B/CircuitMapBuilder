import tkinter as tk
from tkinter.messagebox import showinfo

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
        validNodePoints.append([[x, y], 'b'])


# --------------------- FUNCTIONS ---------------------
def keypress(event):
    global flags
    global prevKey
    if event.keysym == "Shift_L" and flags["flag_edit"]:
        flags["flag_shift"] = True
    elif event.keysym != prevKey or (event.keysym in ['u', 'U'] and len(nodes) > 0):
        print("pressed", event)

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
        elif event.char in ['u', 'U', "\x1a"]:
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
        elif event.char in ['l', 'L']:
            print("LOADING")
            loadbutton()
        elif event.char in ['s', 'S', "\x13"]:
            print("SAVING")
            savebutton()

    prevKey = event.keysym


def createcircle(xorig, yorig, r, **kwargs):
    return canvas.create_oval(xorig - r, yorig - r, xorig + r, yorig + r, **kwargs)


def leftclick(event):
    cursorPosition = [event.x, event.y]
    if 100 < event.y < 700 \
            and 50 < event.x < 1150 \
            and flags["flag_edit"]:

        nearDist = 1000
        nearestNode = [0, 0]

        for node, colour in validNodePoints:
            dist = abs(node[0] - cursorPosition[0]) + abs(node[1] - cursorPosition[1])
            # print(node, curPos, dist)
            if dist < nearDist:
                nearDist = dist
                nearestNode = node

        print("clicked at", event.x, event.y, "nearest node is:", nearestNode)

        if flags["flag_shift"] and len(nodes) > 0 and [nearestNode, 'r'] in nodes:
            print("REMOVE NODE AT:", nearestNode)
            createcircle(nearestNode[0], nearestNode[1], 12, fill="white", outline="white")
            nodes.remove([nearestNode, 'r'])
            print("CURRENT NODES:", nodes)
        elif [nearestNode, 'b'] not in nodes and not flags["flag_shift"]:
            print("ADD NODE AT:", nearestNode)
            nodes.append([nearestNode, 'b'])
            print("CURRENT NODES:", nodes)
            createcircle(nearestNode[0], nearestNode[1], 12, fill="black")


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
        for node in enumerate(nodes):
            if node[1][1] != 'r':
                # print(node[1][0][0])
                createcircle(node[1][0][0], node[1][0][1], 12, fill="red", outline="red")
                nodes[node[0]] = [node[1][0], 'r']
    else:
        for node in enumerate(nodes):
            if node[1][1] != 'b':
                # print(node)
                createcircle(node[1][0][0], node[1][0][1], 12, fill="black", outline="black")
                nodes[node[0]] = [node[1][0], 'b']

    flags["flag_shift"] = False

    setmode()
    root.after(250, update)


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

        createcircle(nodes[-1][0][0], nodes[-1][0][1], 12, fill="white", outline="white")
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
            createcircle(node[0][0], node[0][1], 12, fill="white", outline="white")

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

    for node, colour in validNodePoints:
        dist = abs(node[0] - cursorPosition[0]) + abs(node[1] - cursorPosition[1])
        # print(node, curPos, dist)
        if dist < nearDist:
            nearDist = dist
            nearestNode = node

    cursorPos.set("Cursor pos: " + str(nearestNode[0]) + ", " + str(nearestNode[1]))


def savebutton():
    with open("./nodes.txt", 'w') as savefile:
        for node in nodes:
            savefile.write(str(node[0][0]) + ' ' + str(node[0][1]) + ' ' + str(node[1]) + "\n")

    savefile.close()

    print("SAVE NODES:", nodes)

    showinfo("Save", "Current nodes: " + str(nodes) + " were saved to nodes.txt in the current directory")


def loadbutton():
    print("CLEAR SCREEN")

    clearbutton()

    global nodes
    nodes = []

    with open("./nodes.txt", 'r') as loadfile:
        for line in loadfile.readlines():
            info = line.strip().split(' ')
            nodes.append([[int(info[0]), int(info[1])], info[2]])

    loadfile.close()

    print("LOAD NODES:", nodes)

    print("REDRAWING NODES")

    for node in enumerate(nodes):
        createcircle(node[1][0][0], node[1][0][1], 12, fill="black", outline="black")

    showinfo("Load", "Nodes: " + str(nodes) + " were loaded from nodes.txt in the current directory")


def helpbutton():
    showinfo("Help", "Shortcuts:\n\nView: v, V\n\nEdit: e, E\n\nUndo: crt+z, u, U\n\nClear: c, C\n\nAdd turn: t, "
                     "T\n\nSave: crt+s, s, S\n\nLoad: l, L")


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
save = tk.Button(root, text="Save", width=6, height=1, command=lambda: savebutton())
load = tk.Button(root, text="Load", width=6, height=1, command=lambda: loadbutton())
helper = tk.Button(root, text="Help", width=6, height=1, command=lambda: helpbutton())
f1_nr = tk.OptionMenu(root, f1_nr_text, "F1", "NR")

save.grid(column=10, row=1)
load.grid(column=20, row=1)
mode.grid(column=30, row=1)
view.grid(column=40, row=1)
edit.grid(column=50, row=1)
undoTrackAnchors.grid(column=60, row=1)
clearTrackAnchors.grid(column=70, row=1)
addTurnNumber.grid(column=80, row=1)
f1_nr.grid(column=85, row=1)
curPos.grid(column=90, row=90)
helper.grid(column=90, row=1)

root.after(250, update)

root.mainloop()
