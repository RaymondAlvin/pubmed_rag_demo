from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA, LLMChain  # Import LLMChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st
from openai import OpenAI
import os

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Define a Runnable class for OpenAI queries, satisfying langchain's expectations
class CustomRunnable:
    def __init__(self, client, model="gpt-4"):
        self.client = client
        self.model = model

    def run(self, input_text):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_text}
            ]
        )
        return response.choices[0].message.content

# Instantiate the runnable with the OpenAI client
llm_runnable = CustomRunnable(client)

# Function to load and index the PDF document
@st.cache_resource
def load_pdf():
    pdf_name = 'hope.pdf'  # Your PDF file name
    loaders = [PyPDFLoader(pdf_name)]
    index = VectorstoreIndexCreator(
        embedding=HuggingFaceEmbeddings(model_name='all-MiniLM-L12-v2'),
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    ).from_loaders(loaders)
    return index

index = load_pdf()

# **Instantiate the LLMChain with the custom runnable object**
llm_chain = LLMChain(llm=llm_runnable)

# Create the RetrievalQA chain with the LLMChain object
chain = RetrievalQA.from_chain_type(
    llm=llm_chain,  # Use the LLMChain object here
    chain_type='stuff',
    retriever=index.vectorstore.as_retriever(),
    input_key='question'  # Ensure "prompt" is replaced with "question"
)

st.title('Ask Veera')

# Initialize session state for message history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:    
    st.chat_message(message['role']).markdown(message['content'])

# Input for new prompts
prompt = st.chat_input('Pass your prompt here')

# Process and display response
if prompt:
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    
    # Replace "prompt" with "question" in chain.run
    response = chain.run(question=prompt)  # Use question instead of prompt
    st.chat_message('assistant').markdown(response)
    st.session_state.messages.append({'role': 'assistant', 'content': response})
