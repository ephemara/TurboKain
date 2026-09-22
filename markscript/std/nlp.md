# NLP

MarkScript natural language processing -- text analysis, tokenization,
sentiment, and embeddings. Dispatches to Python's `nltk`, `spaCy`,
and `transformers` through the IVT `run` handler.

---

## tokenize

Split text into individual tokens (words).

> run "python -c \"from nltk.tokenize import word_tokenize; print(word_tokenize('The quick brown fox jumps over the lazy dog.'))\""

```markscript
let text = "The quick brown fox jumps over the lazy dog."
# tokens = ['The', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog', '.']
let count = 10
```

---

## sent_tokenize

Split text into sentences.

> run "python -c \"from nltk.tokenize import sent_tokenize; print(sent_tokenize('Hello world. How are you? I am fine.'))\""

```markscript
let text = "Hello world. How are you? I am fine."
# sentences = ['Hello world.', 'How are you?', 'I am fine.']
let count = 3
```

---

## stem

Reduce words to their base/stem form (Porter Stemmer).

> run "python -c \"from nltk.stem import PorterStemmer; ps=PorterStemmer(); words=['running','runner','ran','easily','fairly']; stems=[ps.stem(w) for w in words]; print(stems)\""

```markscript
let words = ["running" "runner" "ran" "easily" "fairly"]
# stems = ['run', 'runner', 'ran', 'easili', 'fairli']
```

---

## lemmatize

Reduce words to their dictionary base form (lemma).

> run "python -c \"from nltk.stem import WordNetLemmatizer; lemmatizer=WordNetLemmatizer(); words=['running','better','mice','studies']; lemmas=[lemmatizer.lemmatize(w,pos='v') if w=='running' else lemmatizer.lemmatize(w) for w in words]; print(lemmas)\""

```markscript
let words = ["running" "better" "mice" "studies"]
# lemmas = ['running', 'better', 'mouse', 'study']
# lemmatization considers part of speech
```

---

## sentiment

Perform sentiment analysis on text (positive/negative/neutral).

> run "python -c \"from nltk.sentiment import SentimentIntensityAnalyzer; sia=SentimentIntensityAnalyzer(); texts=['This is amazing!','I hate this.','The weather is okay.']; for t in texts: print(sia.polarity_scores(t))\""

```markscript
let text1 = "This is amazing!"
let text2 = "I hate this."
let text3 = "The weather is okay."
# text1: {'neg':0.0, 'neu':0.4, 'pos':0.6, 'compound':0.75}  → positive
# text2: {'neg':0.6, 'neu':0.4, 'pos':0.0, 'compound':-0.78} → negative
# text3: {'neg':0.0, 'neu':1.0, 'pos':0.0, 'compound':0.0}   → neutral
```

---

## ner

Perform Named Entity Recognition (NER) to extract entities.

> run "python -c \"import spacy; nlp=spacy.load('en_core_web_sm'); doc=nlp('Apple Inc. was founded by Steve Jobs in Cupertino.'); for ent in doc.ents: print(f'{ent.text} -> {ent.label_}')\""

```markscript
let text = "Apple Inc. was founded by Steve Jobs in Cupertino."
# Apple Inc. → ORG
# Steve Jobs → PERSON
# Cupertino → GPE (Geopolitical Entity)
```

---

## embeddings

Generate text embeddings (vector representations) using a transformer model.

> run "python -c \"from sentence_transformers import SentenceTransformer; model=SentenceTransformer('all-MiniLM-L6-v2'); emb=model.encode(['Hello world','Machine learning is fun']); print(f'shape={emb.shape}'); print(emb[0][:5])\""

```markscript
let sentences = ["Hello world" "Machine learning is fun"]
let model = "all-MiniLM-L6-v2"
# embeddings shape: (2, 384)
# first 5 values of sentence 0: [0.12 -0.34 0.56 0.78 -0.23]
```

---

## similarity

Compute cosine similarity between two text embeddings.

> run "python -c \"from sentence_transformers import SentenceTransformer; from sklearn.metrics.pairwise import cosine_similarity; import numpy as np; model=SentenceTransformer('all-MiniLM-L6-v2'); e1=model.encode(['I love programming']); e2=model.encode(['I enjoy coding']); sim=cosine_similarity(e1,e2)[0][0]; print(f'similarity={sim:.4f}')\""

```markscript
let text1 = "I love programming"
let text2 = "I enjoy coding"
# cosine similarity ≈ 0.82 (highly similar)
```

---

## pos_tag

Perform part-of-speech tagging on text.

> run "python -c \"import nltk; tokens=nltk.word_tokenize('The dog runs quickly'); print(nltk.pos_tag(tokens))\""

```markscript
let text = "The dog runs quickly"
# [('The', 'DT'), ('dog', 'NN'), ('runs', 'VBZ'), ('quickly', 'RB')]
# DT=determiner, NN=noun, VBZ=verb, RB=adverb
```

---

## word_frequency

Compute word frequency counts in a text.

> run "python -c \"from collections import Counter; import nltk; tokens=nltk.word_tokenize('the cat and the dog and the mouse'); freq=Counter(tokens); print(freq.most_common(5))\""

```markscript
let text = "the cat and the dog and the mouse"
# [('the', 3), ('and', 2), ('cat', 1), ('dog', 1), ('mouse', 1)]
```

---

## stopwords_remove

Remove common stop words from text.

> run "python -c \"from nltk.corpus import stopwords; from nltk.tokenize import word_tokenize; stop=set(stopwords.words('english')); tokens=word_tokenize('This is a sample sentence with some stop words'); filtered=[t for t in tokens if t.lower() not in stop]; print(filtered)\""

```markscript
let text = "This is a sample sentence with some stop words"
# filtered = ['sample', 'sentence', 'stop', 'words']
# removed: This, is, a, with, some
```

---

## ngrams

Generate n-gram sequences from tokenized text.

> run "python -c \"from nltk import ngrams; tokens=['natural','language','processing','is','fun']; bigrams=list(ngrams(tokens,2)); trigrams=list(ngrams(tokens,3)); print(bigrams); print(trigrams)\""

```markscript
let tokens = ["natural" "language" "processing" "is" "fun"]
# bigrams: [('natural','language'), ('language','processing'), ('processing','is'), ('is','fun')]
# trigrams: [('natural','language','processing'), ('language','processing','is'), ('processing','is','fun')]
```
