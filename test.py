import tkinter as tk

def on_resize(event):
    # Do something when the window is resized
    pass

root = tk.Tk()
root.title("Resizable Tkinter App")

# Create a frame as the main container
main_frame = tk.Frame(root)
main_frame.grid(sticky="nsew")  # Make the frame expand with the window
main_frame.grid_propagate(0)  # Prevent the frame from propagating its size to children

# Add widgets to the frame using grid
label = tk.Label(main_frame, text="Resizable App")
label.grid(row=0, column=0, pady=20)

entry = tk.Entry(main_frame)
entry.grid(row=1, column=0, pady=10)

button = tk.Button(main_frame, text="Click me")
button.grid(row=2, column=0, pady=10)

# Set row and column weights to make the frame expand with the window
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_rowconfigure(2, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

# Bind the on_resize function to the <Configure> event of the root window
root.bind("<Configure>", on_resize)

root.mainloop()
