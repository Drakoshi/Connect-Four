from tkinter import *

"""Modify select, make the checking of 4 in a row.
"""

class GUI():
    def __init__(self,root):
        self.root = root
        self.frame = Frame(root)
        self.frame.pack()
        self.root.title("Connect Four")

        self.lNr = 1
        self.MainLabel = Label(self.frame,text = "Player1",fg = "red", font = ("Times New Roman",16))
        self.MainLabel.pack()

        self.canvas = Canvas(self.frame,width = 350, height = 350, bg ="black")
        self.canvas.pack()

    def LabelUp(self):
        """Changes label between Player 1 and 2"""
        if self.lNr == 1:
            self.MainLabel.config(text = "Player 2",fg = "blue")
            self.MainLabel.update()
            self.lNr = 2
        elif self.lNr == 2:
            self.MainLabel.config(text = "Player 1",fg = "red")
            self.MainLabel.update()
            self.lNr = 1

    def Select(self,event):
        """Gets ID of object that was clicked on """
        #print(event.x , event.y)

        objectID = self.canvas.find_closest(event.x,event.y)
        #print(int(objectID[0]))

        self.CircleFill(objectID[0])

    def DropID(self,ID):
        nID = int(ID)
        while True:
            nextFill = self.canvas.itemcget(int(nID)+7,"fill")

            if nextFill == "white" and nID+7 <= 49:
                nID += 7
            else:
                return nID
                break
        
    def CircleFill(self,ID):
        ID = self.DropID(ID)
        cFill = self.canvas.itemcget(ID,"fill")

        if self.lNr == 1 and  cFill == "white":
            self.canvas.itemconfig(int(ID),fill = "red")
            self.canvas.update()
            self.LabelUp()
        elif self.lNr == 2 and cFill == "white":
            self.canvas.itemconfig(int(ID),fill = "blue")
            self.canvas.update()
            self.LabelUp()
        else:
            print("Circle already taken")

        self.Check()

    def Compare(self,target,objects):
        if type(target) == str and type(objects) == list:
            if (target == objects[0] and target == objects[1]) and (target == objects[2] and target == objects[3]):
                return True
            else:
                return False
        else:
            raise TypeError("Target must be a string and objects as list")

    def GetColours(self,i,AddSign,MulSign):

        a = self.canvas.itemcget(i,"fill")
        b = self.canvas.itemcget(i + ((1 * 7) * MulSign) + (1 * AddSign),"fill")
        c = self.canvas.itemcget(i + ((2 * 7) * MulSign) + (2 * AddSign),"fill")
        d = self.canvas.itemcget(i + ((3 * 7) * MulSign) + (3 * AddSign),"fill")

        return a,b,c,d

    def Check(self):
        for i in range(1,50):
            row = int(i % 7)
            collumn = int(i / 7)

            if row + 3 <= 7:
                a,b,c,d = self.GetColours(i,1,0)

                RedW = self.Compare("red",[a,b,c,d])
                BlueW = self.Compare("blue",[a,b,c,d])
                Won = self.Wins(RedW,BlueW)
                if Won:
                    break


            if collumn + 3 <= 7:
                a,b,c,d = self.GetColours(i,0,1)

                RedW = self.Compare("red",[a,b,c,d])
                BlueW = self.Compare("blue",[a,b,c,d])
                Won = self.Wins(RedW,BlueW)
                if Won:
                    break

            if collumn + 3 <= 7 and row + 3 <= 7:
                a,b,c,d = self.GetColours(i,1,1)

                RedW = self.Compare("red",[a,b,c,d])
                BlueW = self.Compare("blue",[a,b,c,d])
                Won = self.Wins(RedW,BlueW)
                if Won:
                    break

            if collumn - 3 >= 0 and row - 3 >= 0:
                a,b,c,d = self.GetColours(i,-1,-1)

                RedW = self.Compare("red",[a,b,c,d])
                BlueW = self.Compare("blue",[a,b,c,d])
                Won = self.Wins(RedW,BlueW)
                if Won:
                    break

            if collumn + 3 <= 7 and row - 3 >= 0:
                a,b,c,d = self.GetColours(i,-1,1)

                RedW = self.Compare("red",[a,b,c,d])
                BlueW = self.Compare("blue",[a,b,c,d])
                self.Wins(RedW,BlueW)
                if Won:
                    break

            if collumn - 3 >= 0 and row + 3 <= 7:
                a,b,c,d = self.GetColours(i,1,-1)

                RedW = self.Compare("red",[a,b,c,d])
                BlueW = self.Compare("blue",[a,b,c,d])
                Won = self.Wins(RedW,BlueW)
                if Won:
                    break

        
    def Wins(self,RedW,BlueW):

        if RedW or BlueW:
            self.canvas.unbind("<Button-1>")
            colour = ""
            if RedW:
                colour = "Red"
            else:
                colour = "Blue"
            winLabel = Label(self.root,text = (colour + " Won"))
            winLabel.pack()

            ExitButton = Button(self.root,text = "Exit",command = lambda: self.root.destroy())
            ExitButton.pack()

            return True
        else:
            return False

def main():

    H = 350
    W = 350
    D = 50

    root = Tk()
    gui = GUI(root)

    for i in range(int(H / D)):
        y = i * D
        for j in range(int(W / D)):
            x = j * D
            
            gui.canvas.create_oval(x,y,x+D,y+D,fill = "white")
            gui.canvas.pack()

    gui.canvas.bind("<Button-1>",gui.Select)
    gui.canvas.pack()

    root.mainloop()

if __name__ == "__main__":
	sys.exit(main())