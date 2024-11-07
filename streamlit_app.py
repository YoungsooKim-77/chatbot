import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("🌍 Travel Chatbot")
st.write(
    "This is a travel chatbot that uses OpenAI's GPT-3.5 model to provide travel-related information and recommendations. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="ℹ️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful travel assistant. Provide concise and informative answers about travel destinations, tips, and recommendations."}
        ]

    # Display the existing chat messages.
    for message in st.session_state.messages[1:]:  # Skip the system message
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field.
    if prompt := st.chat_input("Ask me anything about travel!"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True,
        )

        # Stream the response to the chat and store it.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Add a button to clear the chat history
    if st.button("Clear Chat History"):
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful travel assistant. Provide concise and informative answers about travel destinations, tips, and recommendations."}
        ]
        st.experimental_rerun()
