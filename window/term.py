import tkinter as tk
import subprocess

class TerminalEmulator(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)

        self.text = tk.Text(self, bg='black', fg='white', insertbackground='white')
        self.text.pack(fill=tk.BOTH, expand=True)
        self.text.bind('<Return>', self.execute_command)
        self.text.bind('<BackSpace>', self.handle_backspace)
        self.text.insert(tk.END, "$ ")  # Prompt
        self.text.mark_set("input_start", "insert")

    def execute_command(self, event):
        input_start_index = self.text.index("input_start")
        input_end_index = self.text.index("insert lineend")
        command = self.text.get(input_start_index, input_end_index).strip()

        self.text.insert(tk.END, "\n")
        
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            output = e.output
        
        self.text.insert(tk.END, output)
        self.text.insert(tk.END, "$ ")
        self.text.mark_set("input_start", self.text.index(tk.END))
        self.text.see(tk.END)
        
        return "break"

    def handle_backspace(self, event):
        input_start_index = self.text.index("input_start")
        if self.text.compare("insert", ">", input_start_index):
            return None
        else:
            return "break"

def run():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.85)
    root.geometry("800x600")
    terminal = TerminalEmulator(root)
    root.mainloop()

if __name__ == "__main__":
    run()

