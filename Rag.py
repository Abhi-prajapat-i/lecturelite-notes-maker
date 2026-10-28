from langchain_text_splitters import RecursiveCharacterTextSplitter
from model import llm
from langchain_core.output_parsers import StrOutputParser
from prompt import filter_prompt, note_prompt
import time
def get_chunks(transcript):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 0,
    )
    return splitter.create_documents([transcript])


chain = filter_prompt | llm | StrOutputParser()


def filter_chunks(chunks):

    filtered_chunks = []

    for chunk in chunks:
        result = chain.invoke({"chunk": chunk})
        filtered_chunks.append(result)
        # time.sleep(2)  # when is used Groq model then this is required .

    final_transcript = "\n\n".join(filtered_chunks)

    return final_transcript


def get_notes(final_transcript):
    note_chain = note_prompt | llm | StrOutputParser()

    notes = note_chain.invoke({
        "transcript": final_transcript
        })
    return notes