import tkinter as tk
from tkinter import ttk, messagebox
import csv

class TestGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test Taking Application")
        self.geometry("625x100")  # Initial window size
        self.current_test = None
        self.questions = []

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.test_label = ttk.Label(self.main_frame, text="Select Test:")
        self.test_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.test_var = tk.StringVar()
        self.test_dropdown = ttk.Combobox(self.main_frame, textvariable=self.test_var, state="readonly")
        self.test_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        self.take_test_button = ttk.Button(self.main_frame, text="Take Test", command=self.start_test)
        self.take_test_button.grid(row=0, column=2, padx=10, pady=10)

        self.exit_button_main = ttk.Button(self.main_frame, text="Exit", command=self.quit)
        self.exit_button_main.grid(row=0, column=3, padx=10, pady=10, sticky=tk.E)

        self.load_tests()

    def load_tests(self):
        with open('Documents\QuestionTester\questions.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            tests = {}
            for row in reader:
                test_name, question, *answers, correct_answer = row
                # Remove blank answers before adding to the list
                answers = [answer for answer in answers if answer.strip()]
                if test_name not in tests:
                    tests[test_name] = []
                tests[test_name].append({'question': question, 'answers': answers, 'correct_answer': correct_answer})
        
        self.tests = tests
        self.test_dropdown['values'] = list(self.tests.keys())
        self.test_dropdown.config(width=max(len(test) for test in self.tests.keys()) + 5)

    def start_test(self):
        test_name = self.test_var.get()
        if test_name:
            self.current_test = TestWindow(self, self.tests[test_name])
            self.current_test.geometry("725x400")
            self.current_test.mainloop()

class TestWindow(tk.Toplevel):
    def __init__(self, parent, questions):
        super().__init__(parent)
        self.title("Test Window")
        self.parent = parent
        self.questions = questions
        self.current_question_index = 0

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.question_label = ttk.Label(self.main_frame, text="", anchor=tk.W, wraplength=700)
        self.question_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.answer_var = tk.StringVar()
        self.answer_buttons = []

        self.submit_button = ttk.Button(self.main_frame, text="Submit", command=self.submit_answer, state=tk.DISABLED)
        self.submit_button.grid(row=5, column=0, pady=10, padx=10, sticky=tk.W)

        self.next_button = ttk.Button(self.main_frame, text="Next Question", command=self.next_question)
        self.next_button.grid(row=6, column=0, pady=10, padx=10, sticky=tk.W)
        self.next_button.grid_remove()  # Hide Next Question button initially

        self.feedback_label = ttk.Label(self.main_frame, text="", anchor=tk.W)
        self.feedback_label.grid(row=7, column=0, padx=10, pady=10, sticky=tk.W)

        self.display_question()

    def display_question(self):
        question_data = self.questions[self.current_question_index]
        self.question_label.config(text=question_data['question'])

        answers = question_data['answers']
        num_answers = len(answers)
        
        # Clear existing radio buttons
        for button in self.answer_buttons:
            button.grid_forget()
            button.destroy()
        
        self.answer_buttons.clear()

        # Create and configure radio buttons based on the number of answers
        for i in range(num_answers):
            button = ttk.Radiobutton(self.main_frame, text=answers[i], variable=self.answer_var, value=str(i), command=self.activate_submit)
            self.answer_buttons.append(button)
            button.grid(row=i+1, column=0, padx=10, pady=5, sticky=tk.W)

        self.feedback_label.config(text="")  # Reset feedback label
        self.answer_var.set("")  # Clear selection

    def activate_submit(self):
        self.submit_button.config(state=tk.NORMAL)

    def submit_answer(self):
        selected_answer_index = self.answer_var.get()
        if selected_answer_index == "":
            messagebox.showerror("Error", "Please select an answer.")
            return
        
        selected_answer = chr(65 + int(selected_answer_index))  # Convert index to letter (A, B, C, D)
        correct_answer = self.questions[self.current_question_index]['correct_answer']
        if selected_answer == correct_answer:
            self.feedback_label.config(text="Correct!", foreground="green")
        else:
            self.feedback_label.config(text=f"Incorrect! The correct answer is: {correct_answer}", foreground="red")

        self.submit_button.grid_remove()  # Hide Submit button
        self.next_button.grid()  # Show Next Question button

    def next_question(self):
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.display_question()
            self.submit_button.grid()  # Show Submit button for the next question
            self.next_button.grid_remove()  # Hide Next Question button
        else:
            messagebox.showinfo("End of Test", "You have completed the test.")
            self.destroy()

if __name__ == "__main__":
    app = TestGUI()
    app.mainloop()
