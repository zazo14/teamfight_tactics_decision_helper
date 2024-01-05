import tkinter as tk

def create_overlay(game):
    # Initialize the root window
    root = tk.Tk()
    root.attributes('-topmost', True)  # This line makes the window stay on top

    #root.geometry('120x80')  # Set this to your desired dimensions
    root.overrideredirect(True)  # This removes the title bar

    # Create the label and pack it
    label = tk.Label(root, bg='white')
    label.pack()

    def update_stats():
        # Create the display text
        display_text = f"""
        Status: {game.status}
        \n
        Health: {game.health}
        Stage: {game.stage}
        Round: {game.round}
        Gold: {game.gold}
        XP: {game.xp}
        Level: {game.level}
        """
        label.config(text=display_text)
        root.after(1000, update_stats)  # Schedule the next update

    update_stats()  # Start the updates

    # Start the main loop
    root.mainloop()