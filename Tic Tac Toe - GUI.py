#!usr/bin/env python3


# Tic Tac Toe - zFa3
# Importing all the modules, tkinter, custom TicTacToe Module
# as well as time, which is mostly used for debugging
import tkinter as tk, tkinter.messagebox
from TicTacToe_ab import *
import time, random as rd

# setting the player variable, True is player "X" False is other player
player = True
# Turn this on/off to enable/disable the debug info
# printed in the terminal (during player v player or player v computer)
debug_info = True

# creating the engine from custom module
engine = TicTacToe()

# this dictionary contains the image and colors used for each theme
# Each one has an image for the background, and some shades of colors to use
# for buttons, bg colors, etc

    # the layout of the dict

    # themes = {
    # 1: (image.png, color #1, color #2)
    # 2: (image.png, color #1, color #2)
    # etc. 
    # }
themes = {0: ("DarkMode.png", "#787878", "#E09E20"),\
          1: ("LightMode.png", "#FFFFFF", "#99ff99"),\
          2: ("OOF_DarkMode.png", "#919191", "#9DE4E4"),\
          3: ("OOF_LightMode.png", "#D4D4D4", "#729A77"),\
          4: ("LightTemp.png", "#BBACBB", "#E02020"),\
          5: ("DarkTemp.png", "#787C79", "#59DE69"),\
          6: ("LightGlass.png", "#505050", "#65CC97"),
          7: ("DarkGlass.png", "#6B6B6B", "#7EB7B6"),\
          }

# create the main window
# ----------------------
# I create this outside the main function because whenever you create
# or define a tkinter IntVar, it defaults to 0. In this case, it means
# every time I reopen/refresh the window for a new theme, it wont work
# because it resets to zero every time 

# you also need the root window to assign an IntVar to
# otherwise errors occur
root_window = tk.Tk()
theme = tk.IntVar()
theme.set(1)


def GenRand():
    global color
    # this generates a random color every time you run the program
    while True:
        # checks if the color is the same as the other piece, if so regenerate
        # using Augmented assignment - similar to fstrings
        # using "x" represents hexidecimal python formats it as hexadecimal
        # example #FF99FF or #000000

        # I believe this is actually a depricated feature in favor of format()...
        color = '#%02x%02x%02x' % (rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255))
        if color != themes[theme.get()][2]:
            break

# main function
def main():

    # config, changes the backgroud, color, size, etc.
    root_window.config(background=f"{themes[theme.get()][1]}")
    # dimensions
    root_window.config(width=500, height=500)
    # title
    root_window.title("Tic Tac Toe")
    
    # create an icon for the window
    # similar to a favicon for HTML code
    icon = tk.PhotoImage(file = "icon.png")
    root_window.iconphoto(True, icon)
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
        text = tk.Label(main_frame,\
            text="Lets dive into how to play: Tic Tac Toe\n"\
            "Tic Tac Toe is played with two players, sometimes,\n"\
            "against a bot. Each player takes turns placing their\n"\
            "corresponding symbol onto the game board which is an\n"\
            "empty 3 by 3 grid. A player wins if they manage to get three \n"\
            "of their symbols lined up in a row, before the board fills up.\n"\
            "This can be horizontal, vertical, or even diagonal. However, it may\n"\
            "only be in one direction, not a combination of the three\n\n"\
            "(Make sure you close all windows before clicking play!)", font = ("Courier New", 10)).pack()

        # The order that these widgets are packed is important
        reference_image = tk.PhotoImage(file="Reference.png")
        reference_label = tk.Label(how_to_play, image=reference_image, width=150, height=150)
        # The quit button destroys the window if we want to go back

        # theme.get() retrieves the information stored in the IntVar
        quit_button = tk.Button(main_frame, background=themes[theme.get()][2],\
                                command=how_to_play.destroy, width=10, height=1, text="Back").pack()
        # pack the frames last
        reference_label.pack(side = "top")
        title_frame.pack(side = "top")
        main_frame.pack(side = "top")
    
    # opening the credits window
    def openCredits():
        Credits_window = tk.Toplevel(root_window, width=600, height=600)
        Credits_window.title("Credits")
        # mostly straightforward
        title = tk.Label(Credits_window, text = "Credits", justify = "center",\
                         font = ("Courier New", 18)).pack(side = "top")
        text = tk.Label(Credits_window, text="Python code developed by me (Jayden)\n"\
                        "Minimax algorithm article on the chess programming wiki\n"\
                        "can be found here: https://www.chessprogramming.org/Minimax\n"\
                        "\nImages made in blender (3) open source.\n"\
                        "Written in python and tkinter").pack()
        quit_button = tk.Button(Credits_window, background=themes[theme.get()][2],\
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
        # generate a new set of (random) colors
        GenRand()
        root_window.quit()
        # calls the main function again to reupdate the customization settings
        main()

    # this is the window that opens when the customize button in the settings tab 
    # is clicked. This created all the radiobuttons for each choice, as well as
    # a select and quit button at the bottom 
    def customize_window():
        custom = tk.Toplevel(root_window)
        custom.title("Customize")
        # create all the radiobuttons on the customize screen
        # each one assigned to a key for the dict
        # text, variable to change, value to set the variable to, packing
        rb1 = tk.Radiobutton(custom, text = "[Dark] - Default", variable = theme, value = 0).pack()
        rb2 = tk.Radiobutton(custom, text = "[Light] - Default", variable = theme, value = 1).pack()
        rb3 = tk.Radiobutton(custom, text = "[Dark] - Out Of Focus", variable = theme, value = 2).pack()
        rb4 = tk.Radiobutton(custom, text = "[Light] - Out Of Focus", variable = theme, value = 3).pack()
        rb5 = tk.Radiobutton(custom, text = "[Dark] - Color Temp", variable = theme, value = 5).pack()
        rb6 = tk.Radiobutton(custom, text = "[Light] - Color Temp", variable = theme, value = 4).pack()
        rb7 = tk.Radiobutton(custom, text = "[Dark] - Glass", variable = theme, value = 7).pack()
        rb8 = tk.Radiobutton(custom, text = "[Light] - Glass", variable = theme, value = 6).pack()
        
        selectButton = tk.Button(custom, background=themes[theme.get()][2],\
                        text = "SELECT", width=10, height=1, command=refresh).pack(side = "top")
        ExitButton = tk.Button(custom, background=themes[theme.get()][2],\
                        text = "EXIT", width=10, height=1, command=custom.destroy).pack(side = "top")

    # this is the main window that is launched when people play the game
    def play(is_playing_computer: bool):
        global player
        # This function we will use in the future (unless I forgot)
        # this is used to get the coordinates of a mouse click, so
        # you dont have to use an entrybox as a way of playing the game 
        def coordsToIndex(event):
            global player
            x, y = int(str(event.x)), int(str(event.y))
            # ^^^ finds the x, y values of the click
            # tuple assignment, (a, b) = (int, float)
            '''
            The tkinter window looks like this, the coords respectively:
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

            an easier way to accomplish this is by:

            row = x_coord // {side_length of each small square}
            '''
            # find the specific column where the click occured
            # screen is 600x600, three rows and columns is 200x200 boxes
            
            # this finds the row and column of the click
            row, col = x//200, y//200
            index = row + col * 3
            if debug_info:
                print(f"x: {x}, y: {y}, index: {index}")
                print(f"Player: {player}, Player to move: {not player}")

            # plays the move, the place where you clicked
            # chcks if you are playing against the computer, 
            # if so, then play the engine's best move 
            if engine.gb[index] == " ":
                engine.gb[index] = player
                player = not player
                # draw function creates the elements on the screen
                draw()
                # if playing computer, and neither player has won then find best move
                if is_playing_computer and not engine.checkWin(True) and not engine.checkWin(False):
                    time1 = time.perf_counter()
                    engine.debug = 0
                    evaluation = engine.mmx()
                    # format the time as seconds, with 0.2f to two decimal places
                    # 549945 total positions, ab pruning reduces the positions searched
                    if debug_info:
                        print(f"Engine Evaluation: {evaluation}, difficulty (depth): {engine.difficulty}")
                        print(f"time taken: {format((time.perf_counter()-time1), "0.2f")} seconds")
                        print(f"searched {engine.debug} positions")
                        print("################################################")
                    try: engine.gb[engine.top_moves[rd.randint(0, len(engine.top_moves) - 1)][1]] = player
                        # this line chooses a random move from the top moves. This means it will still play at
                        # maximum performance, but it won't play the same moves over and over
                    except: engine.gb[engine.best_move] = player
                    player = not player
                    draw()
        
        # this makes sure that there is no other play window open
        # fixes a bug where you can open as many windows as you want, which
        # intereferes with each other
        window_isopen = False
        # this is a tkinter method which returns all the children or
        # instances of the root_window. This includes toplevels, menus, etc 
        children = root_window.winfo_children()
        for i in children:
            # is instance returns true if the first item is
            # an instance of the second item, in this case
            # if a widget is a toplevel window

            # example of isinstance:
            # isinstance(1, int)   returns True
            if isinstance(i, tk.Toplevel): window_isopen = True
        if not window_isopen:
            top_level = tk.Toplevel(root_window, width=600, height=600)
            top_level.title("PLAY")
            # this finds the dimensions of the screen, sets the variables accordingly
            screen_width = top_level.winfo_screenwidth()
            screen_height = top_level.winfo_screenheight()

            # Calculate Starting X and Y coordinates for top_level window
            x = int((screen_width/2) - (300))
            y = int((screen_height/2) - (300))

            # geometry sets the top level dimensions and where the window opens up
            top_level.geometry(f'{600}x{600}+{x}+{y}')
            # This just makes the playing window open on top of other active windows
            '''top_level.attributes("-topmost", True)'''
            # this binds the left mouse button to a function that records its coords to determine 
            # where the mouse was when it clicked to generate the moves
            top_level.bind("<Button 1>", coordsToIndex)
            canvas = tk.Canvas(top_level, width=600, height=600, background=f"{themes[theme.get()][1]}")
            # creates the lines that make up the grid for tic tac toe

            # create a function for clearing then resrawing the updated canvas


            def draw():
                # if there is a win/draw/lose then show the corresponding pop up
                
                if engine.checkWin(True):
                    # delay 100 ms
                    top_level.after(100)
                    # destroys the game window
                    top_level.destroy()
                    # makes the new top level window
                    tkinter.messagebox.showinfo("Game Over", "Player X Won!")
                elif engine.checkWin(False):
                    # delay 100 ms
                    top_level.after(100)
                    top_level.destroy()
                    tkinter.messagebox.showinfo("Game Over", "Player O Won!")
                elif engine.checkDraw():
                    # delay 100 ms
                    top_level.after(100)
                    top_level.destroy()
                    tkinter.messagebox.showinfo("Game Over", "You Tied")
                else:
                    # clears the canvas so we dont have overlapping elements
                    canvas.delete("all")
                    # draws all the lines of the board (grid)
                    # x1, y1, x2, y2, width of the line
                    canvas.create_line(-1, 200, 601, 200, width=10, fill="grey")
                    canvas.create_line(-1, 400, 601, 400, width=10, fill="grey")
                    canvas.create_line(200, -1, 200, 601, width=10, fill="grey")
                    canvas.create_line(400, -1, 400, 601, width=10, fill="grey")
                    # loops over the entire board, if there is a piece,
                    # then draw the corresponding shape 
                    for index in engine.gb:
                        if engine.gb[index] == True:
                                # the % sign in this case means modulo rather than string augmentation
                                # a % b basically returns the remainder of a / b

                                # this creates the "X"s of the board, by taking the index and
                                # reverse engineering where to place the piece
                                # take the index, and figure the rows and column by // and %
                                # then take the row and column information
                                # and multiplying it by 200, since the board is 600 x 600
                                canvas.create_line((index%3)*200+50, (index//3)*200 + 50,\
                                                    (index%3)*200 + 150, (index//3)*200 + 150,\
                                                    width=12, fill = f"{themes[theme.get()][2]}")

                                canvas.create_line((index%3)*200+150, (index//3)*200 + 50,\
                                                    (index%3)*200 + 50, (index//3)*200 + 150,\
                                                    width=12, fill = f"{themes[theme.get()][2]}")
                                # the +50 is so that the shape is centered in the square
                        elif engine.gb[index] == False:
                                canvas.create_oval((index%3)*200+50, (index//3)*200 + 50,\
                                                    (index%3)*200 + 150, (index//3)*200 + 150,\
                                                    width=12, outline = f"{color}")
            # call the said function
            draw()
            # packing the canvas
            canvas.pack()
        
    # These two funtions create a way to pass arguements through buttons
    # Since I dont want to rewrite the code just for palying against a 
    # different opponent

    # two (not very effecient) functions that are attatched to the buttons
    # since buttons cannot do multiple things at the same time
    # pvc - player versus computer
    # pvp - player versus player 


    def pvc():
        # global - which player to move, is playing computer
        global player, is_playing_engine
        ####################################################
        # same thing at line 235, checks to make sure there is no 
        # window open before doing the stuff underneath 
        window_isopen = False
        children = root_window.winfo_children()
        for i in children:
            if isinstance(i, tk.Toplevel):
                window_isopen = True
        ####################################################
        if not window_isopen:
            # set the payer to True, computer goes first
            player = True
            # reset is a custom method, resets the gb (gamboard)
            engine.reset()
            # calls the minimax function, gets the best move
            time1 = time.perf_counter()
            engine.debug = 0
            # calling the custom function
            evaluation = engine.mmx()
            if debug_info:
                print(f"Engine Evaluation: {evaluation}, difficulty (depth): {engine.difficulty}")
                print(f"time taken: {format((time.perf_counter()-time1), "0.2f")} seconds")
                print(f"searched {engine.debug} positions")
                print("################################################")
                #-------------------------^^^------------------ prints out the debug information
            # plays the best move
            engine.gb[engine.best_move] = player
            # swaps the "player to move" to the opponent
            player = not player
            # create 
            play(True)
            is_playing_engine = True


    def pvp():
        # global - which player to move, is playing computer
        global player, is_playing_engine
        ####################################################
        # this part of the code makes sure there isn't currently a game running
        window_isopen = False
        children = root_window.winfo_children()
        for i in children:
            if isinstance(i, tk.Toplevel):
                window_isopen = True
        if not window_isopen:
        ####################################################
            player = True
            # resets the game
            engine.reset()
            # calls the main function
            play(False)
            # sets is_playing_engine (is playing computer) to false so the engine
            # doesn't run
            is_playing_engine = False


    def difficulty():
        # opens a new window so users can customize the difficulty of the engine
        query = tk.Toplevel(root_window, width=150, height=150)
        instruction = tk.Label(query, text="Enter diffuculty (1: Easy - 10: Impossible):").pack()
        ##############################################
        entry_box = tk.Entry(query)     ##############
        entry_box.pack()                ##############
        ##############################################
        # tkinter entryboxes must be packed seperately
        # ex: entry_box = tk.Entry(root_window).pack()
        # otherwise they WILL NOT work
        # this is a pain ^
        def set_difficulty():
            try:
                # try to set the difficulty wiht custom setter method
                engine.setter(int(entry_box.get()))
                # destroys the window after selection
                query.destroy()
            except: pass
        # mostly customixation options, create the submit button
        submit = tk.Button(query, text="Enter", relief= "ridge", command=set_difficulty).pack()

    # Adding the buttons in the menu, how to play, credits, etc. 
    menuButton.add_command(label = "How To Play", command = howToPlay)
    menuButton.add_command(label = "Credits", command = openCredits)
    # FIRST MENU ^^^--------------------------------------------

    secondMenu.add_command(label = "Customize", command = customize_window)
    secondMenu.add_command(label = "Difficulty settings", command = difficulty)
    secondMenu.add_command(label = "Close", command = root_window.destroy)
    # SECOND MENU ^^^--------------------------------------------

    # Creating the list of buttons and adding to the menubar
    menu_bar.add_cascade(label = "Game", menu = menuButton)
    menu_bar.add_cascade(label = "Settings", menu = secondMenu)
    # ----------------------------------------------------------
    # These lines below create the items in the home screen
    # root frame holds the background image 
    root_frame = tk.Frame(root_window, width=600, height=600,\
                          background = f"{themes[theme.get()][1]}").place(x = 0, y = 0)
    
    # adds the image behind the button, .pack() doesnt work for this kind of job
    background_image = tk.PhotoImage(file = f"{themes[theme.get()][0]}")
    background_label = tk.Label(root_frame, width=500, height=500, image=background_image)
    # .place() lets us make elements on top of other element,
    # as an example, buttons on top of label or image 
    background_label.place(x=0, y=0)
    # play the game button
    play_button = tk.Button(root_frame, width=30, height=2, command=pvp,\
        text = "PLAYER VS PLAYER", background=themes[theme.get()][2]).place(x = 135, y = 160)
    # play the computer button
    play_computer = tk.Button(root_frame, width=30, height=2, command=pvc,\
        text = "PLAYER VS COMPUTER", background=themes[theme.get()][2]).place(x = 135, y = 240)
    #------------------------------------------------------------------------------------------
    # This is the "packing" of the menubar - so we can see it 
    root_window.config(menu = menu_bar)
    # mainloop for the root window
    root_window.mainloop()
# good practice, makes your files useable for importing as modules
# if run directly, __name__ = "__main__"
# if importing it as a module, it does not run
# avoiding collisions and bugs etc.
if __name__ == "__main__":
    GenRand()
    main()
