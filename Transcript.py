from youtube_transcript_api import YouTubeTranscriptApi


# to get languages from video .
def get_transcript_languages(video_id):

    api = YouTubeTranscriptApi()

    try:
        transcript_list = api.list(video_id)

        languages = []

        for transcript in transcript_list:
            languages.append({
                "language": transcript.language,
                "language_code": transcript.language_code,
                "is_generated": transcript.is_generated
            })

        return languages

    except Exception as e:
        print("Error:", e)
        return []


def get_transcripts(url_id):
    transcript_lang = get_transcript_languages(url_id)

    for lang in transcript_lang :
        if lang["language_code"]== "en":
            
            try:
                api = YouTubeTranscriptApi()

                transcript = api.fetch(
                    url_id,
                    languages=["en"]
                )

                text = " ".join(snippet.text for snippet in transcript)

                transcript_text = text

            except Exception as e:
                print("Error:", e)
    else:
        try:
            api = YouTubeTranscriptApi()

            transcript = api.fetch(
                url_id,
                languages=["hi"]
            )

            text = " ".join(snippet.text for snippet in transcript)

            transcript_text = text

        except Exception as e:
            print("Error:", e)
    return text

