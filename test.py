import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time  # Added for progress bar simulation

def get_url(root):
    root.title("Round Robin Score Prediction Configuration")
    root.geometry("800x600+1000+500")  # Set initial size and position
    root.resizable(False, False)  # Make the window size unchangeable

    # Variables to store URL and selection
    url_var = tk.StringVar()
    selection_var = tk.StringVar(value="Light")

    # Submit button clicked status
    submitted = False

    # Submit button click handler
    def on_submit():
        nonlocal submitted
        submitted = True
        root.quit()

    # Paste from clipboard handler
    def paste_from_clipboard():
        clipboard_content = root.clipboard_get()
        url_var.set(clipboard_content)
        on_submit()

    # GUI components
    label = tk.Label(root, text="Enter Liquipedia URL:")
    label.pack(pady=10)
    entry = tk.Entry(root, width=50, textvariable=url_var)
    entry.pack(pady=5)

    # Dropdown menu
    dropdown_label = tk.Label(root, text="Select mode:")
    dropdown_label.pack(pady=5)
    dropdown = tk.OptionMenu(root, selection_var, "Heavy", "Light")
    dropdown.pack(pady=5)

    # Paste and Submit buttons
    paste_button = tk.Button(root, text="Paste and Go", command=paste_from_clipboard)
    paste_button.pack(pady=5)
    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack(pady=5)

    log_text_widget = None  # Log text widget placeholder
    progress_bar = None  # Progress bar placeholder

    # URL submission and log field creation loop
    while True:
        root.mainloop()

        url = url_var.get()

        if not submitted:
            return None, None  # Return None if the window was closed

        if url == "" or not url.startswith("https://liquipedia.net"):
            messagebox.showerror("Invalid URL", "Please enter a valid Liquipedia URL.\n\nGiven URL:\n" + url)
            url_var.set("")
            submitted = False
        else:
            # Create log field and progress bar
            log_label = tk.Label(root, text="Log:")
            log_label.pack(pady=10)
            log_text_widget = tk.Text(root, height=20, width=80, font=("Courier New", 12), spacing1=5, spacing2=5, spacing3=5, padx=10, pady=10)
            log_text_widget.pack(pady=5, expand=True, fill=tk.BOTH)

            progress_label = tk.Label(root, text="Progress:")
            progress_label.pack(pady=10)
            progress_bar = tk.ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
            progress_bar.pack(pady=5)

            return url, selection_var.get() == "Heavy", log_text_widget, progress_bar  # Return the URL, selection, log widget, and progress bar

def print_log(log_text_widget, message):
    if log_text_widget:
        def insert_text():
            log_text_widget.config(state=tk.NORMAL)  # Enable editing to insert text
            log_text_widget.insert(tk.END, message + "\n")
            log_text_widget.see(tk.END)
            log_text_widget.config(state=tk.DISABLED)  # Disable editing after insertion
        
        threading.Thread(target=insert_text).start()
    else:
        messagebox.showerror("Log Error", "Log widget not initialized")

def update_progress_bar(progress_bar, value):
    if progress_bar:
        progress_bar["value"] = value
    else:
        messagebox.showerror("Progress Error", "Progress bar not initialized")

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    result = get_url(root)
    if result:
        url, is_heavy, log_text_widget, progress_bar = result
        long_message = "Valid URL submitted: " + url + "\n" + "A" * 10000  # Example long message
        print_log(log_text_widget, long_message)

        # Simulate progress update
        for i in range(101):
            update_progress_bar(progress_bar, i)
            time.sleep(0.05)  # Simulate work being done
    root.mainloop()
