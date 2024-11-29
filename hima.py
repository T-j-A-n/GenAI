from transformers import pipeline
import re
import random
import gradio as gr

generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")
question = ""

# Function to check if the numbers are the same
def check_numbers(num1):
    if num1 == correct_answer:
        return "yay"
    else:
        return "sorry"

# Create the Gradio interface


def generate_shop_question_with_ai():
    # Define a prompt to guide the model
    n = random.randint(1, 10)
    things = ["apple", "oranges", "notebooks", "pens", "pencils"]
    prompt = (
        "Create a shop-themed math word problem in Indian rupees. Include the cost of items, "
        "the total payment given, and ask for the change. Example:\n"
        "I bought " + str(n) + " " + things[n%len(things)] + " for " + str(random.randint(10, 100)) + "  rupees each. If I give you 1000 rupees, how much change should I get?"
    )

    # Generate the word problem
    generated_text = generator(prompt, max_length=100, num_return_sequences=1)[0]["generated_text"]

    # Extract the word problem and solution
    # Use regex to capture the problem and attempt parsing numbers (for validation)
    question_match = re.search(r"I bought.*?\?", generated_text)
    question = question_match.group(0) if question_match else "Could not generate a valid question."

    # Extract numbers for cost, quantity, and payment (optional fallback logic for auto-correcting issues)
    try:
        quantity, cost_per_item, payment = map(int, re.findall(r"\d+", question)[0:3])
        total_cost = quantity * cost_per_item
        correct_change = payment - total_cost
    except (ValueError, IndexError):
        correct_change = None  # Fallback for manual review

    return question, correct_change

interface = gr.Interface(
    fn=check_numbers,  # Function to run
    inputs=[gr.Number(label="First Number")],  # Inputs
    outputs="text",  # Output type
    title=question,
)


while True:
    # Generate a question
    question, correct_answer = generate_shop_question_with_ai()

    # Display the question
    print(question)


    # Handle cases where question generation failed
    if correct_answer is None:
        continue
    else:
        break
print(question)

# Launch the interface
interface.launch()