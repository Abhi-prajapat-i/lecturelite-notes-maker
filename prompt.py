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

note_prompt = ChatPromptTemplate.from_template("""
You are an expert academic note-making assistant.

Create clear, structured, and easy-to-understand **study notes** from the following filtered Machine Learning lecture transcript.

### Instructions:

- Extract all important concepts from the transcript.
- Organize the content using clear headings and subheadings.
- Write concise explanations for each concept.
- Include important definitions.
- Include important technical terms and their meanings.
- Include examples given by the teacher.
- Include formulas whenever they are present.
- Explain algorithms and their working steps when discussed.
- Highlight important points for exams and interviews.
- Preserve important details from the transcript.
- Remove unnecessary repetition.
- Use bullet points and numbered lists where appropriate.
- Use simple and clear English.
- Maintain the meaning of the original lecture.
- Do not include casual conversation or classroom discussion.
- Do not add information that is not present in the transcript.
- Do not make the notes unnecessarily short; preserve important explanations.
- If an important concept is explained through an example, keep the example.
- If the transcript contains an important comparison, present it in a table when appropriate.

### Recommended structure:

# Topic Name

## 1. Introduction
Explain the basic idea of the topic.

## 2. Important Concepts
Explain each major concept clearly.

## 3. Important Definitions
List important definitions.

## 4. Examples
Include useful examples from the lecture.

## 5. Algorithms / Methods
Explain the algorithms or methods discussed.

## 6. Important Points
List the key points to remember.

## 7. Exam / Interview Points
Mention concepts that are particularly important for exams or interviews.

## 8. Quick Revision
Give a short summary of the most important concepts at the end.

### Important:
The notes must be based **only on the provided transcript**. Do not hallucinate, assume, or introduce external information.

Filtered lecture transcript:
{transcript}
""")