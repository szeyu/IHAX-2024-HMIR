import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_community.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler
import dotenv
dotenv.load_dotenv()

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text + "▌")

def load_pdf_and_create_qa_chain():
    if 'qa_chain' not in st.session_state:
        file_path = st.session_state['file_path']
        loader = PyPDFLoader(file_path=file_path)
        documents = loader.load()

        embeddings = OpenAIEmbeddings()
        vector_store = DocArrayInMemorySearch.from_documents(documents, embeddings)

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        streaming_llm = OpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0)

        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=streaming_llm,
            retriever=vector_store.as_retriever(),
            memory=memory
        )

        st.session_state['qa_chain'] = qa_chain

def chatbot():
    st.title("AI-Powered Chatbot")

    # Sidebar
    with st.sidebar:
        if st.button("Back"):
            st.session_state["pages"] = "student"
            st.rerun()

    # Load PDF and create QA chain
    load_pdf_and_create_qa_chain()

    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    chat_container = st.container()
    with chat_container:
        st.header("Chat with the AI")
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # User input
    question = st.chat_input("Ask a question about the document")

    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(question)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            stream_handler = StreamHandler(message_placeholder)

            result = st.session_state['qa_chain'](
                {"question": question},
                callbacks=[stream_handler]
            )
            response = result['answer']

            message_placeholder.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.session_state['qa_chain'] = None  # Reset the QA chain
        st.rerun()