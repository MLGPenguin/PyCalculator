import tkinter as tk

'''
Calculator Program
'''

# Create Window and Global Variables
window = tk.Tk()
window.title("Calculator")
expression = ""
currentexpression = ""
lastinput = ""
mainFrame = tk.Frame()

# Layout Frames
mainFrame.pack(fill=tk.BOTH)
label = tk.Label(master=mainFrame, text="0", height=6, relief=tk.GROOVE, font=4, bg="black", anchor="e", padx=6, fg="white")
label.pack(fill=tk.BOTH)


class CalculatorButton(tk.Button):
    """Calculator Button class designed to reduce repetitive code and assist with click event"""
    def __init__(self, textval, buttonval, master, bind: bool = False, width: int = 8, height: int = 5, font: int = 3, bg: str = "gray"):
        super().__init__(master=master, text=textval, width=width, height=height, font=font, bg=bg)
        self.buttonval = buttonval
        if bind:
            self.bind("<Button-1>", click_handler)


nums = ["0","1","2","3","4","5","6","7","8","9"]
ops = ["+","-"]

# Main Input Handler (Keyboard and GUI)
def register_input(button):
    global expression, currentexpression, lastinput
    # Evaluate Expression when '=' is hit.
    if button == "=":
        currentexpression = ""
        label["text"] = compile_expression()
        lastinput = "="
        return
    expression += button
    if len(currentexpression) == 0:
        # Decide whether or not to reset the expression after hitting equals
        if lastinput == "=" and button in nums:
            clear_calc()
            expression = button
            currentexpression = button
            lastinput = button
            label["text"] = button
            return
        # Assuming the expression was continued instead of cancelled
        currentexpression += button
        label["text"] = currentexpression
        lastinput = button
        return
    # Get the most recent value in the expression
    last = getLast(currentexpression)
    # Check if button is an operator or (else) a number
    if button in ops:
        label["text"] = button
        currentexpression = button
    else:
        # Decide whether to start a new number sequence or continue the old one.
        if last in nums:
            currentexpression = str(currentexpression) + button
            label["text"] = currentexpression
        else:
            currentexpression = button
            label["text"] = button
    lastinput = button

def click_handler(event):
    """ Handle the Click Event """
    register_input(str(event.widget.buttonval))

def compile_expression():
    """ Used to compile the mathematical expression and returns a result. """
    global expression
    try:
        return eval(expression)
    except:
        return "Invalid Syntax"

def clear(event):
    """ Calls clear function when Clear button is clicked. """
    clear_calc()

def clear_calc():
    """ Clears / Resets the expression"""
    global currentexpression, expression, label
    currentexpression = ""
    expression = ""
    label["text"] = "0"

def getLast(text):
    """ Get the last character in a string """
    string = str(text)
    return string[len(string)-1]

def type_handler(event):
    """ Handles keyboard input. """
    print(event.char)
    char = str(event.char)
    if char in nums or char in ops or char == "=":
        register_input(char)

window.bind("<Key>", type_handler)
keys = tk.Frame(master=mainFrame)
numpad = tk.Frame(master=keys)
opPad = tk.Frame(master=keys)

# Create Clear button and Operator buttons for the GUI.
opKeys = ["+", "-", "="]
opPad.columnconfigure(0, weight=1)
for i in range(4): opPad.rowconfigure(i, weight=1)
clearbutton = CalculatorButton("C", "C", opPad, False)
clearbutton.grid(column=0, row=0, sticky="nsew")
clearbutton.bind("<Button-1>", clear)
for i in range(3):
    CalculatorButton(opKeys[i], opKeys[i], opPad, True).grid(column=0, row=i+1, sticky="nsew")

# Create the numpad buttons for the GUI.
val = 1
numpad.rowconfigure(3, weight=1)
for row in range(3):
    numpad.columnconfigure(row, weight=1)
    numpad.rowconfigure(row, weight=1)
    for column in range(3):
        CalculatorButton(textval=val, buttonval=val, master=numpad, bind=True).grid(row=row, column=column, sticky="nsew")
        val += 1
    CalculatorButton("0", 0, numpad, True, width=24).grid(row=3, columnspan=3, sticky="nsew")

# Layout the Grid.
numpad.grid(column=0, row=0, sticky="nsew")
opPad.grid(column=1, row=0, sticky="nsew")

keys.columnconfigure(index=0, weight=3)
keys.columnconfigure(index=1, weight=1)
keys.rowconfigure(0, weight=1)

keys.pack(fill=tk.BOTH)

window.mainloop()
