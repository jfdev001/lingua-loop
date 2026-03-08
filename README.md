# lingua-loop

LinguaLoop bundles my technique for learning languages into a simple web
application. The technique is as follows:

1. Select a youtube video in the target language and make sure the video has
   *official* transcripts also in the target language.
2. Listen to the video in small segements (e.g., 10 second segments) and
   attempt to write down what you hear.
3. Once you have made an honest attempt, compare what you have written to the
   official transcript.
4. Repeat for as long as desired.

This app provides an interface for this technique and also computes a score
of how closely your attempted transcription aligns with the official
transcripts.

Future work could include any of the following:

1. Integrate an AI chat bot that is given the full transcript as context and
   subsequently asks the user comprehension questions or engages in
   conversation about the video topic.
2. Integrate Anki-style flash cards for selected words. A word should be added
   to a flash card deck in addition to the context in which it occurred (e.g.,
   sentence or phrase). The user *should* write additional context to keep them
   actively engaged in the learning process. 

# References

[1] [Python FastAPI Tutorial (Part 1): Getting Started - Web App + REST API](https://www.youtube.com/watch?v=7AMjmCTumuo)

[2] [Learn Fast API With This ONE Project](https://www.youtube.com/watch?v=SR5NYCdzKkc)

[3] [Anatomy of a Scalable Python Project (FastAPI)](https://www.youtube.com/watch?v=Af6Zr0tNNdE)

[4] [Developing and Testing an Asynchronous API with FastAPI and Pytest](https://testdriven.io/blog/fastapi-crud/) & [github.com/fastapi-crud-async](https://github.com/testdrivenio/fastapi-crud-async)
