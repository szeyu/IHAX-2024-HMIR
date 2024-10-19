import streamlit as st
from jamaibase import protocol as p
import time


def create_chat_table(jamai, knowledge_base_id):
    try:
        with st.spinner("Creating Chat Table..."):
            table = jamai.create_chat_table(
                p.ChatTableSchemaCreate(
                    id=f"chat-rag-{int(time.time())}",
                    cols=[
                        p.ColumnSchemaCreate(id="User", dtype=p.DtypeCreateEnum.str_),
                        p.ColumnSchemaCreate(
                            id="AI",
                            dtype=p.DtypeCreateEnum.str_,
                            gen_config=p.ChatRequest(
                                model="ellm/meta-llama/Llama-3.1-8B-Instruct",
                                messages=[p.ChatEntry.system(st.session_state["system_prompt"])],
                                rag_params=p.RAGParams(
                                    table_id=knowledge_base_id,
                                    k=5,
                                ),
                                temperature=0.1,
                                top_p=0.1,
                                max_tokens=1024,
                            ).model_dump(),
                        ),
                    ],
                )
            )
        st.success("Successfully created Chat Table")
        return table.id
    except Exception as e:
        st.error(f"An error occurred while creating the chat table: {str(e)}")
        return None

def ask_question(jamai, chat_table_id, question):
    completion = jamai.add_table_rows(
        "chat",
        p.RowAddRequest(
            table_id=chat_table_id,
            data=[dict(User=question)],
            stream=True,
        ),
    )

    full_response = ""
    for chunk in completion:
        if chunk.output_column_name != "AI":
            continue
        if isinstance(chunk, p.GenTableStreamReferences):
            pass
        else:
            full_response += chunk.text
            yield full_response

def chatbot():
    st.title("AI-Powered Chatbot")

    # Sidebar
    with st.sidebar:
        if st.button("Back"):
            st.session_state["pages"] = "student"
            st.rerun()

    # Create chat table if not already created
    if "chat_table_id" not in st.session_state:
        chat_table_id = create_chat_table(st.session_state.jamai_client, st.session_state["knowledge_base_id"])
        if chat_table_id:
            st.session_state.chat_table_id = chat_table_id
        else:
            st.error("Failed to create chat table. Please try again.")
            return

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
            full_response = ""
            for response in ask_question(st.session_state.jamai_client, st.session_state.chat_table_id, question):
                message_placeholder.markdown(response + "▌")
                full_response = response
            message_placeholder.markdown(full_response)
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

if __name__ == "__main__":
    chatbot()