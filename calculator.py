import tkinter as tk
from tkinter import font

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x580")
        self.root.minsize(320, 480)
        self.root.configure(bg="#F0F2F5")

        # Calculator state
        self.current_input = "0"
        self.previous_value = None
        self.operator = None
        self.reset_screen = False
        self.history_text = ""
        self.error_state = False

        self.create_styles()
        self.create_widgets()
        self.bind_keys()

    def create_styles(self):
        # Fonts
        self.display_font = font.Font(family="Segoe UI", size=28, weight="bold")
        self.history_font = font.Font(family="Segoe UI", size=13)
        self.btn_font = font.Font(family="Segoe UI", size=16, weight="bold")
        self.clear_font = font.Font(family="Segoe UI", size=16, weight="bold")

    def create_widgets(self):
        # Main container card
        self.card = tk.Frame(self.root, bg="#FFFFFF", bd=0, highlightthickness=0)
        self.card.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Configure card grid layout (Row 0: Display, Row 1-5: Buttons)
        self.card.rowconfigure(0, weight=1, minsize=110)
        for i in range(1, 6):
            self.card.rowconfigure(i, weight=1)
        for j in range(4):
            self.card.columnconfigure(j, weight=1)

        # Display Frame
        self.display_frame = tk.Frame(self.card, bg="#F8FAFC", bd=0)
        self.display_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=12, pady=12)
        
        # Add subtle border/outline to display frame
        self.display_border = tk.Frame(self.card, bg="#E2E8F0", bd=0)
        self.display_border.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
        
        self.display_inner = tk.Frame(self.display_border, bg="#F8FAFC", bd=0)
        self.display_inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        # History label (expression preview)
        self.history_label = tk.Label(
            self.display_inner, 
            text="", 
            font=self.history_font, 
            bg="#F8FAFC", 
            fg="#64748B", 
            anchor="e",
            padx=12
        )
        self.history_label.pack(side=tk.TOP, fill=tk.X, pady=(10, 0))

        # Main result label
        self.result_label = tk.Label(
            self.display_inner, 
            text="0", 
            font=self.display_font, 
            bg="#F8FAFC", 
            fg="#1E293B", 
            anchor="e",
            padx=12
        )
        self.result_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 10))

        # Button definitions: (text, row, col, rowspan, colspan, type)
        # Types: 'num', 'op', 'clear', 'eq'
        buttons_layout = [
            ("C", 1, 0, 1, 2, "clear"),
            ("/", 1, 2, 1, 1, "op"),
            ("*", 1, 3, 1, 1, "op"),
            
            ("7", 2, 0, 1, 1, "num"),
            ("8", 2, 1, 1, 1, "num"),
            ("9", 2, 2, 1, 1, "num"),
            ("-", 2, 3, 1, 1, "op"),
            
            ("4", 3, 0, 1, 1, "num"),
            ("5", 3, 1, 1, 1, "num"),
            ("6", 3, 2, 1, 1, "num"),
            ("+", 3, 3, 1, 1, "op"),
            
            ("1", 4, 0, 1, 1, "num"),
            ("2", 4, 1, 1, 1, "num"),
            ("3", 4, 2, 1, 1, "num"),
            ("=", 4, 3, 2, 1, "eq"),
            
            ("0", 5, 0, 1, 2, "num"),
            (".", 5, 2, 1, 1, "num"),
        ]

        self.buttons = {}
        for (text, r, c, rs, cs, btype) in buttons_layout:
            btn = self.create_button(text, btype, lambda t=text: self.on_button_click(t))
            btn.grid(row=r, column=c, rowspan=rs, columnspan=cs, sticky="nsew", padx=5, pady=5)
            self.buttons[text] = btn

    def create_button(self, text, btype, command):
        # Color schemes based on button type
        if btype == "num":
            bg = "#F1F5F9"
            hover_bg = "#E2E8F0"
            fg = "#0F172A"
            font_to_use = self.btn_font
        elif btype == "op":
            bg = "#EEF2FF"
            hover_bg = "#E0E7FF"
            fg = "#4F46E5"
            font_to_use = self.btn_font
        elif btype == "eq":
            bg = "#4F46E5"
            hover_bg = "#4338CA"
            fg = "#FFFFFF"
            font_to_use = self.btn_font
        elif btype == "clear":
            bg = "#FEF2F2"
            hover_bg = "#FEE2E2"
            fg = "#DC2626"
            font_to_use = self.clear_font
        else:
            bg = "#F1F5F9"
            hover_bg = "#E2E8F0"
            fg = "#0F172A"
            font_to_use = self.btn_font

        # Create button using tk.Button with flat relief for modern look
        btn = tk.Button(
            self.card,
            text=text,
            font=font_to_use,
            bg=bg,
            fg=fg,
            activebackground=hover_bg,
            activeforeground=fg,
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            command=command
        )

        # Hover effects
        def on_enter(e):
            if not self.error_state or text == "C":
                btn.config(bg=hover_bg)

        def on_leave(e):
            btn.config(bg=bg)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def bind_keys(self):
        self.root.bind("<Key>", self.handle_keypress)

    def handle_keypress(self, event):
        char = event.char
        keysym = event.keysym

        if keysym in ("Return", "KP_Enter") or char == "=":
            self.on_button_click("=")
        elif keysym in ("BackSpace",):
            self.backspace()
        elif keysym in ("Escape",):
            self.on_button_click("C")
        elif char in "0123456789.":
            self.on_button_click(char)
        elif char in "+-*/":
            self.on_button_click(char)

    def backspace(self):
        if self.error_state:
            return
        if self.reset_screen:
            return
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"
        self.update_display()

    def on_button_click(self, char):
        if char == "C":
            self.clear_all()
            return

        if self.error_state:
            return

        if char in "0123456789":
            if self.reset_screen:
                self.current_input = char
                self.reset_screen = False
            else:
                if self.current_input == "0":
                    self.current_input = char
                else:
                    if len(self.current_input) < 14:  # Prevent excessive length
                        self.current_input += char
            self.update_display()

        elif char == ".":
            if self.reset_screen:
                self.current_input = "0."
                self.reset_screen = False
            elif "." not in self.current_input:
                self.current_input += "."
            self.update_display()

        elif char in "+-*/":
            if self.operator and not self.reset_screen:
                self.calculate(intermediate=True)
            else:
                try:
                    self.previous_value = float(self.current_input)
                except ValueError:
                    self.previous_value = 0.0
            
            self.operator = char
            self.reset_screen = True
            
            # Format display value for history
            prev_str = self.format_number(self.previous_value)
            self.history_text = f"{prev_str} {self.operator}"
            self.history_label.config(text=self.history_text)

        elif char == "=":
            if self.operator and self.previous_value is not None:
                self.calculate(intermediate=False)
                self.operator = None
                self.history_text = ""
                self.history_label.config(text=self.history_text)
                self.reset_screen = True

    def calculate(self, intermediate=False):
        try:
            current_value = float(self.current_input)
            result = 0.0

            if self.operator == "+":
                result = self.previous_value + current_value
            elif self.operator == "-":
                result = self.previous_value - current_value
            elif self.operator == "*":
                result = self.previous_value * current_value
            elif self.operator == "/":
                if current_value == 0:
                    self.show_error("Division by zero")
                    return
                result = self.previous_value / current_value

            self.current_input = self.format_number(result)
            self.update_display()

            if intermediate:
                self.previous_value = result
            else:
                self.previous_value = None

        except ZeroDivisionError:
            self.show_error("Division by zero")
        except Exception:
            self.show_error("Error")

    def format_number(self, num):
        if num is None:
            return "0"
        # Check if integer
        if num == int(num) and not (isinstance(num, float) and abs(num) > 1e15):
            val_str = str(int(num))
        else:
            val_str = f"{num:.10g}"  # Up to 10 significant digits, avoids floating inaccuracies
        return val_str

    def update_display(self):
        # Format display string with length check
        display_str = self.current_input
        if len(display_str) > 12:
            try:
                f_val = float(display_str)
                display_str = f"{f_val:.6e}"
            except Exception:
                display_str = display_str[:12]
        self.result_label.config(text=display_str)

    def show_error(self, message):
        self.error_state = True
        self.result_label.config(text=message, fg="#DC2626")
        self.history_label.config(text="")

    def clear_all(self):
        self.current_input = "0"
        self.previous_value = None
        self.operator = None
        self.reset_screen = False
        self.history_text = ""
        self.error_state = False
        self.result_label.config(fg="#1E293B")
        self.history_label.config(text="")
        self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
