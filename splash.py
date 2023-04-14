import tkinter as tk
root = tk.Tk()
root.title("Hand Gestures for HCI")
root.geometry("600x200")

label = tk.Label(root, text="HCI by Michael Ikoku", font=('Arial', 25))
label.pack(pady=40)
tk.

button = tk.Button(root, text="Virtual Mouse", font=('Arial', 16))
button.pack()

root.mainloop()
