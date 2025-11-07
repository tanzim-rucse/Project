# vocab_reminder.py

import random
import tkinter as tk
import csv
import time

# --- This part is unchanged ---
PROGRESS_FILE = 'progress.txt'
my_vocabulary = []
try:
    # --- THIS LINE IS FIXED ---
    with open('vocab.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file) 
        for row in reader:
            my_vocabulary.append(row)
except FileNotFoundError:
    my_vocabulary = [
        {"word": "Error", "meaning": "File not found", "example": "Please create vocab.csv"}
    ] 

# --- This part is unchanged ---
def get_current_index():
    try:
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

# --- This part is unchanged ---
current_index = get_current_index()
vocab_size = len(my_vocabulary)
if current_index >= vocab_size and vocab_size > 0:
    current_index = 0
if my_vocabulary:
    word_data = my_vocabulary[current_index]
else:
    word_data = {"word": "Error", "meaning": "List is empty", "example": "Add words to vocab.csv"}
    current_index = 0
    vocab_size = 0

# --- NEW: Helper function to save progress ---
# We put this in a function because two buttons will use it.
def save_next_index(index_to_learn, total_words):
    next_index = index_to_learn + 1
    if next_index >= total_words:
        next_index = 0 # Loop back to the start
    
    try:
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            f.write(str(next_index))
    except Exception as e:
        print(f"Error saving progress: {e}") # For debugging
    
    return next_index


# --- This is our main window function ---
def show_window(current_word_data, index_to_learn, total_words):
    root = tk.Tk()
    root.title("Vocabulary Reminder")
    root.attributes('-topmost', True) 

    # --- Progress text (Unchanged) ---
    progress_text = f"Word {index_to_learn + 1} of {total_words}"
    label_progress = tk.Label(root, text=progress_text, font=("Arial", 10), fg="grey")
    label_progress.pack(pady=(10,0))

    # --- Word text (Unchanged) ---
    word_text = f"""
Word: {current_word_data['word']}

Bangla Meaning: {current_word_data['meaning']}

Example: {current_word_data['example']}
"""
    label_word = tk.Label(root, text=word_text, font=("Arial", 14), justify=tk.LEFT, padx=20, pady=20)
    label_word.pack() 

    # --- Button Function 1: Snooze (Unchanged) ---
    def snooze_and_reopen():
        root.destroy()
        # FOR TESTING: You can change 300 to 5 (for 5 seconds)
        time.sleep(300) 
        # Re-show the *exact same* window
        show_window(current_word_data, index_to_learn, total_words)

    # --- Button Function 2: Save and show NEXT ---
    def show_next_word():
        # Save the *next* index
        next_index = save_next_index(index_to_learn, total_words)
        
        # Get the next word's data
        next_word_data = my_vocabulary[next_index]
        
        # Close this window
        root.destroy()
        
        # Immediately open the new window with the next word
        show_window(next_word_data, next_index, total_words)

    # --- Button Function 3: Save and EXIT ---
    def mark_as_learned_and_exit():
        # Save the *next* index
        save_next_index(index_to_learn, total_words)
        
        # Close the window and end the program
        root.destroy()

    # --- Create the buttons ---
    # We put them in a Frame to keep them organized
    button_frame = tk.Frame(root)
    button_frame.pack(padx=10, pady=10)

    button_snooze = tk.Button(button_frame, text="Snooze (5 min)", font=("Arial", 12), command=snooze_and_reopen)
    button_snooze.pack(side=tk.LEFT, padx=5)

    # --- NEW "Next Word" Button ---
    button_next = tk.Button(button_frame, text="Next Word", font=("Arial", 12), command=show_next_word, fg="blue", width=12)
    button_next.pack(side=tk.LEFT, padx=5)

    button_done = tk.Button(button_frame, text="Done for Today", font=("Arial", 12), command=mark_as_learned_and_exit)
    button_done.pack(side=tk.RIGHT, padx=5)

    root.mainloop()

# --- This is the line that starts the program (Unchanged) ---
show_window(word_data, current_index, vocab_size)