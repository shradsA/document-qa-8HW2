import streamlit as st
from openai import OpenAI
import cohere
import requests
from bs4 import BeautifulSoup
import time

# Optional Groq import
try:
    from groq import Groq
    groq_available = True
except ModuleNotFoundError:
    groq_available = False

def run_hw2():
    st.title("HW2 - URL Summarizer")
    st.write("Enter a web page URL, choose summary type, language, and LLM to use.")

    # -------------------------------
    # Helper function: read URL
    # -------------------------------
    def read_url_content(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.get_text(separator="\n")
        except requests.RequestException as e:
            st.error(f"Error reading {url}: {e}")
            return None

    # -------------------------------
    # Sidebar controls
    # -------------------------------
    summary_type = st.sidebar.selectbox(
        "Type of Summary", ["Short Summary", "Detailed Summary", "Bullet Points"]
    )
    output_language = st.sidebar.selectbox(
        "Output Language", ["English", "French", "Spanish"]
    )

    # LLM selection in sidebar
    llm_options = ["OpenAI (gpt-4.1)", "Cohere (command-r-plus)"]
    if groq_available:
        llm_options.append("Groq (llama-3.3-70b-versatile)")
    llm_choice = st.sidebar.selectbox("Choose LLM", llm_options)

    # -------------------------------
    # URL input (top of main page)
    # -------------------------------
    url = st.text_input("Enter a webpage URL", placeholder="https://example.com")

    # -------------------------------
    # Run button
    # -------------------------------
    if st.button("Summarize URL"):
        if not url.strip():
            st.error("Please enter a valid URL.")
            return

        with st.spinner("Reading webpage..."):
            content = read_url_content(url)

        if not content:
            st.error("Failed to retrieve content.")
            return

        MAX_CHARS = 4000
        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS]
            st.warning("Webpage is large; only the first part is summarized.")

        prompt = f"""
You are a helpful assistant. Read the following webpage content and provide a {summary_type}.
Make sure your response is in {output_language}.

Webpage Content:
{content}
"""

        start_time = time.time()
        answer = "Not implemented."

        # -------------------------------
        # Run LLM based on sidebar choice
        # -------------------------------
        try:
            if llm_choice.startswith("OpenAI"):
                client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))
                response = client.chat.completions.create(
                    model="gpt-4.1",
                    messages=[{"role": "user", "content": prompt}]
                )
                answer = response.choices[0].message.content

            elif llm_choice.startswith("Cohere"):
                client = cohere.Client(api_key=st.secrets.get("COHERE_API_KEY"))
                response = client.chat(model="command-r-plus", message=prompt)
                answer = response.text

            elif llm_choice.startswith("Groq"):
                if not groq_available:
                    answer = "Groq SDK not installed."
                else:
                    groq_key = st.secrets.get("GROQ_API_KEY")
                    if not groq_key:
                        answer = "Groq API key not found in secrets."
                    else:
                        client = Groq(api_key=groq_key)
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        answer = response.choices[0].message.content

        except Exception as e:
            answer = f"Error: {e}"

        elapsed = time.time() - start_time
        st.subheader(f"Summary ({llm_choice})")
        st.write(f"**Elapsed time:** {elapsed:.2f} seconds")
        st.markdown("**Result:**")
        st.write(answer)


