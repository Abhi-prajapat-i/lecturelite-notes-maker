from langchain_core.prompts import ChatPromptTemplate
 

filter_prompt = ChatPromptTemplate.from_template("""
You are processing one chunk of a recorded educational lecture.

The complete lecture transcript has been divided into small chunks using a text splitter. Your task is to extract **ONLY the actual teaching content** from this chunk.

The final output will be used to create study notes, so remove all communication and keep only information that a student needs to learn the subject.

### REMOVE ALL:
- Greetings and introductions
- Teacher's communication with students
- Casual conversation
- Statements about the previous or next video/lecture
- Statements such as "today we will learn...", "in this video we will...", "let's start...", "moving on..."
- Discussion about what the teacher is going to do
- Course or lecture planning
- Classroom management
- Requests to students
- Filler words and conversational phrases
- Repeated statements that contain no new information
- Personal opinions or unrelated comments
- Meta-commentary about the lecture, video, recording, or teaching process
- Questions that are only for classroom interaction and do not contain useful educational information

### KEEP ONLY:
- Definitions of concepts
- Theories and concepts
- Technical explanations
- Important facts
- Algorithms and their working
- Formulas and equations
- Step-by-step technical processes
- Comparisons and differences between concepts
- Technical examples that explain a concept
- Real-world examples related to the subject
- Important advantages, disadvantages, limitations, and use cases
- Questions and their answers ONLY when they contain useful educational/technical information
- Code that the teacher writes or reads out (imports, class and function names, parameters, variable names), together with the explanation of what the code does
- Outputs or results of code that the teacher shows and explains
- Any statement that directly teaches or explains the subject

### QUESTION-ANSWER RULE:
Keep a question and its answer only if the question-answer pair contains actual educational information.

For example, if the teacher asks a conceptual question and then explains the answer, keep the useful question and answer.

Do NOT keep questions such as:
- "Are you understanding?"
- "Should I continue?"
- "Can you hear me?"
- "Any doubts?"
- "Okay?"
- "Shall we move ahead?"

These are communication, not study content.

### VERY IMPORTANT:
- Do NOT summarize.
- Do NOT create notes.
- Do NOT add new information.
- Do NOT answer questions yourself.
- Do NOT change the meaning of the original teaching content.
- Do NOT rewrite the content unnecessarily.
- Preserve important technical explanations as completely as possible.
- Maintain the original order.
- This is only one chunk of a larger lecture, so do not remove useful content just because a sentence appears incomplete.
- If a chunk contains no useful teaching content, return an empty string.
- Return ONLY the extracted teaching content. Do not add headings such as "Teaching Content" or explanations about what you removed.

### Transcript Chunk:
{chunk}
""")

# The lecture is turned into notes PART BY PART (see Rag.py), so that long
# lectures get complete notes instead of one short summary.
note_part_prompt = ChatPromptTemplate.from_template("""
You are an expert technical note-maker. You write COMPLETE and DETAILED study notes in a clear blog style (like a good technical article on Medium).

You are given ONE PART of a longer lecture. Write the notes for this part only.

{position_instructions}

Headings already written in the earlier parts of the notes (do not repeat them; if a topic continues from the previous part, continue it under a new sub-heading with `###`, do not repeat the topic):
{previous_headings}

### Completeness rules (most important)
- Cover EVERY concept, definition, explanation, example, comparison, code snippet and tip in this part of the transcript. Do NOT skip anything that the teacher taught.
- Do NOT summarize or shorten. The notes of this part should be about as detailed as the teaching content, only written more cleanly.
- Explain each concept fully: what it is, why it is needed, how it works, an example, and when to use it, whenever the teacher covered these.
- Keep the teacher's examples, analogies, numbers, and reasoning. Explain them in simple words.
- Keep every comparison, advantage, disadvantage, limitation and use case that was mentioned.

### Structure and style
- Use `##` for every major topic and `###` for sub-topics. Do NOT put numbers in headings.
- Under each heading write full explanations. Use short paragraphs (2-5 sentences) and bullet points or numbered steps where it helps.
- Use **bold** for key terms.
- If the teacher showed or explained code, include it in a fenced code block with the language (for example ```python). Keep imports, class names, function names and parameters exactly as stated, and add an explanation of what the code does, line by line if the teacher did so.
- If the teacher showed or explained the output of code, show it in a separate fenced code block.
- Use a quote line starting with `> ` for tips, warnings, and common mistakes the teacher mentioned.
- Use a Markdown table when two or more things are compared.
- Do NOT use LaTeX or dollar signs. Write symbols in plain text or Unicode (λ, ≤, ≥, →, ×) and formulas in plain text or in a code block.
- Do NOT use emojis.
- Do NOT include greetings, casual talk or classroom discussion.

### Accuracy rules
- Use ONLY the information in the transcript part below. Do NOT add outside knowledge, extra examples, extra code or extra outputs.
- Do NOT invent code, parameters, or outputs. If the teacher only described code in words, describe it in words.
- If something is unclear in the transcript, leave it out instead of guessing.

### Transcript part:
{transcript}
""")


takeaways_prompt = ChatPromptTemplate.from_template("""
Below are complete study notes of a lecture.

Write the final section of the notes, in this exact format:

## Key Takeaways
(8-12 bullet points that summarize the most important things to remember from the whole lecture)

## Quick Revision
(a short bullet list: one line per major topic of the notes, saying in one sentence what it is or when to use it)

Rules:
- Use ONLY the information in the notes. Do not add anything new.
- Do NOT use LaTeX, emojis or tables.
- Remove duplicate.
- Return only these two sections, nothing else.

### Notes:
{notes}
""")