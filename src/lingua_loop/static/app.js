// ----------
// API Types
// ----------

/**
 * @typedef {Object} Segment
 * @property {number} start
 * @property {number} duration
 * @property {string} text
 */

/**
 * @typedef {Object} TranscriptResponse
 * @property {string} video_id
 * @property {Segment[]} segments
 * @property {boolean} is_generated
 */

/**
  * @typedef {Object} ScoreRequest
  * @property {string} video_id
  * @property {number[]} segment_indices
  * @property {string} user_text
  * @property {string} language_code
  */

/**
 * @typedef {Object} ScoreResponse
 * @property {number} score
 * @property {string} reference_text
 */


const { language_to_language_code } = window.APP_CONFIG;

window.addEventListener("DOMContentLoaded", () => {
  const defaultBbcEnglishLearningVideoId = "Tefu_NvcC0k" // no affiliation
  const defaultLanguageCode = "en"
  const state = {
    /** @type {YT.Player} */ player: null,
    /** @type {TranscriptResponse} */ transcript: null,
    videoId: defaultBbcEnglishLearningVideoId,
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
        'cc_load_policy': 0
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
    if (!videoId) {
      alert("Invalid video URL");
      return;
    }
    state.videoId = videoId;

    // Update the player
    const curVideoId = extractVideoId(state.player.getVideoUrl());
    if (curVideoId != state.videoId) {
      state.player.cueVideoById(videoId);
    }

    // Load transcript
    /** @type {HTMLButtonElement}*/
    const loadVideoBtn = document.getElementById("loadVideoBtn");
    loadVideoBtn.disabled = true;
    const transcript = await getTranscript(state.videoId, state.languageCode);
    loadVideoBtn.disabled = false;

    // TODO: handle when bad transcript?? could be from no transcript found
    // due to language code
    let goodTranscript = true;
    state.transcript = transcript;

    if (goodTranscript) {
      videoUrlEle.value = ""; // TODO: rename this!
    }

    console.log(transcript); // TODO: debug
    return;
  }

  function handleSnapToSegment() {
    // validate segment count
    // seek player (should use the seekTo based on the second mark..)
    // toggle transcription mode (free scrollable or not on player...)
  }

  async function handleScore() {
    // send user input to backend
    /** @type {ScoreRequest} */
    let payload = null;
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

  /**
    * @returns {Promise<TranscriptResponse>}
    */
  async function getTranscript(videoId, languageCode) {
    const resp = await fetchTranscript(videoId, languageCode)
    return resp.json();
  }

  /**
    * @returns {Promise<Response>}
    */
  async function fetchTranscript(videoId, languageCode) {
    return await fetch(`/api/transcript/${videoId}/${languageCode}`);
  }


  /**
    * @param {ScoreRequest} payload
    * @returns {Promise<ScoreResponse>}
    */
  async function scoreTranscript(payload) {
    const resp = await fetchScoreTranscript(payload);
    return resp.json();
  }

  /**
    * @param {ScoreRequest} payload
    * @returns {Promise<Response>}
    */
  async function fetchScoreTranscript(payload) {
    const res = await fetch("/api/score", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    return res
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
