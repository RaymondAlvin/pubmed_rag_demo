from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st
from watsonxlangchain import LangChainInterface

creds = {
    'apikey': '', # add api key
    'url': 'https://us-south.ml.cloud.ibm.com'
}

llm = LangChainInterface(
    credentials = creds,
    model = 'meta-llama/llama-2-70b-chat',
    params = {
        'decoding_method':'sample',
        'max_new_tokens': 200,
        'temperature':0.5
    },
    project_id='xxx')  # specify project id

@st.cache_resource
def load_pdf():
    pdf_name = 'what is genai.pdf' # change pdf - maybe make json file instead
    loaders = [PyPDFLoader(pdf_name)]
    index = VectorstoreIndexCreator(
        embedding=HuggingFaceEmbeddings(model_name='all-MiniLM-L12-v2'),
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    ).from_loaders(loaders)
    return index

index = load_pdf()

chain = RetrievalQA.from_chain_type(llm=llm,
                                    chain_type='stuff',
                                    retriever=index.vectorstore.as_retriever(),
                                    input_key='question')


st.title('Ask Veera')

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:    
    st.chat_message(message['role']).makrdown(message['content'])

prompt = st.chat_input('Pass your prompt here')

if prompt:
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role':'user', 'content':prompt})
    response = chain.run(prompt)
    st.chat_message('assistant').markdown(response)
    st.session_state.messages.append({'role':'assistant', 'contant': response})

