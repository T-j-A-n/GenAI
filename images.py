import cv2
import numpy as np
import random
from PIL import ImageFont, ImageDraw, Image

# Step 1: List of 50 phrases
phrases = [
    "Hello World!", "Python is awesome", "Learning AI", "OpenCV is cool", "Happy coding",
    "Keep going!", "Good vibes only", "AI for everyone", "Embrace the future", "Start today",
    "You got this!", "Code your dreams", "Machine learning rocks", "Never stop learning", "Stay curious",
    "Believe in yourself", "Innovation is key", "Think outside the box", "Make it happen", "Coding is fun",
    "Challenges make you stronger", "Think big, act bigger", "Explore the unknown", "Keep pushing forward",
    "Make mistakes, learn from them", "Knowledge is power", "Create your future", "Dare to dream", "Live life",
    "Happiness is a choice", "Create and innovate", "The sky is the limit", "Dream big", "Success comes from within",
    "Positive thoughts only", "Change the world", "Make a difference", "Love what you do", "Be unstoppable",
    "Future belongs to the curious", "Strive for excellence", "Do what you love", "Be the change",
    "Life is beautiful", "Coding is my superpower", "Innovation leads to progress", "Grow through what you go through",
    "Life is an adventure", "Believe in progress", "Empower yourself", "Your time is now", "The best is yet to come"
]

# Step 2: Randomly select a phrase
key = random.choice(phrases)

# Step 3: Create image with selected text phrase
def create_image_with_text(text):
    # Image size
    width, height = 600, 200
    # Create a blank white image
    img = np.ones((height, width, 3), dtype=np.uint8) * 255

    # Use a default font (e.g., DejaVuSans)
    font = ImageFont.load_default()

    # Create image using PIL
    pil_img = Image.fromarray(img)
    draw = ImageDraw.Draw(pil_img)
    
    # Calculate text size and position
    text_width, text_height = draw.textsize(text, font)
    position = ((width - text_width) // 2, (height - text_height) // 2)

    # Draw text on image
    draw.text(position, text, font=font, fill=(0, 0, 0))  # Black text
    
    # Convert back to OpenCV format
    img = np.array(pil_img)
    
    return img

# Create the original image
original_image = create_image_with_text(key)

# Step 4: Apply increasing blur to the image
def apply_blur(image, ksize):
    return cv2.GaussianBlur(image, (ksize, ksize), 0)

blurred_images = []
for i in range(1, 4):
    ksize = 2 * i + 1  # Increasing blur kernel size
    blurred_images.append(apply_blur(original_image, ksize))

# Step 5: Show blurred images and get user input
score = 0

for i, blurred_image in enumerate(blurred_images):
    cv2.imshow(f"Blurred Image {i+1}", blurred_image)
    
    # Ask for text input
    user_input = input(f"Enter the text for the blurred image {i+1}: ")
    
    if user_input.strip() == key:
        score += 1  # Increment score if match

# Step 6: Display the final score
print(f"Your final score is: {score}")

# Wait for user to press a key and close the windows
cv2.waitKey(0)
cv2.destroyAllWindows()
