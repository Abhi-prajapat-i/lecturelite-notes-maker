from langchain_text_splitters import RecursiveCharacterTextSplitter
from model import llm
from langchain_core.output_parsers import StrOutputParser
from prompt import filter_prompt, note_part_prompt, takeaways_prompt
import time

# Size (in characters) of one part of the lecture that is turned into notes.
# Smaller value  -> more detailed notes (but more LLM calls).
# Bigger value   -> shorter notes (fewer LLM calls).
NOTES_PART_SIZE = 5000


def get_chunks(transcript):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 0,
    )
    return splitter.create_documents([transcript])


chain = filter_prompt | llm | StrOutputParser()


# How many chunks are sent to the model at the same time while filtering.
# Use 1 if you get rate-limit errors (for example with the Groq model).
MAX_CONCURRENCY = 5


def filter_chunks(chunks):
    """Filter all chunks using .batch() (parallel) instead of .invoke() in a loop."""
    inputs = [{"chunk": chunk} for chunk in chunks]

    # batch() keeps the same order as the input, so the lecture order is safe.
    filtered_chunks = chain.batch(
        inputs,
        config={"max_concurrency": MAX_CONCURRENCY},
    )

    final_transcript = "\n\n".join(filtered_chunks)

    return final_transcript


note_chain = note_part_prompt | llm | StrOutputParser()
takeaways_chain = takeaways_prompt | llm | StrOutputParser()


def _get_headings(text):
    """Return the Markdown headings already written (ignores lines inside code blocks)."""
    headings = []
    in_code = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if not in_code and stripped.startswith("#"):
            headings.append(stripped)
    return headings


def get_notes(final_transcript, progress_callback=None):
    """
    Generate complete notes.

    The filtered transcript is split into parts and notes are written for each
    part separately, so nothing is skipped and the output is not limited by the
    model's reply length. Then a final Key Takeaways / Quick Revision section
    is added.

    progress_callback(done, total) is optional (useful for a progress bar).
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=NOTES_PART_SIZE,
        chunk_overlap=0,
    )
    parts = splitter.split_text(final_transcript)
    total = len(parts)

    notes_parts = []

    for index, part in enumerate(parts):
        if index == 0:
            position = (
                "This is the FIRST part of the lecture. Start with a single `#` title "
                "for the main topic of the lecture, followed by a short overview "
                "(2-3 lines: what the topic is and why it matters). Then continue with the notes."
            )
        else:
            position = (
                f"This is part {index + 1} of {total}. Do NOT write a `#` title or an overview again. "
                "Continue the notes directly with `##` sections."
            )

        previous = "\n".join(_get_headings("\n\n".join(notes_parts))) or "None yet"

        note = note_chain.invoke({
            "transcript": part,
            "position_instructions": position,
            "previous_headings": previous,
        })
        notes_parts.append(note.strip())

        if progress_callback:
            progress_callback(index + 1, total)
        # time.sleep(2)  # when is used Groq model then this is required .

    notes = "\n\n".join(notes_parts)

    # Final summary section based on the complete notes.
    try:
        ending = takeaways_chain.invoke({"notes": notes[-30000:]})
        notes = notes + "\n\n" + ending.strip()
    except Exception as e:
        print("Could not generate key takeaways:", e)

    return notes