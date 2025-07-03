from transcriber import transcribe_audio #function that converts video audio to text
from summarizer import summarize_text #function that summarizes text

def chunk_text(text, max_words=1000):
    """
    This splits the input text into smaller chunks, each containing up to max_words words.
    This helps to avoid exceeding model token limits during summarization.
    """
    words = text.split()
    for i in range(0, len(words), max_words):
        yield ' '.join(words[i:i + max_words]) #THis yields a chunk by joining the next max_words words into a string

video_path = "uploads/lockdown_side_effects.mp4"  #Path to the video

print("Transcribing the video....")
transcription = transcribe_audio(video_path) #Call the transcriber function to get full transcription text
print("Transcription: \n", transcription) #Print the full transcription (can be long!)

print("\nSummarizing in chunks...") 

chunk_summaries = []
for i, chunk in enumerate(chunk_text(transcription, max_words=300)):
    print(f"Summarizing chunk {i + 1}...") # Inform which chunk is being summarized
    chunk_summary = summarize_text(chunk) # Summarize the current chunk using your summarizer function
    print(f"Chunk {i + 1} summary:\n{chunk_summary}\n")
    chunk_summaries.append(chunk_summary) #Save this chunk's summary to the list

# Combine all chunk summaries into one text
final_summary_text = ' '.join(chunk_summaries)

# Optionally, summarize the combined summary again to get a concise final summary
print("Generating final summary from chunk summaries...") #Inform user that final summarization starts
final_summary = summarize_text(final_summary_text) #Summarize the combined chunk summaries to get a concise summary

print("\nFinal Summary:\n", final_summary)

with open("summary.txt", "w") as f:
    f.write(final_summary)

print("Saved summary to summary.txt")
