import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque

import pyperclip

from password_generator import generate_password


# ---------- Colors ----------
BG = "#F3F6FB"
CARD = "#FFFFFF"
TEXT = "#172033"
MUTED = "#64748B"
ACCENT = "#2563EB"
BORDER = "#DCE4EF"

WEAK = "#DC2626"
MEDIUM = "#D97706"
STRONG = "#16A34A"


def estimate_strength(length, types_used):
    """
    Estimate password strength using length and character diversity.

    This is a simple educational heuristic, not a formal
    password-strength measurement.
    """
    if length >= 16 and types_used >= 3:
        return "Strong", 100, STRONG

    if length >= 12 and types_used >= 2:
        return "Medium", 60, MEDIUM

    return "Weak", 30, WEAK


def main():
    root = tk.Tk()
    root.title("Secure Password Generator")
    root.geometry("590x790")
    root.minsize(560, 740)
    root.configure(bg=BG)

    # Keep the last five passwords in memory only.
    password_history = deque(maxlen=5)
    current_password = ""

    # ---------- Theme and styles ----------

    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(
        "TFrame",
        background=BG
    )

    style.configure(
        "Card.TFrame",
        background=CARD
    )

    style.configure(
        "TLabel",
        background=BG,
        foreground=TEXT,
        font=("Segoe UI", 10)
    )

    style.configure(
        "Title.TLabel",
        background=BG,
        foreground=TEXT,
        font=("Segoe UI", 21, "bold")
    )

    style.configure(
        "Subtitle.TLabel",
        background=BG,
        foreground=MUTED,
        font=("Segoe UI", 10)
    )

    style.configure(
        "Section.TLabel",
        background=CARD,
        foreground=TEXT,
        font=("Segoe UI", 11, "bold")
    )

    style.configure(
        "Card.TLabel",
        background=CARD,
        foreground=TEXT,
        font=("Segoe UI", 10)
    )

    style.configure(
        "Muted.Card.TLabel",
        background=CARD,
        foreground=MUTED,
        font=("Segoe UI", 9)
    )

    style.configure(
        "TCheckbutton",
        background=CARD,
        foreground=TEXT,
        font=("Segoe UI", 10)
    )

    style.map(
        "TCheckbutton",
        background=[("active", CARD)]
    )

    style.configure(
        "TButton",
        font=("Segoe UI", 10),
        padding=(12, 8)
    )

    style.configure(
        "Accent.TButton",
        background=ACCENT,
        foreground="#FFFFFF",
        font=("Segoe UI", 10, "bold"),
        padding=(14, 9)
    )

    style.map(
        "Accent.TButton",
        background=[
            ("pressed", "#1D4ED8"),
            ("active", "#1D4ED8")
        ],
        foreground=[("disabled", "#FFFFFF")]
    )

    style.configure(
        "TSpinbox",
        padding=5,
        font=("Segoe UI", 10)
    )

    style.configure(
        "Weak.Horizontal.TProgressbar",
        troughcolor="#E5E7EB",
        background=WEAK,
        thickness=10
    )

    style.configure(
        "Medium.Horizontal.TProgressbar",
        troughcolor="#E5E7EB",
        background=MEDIUM,
        thickness=10
    )

    style.configure(
        "Strong.Horizontal.TProgressbar",
        troughcolor="#E5E7EB",
        background=STRONG,
        thickness=10
    )

    # ---------- Page header ----------

    page = ttk.Frame(root, padding=(24, 20))
    page.pack(fill="both", expand=True)

    ttk.Label(
        page,
        text="Secure Password Generator",
        style="Title.TLabel"
    ).pack(anchor="w")

    ttk.Label(
        page,
        text="Create a unique password for your accounts.",
        style="Subtitle.TLabel"
    ).pack(anchor="w", pady=(4, 18))

    # ---------- Settings card ----------

    settings = ttk.Frame(
        page,
        style="Card.TFrame",
        padding=18
    )
    settings.pack(fill="x", pady=(0, 14))

    ttk.Label(
        settings,
        text="PASSWORD SETTINGS",
        style="Section.TLabel"
    ).pack(anchor="w", pady=(0, 12))

    length_row = ttk.Frame(
        settings,
        style="Card.TFrame"
    )
    length_row.pack(fill="x", pady=(0, 14))

    ttk.Label(
        length_row,
        text="Password length",
        style="Card.TLabel"
    ).pack(side="left")

    length_var = tk.IntVar(value=16)

    length_spinbox = ttk.Spinbox(
        length_row,
        from_=8,
        to=128,
        increment=1,
        textvariable=length_var,
        width=8,
        justify="center"
    )
    length_spinbox.pack(side="right")

    ttk.Label(
        settings,
        text="Choose at least two character types",
        style="Muted.Card.TLabel"
    ).pack(anchor="w", pady=(0, 7))

    uppercase_var = tk.BooleanVar(value=True)
    lowercase_var = tk.BooleanVar(value=True)
    numbers_var = tk.BooleanVar(value=True)
    symbols_var = tk.BooleanVar(value=True)

    ttk.Checkbutton(
        settings,
        text="Uppercase letters  (A–Z)",
        variable=uppercase_var
    ).pack(anchor="w", pady=2)

    ttk.Checkbutton(
        settings,
        text="Lowercase letters  (a–z)",
        variable=lowercase_var
    ).pack(anchor="w", pady=2)

    ttk.Checkbutton(
        settings,
        text="Numbers  (0–9)",
        variable=numbers_var
    ).pack(anchor="w", pady=2)

    ttk.Checkbutton(
        settings,
        text="Symbols  (!@#$...)",
        variable=symbols_var
    ).pack(anchor="w", pady=2)

    ambiguous_var = tk.BooleanVar(value=False)

    ttk.Checkbutton(
        settings,
        text="Exclude ambiguous characters (0, O, l, 1)",
        variable=ambiguous_var
    ).pack(anchor="w", pady=(9, 0))

    # ---------- Password result card ----------

    result = ttk.Frame(
        page,
        style="Card.TFrame",
        padding=18
    )
    result.pack(fill="x", pady=(0, 14))

    ttk.Label(
        result,
        text="YOUR PASSWORD",
        style="Section.TLabel"
    ).pack(anchor="w", pady=(0, 9))

    password_var = tk.StringVar(
        value="Generate a password to begin"
    )

    

    password_entry = tk.Entry(
        result,
        textvariable=password_var,
        state="readonly",
        readonlybackground="#F0F5FF",
        foreground="#163A70",
        relief="solid",
        bd=1,
        highlightthickness=1,
        highlightbackground=BORDER,
        font=("Consolas", 13),
        justify="center"
    )

    password_entry.pack(fill="x", ipady=9, pady=(0, 12))

    # ---------- Strength indicator ----------

    strength_row = ttk.Frame(
        result,
        style="Card.TFrame"
    )
    strength_row.pack(fill="x")

    ttk.Label(
        strength_row,
        text="Estimated strength",
        style="Card.TLabel"
    ).pack(side="left")

    strength_var = tk.StringVar(value="Not generated")

    strength_label = tk.Label(
        strength_row,
        textvariable=strength_var,
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 10, "bold")
    )
    strength_label.pack(side="right")

    strength_bar = ttk.Progressbar(
        result,
        orient="horizontal",
        mode="determinate",
        maximum=100,
        value=0,
        style="Weak.Horizontal.TProgressbar"
    )
    strength_bar.pack(fill="x", pady=(8, 7))

    ttk.Label(
        result,
        text=(
            "Estimate based on length and selected character types. "
            "This is not a security guarantee."
        ),
        style="Muted.Card.TLabel",
        wraplength=490,
        justify="left"
    ).pack(anchor="w")

    # ---------- Clipboard ----------

    def copy_password(show_message=True):
        if not current_password:
            messagebox.showinfo(
                "No password",
                "Generate a password first.",
                parent=root
            )
            return

        try:
            pyperclip.copy(current_password)

            if show_message:
                messagebox.showinfo(
                    "Copied",
                    "Password copied to the clipboard.",
                    parent=root
                )

        except pyperclip.PyperclipException:
            messagebox.showerror(
                "Clipboard error",
                "Could not access the clipboard. "
                "You can select and copy the password manually.",
                parent=root
            )

    # ---------- Password generation ----------

    def generate():
        nonlocal current_password

        try:
            length = int(length_spinbox.get())

            selected = [
                uppercase_var.get(),
                lowercase_var.get(),
                numbers_var.get(),
                symbols_var.get()
            ]

            types_used = sum(selected)

            if not 8 <= length <= 128:
                raise ValueError(
                    "Password length must be between 8 and 128."
                )

            if types_used < 2:
                raise ValueError(
                    "Please select at least two character types."
                )

            password = generate_password(
                length,
                uppercase_var.get(),
                lowercase_var.get(),
                numbers_var.get(),
                symbols_var.get(),
                ambiguous_var.get()
            )

            current_password = password
            password_var.set(password)

            # Update estimated strength.
            label, score, color = estimate_strength(
                length,
                types_used
            )

            strength_var.set(label)
            strength_label.configure(fg=color)

            if label == "Strong":
                bar_style = "Strong.Horizontal.TProgressbar"
            elif label == "Medium":
                bar_style = "Medium.Horizontal.TProgressbar"
            else:
                bar_style = "Weak.Horizontal.TProgressbar"

            strength_bar.configure(
                value=score,
                style=bar_style
            )

            # Store history in memory only.
            password_history.appendleft(password)
            update_history()

            # Automatically copy after generation.
            copy_password(show_message=False)

        except (ValueError, tk.TclError) as error:
            messagebox.showerror(
                "Check your settings",
                str(error),
                parent=root
            )

    # ---------- Action buttons ----------

    button_row = ttk.Frame(page)
    button_row.pack(fill="x", pady=(0, 14))

    ttk.Button(
        button_row,
        text="Generate Password",
        style="Accent.TButton",
        command=generate
    ).pack(side="left", expand=True, fill="x", padx=(0, 6))

    ttk.Button(
        button_row,
        text="Copy Password",
        command=copy_password
    ).pack(side="left", expand=True, fill="x", padx=(6, 0))

    # ---------- History card ----------

    history_card = ttk.Frame(
        page,
        style="Card.TFrame",
        padding=18
    )
    history_card.pack(fill="both", expand=True)

    history_heading = ttk.Frame(
        history_card,
        style="Card.TFrame"
    )
    history_heading.pack(fill="x", pady=(0, 8))

    ttk.Label(
        history_heading,
        text="RECENT PASSWORDS",
        style="Section.TLabel"
    ).pack(side="left")

    ttk.Label(
        history_heading,
        text="Last 5 · This session only",
        style="Muted.Card.TLabel"
    ).pack(side="right")

    history_list = tk.Listbox(
        history_card,
        height=5,
        font=("Consolas", 10),
        bg="#F8FAFC",
        fg=TEXT,
        selectbackground="#DBEAFE",
        selectforeground=TEXT,
        relief="solid",
        bd=1,
        highlightthickness=0,
        activestyle="none",
        exportselection=False
    )
    history_list.pack(fill="both", expand=True)

    def update_history():
        history_list.delete(0, tk.END)

        for password in password_history:
            history_list.insert(tk.END, password)

    def copy_selected_history(event=None):
        selection = history_list.curselection()

        if selection:
            selected_password = history_list.get(selection[0])

            try:
                pyperclip.copy(selected_password)
            except pyperclip.PyperclipException:
                messagebox.showerror(
                    "Clipboard error",
                    "Could not access the clipboard.",
                    parent=root
                )

    history_list.bind(
        "<Double-Button-1>",
        copy_selected_history
    )

    ttk.Label(
        history_card,
        text="Double-click a password to copy it.",
        style="Muted.Card.TLabel"
    ).pack(anchor="w", pady=(8, 0))

    # Start the application.
    root.mainloop()


if __name__ == "__main__":
    main()
