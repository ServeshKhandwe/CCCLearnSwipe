import streamlit as st
import PyPDF2
import io
import openai

# Initialize the OpenAI client
openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_summary(text, max_length=50):
    try:
        chat_completion = openai.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize the following text into concise bullet points:\n\n{text}",
                }
            ],
            model="gpt-3.5-turbo",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
    text = ''
    for page in reader.pages:
        text += page.extract_text() + '\n'
    return text

def main():
    st.title("Gamified Learning Experience")

    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        facts = generate_summary(text)

        for index, fact in enumerate(facts.split('\n')):
            st.write(fact)
            # Assign a unique key to each button using the index
            if st.button("Next", key=f"next_button_{index}"):
                continue


if __name__ == "__main__":
    main()
