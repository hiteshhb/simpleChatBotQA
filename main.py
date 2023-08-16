# First Install the req. libraries
# pip install Flask PyPDF2 nltk


from flask import Flask, render_template, request
import PyPDF2 
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

# downloading the latest stopwords & punkt
nltk.download('punkt')
nltk.download('stopwords')


# Function to extract text from the PDF
def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to process the question (logic for chat bot)
def process_question(text, question):
    # Tokenize the question and remove stopwords
    question_tokens = nltk.word_tokenize(question.lower())
    question_tokens = [token for token in question_tokens if token not in stopwords.words('english')]

    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Find the sentences that contain the keywords from the question
    relevant_sentences = []
    for sentence in sentences:
        sentence_tokens = nltk.word_tokenize(sentence.lower())
        if any(token in sentence_tokens for token in question_tokens):
            relevant_sentences.append(sentence)

    # Return the first relevant sentence as the answer
    if relevant_sentences:
        return relevant_sentences[0]
    else:
        return "Sorry, I couldn't find an answer to your question."
    

# Creating flask instance here
app = Flask(__name__)

# Home page API
@app.route('/')
def home():
    return render_template('index.html')

# Chatbot page API
@app.route('/chat', methods=['POST'])
def chat():
    # Get the uploaded file
    pdf_file = request.files['pdf_file']

    # # Save the uploaded file
    # pdf_path = 'temp.pdf'
    # pdf_file.save(pdf_path)

    # Extract text from the PDF
    text = extract_text(pdf_file)

    # Process the user's question
    question = request.form['question']
    answer = process_question(text, question)  # Replace this with your chatbot's logic

    # Render the answer in the template
    return render_template('chat.html', question=question, answer=answer)



# Run the Flask application
if __name__ == "__main__":
    app.run(debug = False)  # By default Prameters