from flask import Flask, render_template, request, redirect, url_for
import openai  # Or another model API for generating questions

app = Flask(__name__)
app.secret_key = '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'  # For flash messages (if you use them)

# Initialize OpenAI API Key (use your own API key here)
openai.api_key = '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'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        disability = request.form['disability']
        languages = request.form['languages']
        vocational_skills = request.form['vocational_skills']

        # Generate questions based on the input
        questions = generate_questions(disability, languages, vocational_skills)

        # Redirect to the results page with the generated questions
        return redirect(url_for('results', questions=questions))

    return render_template('form.html')


@app.route('/results')
def results():
    # Retrieve the generated questions passed from the previous route
    questions = request.args.getlist('questions')

    return render_template('result.html', questions=questions)


def generate_questions(disability, languages, vocational_skills):
    # Example of generating questions using OpenAI API
    prompt = f"Generate relevant questions based on the following input:\nDisability: {disability}\nLanguages Known: {languages}\nVocational Skills: {vocational_skills}"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )

    questions = response.choices[0].text.strip().split('\n')
    return questions


if __name__ == '__main__':
    app.run(debug=True)
