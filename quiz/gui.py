import tkinter as tk
import subprocess
import json

def button_click():
    text = text_entry.get("1.0", "end-1c")  # Get the text from the text box
    # print("Text entered:", text)
    print("Button clicked!")

    # Pass the text to the main file using subprocess
    subprocess.call(["python", "main.py", text])
    
    # print("Sucessful executed!")
    text_label = tk.Label(window, text="Successfully Executed! Click on Show generated MCQ to see the Results")
    text_label.pack()
    

def load_file():
    file_path = "mcqs.json"  # Changed file extension to .json
    try:
        with open(file_path, 'r') as file:
            mcqs_list = json.load(file)  # Load JSON content
            text_area.delete(1.0, tk.END)  # Clear previous content
            for mcq in mcqs_list:
                text_area.insert(tk.END, f"Question {mcq['question_number']}: {mcq['question_text']}\n")
                for option in mcq['options']:
                    text_area.insert(tk.END, f"{option['option_letter']}) {option['option_text']}\n")
                text_area.insert(tk.END, "\n")
            text_area.pack()  # Make the text area visible
    except FileNotFoundError:
        text_area.delete(1.0, tk.END)  # Clear previous content
        text_area.insert(tk.END, "File not found!")


# Create the main window
window = tk.Tk()
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
window.title("TEXT TO MCQ")

# Create a text box widget
text_entry = tk.Text(window, height=15, width=150)
text_entry.pack(pady=20)

# Create a button widget
button = tk.Button(window, text="Text to MCQ", command=button_click, width=15, height=2)
button.pack(pady=10)

# Create a button to load the file
button = tk.Button(window, text="Show generated MCQ", command=load_file)
button.pack(padx=10, pady=10)

# Create a text area to display file content (initially hidden)
text_area = tk.Text(window, height=20, width=170)
text_area.pack_forget()

# Start the main event loop
window.mainloop()
