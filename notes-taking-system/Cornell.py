from tkinter import *
from tkinter import filedialog, messagebox

class CornellNote:
    def __init__(self, master):
        self.master = master
        master.title("Cornell Note Taking System")

        # Control Panel Frame for Button Placement
        self.control_frame = Frame(master)
        self.control_frame.pack(side=TOP, fill=X)

        self.save_button = Button(self.control_frame, text="Save", command=self.save_notes)
        self.save_button.pack(side=LEFT)

        # Main Content Frame (Cues and Notes)
        self.content_frame = Frame(master)
        self.content_frame.pack(fill=BOTH, expand=True)

        self.left_frame = Frame(self.content_frame, width=200, height=500, bg="lightgray")
        self.left_frame.pack(side=LEFT, fill=Y)
        Label(self.left_frame, text="Cues", font=("Arial", 12, "bold")).pack(pady=10)
        self.cue_text = Text(self.left_frame, font=("Arial", 12))
        self.cue_text.pack(fill=BOTH, expand=True)

        self.right_frame = Frame(self.content_frame, width=600, height=500)
        self.right_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        Label(self.right_frame, text="Notes", font=("Arial", 12, "bold")).pack(pady=10)
        self.notes_text = Text(self.right_frame, font=("Arial", 12))
        self.notes_text.pack(fill=BOTH, expand=True)
        Label(self.right_frame, text="Summary", font=("Arial", 12, "bold")).pack(pady=10)
        self.summary_text = Text(self.right_frame, font=("Arial", 12))
        self.summary_text.pack(fill=X)

    def save_notes(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Save Cornell Notes",
        )

        if filename:
            # Extract and format text from each section
            cues = self.cue_text.get("1.0", END).strip()
            notes = self.notes_text.get("1.0", END).strip()
            summary = self.summary_text.get("1.0", END).strip()

            # Combine content and write to file
            content = f"**Cues:**\n{cues}\n\n**Notes:**\n{notes}\n\n**Summary:**\n{summary}"
            with open(filename, "w") as file:
                file.write(content)

            # Show confirmation message
            messagebox.showinfo("Success", "Notes saved successfully!")

# Run the main loop
root = Tk()
app = CornellNote(root)
root.mainloop()
