import tkinter as tk
from transformers import pipeline
import requests


def send_email():
    mail_text = mail_text_entry.get("1.0", tk.END)
    choice = choice_var.get()

    if choice and mail_text:
        return_dict = {"Email Text": mail_text, "Choice": choice}
        mail.append(return_dict)
        window.destroy()


mail = []

window = tk.Tk()
window.title("G-Mail")

mail_text_label = tk.Label(window, text="Mail Text:")
mail_text_label.pack()

mail_text_entry = tk.Text(window, height=20, width=60)
mail_text_entry.pack()

choice_var = tk.StringVar()

choice_label = tk.Label(window, text="Select Suitable Compression Method:")
choice_label.pack()

choice1_radio = tk.Radiobutton(window, text="Table", variable=choice_var, value="Choice 1")
choice1_radio.pack()

choice2_radio = tk.Radiobutton(window, text="Summarization", variable=choice_var, value="Choice 2")
choice2_radio.pack()

send_button = tk.Button(window, text="Send", command=send_email)
send_button.pack()

window.mainloop()

input_dictionary = mail[0]

pre_prompt = ""

if input_dictionary["Choice"] == "Choice 1":
    pre_prompt = "\n\nCompress this email into a python dictionary. Write only the dictionary in the output."

    url = "https://api.openai.com/v1/chat/completions"
    api_token = "" #API Key

    prompt = input_dictionary["Email Text"] + pre_prompt

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
    )

    data = response.json()
    print(data["choices"][0]["message"]["content"])


elif input_dictionary["Choice"] == "Choice 2":

    classifier = pipeline("summarization")
    summary = classifier(input_dictionary["Email Text"])
    print(summary[0]["summary_text"])

    """
    # Extractive Summarization
    text = input_dictionary["Email Text"]
    
    import spacy
    from spacy.lang.en.stop_words import STOP_WORDS
    from string import punctuation
    from heapq import nlargest
    
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
    
    nlp = spacy.load('en_core_web_sm')
    
    doc = nlp(text)
    
    tokens = [token.text for token in doc]
    
    punctuation = punctuation + '\n'
    
    word_frequencies = {}
    for word in doc:
      if word.text.lower() not in stopwords:
        if word.text.lower() not in punctuation:
          if word.text not in word_frequencies.keys():
            word_frequencies[word.text] = 1
          else:
            word_frequencies[word.text] += 1
    
    
    
    max_frequency = max(word_frequencies.values())
    
    
    
    for word in word_frequencies.keys():
      word_frequencies[word] = word_frequencies[word]/max_frequency
    
    
    
    sentence_tokens = [sent for sent in doc.sents]
    
    sentence_scores = {}
    for sent in sentence_tokens:
      for word in sent:
        if word.text.lower() in word_frequencies.keys():
          if sent not in sentence_scores.keys():
            sentence_scores[sent] = word_frequencies[word.text.lower()]
          else:
            sentence_scores[sent] += word_frequencies[word.text.lower()]
    
    
    
    select_length = int(len(sentence_tokens)*0.3)
    
    summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)
    
    
    
    final_summary = [word.text for word in summary]
    
    summary = ' '.join(final_summary)
    
    print(summary)
    """


