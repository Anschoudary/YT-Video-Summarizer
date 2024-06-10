
import textwrap
import streamlit as st
import google.generativeai as genai
from IPython.display import Markdown
from youtube_transcript_api import YouTubeTranscriptApi
genai.configure(api_key='AIzaSyC2hyU7GkXWUo7Yjclgt4BtLAwa8kSY-zY')    # your-google-generativeai-api
model = genai.GenerativeModel('gemini-1.5-flash')

def transcript(link):  

    text = ""
    response = []
    link = link.split("/")[-1]

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(link)
        for transcript in transcript_list:
            response = transcript.translate('en').fetch()

        for i in response:
            text = text + i['text']

        generated = model.generate_content(f"Assist as an expert content writer. Summarize this text (60 to 800 words) and remove all kind of formatting (plain-text): {text}")
        text = generated.text

        text = text.replace('•', '  *')
        text = Markdown(textwrap.indent(text, '> ', predicate=lambda _: True)).data
        return text

    except Exception as e:
        return ("Something went wrong, Try another video!")



# Set the title of the app
st.title("YouTube Transcript Analyzer")

# Initialize a session state variable to store YouTube links
if 'youtube_links' not in st.session_state:
    st.session_state.youtube_links = ['']

# Function to add a new input field for a YouTube link
def add_link():
    if len(st.session_state.youtube_links) < 5:
        st.session_state.youtube_links.append('')

# Remove the last input field for a YouTube link
def remove_link():
    if len(st.session_state.youtube_links) > 1:
        st.session_state.youtube_links.pop()

# Display input fields for each YouTube link
for i, link in enumerate(st.session_state.youtube_links):
    st.session_state.youtube_links[i] = st.text_input(f"YouTube Link {i+1}", value=link)

# Add buttons to add or remove links
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    st.button("Add Link", on_click=add_link)
with col2:
    st.button("Remove Link", on_click=remove_link)

# Display a submit button
if st.button("Submit"):
    st.write("YouTube Links Submitted:")
    for link in st.session_state.youtube_links:
        st.write(link)
    i = 1
    st.success("Processing completed. Check the results below.")
    for link in st.session_state.youtube_links:
        text = transcript(link)
        st.text_area(f"Generated Script {i}", value=text, height=300)
        i += 1

