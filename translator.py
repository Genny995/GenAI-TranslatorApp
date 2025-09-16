import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

#Loading environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

#prompt
prompt = ChatPromptTemplate.from_messages(
    [("system", "Translate the following text from {origin_language} to {destination_language} with just one version."),
     ("user", "{text}")]
)

#Pipeline: prompt -> model -> parser
def build_chain():
    #select model from Groq
    llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)
    parser = StrOutputParser()
    return prompt | llm | parser

#build the chain
chain = build_chain()

#Streamlit
st.set_page_config(page_title="AI Translator by Gennaro", page_icon=":world_map:", layout="centered")
st.title("AI (Groq) Translator")
st.caption("This is a simple app that translates input text to a given language using Groq's Gemma2 model and LangChain.")


#languages
languages = [
    "Automatic Detection",
    "Italian",
    "English",
    "Spanish",
    "French",
    "German",
    "Chinese",
    "Japanese",
    "Dutch",
    "Russian",
    "Portuguese",
    "Swedish",
]

#callback for the swap button
def swap_languages():
    if st.session_state["origin_language"] == "Automatic Detection":
        st.session_state["swap_warning"] = True
        return
    # scambia i valori nello stato
    st.session_state["origin_language"], st.session_state["destination_language"] = (
        st.session_state["destination_language"],
        st.session_state["origin_language"],
    )


col_lang1, col_swap, col_lang2 = st.columns([10, 4, 10]) #create three columns with different widths
with col_lang1:
    origin_language = st.selectbox("Select the origin language:", 
                                   languages, 
                                   index=0, #default Automatic Detection
                                   key = "origin_language") #key to access the value in the state

with col_swap:
    st.button(
        "Swap Languages",
        help="Swap the origin and destination languages",
        use_container_width=True,
        on_click=swap_languages  # <-- usa il callback
    )

with col_lang2:
    destination_language = st.selectbox("Select the destination language:", 
                                        languages[1:], #exclude Automatic Detection
                                        index=1, #default italian
                                        key="destination_language") #key to access the value in the state


text = st.text_area(
    "Enter the text you want to translate:",
    height=150, #height of the text box (pixels)
    placeholder="Type your text here...", #gray text when box is empty
)


col1, col2 = st.columns([1,1]) #create two columns of equal width
with col1:
    btn = st.button("Translate") #button to trigger translation
with col2:
    clear = st.button("Clear") #button to clear text area

if clear: #if clear button is pressed
    text = "" #clear text area
    st.experimental_rerun() #rerun the app to reflect changes

if btn: #if translate button is pressed
    if not groq_api_key:
        st.error("Please set your GROQ_API_KEY in the .env file.")
    elif not text.strip(): #if text area is empty
        st.warning("Please enter some text to translate.")
    else:
        with st.spinner("Translating..."): #show spinner while translating
            try:
                response = chain.invoke({
                    "origin_language": origin_language, 
                    "destination_language": destination_language,
                    "text": text
                    }) #invoke the chain with user inputs
                
                st.success("Translation completed!") #show success message
                st.text_area("Translated Text:", value=response, height=150) #show translated text in a text area
            except Exception as e:
                st.error(f"An error occurred during the translation: {e}") #show error message if something goes wrong

#footer info
st.markdown("---")
st.caption("Model: Gemma2-9b-It by Groq | Built with LangChain and Streamlit | Author: Gennaro Auricchio")