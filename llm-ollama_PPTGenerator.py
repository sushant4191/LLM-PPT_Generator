import ollama # type: ignore
import time
import threading
import sys

# Spinner for loading animation
def spinning_cursor():
    """Displays a spinning cursor while processing."""
    while not stop_spinner:
        for cursor in "|/-\\":
            sys.stdout.write(f"\r🔄 Processing... {cursor}")
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write("\r✅ Processing complete!      \n")

# Function to read text from a file
def read_text_from_file(file_path):
    """Reads text from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Function to summarize text using Ollama
def summarize_text(text, model="mistral"):
    """Generates a summary using Ollama with a spinner."""
    global stop_spinner
    stop_spinner = False
    spinner_thread = threading.Thread(target=spinning_cursor)
    spinner_thread.start()

    response = ollama.chat(model=model, messages=[{"role": "user", "content": f"Summarize this: {text}"}])

    stop_spinner = True
    spinner_thread.join()

    return response["message"]["content"]

# Function to generate slide content
def generate_slide_content(text, model="mistral"):
    """Formats summarized text into a structured PowerPoint slide layout."""
    prompt = f"""
    Convert this content into a structured PowerPoint slide format:

    Content: {text}

    Output format:
    Slide Title: [Title]
    Bullet Points:
    - [Point 1]
    - [Point 2]
    - [Point 3]
    """

    global stop_spinner
    stop_spinner = False
    spinner_thread = threading.Thread(target=spinning_cursor)
    spinner_thread.start()

    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])

    stop_spinner = True
    spinner_thread.join()

    return response["message"]["content"]

# File path (Change this to your actual file path)
file_path = "summarize.txt"

# Read the text from the file
text = read_text_from_file(file_path)

# Summarize the text
summary = summarize_text(text)

# Print the summary
print("\n🔹 Summary:\n", summary)

# Generate slide content
slide_content = generate_slide_content(summary)

# Print the slide content
print("\n📊 Slide Content:\n", slide_content)
