import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from transformers import pipeline
from spellchecker import SpellChecker

model = pipeline("text2text-generation", model="t5-small")
spell = SpellChecker()

def correctSpelling():
    inputText = textInput.get("1.0", "end-1c")
    
    if not inputText.strip():
        messagebox.showwarning("Input Error", "Please enter some text to correct.")
        return

    words = inputText.split()
    correctedWords = [spell.correction(word) for word in words]
    correctedText = " ".join(correctedWords)
    
    finalText = model(f"correct spelling: {correctedText}")
    
    textOutput.delete("1.0", "end")
    textOutput.insert(tk.END, finalText[0]['generated_text'])
    
    historyList.insert(tk.END, finalText[0]['generated_text'])

def clearText():
    textInput.delete("1.0", "end")
    textOutput.delete("1.0", "end")

def saveText():
    correctedText = textOutput.get("1.0", "end-1c")
    if not correctedText.strip():
        messagebox.showwarning("Save Error", "There is no corrected text to save.")
        return

    filePath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filePath:
        with open(filePath, 'w') as file:
            file.write(correctedText)
        messagebox.showinfo("Save Successful", f"Text saved to {filePath}")

def viewHistory():
    try:
        selectedHistory = historyList.get(historyList.curselection())
        textOutput.delete("1.0", "end")
        textOutput.insert(tk.END, selectedHistory)
    except tk.TclError:
        messagebox.showwarning("History Error", "Please select an entry from the history.")

window = tk.Tk()
window.title("Spelling Correction System")
window.geometry("650x600")
window.resizable(True, True)
window.configure(bg="#F5F5F5")

inputLabel = ttk.Label(window, text="Enter Text :", font=("Arial", 12, "bold"), background="#F5F5F5")
inputLabel.pack(pady=10)

textInput = tk.Text(window, height=6, width=60, wrap=tk.WORD, font=("Arial", 12), bd=2, relief="solid")
textInput.pack(pady=10)

correctButton = ttk.Button(window, text="Correct Spelling", command=correctSpelling, width=20, style="TButton")
correctButton.pack(pady=10)

clearButton = ttk.Button(window, text="Clear Text", command=clearText, width=20, style="TButton")
clearButton.pack(pady=5)

saveButton = ttk.Button(window, text="Save Corrected Text", command=saveText, width=20, style="TButton")
saveButton.pack(pady=5)

outputLabel = ttk.Label(window, text="Corrected Text:", font=("Arial", 12, "bold"), background="#F5F5F5")
outputLabel.pack(pady=10)

textOutput = tk.Text(window, height=6, width=60, wrap=tk.WORD, font=("Arial", 12), bd=2, relief="solid")
textOutput.pack(pady=10)

scrollbarInput = tk.Scrollbar(window, command=textInput.yview)
scrollbarInput.pack(side=tk.RIGHT, fill=tk.Y)
textInput.config(yscrollcommand=scrollbarInput.set)

scrollbarOutput = tk.Scrollbar(window, command=textOutput.yview)
scrollbarOutput.pack(side=tk.RIGHT, fill=tk.Y)
textOutput.config(yscrollcommand=scrollbarOutput.set)

historyLabel = ttk.Label(window, text="History of Corrected Texts:", font=("Arial", 12, "bold"), background="#F5F5F5")
historyLabel.pack(pady=10)

historyList = tk.Listbox(window, height=5, width=60, font=("Arial", 12), bd=2, relief="solid")
historyList.pack(pady=10)

viewButton = ttk.Button(window, text="View Selected History", command=viewHistory, width=20, style="TButton")
viewButton.pack(pady=5)

style = ttk.Style(window)
style.configure("TButton", font=("Arial", 12), width=20, padding=6)

window.mainloop()
