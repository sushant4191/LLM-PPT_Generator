import ollama
import time
import threading
import sys
# from PPT_maker_plainGenerator import create_ppt_from_text #This is the function for plain ppt generation
from enhanced_pptMaker import create_ppt_from_text #This is the function for enhanced ppt generation


# Function to display a loading animation
def show_loader(step):
    global stop_spinner
    stop_spinner = False

    def spinning_cursor():
        while not stop_spinner:
            for cursor in "|/-\\":
                sys.stdout.write(f"\r🔄 {step}... {cursor}")
                sys.stdout.flush()
                time.sleep(0.1)
        sys.stdout.write(f"\r✅ {step} completed!        \n")

    spinner_thread = threading.Thread(target=spinning_cursor)
    spinner_thread.start()
    return spinner_thread

# Function to read text from a file
def read_text_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Function to write text to a file
def write_text_to_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

# Summarize text using Ollama
def summarize_text(text, model="mistral"):
    spinner_thread = show_loader("Generating Summarization")
    
    response = ollama.chat(model=model, messages=[{"role": "user", "content": f"Summarize this: {text}"}])
    
    global stop_spinner
    stop_spinner = True
    spinner_thread.join()

    return response["message"]["content"]

# Generate slide content
# def generate_slide_content(text, model="mistral"):
#     spinner_thread = show_loader("Generating Slide Content")
    
#     prompt = f"""
#     Convert this content into a structured PowerPoint slide format:

#     Content: {text}

#     Output format:
#     Slide Title: [Title]
#     Bullet Points:
#     - [Point 1]
#     - [Point 2]
#     - [Point 3]
#     """

#     response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    
#     global stop_spinner
#     stop_spinner = True
#     spinner_thread.join()

#     return response["message"]["content"]



def generate_slide_content(text, model="mistral"):
    spinner_thread = show_loader("Generating Slide Content")
    
    prompt = f"""
    You are an expert in creating PowerPoint slide content. Convert the given text into structured slide content.

    ### Instructions:
    - Extract the key topics as **slide titles**.
    - Provide **3 to 5 bullet points** for each slide.
    - Keep each bullet point **short and concise** (max 20 words).
    - Format response **exactly** as follows:

    Slide Title: [Title]
    Bullet Points:
    - [Point 1]
    - [Point 2]
    - [Point 3]
    - [Point 4] (if needed)
    - [Point 5] (if needed)

    ### Content:
    {text}

    **Important:** Only return the formatted slides, without additional explanations.
    """

    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    
    global stop_spinner
    stop_spinner = True
    spinner_thread.join()

    return response["message"]["content"]

# Step 1: Read content from input file
input_file = "input.txt"
text = read_text_from_file(input_file)

# Step 2: Summarize the text
summary = summarize_text(text)

# Step 3: Generate slide content
slide_content = generate_slide_content(summary)

# Step 4: Save slide content to a file
slides_file = "slides.txt"
write_text_to_file(slides_file, slide_content)

# Step 5: Generate PPT from slides file
spinner_thread = show_loader("Creating PowerPoint")
output_ppt = "output.pptx"
create_ppt_from_text(slides_file, output_ppt)

global stop_spinner
stop_spinner = True
spinner_thread.join()

print("\n🎉 PowerPoint file created: output.pptx ✅")
