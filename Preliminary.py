# Tic Tac Toe - Jayden
# Importing all the modules, tkinter, custom TicTacToe Module
import tkinter as tk
from TicTacToe_ab import *
import time

# setting the player variable
player = True
# creating the engine from custom module
engine = Engine()

# create the main window
# ----------------------
# I create this outside the main function because whenever you create
# or define a tkinter IntVar, it defaults to 0. In this case, it means
# every time i reopen/refresh the window for a new theme, it wont work
# because it resets to zero every time 

# you also need the root window to assign an IntVar to
# otherwise errors occur
root_window = tk.Tk()
theme = tk.IntVar()
theme.set(1)
# main function
def main():
    global theme

    # config, changes the backgroud, color, size, etc.
    # dimensions
    root_window.config(width=500, height=500)
    # title
    root_window.title("Tic Tac Toe")
    
    # create an icon for the window
    # similar to a favicon for HTML code
    #--------------------------------------------------------- 

    # This creates the menubar at the top of the screen
    menu_bar = tk.Menu(root_window)
    # attach it to the main window, then add the menu for
    # the buttons on the menubar 
    menuButton = tk.Menu(menu_bar, tearoff = 0)
    secondMenu = tk.Menu(menu_bar, tearoff = 0)

    #---------------------------------------------------------
    # You have to create the button functions before they are created
    # otherwise, they will not work

    # This is the function that creates the new window for "how to play" 
    def howToPlay():

        # I researched on this topic, and it turns out that tkinter has a bug
        # where if an image is created BUT NOT GLOBALLY, then the python
        # garbage collector mistakes it as already used and it destroys the object
        # which is why we have to declare it global, otherwise it wont show up on
        # our top level window 
        global reference_image

        # This function creates the top level window for "how to play"
        # specifies the dimensions 
        how_to_play = tk.Toplevel(width=600, height=600)
        # Title and frames etc.
        how_to_play.title = "How to play"
        title_frame = tk.Frame(how_to_play)
        main_frame = tk.Frame(how_to_play)
        
        # creates the title for the window, done with larger font size
        title = tk.Label(title_frame, text = "How to play", justify = "center",\
                         font = ("Courier New", 24)).pack(side = "top")

        # These are all the instructions that are on the how to play page
        text = tk.Label(main_frame, text="Tic Tac Toe, or noughts and crosses is a game dating back to the Roman Empire\n"\
                        "The first time \"noughts and crosses\" was used was around the 1800s.\n"\
                        "This is a very simple game that many have played for fun when there was\n"\
                        "no internet or social media. Now, lets dive into how to play: Tic Tac Toe\n"\
                        "Tic Tac Toe is played with two players, sometimes, against a bot. Each\n"\
                        "player takes turns placing their corresponding symbol onto the game board\n"\
                        "which is an empty 3 by 3 grid. A player wins if they manage to get three \n"\
                        "of their symbols lined up in a row, before the board fills up.\n"\
                        "This can be horizontal, vertical, or even diagonal. However, it may\n"\
                        "only be in one direction, not a combination of the three", font = ("Courier New", 10)).pack()

        # The order that these widgets are packed is important
        reference_image = tk.PhotoImage(file="Reference.png")
        reference_label = tk.Label(how_to_play, image=reference_image, width=300, height=300)
        # The quit button destroys the window if we want to go back

        # theme.get() retrieves the information stored in the IntVar
        quit_button = tk.Button(main_frame,\
                                command=how_to_play.destroy, width=10, height=1, text="Back").pack()
        # pack the frames last
        reference_label.pack(side = "top")
        title_frame.pack(side = "top")
        main_frame.pack(side = "top")
    
    # opening the credits window
    def openCredits():
        Credits_window = tk.Toplevel(root_window, width=600, height=600)
        Credits_window.title("Credits")

        title = tk.Label(Credits_window, text = "Credits", justify = "center",\
                         font = ("Courier New", 18)).pack(side = "top")
        text = tk.Label(Credits_window, text="Python code developed by me (Jayden)\n"\
                        "Minimax algorithm article on the chess programming wiki\n"\
                        "can be found here: https://www.chessprogramming.org/Minimax\n"\
                        "\nImages made in blender (3) open source.\n"\
                        "Written in python and tkinter").pack()
        quit_button = tk.Button(Credits_window,\
                                command=Credits_window.destroy, width=10, height=1, text="Back").pack()

    # this is a unique function, it is used to refresh the
    # page every time you update your customization preferences

    # the reason why it is .quit() instead of .destroy() is because
    # .quit() destroys everything, including the widgets, and also
    # break out of the mainloop. Replacing the .quit() with
    # .destroy() will result in a (very cryptic) error, which
    # if you lok into it with a linter or debug tool shows something 
    # is wrong with the mainloop() after .destroy() 
    def refresh():
        root_window.quit()
        # calls the main function again to reupdate the customization settings
        main()

    # this is the window that opens when the customize button in the settings tab 
    # is clicked. This created all the radiobuttons for each choice, as well as
    # a select and quit button at the bottom 
    def customize_window():
        custom = tk.Toplevel(root_window)
        custom.title("Customize")
        rb1 = tk.Radiobutton(custom, text = "[Dark] - Default", variable = theme, value = 0).pack()
        rb2 = tk.Radiobutton(custom, text = "[Light] - Default", variable = theme, value = 1).pack()
        rb3 = tk.Radiobutton(custom, text = "[Dark] - Out Of Focus", variable = theme, value = 2).pack()
        rb4 = tk.Radiobutton(custom, text = "[Light] - Out Of Focus", variable = theme, value = 3).pack()
        rb5 = tk.Radiobutton(custom, text = "[Dark] - Color Temp", variable = theme, value = 5).pack()
        rb6 = tk.Radiobutton(custom, text = "[Light] - Color Temp", variable = theme, value = 4).pack()
        rb6 = tk.Radiobutton(custom, text = "[Dark] - Glass", variable = theme, value = 7).pack()
        rb6 = tk.Radiobutton(custom, text = "[Light] - Glass", variable = theme, value = 6).pack()
        
        selectButton = tk.Button(custom,\
                                 text = "SELECT", width=10, height=1, command=refresh).pack(side = "top")
        ExitButton = tk.Button(custom,\
                                 text = "EXIT", width=10, height=1, command=custom.destroy).pack(side = "top")

    # this is the main window that is launched when people play the game
    def play(is_playing_computer: bool):
        global player
        # This function we will use in the future (unless I forgot)
        # this is used to get the coordinates of a mouse click, so
        # you dont have to use an entrybox as a way of playing the game 
        def coordsToIndex(event):
            global player
            x = int(str(event.x))
            y = int(str(event.y))
            # ^^^ finds the x, y values of the click
            
            print(f"debugging info {time.time()}\n")
            print(f" Mouse coordinates X:{x} Y:{y}")
            '''
            Sort of how the code determines the index
            The board looks like this:
              |  |  
            --------
              |  |  
            --------
              |  |  
            ____________________________________________
            0     600 x axis
            ---------

            ---------
            600
            y axis
            ____________________________________________
            and the coords of the window are 600 by 600
            div by 3, we get 200, 200 for the top left intersect
            Using this we can create an algorithm that checks which
            box the mouse was in when it was clicked

            is mouse.x > 200:
                is mouse.x > 400:
                    the mouse x is < 600 (screen size)
                else:
                    the mouse x is < 400
            else:
                the mouse x is < 200
            '''
            # amke the temp variables
            col = None
            row = None
            #find the specific column where the click occured
            if x < 201:col = 0
            elif x < 401:col = 1
            else:col = 2
            #finding the specific row the click occured
            if y < 201:row = 0
            elif y < 401:row = 1
            else:row = 2
            index = row * 3 + col
            print(f"Coordinates to list index: {index}")
            if engine.gb[index] == " ":
                engine.gb[index] = player
                player = not player
                draw()
                if is_playing_computer:
                    engine.mmx()
                    engine.gb[engine.best_move] = player
                    player = not player
                    draw()
        
        top_level = tk.Toplevel(root_window, width=600, height=600)
        top_level.title("PLAY")

        screen_width = top_level.winfo_screenwidth()  #find the width of the screen
        screen_height = top_level.winfo_screenheight() # find the height of the screen

        # Calculate Starting X and Y coordinates for Window
        x = int((screen_width/2) - (300))
        y = int((screen_height/2) - (300))

        top_level.geometry(f'{600}x{600}+{x}+{y}')
        # This just makes the playing window open on top of other active windows
        '''top_level.attributes("-topmost", True)'''
        # this binds the left mouse button to a function that records its coords to determine 
        # where the mouse was when it clicked to generate the moves
        top_level.bind("<Button 1>", coordsToIndex)
        canvas = tk.Canvas(top_level, width=600, height=600)
        # creates the lines that make up the grid for tic tac toe

        def draw():
            canvas.delete("all")
            canvas.create_line(-1, 200, 601, 200, width=10)
            canvas.create_line(-1, 400, 601, 400, width=10)
            canvas.create_line(200, -1, 200, 601, width=10)
            canvas.create_line(400, -1, 400, 601, width=10)
            for index in engine.gb:
                if engine.gb[index] == True:
                        canvas.create_line((index%3)*200+50, (index//3)*200 + 50, (index%3)*200 + 150, (index//3)*200 + 150, width=5)
                        canvas.create_line((index%3)*200+150, (index//3)*200 + 50, (index%3)*200 + 50, (index//3)*200 + 150, width=5)
                elif engine.gb[index] == False:
                        canvas.create_oval((index%3)*200+50, (index//3)*200 + 50, (index%3)*200 + 150, (index//3)*200 + 150, width=5)
            if engine.checkWin(True):
                top_level.destroy()
                game_over = tk.Toplevel()
                game_over.title("Game Over!")
                game_over_label = tk.Label(game_over, text="Player X won!").pack()
                exit_btn = tk.Button(game_over, text = "Back", command = game_over.destroy).pack()
            if engine.checkWin(False):
                top_level.destroy()
                game_over = tk.Toplevel()
                game_over.title("Game Over!")
                game_over_label = tk.Label(game_over, text="Player O won!").pack()
                exit_btn = tk.Button(game_over, text = "Back", command = game_over.destroy).pack()
            if engine.checkDraw():
                top_level.destroy()
                game_over = tk.Toplevel()
                game_over.title("Game Over!")
                game_over_label = tk.Label(game_over, text="It's a draw!").pack()
                exit_btn = tk.Button(game_over, text = "Back", command = game_over.destroy).pack()
        draw()
        # packing the canvas
        canvas.pack()
        
    # These two funtions create a way to pass arguements through buttons
    # Since I dont want to rewrite the code just for palying against a 
    # different opponent
    def pvc():
        global player, ipc
        player = True
        engine.reset()
        engine.mmx()
        engine.gb[engine.best_move] = player
        player = not player
        play(True)
        ipc = True
    def pvp():
        global player
        player = True
        engine.reset()
        play(False)
        global ipc
        ipc = False

    # Adding the buttons in the menu, how to play, credits, etc. 
    menuButton.add_command(label = "How To Play", command = howToPlay)
    menuButton.add_command(label = "Credits", command = openCredits)
    # FIRST MENU ^^^--------------------------------------------

    secondMenu.add_command(label = "Customize", command = customize_window)
    secondMenu.add_command(label = "Close", command = root_window.destroy)
    # SECOND MENU ^^^--------------------------------------------


    # Creating the list of buttons and adding to the menubar
    menu_bar.add_cascade(label = "Game", menu = menuButton)
    menu_bar.add_cascade(label = "Settings", menu = secondMenu)
    # ----------------------------------------------------------
    # 
    # These lines below create the items in the home screen
    # root frame holds the background image 
    root_frame = tk.Frame(root_window, width=600, height=600).place(x = 0, y = 0)
    
    
    # play the game button
    play_button = tk.Button(root_frame, width=30, height=2, command=pvp, text = "PLAYER VS PLAYER").place(x = 135, y = 160)
    play_computer = tk.Button(root_frame, width=30, height=2, command=pvc, text = "PLAYER VS COMPUTER").place(x = 135, y = 240)


    # This is the "packing" of the menubar - so we can see it 
    root_window.config(menu = menu_bar)
    # mainloop for the root window
    root_window.mainloop()

# good practice, makes your files useable for importing as modules
if __name__ == "__main__":
    main()
