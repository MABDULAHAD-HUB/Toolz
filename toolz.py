import os
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from pdfminer.high_level import extract_text
from docx import Document
from fpdf import FPDF

# Define a class for PDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Document Title", ln=True, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def sanitize_text(text):
    """Sanitize text to remove or replace unsupported characters."""
    return ''.join(c if ord(c) < 256 else ' ' for c in text)  # Replace with a space

def convert_doc_to_pdf(input_path, output_path):
    """Convert a .docx file to PDF."""
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    doc = Document(input_path)
    for paragraph in doc.paragraphs:
        pdf.multi_cell(0, 10, sanitize_text(paragraph.text))

    pdf.output(output_path)

def convert_pdf_to_text(input_path):
    """Convert a PDF file to text."""
    return extract_text(input_path)

def select_input_file():
    """Open a file dialog to select the input file."""
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if file_path:
        input_file_var.set(file_path)

def select_output_file():
    """Open a file dialog to select the output file."""
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        output_file_var.set(file_path)

def on_convert():
    """Handle the conversion process."""
    input_file = input_file_var.get()
    output_file = output_file_var.get()
    
    if not input_file or not output_file:
        messagebox.showerror("Error", "Please select input and output files.")
        return
    
    try:
        if input_file.endswith(".docx"):
            convert_doc_to_pdf(input_file, output_file)
            messagebox.showinfo("Success", "Document converted to PDF successfully.")
        elif input_file.endswith(".pdf"):
            text = convert_pdf_to_text(input_file)
            with open(output_file.replace(".pdf", ".txt"), "w") as text_file:
                text_file.write(text)
            messagebox.showinfo("Success", "PDF converted to text successfully.")
        else:
            messagebox.showerror("Error", "Unsupported file type. Please select a .docx or .pdf file.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def on_enter(event):
    """Change button color on hover."""
    event.widget['background'] = 'lightblue'

def on_leave(event):
    """Reset button color on leave."""
    event.widget['background'] = 'SystemButtonFace'

# Initialize the main window
root = Tk()
root.title("Toolz - Document Converter")
root.geometry("400x500")

# Initialize the bg_image variable
bg_image = None

# Load and set a background image
try:
    image_path = r"D:\toolz\toolz\test.png"  # Ensure this path is correct
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The image file does not exist at {image_path}")
    
    background_image = Image.open(image_path)
    background_image = background_image.resize((400, 500), Image.LANCZOS)  # Adjust height to fit the window
    bg_image = ImageTk.PhotoImage(background_image)
except FileNotFoundError as e:
    messagebox.showerror("Error", str(e))
    root.quit()  # Exit if the image cannot be loaded
except OSError as e:
    messagebox.showerror("Error", f"Failed to load image: {e}")
    root.quit()  # Exit if the image cannot be loaded

# Create the background label only if the image is loaded successfully
if bg_image is not None:
    bg_label = Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)

# Variables to hold file paths
input_file_var = StringVar()
output_file_var = StringVar()

# UI Elements
Label(root, text="Input File:", bg='white').pack(pady=5)
input_entry = Entry(root, textvariable=input_file_var, width=50, bg='lightyellow')
input_entry.pack(pady=5)
Button(root, text="Browse", command=select_input_file).pack(pady=5)

Label(root, text="Output File:", bg='white').pack(pady=5)
output_entry = Entry(root, textvariable=output_file_var, width=50, bg='lightyellow')
output_entry.pack(pady=5)
Button(root, text="Browse", command=select_output_file).pack(pady=5)

# Text box for writing text
Label(root, text="Write Text:", bg='white').pack(pady=5)
text_box = Text(root, width=48, height=10, bg='lightyellow')
text_box.pack(pady=5)

convert_button = Button(root, text="Convert", command=on_convert)
convert_button.pack(pady=20)
convert_button.bind("<Enter>", on_enter)
convert_button.bind("<Leave>", on_leave)

# Run the application
root.mainloop()


