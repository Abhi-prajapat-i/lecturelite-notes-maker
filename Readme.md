# 👩‍🏫 LectureLite – YouTube Lecture Notes Generator

LectureLite turns long YouTube lectures into light, quick **study notes**. It is a Streamlit app that uses AI to pull out only the important teaching content. Paste a video link, get structured notes in seconds, and **download them as a PDF**.

## ✨ Features

- 🔗 Paste any YouTube video URL (`youtube.com` or `youtu.be`)
- 📝 Fetches the video transcript automatically (English, with Hindi fallback)
- 🧹 Filters out greetings, filler and classroom chatter, keeping only the teaching content
- 🤖 Generates structured notes: introduction, concepts, definitions, examples, algorithms, key points, exam/interview points and a quick revision
- 📥 Downloads the notes as a nicely formatted PDF (headings, bullet lists, tables, code blocks, page numbers)
- 🎨 Simple and clean Streamlit interface

## 🛠️ How It Works

```
YouTube URL
    │
    ▼
Extract video ID ──► Fetch transcript ──► Split into chunks
                                              │
                                              ▼
                                  LLM filters each chunk
                                  (keeps only teaching content)
                                              │
                                              ▼
                                  LLM generates Markdown notes
                                              │
                                              ▼
                              Show in app  +  Download as PDF
```

## 📁 Project Structure

```
LectureLite/
├── main.py                 # Streamlit app (UI + workflow)
├── Video_id_generater.py   # Extracts the video ID from a YouTube URL
├── Transcript.py           # Fetches the video transcript
├── Rag.py                  # Chunking, transcript filtering and note generation
├── prompt.py               # Prompts for filtering and note making
├── model.py                # LLM configuration (OpenRouter / Groq)
├── pdf_maker.py            # Converts the Markdown notes into a PDF
├── requirements.txt        # Python dependencies
├── .gitignore              # Files ignored by Git (.env, __pycache__, ...)
├── .env                    # API keys (not committed)
└── README.md
```

## 🧰 Tech Stack

- **Python 3.12**
- **Streamlit** – web interface
- **LangChain** – prompts, chains and text splitting
- **OpenRouter** (`google/gemma-4-31b-it`) – LLM (Groq is also supported)
- **youtube-transcript-api** – transcript extraction
- **ReportLab** – PDF generation

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/LectureLite.git
cd LectureLite
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
# Optional – only needed if you switch to the Groq model in model.py
GROQ_API_KEY=your_groq_api_key_here
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

### 5. Run the app

```bash
streamlit run main.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`).

## 📖 Usage

1. Paste a YouTube video link into the input box.
2. Click **🚀 Generate Notes**.
3. Wait while the transcript is processed and the notes are generated.
4. Read the notes in the app, or click **📥 Download Notes as PDF**.

## 📄 PDF Export

PDF creation lives in `pdf_maker.py`:

```python
from pdf_maker import create_pdf

pdf_bytes = create_pdf(notes_markdown, title="Study Notes", source_url="https://youtu.be/...")
```

For best results with special symbols (≤, →, α, β, ...), place the DejaVu Sans font files
(`DejaVuSans.ttf`, `DejaVuSans-Bold.ttf`, `DejaVuSans-Oblique.ttf`, `DejaVuSans-BoldOblique.ttf`)
in a `fonts/` folder next to `pdf_maker.py`. Without them, the app falls back to a system font.

You can test the PDF generator on its own:

```bash
python pdf_maker.py   # creates sample_notes.pdf
```

## ⚠️ Limitations

- The video must have captions/transcripts available (English or Hindi).
- Very long videos take longer, because every transcript chunk is sent to the LLM.
- Free-tier models on OpenRouter or Groq may have rate limits.
- Notes are generated only from the transcript, so their quality depends on the transcript quality.

## 🔮 Future Improvements

- Support for more transcript languages
- Download notes as Word / Markdown
- Progress bar for long videos
- Notes history

## 🤝 Contributing

Contributions are welcome! Fork the repository, create a feature branch and open a pull request.

## 👨‍💻 Author

**Abhishek Kumar** – AI Learner

---

⭐ If you found this project useful, consider giving it a star on GitHub!