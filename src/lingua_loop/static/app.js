
const { language_to_language_code } = window.APP_CONFIG;

window.addEventListener("DOMContentLoaded", () => {
  const defaultBbcEnglishLearningVideoId = "Tefu_NvcC0k" // no affiliation
  const defaultLanguageCode = "en"
  const state = {
    /** @type {YT.Player */ player: null,
    videoId: defaultBbcEnglishLearningVideoId,
    segments: [],
    currentSegment: 0,
    isTranscribing: false,
    languageCode: defaultLanguageCode
  };

  // -------------------
  // Youtube player
  // https://developers.google.com/youtube/iframe_api_reference
  // -------------------
  window.onYouTubeIframeAPIReady = function() {
    state.player = new YT.Player('player', {
      height: '390',
      width: '640',
      videoId: state.videoId,
      playerVars: {
        'playsinline': 1,
        'autoplay': 0,
        'rel': 0,
      },
    });
  }

  const tag = document.createElement("script");
  tag.src = "https://www.youtube.com/iframe_api";
  document.head.appendChild(tag);

  // -------------------
  // Event Handlers
  // -------------------

  async function handleLoadVideo() {
    /** @type { HTMLInputElement } */
    const videoUrlEle = document.getElementById("videoUrl");
    const videoUrl = videoUrlEle.value;
    const videoId = extractVideoId(videoUrl);
    state.videoId = videoId;
    state.player.cueVideoById(videoId);
    // show loading
    // fetch transcript -- warn user if transcript.is_generated
  }

  function handleSnapToSegment() {
    // validate segment count
    // seek player (should use the seekTo based on the second mark..)
    // toggle transcription mode (free scrollable or not on player...)
  }

  async function handleScore() {
    // send user input to backend
    // update reference text
  }

  // -------------------
  // Utility functions
  // -------------------

  // References:
  // https://gist.github.com/takien/4077195
  // https://www.tutorialspoint.com/article/get-the-youtube-video-id-from-a-url-using-javascript
  function extractVideoId(url) {
    try {
      const parsedUrl = new URL(url);

      // youtu.be/VIDEO_ID
      if (parsedUrl.hostname === "youtu.be") {
        return parsedUrl.pathname.slice(1);
      }

      // youtube.com/watch?v=VIDEO_ID
      if (parsedUrl.searchParams.has("v")) {
        return parsedUrl.searchParams.get("v");
      }

      // youtube.com/embed/VIDEO_ID
      if (parsedUrl.pathname.startsWith("/embed/")) {
        return parsedUrl.pathname.split("/")[2];
      }

      return null;
    } catch (err) {
      return null; // invalid URL
    }
  }

  // -------------------
  // API Calls
  // -------------------

  async function getTranscript(videoId) {
    const res = await fetch("/transcript", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ video_id: videoId }),
    });

    return res.json();
  }

  async function scoreTranscript(payload) {
    const res = await fetch("/score", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    return res.json();
  }

  // -------------------
  // Wire up DOM
  // -------------------

  document
    .getElementById("loadVideoBtn")
    .addEventListener("click", handleLoadVideo);

  document
    .getElementById("startTranscriptionBtn")
    .addEventListener("click", handleSnapToSegment);
})
