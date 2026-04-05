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


// ----------
// Youtube Types
// ----------

// https://developers.google.com/youtube/iframe_api_reference#onStateChange
/**
 * @typedef {(
 *   typeof YT.PlayerState.ENDED |
 *   typeof YT.PlayerState.PLAYING |
 *   typeof YT.PlayerState.PAUSED |
 *   typeof YT.PlayerState.BUFFERING |
 *   typeof YT.PlayerState.CUED
 * )} PlayerStateData
 */

// ----------
// Configuration
// ----------
const { language_to_language_code } = window.APP_CONFIG;


// ----------
// Application
// ----------
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
        'autoplay': 0,
        'rel': 0,
        'cc_load_policy': 0,
        'controls': 0,
      },
      events: { onReady: onPlayerReady, onStateChange: onPlayerStateChange }
    });
  }


  const tag = document.createElement("script");
  tag.src = "https://www.youtube.com/iframe_api";
  document.head.appendChild(tag);


  const videoConfiguration = {
    duration: 0,
    lastVolume: 80,
    /** @type {HTMLInputElement} */ seekBar: null,
    /** @type {HTMLInputElement} */ volumeSlider: null,
    skipIntervalInSeconds: 3     // TODO: could make modifiable
  }


  /**
    * @param {{ data: PlayerStateData }} event
    */
  function onPlayerStateChange(event) {
    const btn = document.getElementById("playPauseBtn");
    const overlay = document.getElementById("overlayPlay");
    if (event.data === YT.PlayerState.PLAYING) {
      btn.innerHTML = '<i class="fas fa-pause"></i>';
      overlay.style.opacity = "0";
    } else if (event.data === YT.PlayerState.PAUSED) {
      btn.innerHTML = '<i class="fas fa-play"></i>';
      overlay.style.opacity = "1";
    }
  }


  function onPlayerReady() {
    try {
      state.player.setVolume(videoConfiguration.lastVolume);
    } catch (e) { }
    state.player.unMute();

    videoConfiguration.duration = state.player.getDuration();
    document.getElementById("duration").textContent = formatTime(
      videoConfiguration.duration);

    videoConfiguration.seekBar = document.getElementById("seekBar");
    videoConfiguration.volumeSlider = document.getElementById("volumeSlider");
    videoConfiguration.volumeSlider.value = videoConfiguration.lastVolume;

    videoConfiguration.volumeSlider.addEventListener("input", handleVolume);
    videoConfiguration.seekBar.addEventListener("input", handleSeek);

    /** @type {HTMLInputElement} */
    const numSecondsOfVideoToTranscribe = document.getElementById(
      "numSecondsOfVideoToTranscribe")
    numSecondsOfVideoToTranscribe.max = videoConfiguration.duration

    updateSliderFill(videoConfiguration.seekBar);
    updateSliderFill(videoConfiguration.volumeSlider);
    setInterval(updateProgress, 500);
  }


  function handleSeek(e) {
    state.player.seekTo((e.target.value / 100) * videoConfiguration.duration, true);
    updateSliderFill(videoConfiguration.seekBar);
  }


  function updateSliderFill(slider) {
    const pct = ((slider.value - slider.min) / (slider.max - slider.min)) * 100;
    slider.style.background = `linear-gradient(to right, #c8ff00 ${pct}%, rgba(240,237,230,0.12) ${pct}%)`;
  }


  function handleVolume(e) {
    const v = parseInt(e.target.value);
    videoConfiguration.lastVolume = v;
    try {
      if (v === 0) {
        state.player.mute();
        document.getElementById("muteBtn").innerHTML =
          '<i class="fas fa-volume-xmark"></i>';
      } else {
        state.player.unMute();
        state.player.setVolume(v);
        document.getElementById("muteBtn").innerHTML =
          '<i class="fas fa-volume-high"></i>';
      }
    } catch (e) { }
    updateSliderFill(videoConfiguration.volumeSlider);
  }


  function toggleMute() {
    const btn = this;
    try {
      if (state.player.isMuted()) {
        state.player.unMute();
        btn.innerHTML = '<i class="fas fa-volume-high"></i>';
        videoConfiguration.volumeSlider.value = videoConfiguration.lastVolume;
        state.player.setVolume(videoConfiguration.lastVolume);
      } else {
        videoConfiguration.lastVolume = videoConfiguration.volumeSlider.value;
        state.player.mute();
        btn.innerHTML = '<i class="fas fa-volume-xmark"></i>';
        videoConfiguration.volumeSlider.value = 0;
      }
    } catch (e) { }
    updateSliderFill(videoConfiguration.volumeSlider);
  }


  function updateProgress() {
    if (!state.player || !state.player.getCurrentTime) return;
    const current = state.player.getCurrentTime();
    document.getElementById("currentTime").textContent = formatTime(current);
    // console.log(current)
    // console.log(videoConfiguration.duration)
    videoConfiguration.seekBar.value = (current / videoConfiguration.duration) * 100;
    updateSliderFill(videoConfiguration.seekBar);
  }


  function togglePlayPause() {
    const playerState = state.player.getPlayerState();
    const overlay = document.getElementById("overlayPlay");
    const btn = document.getElementById("playPauseBtn");
    if (playerState === YT.PlayerState.PLAYING) {
      state.player.pauseVideo();
      overlay.style.opacity = "1";
      btn.innerHTML = '<i class="fas fa-play"></i>';
    } else {
      state.player.playVideo();
      overlay.style.opacity = "0";
      btn.innerHTML = '<i class="fas fa-pause"></i>';
    }
  }


  function handleSpeedChange(e) {
    state.player.setPlaybackRate(parseFloat(e.target.value));
  }

  function handleSnapToSegment() {
    // validate segment count
    // seek player (should use the seekTo based on the second mark..)
    // toggle transcription mode (free scrollable or not on player...)
  }


  function formatTime(s) {
    const m = Math.floor(s / 60);
    const ss = Math.floor(s % 60)
      .toString()
      .padStart(2, "0");
    return `${m}:${ss}`;
  }

  // -------------------
  // Other Event Handlers
  // -------------------

  function handleLanguageToTranscribeUpdate() {
    const form = this;
    const selectedRadio = form.elements["language"];

    for (const radio of selectedRadio) {
      if (radio.checked) {
        console.log("Selected language code:", radio.value);
        state.languageCode = radio.value;
        console.log(state.languageCode);
        break;
      }
    }
    return;
  }

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

    console.log(transcript); // TODO: debug
    if (transcript) {
      videoUrlEle.value = ""; // TODO: rename this
    } else {
      alert(`
        No transcript found.
        Make sure the 'Language to Transcribe' matches the language in the video!
      `)
      return;
    }

    state.transcript = transcript;
    return;
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


  function replaceNonNumericInput() {
    const input = this;
    input.value = input.value.replace(/[^0-9]/g, "");
    return;
  }

  function constrainToMaxDuration() {
    const input = this;
    if (input.value > videoConfiguration.duration) {
      input.value = videoConfiguration.duration
    }
  }

  // -------------------
  // API Calls
  // -------------------

  /**
    * @returns {Promise<TranscriptResponse> | null}
    */
  async function getTranscript(videoId, languageCode) {
    const resp = await fetchTranscript(videoId, languageCode)
    const data = await resp.json();
    if (!resp.ok) {
      console.log(data);
      return null;
    }
    return data;
  }

  /**
    * @returns {Promise<Response>}
    */
  async function fetchTranscript(videoId, languageCode) {
    const resp = await fetch(`/api/transcript/${videoId}/${languageCode}`);
    return resp;
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

  // Youtube stuff

  document
    .getElementById("playPauseBtn")
    .addEventListener("click", togglePlayPause);

  document
    .getElementById("overlayPlay")
    .addEventListener("click", togglePlayPause);

  document
    .getElementById("muteBtn")
    .addEventListener("click", toggleMute);

  document
    .getElementById("playbackSpeed")
    .addEventListener("change", handleSpeedChange);

  document.addEventListener("keydown", (e) => {
    if (e.key === " ") {
      e.preventDefault();
      togglePlayPause();
    }
    if (e.key === "ArrowRight")
      state.player.seekTo(
        state.player.getCurrentTime() + videoConfiguration.skipIntervalInSeconds,
        true
      );
    if (e.key === "ArrowLeft")
      state.player.seekTo(
        state.player.getCurrentTime() - videoConfiguration.skipIntervalInSeconds,
        true
      );
    if (e.key === "m") toggleMute.call(document.getElementById("muteBtn"));
  });

  document
    .getElementById("numSecondsOfVideoToTranscribe")
    .addEventListener("input", replaceNonNumericInput)

  document
    .getElementById("numSecondsOfVideoToTranscribe")
    .addEventListener("input", constrainToMaxDuration)

  // API stuff

  document
    .getElementById("languageToTranscribeForm")
    .addEventListener("change", handleLanguageToTranscribeUpdate)

  document
    .getElementById("loadVideoBtn")
    .addEventListener("click", handleLoadVideo);

  document
    .getElementById("startTranscriptionBtn")
    .addEventListener("click", handleSnapToSegment);


})
