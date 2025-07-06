from transformers import pipeline #Uses Huggingface's transformers library
summarizer = pipeline("summarization")
def chunk_text(text, max_words=1000):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield ' '.join(words[i:i + max_words])

def summarize_text(text):
    # If text is short enough, summarize directly
    if len(text.split()) <= 1000:
        summarized = summarizer(text, max_length=300, min_length=100, do_sample=False)
        return summarized[0]["summary_text"]

    # Otherwise chunk the text and summarize each chunk separately
    chunk_summaries = []
    for chunk in chunk_text(text, max_words=1000):
        summary = summarizer(chunk, max_length=300, min_length=100, do_sample=False)
        chunk_summaries.append(summary[0]["summary_text"])

    # Combine all chunk summaries and summarize again to get a concise summary
    combined_summary = " ".join(chunk_summaries)
    final_summary = summarizer(combined_summary, max_length=300, min_length=100, do_sample=False)
    return final_summary[0]["summary_text"]