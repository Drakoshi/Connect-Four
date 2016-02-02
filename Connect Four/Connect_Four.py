try:
    # for Python 3
    from tkinter import *
except ImportError:
    # for Python 2
    from Tkinter import *

"""Basic Connect four game, By Tadas Kivilius (nickname Drakoshi)"""


class Game():
    """Just call it"""
    def __init__(self):
        self.Setup()

    def Setup(self):
        """Runs the game"""   
        self.__root = Tk()
        self.__frame = Frame(self.__root)
        self.__frame.pack()
        self.__root.title("Connect Four")

        self.__RedScore = 0
        self.__BlueScore = 0

        self.__gFont = ("Arial",16,"bold")

        self.__CreateGame()

        self.__root.mainloop()

    def __CreateGame(self):
        """Create the game, main method to start the game"""

        D = 50
        W = 350 # Width
        H = 350 # Height

        self.__CreateTopFrame()

        # Setup canvas for the game 
        self.__canvas = Canvas(self.__frame,width = W, height = H, bg ="black")
        self.__canvas.pack()
  
        for i in range(int(W / D)):
            y = i * D
            for j in range(int(H / D)):
                x = j * D
            
                self.__canvas.create_oval(x,y,x+D-1,y+D-1,fill = "white") # -1 because they were/are a bit overlapping
                self.__canvas.pack()

        self.__canvas.bind("<Button-1>",self.__Select) # binds the left mouse button and from here it proceeds on
        self.__canvas.pack()
    def __CreateTopFrame(self):
        """Creates top frame with current player turn and players scores"""

        topFrame = Frame(self.__frame)
        topFrame.pack(fill = BOTH)

        self.__lNr = 1 # initial number set 
        self.__pLabel = Label(topFrame,text = "Player 1",fg = "red", font = self.__gFont)
        self.__pLabel.pack()

        self.__rScore = Label(topFrame,text = str(self.__RedScore), fg = "red", font = self.__gFont)
        self.__rScore.pack(side = LEFT)

        self.__bScore = Label(topFrame,text = str(self.__BlueScore), fg = "blue", font = self.__gFont)
        self.__bScore.pack(side = RIGHT)

    def __RestartGame(self):
        """Restarts the game"""
        self.__frame.destroy()
        self.__frame = Frame(self.__root)
        self.__frame.pack()
        self.__CreateGame()
    
    def __Select(self,event):
        """Selects and proceeds on with filling the circle"""

        objectID = self.__canvas.find_closest(event.x,event.y)
        self.__CircleFill(objectID[0])    
    def __CircleFill(self,ID):
        """Fills the lowest possible circle in the collumn and checks the grid if there is a 4 in a sequence red or blue"""

        ID = self.__DropID(ID)
        cFill = self.__canvas.itemcget(ID,"fill")

        if self.__lNr == 1 and  cFill == "white":
            self.__canvas.itemconfig(ID,fill = "red")
            self.__canvas.update()
            self.__LabelUpdate()
        elif self.__lNr == 2 and cFill == "white":
            self.__canvas.itemconfig(ID,fill = "blue")
            self.__canvas.update()
            self.__LabelUpdate()
        else:
            pass #print("Circle already taken")

        self.__Check()
    def __DropID(self,ID):
        """ Actualy increases object ID to make it drop in the grid,
            to always be on lowest possible level to imitate the drop"""
        while True:
            nextFill = self.__canvas.itemcget(int(ID)+7,"fill")

            if nextFill == "white" and ID+7 <= 49:
                ID += 7
            else:
                return ID
    def __LabelUpdate(self):
        """Changes label between Player 1 and 2"""
        if self.__lNr == 1:
            self.__pLabel.config(text = "Player 2",fg = "blue")
            self.__pLabel.update()
            self.__lNr = 2
        elif self.__lNr == 2:
            self.__pLabel.config(text = "Player 1",fg = "red")
            self.__pLabel.update()
            self.__lNr = 1

    def __Check(self):
        for i in range(1,50):
            row = int(i % 7)
            collumn = int(i / 7)

            if row + 3 <= 7:
                Colours = self.__GetColours(i,1,0) # Right

                RedW = self.__Compare("red",Colours)
                BlueW = self.__Compare("blue",Colours)       
                if self.__Wins(RedW,BlueW):
                    break

            if collumn + 3 <= 7:
                Colours = self.__GetColours(i,0,1) # Down

                RedW = self.__Compare("red",Colours)
                BlueW = self.__Compare("blue",Colours)
                if self.__Wins(RedW,BlueW):
                    break

            if collumn + 3 <= 7 and row + 3 <= 7: # Down Right
                Colours = self.__GetColours(i,1,1)

                RedW = self.__Compare("red",Colours)
                BlueW = self.__Compare("blue",Colours)
                if self.__Wins(RedW,BlueW):
                    break

            if collumn - 3 >= 0 and row - 3 >= 0: # Up Left
                Colours = self.__GetColours(i,-1,-1)

                RedW = self.__Compare("red",Colours)
                BlueW = self.__Compare("blue",Colours)
                if self.__Wins(RedW,BlueW):
                    break

            if collumn + 3 <= 7 and row - 3 >= 0:
                Colours = self.__GetColours(i,-1,1) # Down Left

                RedW = self.__Compare("red",Colours)
                BlueW = self.__Compare("blue",Colours)
                if self.__Wins(RedW,BlueW):
                    break

            if collumn - 3 >= 0 and row + 3 <= 7:
                Colours = self.__GetColours(i,1,-1) # Up Right

                RedW = self.__Compare("red",Colours)
                BlueW = self.__Compare("blue",Colours)
                if self.__Wins(RedW,BlueW):
                    break
    def __GetColours(self,i,AddSign,MulSign):
        """Gets the colours of specific row/collumn,
           AddSign 1 = add, 0 = no add, -1 = minus,
           MulSign 1 = going down, 0 = same collumn, -1 = going up"""

        Colours = []
        Colours.append(self.__canvas.itemcget(i,"fill"))
        
        for j in range(1,4):
            Colours.append(self.__canvas.itemcget(i + ((j * 7) * MulSign) + (j * AddSign),"fill"))

        return Colours
    def __Compare(self,target,objects):
        """Compares the colours that were given to it, returns True, if all were True
           Checks for correct types"""
        if type(target) == str and type(objects) == list:
            return (target == objects[0] and target == objects[1]) and (target == objects[2] and target == objects[3])
        else:
            raise TypeError("Target must be a string and objects as list")
         
    def __Wins(self,RedW,BlueW):
        """checks if one of the colours won, 
           stops the game, shows buttons"""

        if RedW or BlueW:
            self.__canvas.unbind("<Button-1>")

            colour = ""
            if RedW:
                colour = "Red"
                self.__RedScore += 1              
            else:
                colour = "Blue"
                self.__BlueScore += 1

            WinFrame = Frame(self.__frame)
            WinFrame.pack()

            winLabel = Label(WinFrame,text = (colour + " Won"),font = self.__gFont,fg = colour)
            winLabel.pack()

            RestartButton = Button(WinFrame,text = "Restart",command = lambda:self.__RestartGame())
            RestartButton.pack()

            ExitButton = Button(WinFrame,text = "Exit",command = lambda: self.__root.destroy())
            ExitButton.pack()

            return True
        else:
            return False

def main():
    Game()

if __name__ == "__main__":
	sys.exit(main())