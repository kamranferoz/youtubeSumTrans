import os
import openai
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import RecursiveCharacterTextSplitter

openai.api_key =  st.secrets["OPENAI_API_KEY"]

# Include sidebar with credentials
with st.sidebar:
    st.markdown('YouTube video summarizer/translator (V 0.2)')
    st.markdown(""" 
                #### Let's contact:
                [Kamran Feroz](https://www.linkedin.com/in/kamranferoz/)

                #### Powered by:
                [OpenAI](https://openai.com/)
                [Langchain](https://github.com/hwchase17/langchain)\n

                #### Source code:
                [DIDX Bot!](https://github.com/kamranferoz/youtubeSumTrans)
                """)
st.markdown(
    "<style>#MainMenu{visibility:hidden;}</style>",
    unsafe_allow_html=True)


def get_language_code(language):
    language_codes = {
        "English": "en",
        "Urdu": "ur"
    }
    if language in language_codes:
        return language_codes[language]
    else:
        raise ValueError("Unsupported language")
    

def get_transcript(youtube_url, language):
    video_id = youtube_url.split("v=")[-1]
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    # Try fetching the manual transcript
    try:
        transcript = transcript_list.find_manually_created_transcript()
        # language_code = transcript.language_code  # Save the detected language
        language_code = get_language_code(language)
    except:
        # If no manual transcript is found, try fetching an auto-generated transcript in a supported language
        try:
            generated_transcripts = [trans for trans in transcript_list if trans.is_generated]
            transcript = generated_transcripts[0]
            # language_code = transcript.language_code  # Save the detected language
            language_code = get_language_code(language)
        except:
            # If no auto-generated transcript is found, raise an exception
            raise Exception("No suitable transcript found.")

    full_transcript = " ".join([part['text'] for part in transcript.fetch()])
    return full_transcript, language_code  # Return both the transcript and detected language


def summarize_with_langchain_and_openai(transcript, language, model_name='gpt-3.5-turbo'):
    # Split the document if it's too long
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    texts = text_splitter.split_text(transcript)
    text_to_summarize = " ".join(texts[:4]) # Adjust this as needed

    # Prepare the prompt for summarization
    system_prompt = 'I want you to act as a Life Coach that can create good summaries!'
    prompt = f'''Summarize the following text in {language}.
    Text: {text_to_summarize}

    Add a title to the summary in {language}. 
    Include an INTRODUCTION, BULLET POINTS if possible, and a CONCLUSION in {language}.'''

    # Start summarizing using OpenAI
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        temperature=1
    )
    
    return response['choices'][0]['message']['content']


def transCript(transcript, language, model_name='gpt-3.5-turbo'):
    # Split the document if it's too long
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    texts = text_splitter.split_text(transcript)
    text_to_summarize = " ".join(texts[:4]) # Adjust this as needed

    # Prepare the prompt for summarization
    system_prompt = 'I want you to act as a professional translator that can translate into any given language!'
    prompt = f'''Translate the following text in {language}.
    Text: {text_to_summarize}'''

    # Start summarizing using OpenAI
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        temperature=1
    )
    
    return response['choices'][0]['message']['content']

def main():
    st.title('YouTube video summarizer')
    link = st.text_input('Enter the link of the YouTube video you want to summarize:')
    language = st.selectbox('Select language', ['English', 'Urdu'])

    if st.button('Start'):
        if link:
            try:
                progress = st.progress(0)
                status_text = st.empty()

                status_text.text('Loading the transcript...')
                progress.progress(25)

                # Getting both the transcript and language_code
                transcript, language_code = get_transcript(link, language)
            
                status_text.text(f'Creating summary...')
                progress.progress(75)

                model_name = 'gpt-3.5-turbo'
                summary = summarize_with_langchain_and_openai(transcript, language, model_name)

                status_text.text('Summary:')
                st.markdown(summary)

                TranslateTranscript = transCript(transcript, language, model_name)
                status_text.text('Transcript:')
                st.markdown(TranslateTranscript)

                progress.progress(100)
            except Exception as e:
                st.write(str(e))
        else:
            st.write('Please enter a valid YouTube link.')

if __name__ == "__main__":
    main()
