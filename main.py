import streamlit as st
from Video_id_generater import get_id
from Transcript import get_transcripts
from Rag import get_chunks, get_notes,filter_chunks
from pdf_maker import create_pdf

def main():

    # Page Configuration
    st.set_page_config(
        page_title="Note Maker",
        page_icon="👩‍🏫",
        layout="wide"
    )


    # Global Styling 
   
    st.markdown(
        """
        <style>
        .main-header {
            background: linear-gradient(135deg, #00695c 0%, #4db6ac 100%);
            padding: 2rem 2.2rem;
            border-radius: 14px;
            color: white;
            margin-bottom: 1.5rem;
        }
        .main-header h1 {
            margin-bottom: 0.3rem;
            font-size: 2.1rem;
        }
        .main-header p {
            margin: 0;
            font-size: 1.02rem;
            opacity: 0.92;
        }
        .section-card {
            background-color: #ffffff;
            border: 1px solid #e3e8e3;
            border-radius: 12px;
            padding: 1.3rem 1.4rem;
            margin-bottom: 1rem;
        }
        .result-card {
            background-color: #f1f8f2;
            border: 1px solid #cfe8d1;
            border-radius: 12px;
            padding: 1.2rem 1.4rem;
            margin-bottom: 1rem;
        }
        .chat-row {
            display: flex;
            margin-bottom: 0.6rem;
        }
        .chat-row-user {
            justify-content: flex-end;
        }
        .chat-row-ai {
            justify-content: flex-start;
        }
        .chat-bubble-user {
            background-color: #e8f5e9;
            color: #1b1b1b;
            border-radius: 10px;
            padding: 0.6rem 0.9rem;
            max-width: 75%;
            text-align: right;
        }
        .chat-bubble-ai {
            background-color: #f5f5f5;
            color: #1b1b1b;
            border-radius: 10px;
            padding: 0.6rem 0.9rem;
            max-width: 75%;
            text-align: left;
        }
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
        }
        .app-footer {
            margin-top: 2.5rem;
            padding: 1rem 0 0.5rem 0;
            border-top: 1px solid #e3e8e3;
            text-align: center;
            color: #6b7a6b;
            font-size: 0.9rem;
        }
        .app-footer b {
            color: #2e7d32;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Header
    st.markdown(
        """
        <div class="main-header">
            <h1> 👩‍🏫 Note Maker</h1>
            <h2>    YouTube Video Notes Maker </h2>
            <p> Paste a YouTube video link and AI will generate the Notes.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar
   
    with st.sidebar:

        st.markdown("---")

        st.markdown("#### 🤖 AI Note Generater")
        ai = st.checkbox(
            "Enable AI Notes Generation",
            value=True,
        )

        st.markdown("---")

        st.info(
            "💡 **Tip:** Upload the currect url of video."

        )

        st.caption("👩‍🏫  Powered by AskTube AI.")


    # Main Layout
    st.subheader("📤 Paste YouTube Url")
    youtube_url = st.text_input(" ",
    placeholder="Paste your YouTube video link here..."
    )

    # Keep the generated notes in session_state. Streamlit re-runs the whole
    # script when the download button is clicked, so without this the notes
    # would disappear.
    if "notes" not in st.session_state:
        st.session_state.notes = None
        st.session_state.pdf_bytes = None
        st.session_state.video_id = None

    if st.button("🚀 Generate Notes"):
        if not youtube_url:
            st.warning("Please enter a YouTube URL.")
        else:
            # 1. Extract video ID
            url_id = get_id(youtube_url)

            if url_id is None:
                st.warning("Not able to Find the url id.")
            else:
                with st.spinner("Generating notes... this may take a minute."):
                    # 2. Load transcripts and generate notes
                    transcript_text = get_transcripts(url_id)
                    chunks = get_chunks(transcript_text)
                    filter_transcripts = filter_chunks(chunks)
                    notes = get_notes(filter_transcripts)

                    # 3. Create the PDF once and keep it for the download button
                    try:
                        pdf_bytes = create_pdf(
                            notes,
                            title="YouTube Video Notes",
                            source_url=youtube_url,
                        )
                    except Exception as e:
                        pdf_bytes = None
                        st.error(f"Could not create the PDF: {e}")

                st.session_state.notes = notes
                st.session_state.pdf_bytes = pdf_bytes
                st.session_state.video_id = url_id
                st.success("Generation Complete.")

    # Show the notes + download button (stays visible after download click)
    if st.session_state.notes:
        if st.session_state.pdf_bytes:
            st.download_button(
                label="📥 Download Notes as PDF",
                data=st.session_state.pdf_bytes,
                file_name=f"notes_{st.session_state.video_id}.pdf",
                mime="application/pdf",
            )
        st.markdown(st.session_state.notes)

    # -------------------------
    # Footer
    # -------------------------

    st.markdown(
        """
        <div class="app-footer">
            🌿 Developed by <b>Abhishek Kumar</b> — AI Learner.
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()