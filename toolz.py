import tkinter as tk

from tkinter import filedialog, ttk

from tkinter.font import Font

from PIL import Image, ImageTk

import pillow_heif

from fpdf import FPDF

from pdfminer.high_level import extract_text

from docx import Document

import os

import re



# Enable HEIF format support in Pillow

pillow_heif.register_heif_opener()



# Create the main application window

root = tk.Tk()

root.title("Advanced Converter Tool")

root.geometry("850x700")

root.config(bg="black")



# Load and set background image

bg_image_path = "/home/ahad/test.jpg"  # Updated to the desired path

bg_image = Image.open(bg_image_path)

bg_image = bg_image.resize((850, 700), Image.LANCZOS)

bg_photo = ImageTk.PhotoImage(bg_image)



background_label = tk.Label(root, image=bg_photo)

background_label.place(relwidth=1, relheight=1)



# Set fonts

title_font = Font(family="Helvetica", size=18, weight="bold")

label_font = Font(family="Helvetica", size=12, weight="bold")

button_font = Font(family="Helvetica", size=11)



# Configure styles for buttons and labels

style = ttk.Style()

style.configure("TButton", font=button_font, padding=10, background="#00aaff", foreground="white", relief="raised")

style.configure("Custom.TButton", foreground="black", background="#00aaff", padding=10)

style.configure("TLabel", background="black", foreground="white")

style.configure("TFrame", background="black")



# Create a status label to show messages and paths

status_label = tk.Label(root, text="", font=label_font, bg="black", fg="white")

status_label.pack(pady=(10, 20))



# Function to update status

def update_status(status_message):

    status_label.config(text=status_message)

    root.update_idletasks()



# Function to clean text and remove control characters

def clean_text(text):

    return re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)



# Function to handle image conversion

def convert_image(file_ext):

    file_paths = filedialog.askopenfilenames(filetypes=[("Image files", f"*.{file_ext}")])

    if not file_paths:

        return



    progress["value"] = 0

    root.update_idletasks()



    output_dir = filedialog.askdirectory(title="Select Output Folder")

    if not output_dir:

        return



    for file_path in file_paths:

        img = Image.open(file_path)

        filename = os.path.splitext(os.path.basename(file_path))[0]

        output_path = os.path.join(output_dir, f"{filename}.{file_ext}")



        img.save(output_path)

        progress["value"] += 100 // len(file_paths)

        update_status(f"Converted {file_path} to {output_path}")



    progress["value"] = 100

    update_status(f"Image conversion to {file_ext.upper()} completed! Files saved to: {output_dir}")



# Animated fade-in effect for label widgets

def fade_in(widget, start_color="black", end_color="white", steps=100):

    for i in range(steps + 1):

        widget.update_idletasks()

        widget.after(5)



        # Calculate the intermediate color value

        r = int((1 - i / steps) * 255)

        g = int((1 - i / steps) * 255)

        b = int((1 - i / steps) * 255)

        color = f'#{r:02x}{g:02x}{b:02x}'



        # Check if the widget is a Button or Label

        if isinstance(widget, ttk.Button):

            widget.configure(style="Custom.TButton")  # Update style to a custom one

        else:

            widget.config(fg=color)



# Progress bar animation

def animate_progress_bar():

    progress.start(20)  # Start progress bar animation at 20ms intervals



# Function to convert PDF to DOCX

def convert_pdf_to_docx():

    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])

    if not file_paths:

        return



    progress["value"] = 0

    for file_path in file_paths:

        output_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word files", "*.docx")])

        if not output_path:

            return



        text = extract_text(file_path)

        cleaned_text = clean_text(text)



        doc = Document()

        doc.add_paragraph(cleaned_text)

        doc.save(output_path)



        progress["value"] += 100 // len(file_paths)

        update_status(f"Converted {file_path} to DOCX. Saved to: {output_path}")



    progress["value"] = 100



# Function to convert Text to PDF

def convert_text_to_pdf():

    text = text_box.get("1.0", tk.END).strip()

    if not text:

        update_status("Please enter text to convert")

        return



    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

    if not output_path:

        return



    pdf = FPDF()

    pdf.add_page()

    pdf.set_font('Arial', size=12)

    pdf.multi_cell(200, 10, text)

    pdf.output(output_path)



    update_status(f"Text converted to PDF: {output_path}")



# Function to convert PDF to Text

def convert_pdf_to_text():

    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])

    if not file_paths:

        return



    progress["value"] = 0

    for file_path in file_paths:

        text = extract_text(file_path)

        text_box.delete("1.0", tk.END)

        text_box.insert(tk.END, text)

        progress["value"] += 100 // len(file_paths)

        update_status(f"Converted {file_path} to text. Displayed in text box.")



    progress["value"] = 100



# Function to convert DOCX to PDF

def convert_doc_to_pdf():

    file_paths = filedialog.askopenfilenames(filetypes=[("Word files", "*.docx")])

    if not file_paths:

        return



    progress["value"] = 0

    for file_path in file_paths:

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if not output_path:

            return



        doc = Document(file_path)

        pdf = FPDF()

        pdf.add_page()

        pdf.set_font('Arial', size=12)



        for paragraph in doc.paragraphs:

            pdf.multi_cell(200, 10, paragraph.text)



        pdf.output(output_path)

        progress["value"] += 100 // len(file_paths)

        update_status(f"Converted {file_path} to PDF. Saved to: {output_path}")



    progress["value"] = 100



# Function to convert DOCX to Text

def convert_docx_to_text():

    file_paths = filedialog.askopenfilenames(filetypes=[("Word files", "*.docx")])

    if not file_paths:

        return



    progress["value"] = 0

    for file_path in file_paths:

        doc = Document(file_path)

        full_text = '\n'.join([para.text for para in doc.paragraphs])

        text_box.delete("1.0", tk.END)

        text_box.insert(tk.END, full_text)



        progress["value"] += 100 // len(file_paths)

        update_status(f"Converted {file_path} to text. Displayed in text box.")



    progress["value"] = 100



# Function to create section titles

def create_section_title(title):

    title_label = tk.Label(root, text=title, font=title_font, bg="black", fg="white")

    title_label.pack(pady=(20, 10))

    fade_in(title_label)



# Function to create button sections

def create_button_section(buttons):

    button_frame = ttk.Frame(root)

    button_frame.pack(pady=10)

    for (text, command) in buttons:

        btn = ttk.Button(button_frame, text=text, command=command)

        btn.pack(pady=5)

        fade_in(btn)



# Progress bar for visual feedback

progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")

progress.pack(pady=20)



# Create UI elements

create_section_title("Image Converters")

create_button_section([

    ("Convert PNG to JPG", lambda: convert_image("jpg")),

    ("Convert JPG to PNG", lambda: convert_image("png")),

    ("Convert HEIC to JPG", lambda: convert_image("jpg")),

])



create_section_title("Document Converters")

create_button_section([

    ("Convert PDF to DOCX", convert_pdf_to_docx),

    ("Convert Text to PDF", convert_text_to_pdf),

    ("Convert PDF to Text", convert_pdf_to_text),

    ("Convert DOCX to PDF", convert_doc_to_pdf),

    ("Convert DOCX to Text", convert_docx_to_text),

])



# Textbox for entering or displaying text

text_box_frame = ttk.Frame(root)

text_box_frame.pack(pady=20, fill="x")



text_box = tk.Text(text_box_frame, height=10, font=("Helvetica", 12), wrap="word", bg="#f4f4f4", fg="black", relief="solid")

text_box.pack(fill="x", padx=10, pady=10)



# Animate the progress bar

animate_progress_bar()



# Start the main event loop

root.mainloop()

