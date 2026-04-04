
/**
 * @typedef {{ code: string, label: string }} LanguageCodeToLabel
 */

/**
 * @typedef {{ languages: LanguageCodeToLabel[] }} Languages
 */

/** @type {Languages} */
const { languages } = window.APP_CONFIG;

window.addEventListener("DOMContentLoaded", () => {
  const state = {
    /** @type {YT.Player */ player: null,
    videoId: null,
    segments: [],
    currentSegment: 0,
    isTranscribing: false,
  };

  let seekBar;
  let volumeSlider;

  // -------------------
  // Event Handlers
  // -------------------

  async function handleLoadVideo() {
    // show loading
    // fetch transcript -- warn user if transcript.is_generated
    // initialize player if needed
  }

  function handleSnapToSegment() {
    // validate segment count
    // seek player
    // toggle transcription mode (free scrollable or not on player...)
  }

  async function handleScore() {
    // send user input to backend
    // update reference text
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
