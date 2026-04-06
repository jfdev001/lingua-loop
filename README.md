# lingua-loop

> Train your listening skills by transcribing real speech from YouTube videos.

LinguaLoop is a single-page web application designed to improve language
listening skills through active transcription. It is based on a
transcription-first learning approach where users repeatedly listen to short
audio segments and attempt to write down what they've heard.

To run the web application on your computer, you need Python version 3.12
or higher installed. Then you can do the following (in a virtual environment
if you want) in a terminal:

```
pip install lingua-loop
```

You can launch the app, which will automatically open a web browser, by doing
the following in a terminal:

```
lingua-loop
```

Here's how you use the app:

1. Select the target language you want to study.
2. Copy and paste a YouTube video URL corresponding to that target language.
   Ideally, the video should have **official** transcripts since those will be
   used as the reference for scoring your transcription attempt.
3. Listen to short segments of the video (e.g., 10 seconds) and type what you
   hear. You may replay each segment as many times as needed.
4. Once you have made an honest attempt, you can submit your transcription
   attempt and will receive a score from 0 to 1. A score of 1 indicates a
   perfect transcription and a score of 0 indicates a complete mismatch.
5. Repeat as long as desired.

The scoring algorithm uses [Gestalt pattern
matching](https://en.wikipedia.org/wiki/Gestalt_pattern_matching), which
compares your input to the reference transcript by finding the longest common
subsequences of characters. For example, if you type

$$
\text{wikim}\textcolor{red}{an}\text{ia}
$$

but the official transcript has


$$
\text{wikim}\textcolor{red}{ed}\text{ia}
$$

you would receive a score of 0.70 because, despite the error, there are common
characters that you correctly typed.

# Future Work

Some possible extension ideas:

1. Integrate Anki-style flash cards for selected words. A word should be added
   to a flash card deck in addition to the context in which it occurred (e.g.,
   sentence or phrase). The user *should* write additional context to keep them
   actively engaged in the learning process.
2. Support more languages. Currently only Indo-European languages are
   supported, though support for languages such as Mandarin would be extremely
   valuable. For Mandarin, I think text normalization would require
   [pinyin](https://en.wikipedia.org/wiki/Pinyin).
3. More sophisticated scoring algorithms.
4. Integrate an AI chat bot that is given the full transcript as context and
   subsequently asks the user comprehension questions or engages in
   conversation about the video topic. Could be executed using local models
   or combined with API keys.

# Developers

The directory structure is inspired by a number of projects, so it is
intended to be as standard and intuitive as possible:

```
lingua-loop
├── data             # where transcripts.db is stored
├── src
│   └── lingua_loop
│       ├── api
│       │   └── routers
│       │       └── transcript.py
│       ├── constants.py
│       ├── db
│       │   ├── models.py
│       │   ├── session.py
│       │   └── transcript.py
│       ├── exceptions.py
│       ├── integrations
│       │   └── youtube
│       │       ├── types.py
│       │       └── wrapper.py
│       ├── main.py
│       ├── schemas
│       │   └── transcript.py
│       ├── scripts
│       │   └── run.py
│       ├── services
│       │   ├── text_normalization.py
│       │   └── transcript.py
│       ├── static
│       │   ├── app.js
│       │   └── style.css
│       └── templates
│           └── index.html
└── tests
    ├── boundary
    │   ├── conftest.py
    │   └── test_youtube_transcript_api.py
    ├── conftest.py
    ├── constants.py
    ├── integration
    │   └── test_integration.py
    └── unit
        ├── api
        │   └── test_api.py
        ├── db
        │   └── test_db.py
        └── services
            └── test_services.py
```

The fast package manger `uv` was used in the development of this project.
You can install `lingua-loop` in development mode by doing the following:

```shell
git clone git@github.com:jfdev001/lingua-loop.git
cd lingua-loop
uv sync
```

As a sanity check, you should verify the FastAPI backend tests pass:

```shell
pytest -v tests/
```

There are tests to verify the outputs of the `youtube_transcript_api`
dependency, however, these make requests to YouTube, and are therefore *not*
run by default. You can run those tests if you want by including the `--slow`
flag like:

```shell
pytest -v --slow tests/
```

You should also make sure that your files are formatted according to
the conventions defined in `.pre-commit-config.yaml`. To that end, use
the fast git hook runner framework [prek](https://github.com/j178/prek):

```
prek install
```

If you'd like to contribute, consider opening an issue first and/or addressing
one of the issues already available. AI contributions will **not** be accepted.
You should fork the project first before contributing. Pull requests should
come from branches with the following structure:

```
<name>/<issue-number-if-applicable>-<feature-description>
```

The frontend is vanilla JS/HTML/CSS, so using `npm` is not strictly necessary,
but if you'd like type hints for the Youtube iframe API, you can install
the frontend dependencies with:

```
npm install
```

# References

Below are a series of references, in no particular order, that I used to gain
the necessary background knowledge for the project:

[1] [Python FastAPI Tutorial (Part 1): Getting Started - Web App + REST
API](https://www.youtube.com/watch?v=7AMjmCTumuo)

[2] [Learn Fast API With This ONE
Project](https://www.youtube.com/watch?v=SR5NYCdzKkc)

[3] [Anatomy of a Scalable Python Project
(FastAPI)](https://www.youtube.com/watch?v=Af6Zr0tNNdE)

[4] [Developing and Testing an Asynchronous API with FastAPI and
Pytest](https://testdriven.io/blog/fastapi-crud/) &
[github.com/fastapi-crud-async](https://github.com/testdrivenio/fastapi-crud-async)

[5] [Netflix/dispatch](https://github.com/Netflix/dispatch)

[6] [polarsource/polar](https://github.com/polarsource/polar)

[7] [FastAPI: Modern Web Development (Lubanovic
2024)](https://www.oreilly.com/library/view/fastapi/9781098135492/)

[8] [ecmwf/forecast-in-a-box](https://github.com/ecmwf/forecast-in-a-box)

[9] [fastapi-docs: Testing
Dependencies](https://fastapi.tiangolo.com/advanced/testing-dependencies/)

[10] [Build Advanced Youtube Player UI --
Video](https://www.youtube.com/watch?v=lsu-g-_6i_A&list=PLzKme01IAXkLBmWBihSwIhLk8Qluli0Jl&index=2)
and [Build Advanced Youtube Player UI -- Source
Code](https://codepen.io/PixelPerfectLabs/pen/PwwrJge)
