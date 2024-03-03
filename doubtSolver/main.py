from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
from PyPDF2 import PdfReader
import os



def question_ans_ai(question):
    model_name = "deepset/roberta-base-squad2"
    nlp = pipeline("question-answering", model=model_name, tokenizer=model_name)

    # Specify the PDF file path
    pdf_directory = "pdf"
    pdf_filename = "context.pdf"
    pdf_file_path = os.path.join(pdf_directory, pdf_filename)
    print(pdf_file_path)
    question = question

    # Read the context from the PDF file
    pdf_text = ""
    with open(pdf_file_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            pdf_text += page.extract_text()

    # Create QA input
    QA_input = {
        'question': question,
        'context': pdf_text
    }

    # Get answer
    res = nlp(QA_input)

    print("Using pipeline:")
    print(f"Answer: {res['answer']}")
    print(f"Score: {res['score']}")
    print("----------")
    return [res['answer'],question]

question = input("enter you question = ")
# question = "Why did Mozart include alternate endings for Don Giovanni but not for his other famous operas like Die Zauberflöte and Le Nozze di Figaro?"
print(question_ans_ai(question))