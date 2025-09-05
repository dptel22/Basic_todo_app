import customtkinter as ctk
from tkinter import messagebox
import functions
import time
import threading
from datetime import datetime
import json

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # "dark", "light", "system"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


class ModernTodoApp:
    def __init__(self):
        self.setup_window()
        self.setup_variables()
        self.setup_ui()
        self.load_todos()
        self.start_clock()

    def setup_window(self):
        """Initialize the main window with modern styling"""
        self.root = ctk.CTk()
        self.root.title("✨ Modern Todo Manager")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)

        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"800x700+{x}+{y}")

        # Configure grid weights for responsiveness
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

    def setup_variables(self):
        """Initialize application variables"""
        self.todos = []
        self.filtered_todos = []
        self.search_var = ctk.StringVar()
        self.search_var.trace('w', self.on_search)
        self.selected_indices = set()

    def setup_ui(self):
        """Create the modern user interface"""
        # Header frame with gradient-like effect
        self.header_frame = ctk.CTkFrame(self.root, height=80, corner_radius=15)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        self.header_frame.grid_propagate(False)
        self.header_frame.grid_columnconfigure(1, weight=1)

        # App icon and title
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="✨ Todo Manager",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=20, pady=20)

        # Clock and stats
        self.clock_label = ctk.CTkLabel(
            self.header_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.clock_label.grid(row=0, column=1, sticky="e", padx=20, pady=20)

        # Input section
        self.input_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.input_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.input_frame.grid_columnconfigure(1, weight=1)

        # Search bar
        self.search_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="🔍 Search todos...",
            textvariable=self.search_var,
            font=ctk.CTkFont(size=14),
            height=40,
            corner_radius=20
        )
        self.search_entry.grid(row=0, column=0, columnspan=3, sticky="ew", padx=20, pady=(20, 10))

        # Add todo entry
        self.todo_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="✍️ What needs to be done?",
            font=ctk.CTkFont(size=16),
            height=50,
            corner_radius=25
        )
        self.todo_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(20, 10), pady=(10, 20))
        self.todo_entry.bind("<Return>", self.add_todo)

        # Add button with hover effect
        self.add_button = ctk.CTkButton(
            self.input_frame,
            text="➕ Add",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=50,
            width=100,
            corner_radius=25,
            command=self.add_todo
        )
        self.add_button.grid(row=1, column=2, sticky="e", padx=(10, 20), pady=(10, 20))

        # Main content frame
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.main_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Todo list with custom scrollbar
        self.todo_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            corner_radius=10,
            scrollbar_button_color=("gray70", "gray30"),
            scrollbar_button_hover_color=("gray60", "gray40")
        )
        self.todo_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.todo_frame.grid_columnconfigure(0, weight=1)

        # Control buttons frame
        self.controls_frame = ctk.CTkFrame(self.root, corner_radius=15, height=80)
        self.controls_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(10, 20))
        self.controls_frame.grid_propagate(False)

        # Create control buttons with modern styling
        buttons = [
            ("✏️ Edit", self.edit_todo, "blue"),
            ("✅ Complete", self.complete_selected, "green"),
            ("❌ Delete", self.delete_selected, "red"),
            ("🗑️ Clear All", self.clear_all, "orange"),
            ("💾 Export", self.export_todos, "purple")
        ]

        for i, (text, command, color) in enumerate(buttons):
            btn = ctk.CTkButton(
                self.controls_frame,
                text=text,
                font=ctk.CTkFont(size=13, weight="bold"),
                height=40,
                width=120,
                corner_radius=20,
                fg_color=self.get_color_for_theme(color),
                hover_color=self.get_hover_color_for_theme(color),
                command=command
            )
            btn.grid(row=0, column=i, padx=10, pady=20)

        # Stats label
        self.stats_label = ctk.CTkLabel(
            self.controls_frame,
            text="📊 0 todos",
            font=ctk.CTkFont(size=12)
        )
        self.stats_label.grid(row=0, column=len(buttons), sticky="e", padx=(20, 10), pady=20)

        # Configure controls frame columns
        for i in range(len(buttons) + 1):
            self.controls_frame.grid_columnconfigure(i, weight=1)

    def get_color_for_theme(self, color):
        """Get appropriate colors for the current theme"""
        colors = {
            "blue": ("#1f538d", "#14375e"),
            "green": ("#2d8f2d", "#1e5f1e"),
            "red": ("#d42c2c", "#8b1c1c"),
            "orange": ("#e07b1a", "#b8610d"),
            "purple": ("#9333ea", "#7c2d9b")
        }
        return colors.get(color, colors["blue"])

    def get_hover_color_for_theme(self, color):
        """Get hover colors for buttons"""
        hover_colors = {
            "blue": ("#144870", "#0f2d4a"),
            "green": ("#236b23", "#174517"),
            "red": ("#a32222", "#6b1515"),
            "orange": ("#c4630f", "#9b4f0a"),
            "purple": ("#7c2bb8", "#5e2089")
        }
        return hover_colors.get(color, hover_colors["blue"])

    def create_todo_item(self, todo_text, index):
        """Create a modern todo item widget"""
        # Main container for todo item
        item_frame = ctk.CTkFrame(
            self.todo_frame,
            corner_radius=12,
            height=60,
            fg_color=("gray90", "gray20") if index % 2 == 0 else ("gray85", "gray25")
        )
        item_frame.grid(row=index, column=0, sticky="ew", pady=3, padx=5)
        item_frame.grid_propagate(False)
        item_frame.grid_columnconfigure(1, weight=1)

        # Checkbox for selection
        checkbox = ctk.CTkCheckBox(
            item_frame,
            text="",
            width=20,
            command=lambda: self.toggle_selection(index)
        )
        checkbox.grid(row=0, column=0, padx=(15, 10), pady=15, sticky="w")

        # Todo text with better formatting
        if todo_text.startswith('['):
            # Extract timestamp and text
            end_bracket = todo_text.find(']')
            if end_bracket != -1:
                timestamp = todo_text[1:end_bracket]
                text = todo_text[end_bracket + 2:]
                display_text = f"{text}\n🕐 {timestamp}"
            else:
                display_text = todo_text
        else:
            display_text = todo_text

        todo_label = ctk.CTkLabel(
            item_frame,
            text=display_text,
            font=ctk.CTkFont(size=14),
            anchor="w",
            justify="left"
        )
        todo_label.grid(row=0, column=1, sticky="ew", padx=10, pady=15)

        # Priority indicator (you can extend this)
        priority_indicator = ctk.CTkLabel(
            item_frame,
            text="📌",
            font=ctk.CTkFont(size=16),
            width=30
        )
        priority_indicator.grid(row=0, column=2, padx=(5, 15), pady=15)

        # Store references for later manipulation
        setattr(item_frame, 'checkbox', checkbox)
        setattr(item_frame, 'todo_label', todo_label)

        return item_frame

    def load_todos(self):
        """Load todos and refresh display"""
        self.todos = functions.get_todos()
        self.filtered_todos = self.todos.copy()
        self.refresh_todo_display()

    def refresh_todo_display(self):
        """Refresh the todo list display"""
        # Clear existing todo items
        for widget in self.todo_frame.winfo_children():
            widget.destroy()

        # Create new todo items
        for i, todo in enumerate(self.filtered_todos):
            self.create_todo_item(todo, i)

        # Update stats
        self.update_stats()

    def on_search(self, *args):
        """Handle search input"""
        search_term = self.search_var.get().lower()
        if search_term:
            self.filtered_todos = [
                todo for todo in self.todos
                if search_term in todo.lower()
            ]
        else:
            self.filtered_todos = self.todos.copy()
        self.refresh_todo_display()

    def toggle_selection(self, index):
        """Toggle todo selection"""
        if index in self.selected_indices:
            self.selected_indices.remove(index)
        else:
            self.selected_indices.add(index)

    def add_todo(self, event=None):
        """Add a new todo with modern styling"""
        todo_text = self.todo_entry.get().strip()
        if not todo_text:
            self.show_modern_message("⚠️ Warning", "Please enter a todo item!", "warning")
            return

        # Check for duplicates
        if any(todo_text.lower() in todo.lower() for todo in self.todos):
            if not messagebox.askyesno("Duplicate Todo",
                                       f"Similar todo exists. Add anyway?"):
                return

        # Add timestamp
        timestamp = datetime.now().strftime("%m/%d %H:%M")
        formatted_todo = f"[{timestamp}] {todo_text}"

        # Update data
        self.todos.append(formatted_todo)
        functions.write_todos(self.todos)

        # Clear input and refresh
        self.todo_entry.delete(0, 'end')
        self.load_todos()

        # Show success animation
        self.show_success_animation("Todo added!")

    def edit_todo(self):
        """Edit selected todo"""
        selected = list(self.selected_indices)
        if not selected:
            self.show_modern_message("⚠️ Warning", "Please select a todo to edit!", "warning")
            return

        if len(selected) > 1:
            self.show_modern_message("⚠️ Warning", "Please select only one todo to edit!", "warning")
            return

        index = selected[0]
        if index >= len(self.filtered_todos):
            return

        current_todo = self.filtered_todos[index]

        # Create edit dialog
        self.create_edit_dialog(current_todo, index)

    def create_edit_dialog(self, current_todo, index):
        """Create modern edit dialog"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("✏️ Edit Todo")
        dialog.geometry("500x200")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (500 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (200 // 2)
        dialog.geometry(f"500x200+{x}+{y}")

        # Extract current text
        if current_todo.startswith('['):
            end_bracket = current_todo.find(']')
            current_text = current_todo[end_bracket + 2:] if end_bracket != -1 else current_todo
        else:
            current_text = current_todo

        # Entry field
        entry = ctk.CTkEntry(
            dialog,
            font=ctk.CTkFont(size=16),
            height=50,
            corner_radius=25
        )
        entry.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=20)
        entry.insert(0, current_text)
        entry.select_range(0, 'end')
        entry.focus()

        # Buttons
        save_btn = ctk.CTkButton(
            dialog,
            text="💾 Save",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            command=lambda: self.save_edit(dialog, entry, index)
        )
        save_btn.grid(row=1, column=0, sticky="ew", padx=(20, 10), pady=20)

        cancel_btn = ctk.CTkButton(
            dialog,
            text="❌ Cancel",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="gray",
            hover_color="darkgray",
            command=dialog.destroy
        )
        cancel_btn.grid(row=1, column=1, sticky="ew", padx=(10, 20), pady=20)

        dialog.grid_columnconfigure(0, weight=1)
        dialog.grid_columnconfigure(1, weight=1)

        # Bind Enter key
        entry.bind("<Return>", lambda e: self.save_edit(dialog, entry, index))

    def save_edit(self, dialog, entry, index):
        """Save edited todo"""
        new_text = entry.get().strip()
        if not new_text:
            return

        # Find original todo in main list
        original_todo = self.filtered_todos[index]
        original_index = self.todos.index(original_todo)

        # Preserve timestamp
        if original_todo.startswith('['):
            end_bracket = original_todo.find(']')
            timestamp = original_todo[:end_bracket + 2]
            self.todos[original_index] = f"{timestamp}{new_text}"
        else:
            timestamp = datetime.now().strftime("%m/%d %H:%M")
            self.todos[original_index] = f"[{timestamp}] {new_text}"

        functions.write_todos(self.todos)
        self.load_todos()
        dialog.destroy()
        self.show_success_animation("Todo updated!")

    def complete_selected(self):
        """Mark selected todos as complete"""
        if not self.selected_indices:
            self.show_modern_message("⚠️ Warning", "Please select todos to complete!", "warning")
            return

        selected_todos = [self.filtered_todos[i] for i in sorted(self.selected_indices, reverse=True)]

        for todo in selected_todos:
            if todo in self.todos:
                self.todos.remove(todo)

        functions.write_todos(self.todos)
        self.selected_indices.clear()
        self.load_todos()
        self.show_success_animation(f"Completed {len(selected_todos)} todo(s)!")

    def delete_selected(self):
        """Delete selected todos"""
        if not self.selected_indices:
            self.show_modern_message("⚠️ Warning", "Please select todos to delete!", "warning")
            return

        if messagebox.askyesno("Confirm Delete",
                               f"Delete {len(self.selected_indices)} selected todo(s)?"):
            self.complete_selected()

    def clear_all(self):
        """Clear all todos"""
        if not self.todos:
            self.show_modern_message("ℹ️ Info", "No todos to clear!", "info")
            return

        if messagebox.askyesno("Confirm Clear All",
                               f"Delete all {len(self.todos)} todos? This cannot be undone!"):
            functions.write_todos([])
            self.todos.clear()
            self.filtered_todos.clear()
            self.selected_indices.clear()
            self.refresh_todo_display()
            self.show_success_animation("All todos cleared!")

    def export_todos(self):
        """Export todos to JSON file"""
        if not self.todos:
            self.show_modern_message("ℹ️ Info", "No todos to export!", "info")
            return

        try:
            filename = f"todos_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump({
                    'todos': self.todos,
                    'exported_at': datetime.now().isoformat(),
                    'total_count': len(self.todos)
                }, f, indent=2)
            self.show_success_animation(f"Exported to {filename}!")
        except Exception as e:
            self.show_modern_message("❌ Error", f"Export failed: {str(e)}", "error")

    def update_stats(self):
        """Update statistics display"""
        total = len(self.todos)
        showing = len(self.filtered_todos)

        if total == showing:
            stats_text = f"📊 {total} todos"
        else:
            stats_text = f"📊 {showing}/{total} todos"

        self.stats_label.configure(text=stats_text)

    def start_clock(self):
        """Start the clock update thread"""

        def update_clock():
            while True:
                current_time = datetime.now().strftime("%H:%M:%S • %B %d, %Y")
                try:
                    self.clock_label.configure(text=f"🕐 {current_time}")
                except:
                    break
                time.sleep(1)

        clock_thread = threading.Thread(target=update_clock, daemon=True)
        clock_thread.start()

    def show_modern_message(self, title, message, msg_type="info"):
        """Show styled message box"""
        if msg_type == "warning":
            messagebox.showwarning(title, message)
        elif msg_type == "error":
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)

    def show_success_animation(self, message):
        """Show success message with animation"""
        # Create temporary success label
        success_label = ctk.CTkLabel(
            self.root,
            text=f"✅ {message}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="lightgreen"
        )
        success_label.place(relx=0.5, rely=0.1, anchor="center")

        # Remove after 2 seconds
        self.root.after(2000, success_label.destroy)

    def run(self):
        """Start the application"""
        # Focus on todo entry
        self.todo_entry.focus()

        # Run main loop
        self.root.mainloop()


# Installation requirements message
def check_requirements():
    """Check if required packages are installed"""
    try:
        import customtkinter
        return True
    except ImportError:
        print("🚨 CustomTkinter not found!")
        print("📦 Install with: pip install customtkinter")
        print("🔗 GitHub: https://github.com/TomSchimansky/CustomTkinter")
        return False


if __name__ == "__main__":
    if check_requirements():
        app = ModernTodoApp()
        app.run()
    else:
        print("\n⚡ Once installed, your todo app will look amazing!")
        print("✨ Modern UI with dark/light themes")
        print("🎨 Smooth animations and rounded corners")
        print("📱 Responsive design that scales beautifully")