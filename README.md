# youtubeSumTrans
YouTube Video Summary with Translation

**Libraries to install:**
pip install openai streamlit youtube_transcript_api langchain

<img width="825" alt="image" src="https://github.com/kamranferoz/youtubeSumTrans/assets/34434270/65d7ae84-96d4-4cce-9d29-54e6fd0948ec">

This program is a YouTube video summarizer and translator. It allows users to input a YouTube video link and select a language (English or Urdu). The program fetches the transcript of the video using the YouTube Transcript API.

The transcript is then summarized and translated into the selected language using OpenAI's GPT-3.5 Turbo model. The summarization and translation are done in a way that simulates a life coach creating good summaries and a professional translator translating into any given language, respectively.

The summarized text and translated transcript are displayed to the user. The program also includes a progress bar and status text to keep the user informed about the process.

In the sidebar, the program provides links to the developer's LinkedIn profile, the source code of the application, and the libraries used (OpenAI and Langchain). The main menu of Streamlit is hidden for a cleaner user interface.

The sample app can be found at https://yousum.streamlit.app/
