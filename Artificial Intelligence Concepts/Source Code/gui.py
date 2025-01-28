import tkinter as tk
from tkinter import ttk
import webbrowser
from owlready2 import get_ontology

class IntelligentTutoringSystem:
    def __init__(self, root, ontology_path):
        self.root = root
        self.root.title("Intelligent Tutoring System For Mathematics (Area Calculation of Geometrics Shapes)")
        self.root.geometry("800x600")

        # Load ontology
        self.ontology = get_ontology(ontology_path).load()

        # Create a tab control
        self.tab_control = ttk.Notebook(root)

        # Create tabs
        self.learning_tab = ttk.Frame(self.tab_control)
        self.assessment_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.learning_tab, text='Learning')
        self.tab_control.add(self.assessment_tab, text='Assessment')

        self.tab_control.pack(expand=1, fill='both')

        self.create_learning_tab()
        self.create_assessment_tab()

        # Initialize assessment variables
        self.current_level = 1
        self.questions = self.load_questions_from_ontology()

    def create_learning_tab(self):
        # Shape selection
        self.shape_var = tk.StringVar()
        self.shape_label = tk.Label(self.learning_tab, text="Select a shape:", font=("Arial", 12))
        self.shape_label.pack(pady=10)

        self.shape_options = ['Circle', 'Rectangle', 'Square', 'Triangle', 'Cube', 'Cuboid']
        self.shape_menu = ttk.Combobox(self.learning_tab, textvariable=self.shape_var, values=self.shape_options, font=("Arial", 12))
        self.shape_menu.pack(pady=10)

        self.get_formula_button = tk.Button(self.learning_tab, text="Get Formula", command=self.show_formula, font=("Arial", 12))
        self.get_formula_button.pack(pady=10)

        self.formula_label = tk.Label(self.learning_tab, text="", font=("Arial", 12))
        self.formula_label.pack(pady=10)

        self.youtube_link_label = tk.Label(self.learning_tab, text="", fg="blue", cursor="hand2", font=("Arial", 12))
        self.youtube_link_label.pack(pady=10)
        self.youtube_link_label.bind("<Button-1>", self.open_youtube)

        self.input_frame = tk.Frame(self.learning_tab)
        self.input_frame.pack(pady=10)

        self.calculate_button = tk.Button(self.learning_tab, text="Calculate Area", command=self.calculate_area, font=("Arial", 12))
        self.calculate_button.pack(pady=10)

        self.result_label = tk.Label(self.learning_tab, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

    def create_assessment_tab(self):
        # Assessment section title
        self.assessment_label = ttk.Label(
            self.assessment_tab,
            text="Quiz Questions",
            font=("Arial", 14, "bold"),
            justify="center",
        )
        self.assessment_label.pack(pady=20)

        # Question label
        self.question_label = ttk.Label(
            self.assessment_tab,
            text="",
            wraplength=500,
            justify="center",
            font=("Arial", 12),
        )
        self.question_label.pack(pady=15)

        # Answer entry field
        self.answer_entry_label = ttk.Label(
            self.assessment_tab,
            text="Enter your answer:",
            font=("Arial", 12),
        )
        self.answer_entry_label.pack(pady=5)

        self.answer_entry = ttk.Entry(self.assessment_tab, font=("Arial", 12))
        self.answer_entry.pack(pady=10)

        # Submit button
        self.submit_button = ttk.Button(
            self.assessment_tab, text="Submit Answer", command=self.check_answer
        )
        self.submit_button.pack(pady=15)

        # Feedback label
        self.feedback_label = ttk.Label(
            self.assessment_tab,
            text="",
            wraplength=500,
            justify="center",
            font=("Arial", 12),
            foreground="green",
        )
        self.feedback_label.pack(pady=15)

        # Initialize first question
        self.load_question()

    def load_questions_from_ontology(self):
        self.current_level = 1
        self.questions = [
            {"question": "What is the area of a rectangle with length 40 cm and breadth 20 cm?", "answer": 800},
            {"question": "What is the area of a triangle with base 10 cm and height 5 cm?", "answer": 25},
            {"question": "What is the area of a circle with radius 7 cm? (Use π = 3.14)", "answer": 153.86},
            {"question": "What is the area of a square with side 6 cm?", "answer": 36},
            {"question": "What is the surface area of a cube with side 4 cm?", "answer": 96}
        ]
        return self.questions

    def load_question(self):
        self.current_level = 1
        self.questions = [
            {"question": "What is the area of a rectangle with length 40 cm and breadth 20 cm?", "answer": 800},
            {"question": "What is the area of a triangle with base 10 cm and height 5 cm?", "answer": 25},
            {"question": "What is the area of a circle with radius 7 cm? (Use π = 3.14)", "answer": 153.86},
            {"question": "What is the area of a square with side 6 cm?", "answer": 36},
            {"question": "What is the surface area of a cube with side 4 cm?", "answer": 96}
        ]
        if self.current_level <= len(self.questions):
            question = self.questions[self.current_level - 1]
            self.question_label.config(text=f"Question {self.current_level}: {question['question']}")
            self.answer_entry.delete(0, tk.END)
            self.feedback_label.config(text="")
        else:
            self.question_label.config(text="\U0001F389 Congratulations! You've completed all the questions.")
            self.answer_entry.config(state="disabled")
            self.submit_button.config(state="disabled")
            self.feedback_label.config(
                text="Great job! You’ve successfully completed the assessment.",
                foreground="blue",
            )

    def check_answer(self):
        try:
            if self.current_level <= len(self.questions):
                user_answer = float(self.answer_entry.get())
                correct_answer = self.questions[self.current_level - 1]["answer"]

                if abs(user_answer - correct_answer) < 0.01:
                    self.feedback_label.config(
                        text="\u2705 Congratulations, correct answer!",
                        foreground="green",
                    )
                    self.current_level += 1
                    self.root.after(2000, self.load_question)
                else:
                    self.feedback_label.config(
                        text=f"\u274C Wrong answer. The correct answer is {correct_answer}.",
                        foreground="red",
                    )
                    self.provide_correction()
            else:
                self.feedback_label.config(
                    text="\U0001F389 Great job! You've completed the assessment.",
                    foreground="blue",
                )
                self.question_label.config(text="")
                self.answer_entry.config(state="disabled")
                self.submit_button.config(state="disabled")
        except ValueError:
            self.feedback_label.config(
                text="\u26A0\uFE0F Please enter a valid numerical answer.",
                foreground="orange",
            )
            
    def provide_correction(self):
        if self.current_level <= len(self.questions):
            correct_answer = self.questions[self.current_level - 1]["answer"]
            if self.current_level == 1:
                self.feedback_label.config(
                    text=f"❌ Wrong answer. Area = length * breadth = 40 cm * 20 cm = {correct_answer} cm²",
                )
            elif self.current_level == 2:
                self.feedback_label.config(
                    text=f"❌ Wrong answer. Area = 0.5 * base * height = 0.5 * 10 cm * 5 cm = {correct_answer} cm²",
                )
            elif self.current_level == 3:
                self.feedback_label.config(
                    text=f"❌ Wrong answer. Area = π * r² = 3.14 * (7 cm)² = {correct_answer} cm²",
                )
            elif self.current_level == 4:
                self.feedback_label.config(
                    text=f"❌ Wrong answer. Area = side² = (6 cm)² = {correct_answer} cm²",
                )
            elif self.current_level == 5:
                self.feedback_label.config(
                    text=f"❌ Wrong answer. Surface Area = 6 * side² = 6 * (4 cm)² = {correct_answer} cm²",
                )

    def show_formula(self):
        shape = self.shape_var.get()
        self.clear_input_fields()

        if shape == 'Circle':
            self.formula_label.config(text="Area = π * r²")
            self.youtube_link_label.config(text="YouTube Link: Area of Circle")
            self.youtube_link = "https://www.youtube.com/results?search_query=area+of+circle"
            self.create_input_fields(["Enter radius of circle"])
        elif shape == 'Rectangle':
            self.formula_label.config(text="Area = length * breadth")
            self.youtube_link_label.config(text="YouTube Link: Area of Rectangle")
            self.youtube_link = "https://www.youtube.com/results?search_query=area+of+rectangle"
            self.create_input_fields(["Enter length of rectangle", "Enter breadth of rectangle"])
        elif shape == 'Square':
            self.formula_label.config(text="Area = side²")
            self.youtube_link_label.config(text="YouTube Link: Area of Square")
            self.youtube_link = "https://www.youtube.com/results?search_query=area+of+square"
            self.create_input_fields(["Enter side of square"])
        elif shape == 'Triangle':
            self.formula_label.config(text="Area = 0.5 * base * height")
            self.youtube_link_label.config(text="YouTube Link: Area of Triangle")
            self.youtube_link = "https://www.youtube.com/results?search_query=area+of+triangle"
            self.create_input_fields(["Enter base of triangle", "Enter height of triangle"])
        elif shape == 'Cube':
            self.formula_label.config(text="Surface Area = 6 * side²")
            self.youtube_link_label.config(text="YouTube Link: Surface Area of Cube")
            self.youtube_link = "https://www.youtube.com/results?search_query=surface+area+of+cube"
            self.create_input_fields(["Enter side of cube"])
        elif shape == 'Cuboid':
            self.formula_label.config(text="Surface Area = 2 * (length * breadth + breadth * height + height * length)")
            self.youtube_link_label.config(text="YouTube Link: Surface Area of Cuboid")
            self.youtube_link = "https://www.youtube.com/results?search_query=surface+area+of+cuboid"
            self.create_input_fields(["Enter length of cuboid", "Enter breadth of cuboid", "Enter height of cuboid"])

    def create_input_fields(self, labels):
        self.input_frame.entries = []
        for label in labels:
            input_label = ttk.Label(self.input_frame, text=label, font=("Arial", 12))
            input_label.pack(pady=5)
            entry = ttk.Entry(self.input_frame, font=("Arial", 12))
            entry.pack(pady=5)
            self.input_frame.entries.append(entry)

    def clear_input_fields(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

    def calculate_area(self):
        shape = self.shape_var.get()
        inputs = [entry.get() for entry in self.input_frame.entries if entry.get()]
        try:
            if shape == 'Circle':
                r = float(inputs[0])
                area = 3.14 * r ** 2
                self.result_label.config(text=f"Area of Circle: {area:.2f} cm²")
            elif shape == 'Rectangle':
                length = float(inputs[0])
                breadth = float(inputs[1])
                area = length * breadth
                self.result_label.config(text=f"Area of Rectangle: {area:.2f} cm²")
            elif shape == 'Square':
                side = float(inputs[0])
                area = side ** 2
                self.result_label.config(text=f"Area of Square: {area:.2f} cm²")
            elif shape == 'Triangle':
                base = float(inputs[0])
                height = float(inputs[1])
                area = 0.5 * base * height
                self.result_label.config(text=f"Area of Triangle: {area:.2f} cm²")
            elif shape == 'Cube':
                side = float(inputs[0])
                surface_area = 6 * side ** 2
                self.result_label.config(text=f"Surface Area of Cube: {surface_area:.2f} cm²")
            elif shape == 'Cuboid':
                length = float(inputs[0])
                breadth = float(inputs[1])
                height = float(inputs[2])
                surface_area = 2 * (length * breadth + breadth * height + height * length)
                self.result_label.config(text=f"Surface Area of Cuboid: {surface_area:.2f} cm²")
        except ValueError:
            self.result_label.config(text="\u26A0\uFE0F Please enter valid numerical values.")

    def open_youtube(self, event):
        webbrowser.open(self.youtube_link)

# Create the main window
root = tk.Tk()

# Initialize the Intelligent Tutoring System with ontology path
ontology_path = "D:\MSc Classes\SEM-2\AI\intelligent_tutoring_system.owl"
intelligent_tutoring_system = IntelligentTutoringSystem(root, ontology_path)

# Run the application
root.mainloop()
