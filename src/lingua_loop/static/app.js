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
window.addEventListener("DOMContentLoaded", async () => {
  const defaultBbcEnglishLearningVideoId = "Tefu_NvcC0k" // no affiliation
  const defaultLanguageCode = "en"
  const state = {
    /** @type {YT.Player} */
    player: null,
    /** @type {TranscriptResponse} */
    transcript: await getTranscript(defaultBbcEnglishLearningVideoId, defaultLanguageCode),
    /** @type {number[]} */
    segmentIndices: [],
    videoId: defaultBbcEnglishLearningVideoId,
    isTranscribing: false,
    /** @type {number} */
    startTranscriptionTime: null,
    /** @type {number} */
    stopTranscriptionTime: null,
    languageCode: defaultLanguageCode
  };

  // -------------------
  // Youtube player
  // https://developers.google.com/youtube/iframe_api_reference
  // https://www.youtube.com/watch?v=lsu-g-_6i_A
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
    skipIntervalInSeconds: 3     // TODO: could make modifiable html ele
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
    return;
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

    // enable the snap to segment button now that the video is loaded
    document.getElementById("snapToSegmentBtn").disabled = false;

    // update sliders
    updateSliderFill(videoConfiguration.seekBar);
    updateSliderFill(videoConfiguration.volumeSlider);

    // Watch the progress bar and update it periodically with new value
    setInterval(updateProgress, 500);
    return;
  }


  function handleSeek(e) {
    state.player.seekTo((e.target.value / 100) * videoConfiguration.duration, true);
    updateSliderFill(videoConfiguration.seekBar);
    return;
  }


  function updateSliderFill(slider) {
    const pct = ((slider.value - slider.min) / (slider.max - slider.min)) * 100;
    slider.style.background = `linear-gradient(to right, #c8ff00 ${pct}%, rgba(240,237,230,0.12) ${pct}%)`;
    return;
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
    return;
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
    return;
  }


  function updateProgress() {
    if (!state.player || !state.player.getCurrentTime) return;
    let current = state.player.getCurrentTime();

    // Prevent time from exceeding bounds of desired segments while transcribing
    if (state.isTranscribing && current > state.stopTranscriptionTime) {
      state.player.seekTo(state.stopTranscriptionTime, true)
      state.player.pauseVideo();
      current = state.player.getCurrentTime();
    }

    if (state.isTranscribing && current < state.startTranscriptionTime) {
      state.player.seekTo(state.startTranscriptionTime, true)
      state.player.pauseVideo();
      current = state.player.getCurrentTime();
    }

    document.getElementById("currentTime").textContent = formatTime(current);
    videoConfiguration.seekBar.value = (current / videoConfiguration.duration) * 100;
    updateSliderFill(videoConfiguration.seekBar);
    return;
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
      if (state.isTranscribing) {
        state.player.seekTo(state.startTranscriptionTime, true);
      }
      state.player.playVideo();
      overlay.style.opacity = "0";
      btn.innerHTML = '<i class="fas fa-pause"></i>';
    }
    return;
  }


  function handleSpeedChange(e) {
    state.player.setPlaybackRate(parseFloat(e.target.value));
    return;
  }


  function handleSnapToSegment() {
    /** @type {HTMLButtonElement} */
    const snapToSegmentBtn = this;

    const numSecondsOfVideoToTranscribe = Number(
      document
        .getElementById("numSecondsOfVideoToTranscribe")
        .value
    );

    const segments = state.transcript.segments;
    const currentTimeInSeconds = state.player.getCurrentTime();
    const indexOfStartSegment = getIndexOfStartSegment(
      segments,
      currentTimeInSeconds
    );
    const startSegment = segments[indexOfStartSegment];

    state.player.seekTo(startSegment.start, true);
    state.player.pauseVideo();
    state.segmentIndices = getSegmentIndices(
      segments,
      indexOfStartSegment,
      numSecondsOfVideoToTranscribe
    );
    console.log(state.segmentIndices); // TODO: debug
    for (const segmentIndex of state.segmentIndices) {
      console.log(segments[segmentIndex]);
    }

    // Update the segment time span with the start and stop segments
    /** @type {HTMLSpanElement} */
    const segmentTimeSpan = document.getElementById("segmentTimeSpan");
    const stopSegment = segments[state.segmentIndices[state.segmentIndices.length - 1]];
    const startSegmentTime = formatTime(startSegment.start);
    const stopSegmentTime = formatTime(stopSegment.start + stopSegment.duration);
    segmentTimeSpan
      .innerHTML = `${startSegmentTime} to ${stopSegmentTime}`

    // enables transcription once you've got valid indices
    document.getElementById("toggleStartTranscriptionBtn").disabled = false
    return;
  }

  /**
    * @param {Segment[]} segments
    * @param {number} currentTimeInSeconds
    * @returns {number | null}
    */
  function getIndexOfStartSegment(segments, currentTimeInSeconds) {
    let indexOfStartSegment = segments.length - 1; // default to last segment
    let start;
    for (const [index, segment] of segments.entries()) {
      start = segment.start;
      if (start >= currentTimeInSeconds) {
        indexOfStartSegment = index == 0 ? index : index - 1;
        return indexOfStartSegment;
      }
    }
    return indexOfStartSegment;
  }


  /**
    * @param {Segment[]} segments
    * @param {number} indexOfStartSegment
    * @param {number} numSecondsOfVideoToTranscribe
    * @returns {number[]}
    */
  function getSegmentIndices(segments, indexOfStartSegment, numSecondsOfVideoToTranscribe) {
    let segmentIndices = [indexOfStartSegment];
    let segment = segments[indexOfStartSegment];
    let totalSegmentsDuration = segment.duration
    const numSegments = segments.length;
    let index = indexOfStartSegment + 1;
    while (index < numSegments) {
      segment = segments[index];
      totalSegmentsDuration += segment.duration
      // prevents overshooting the time the user wants to transcribe
      // (i.e., enforcing undershooting, e.g., 5 seconds desired, you would
      // get 4.72 seconds (undershot) instead of 8.72 secs (overshot)
      if (totalSegmentsDuration >= numSecondsOfVideoToTranscribe) {
        break;
      }
      segmentIndices.push(index);
      index += 1;
    }
    return segmentIndices;
  }


  function handleToggleStartTranscription() {
    /** @type {HTMLButtonElement} */
    const toggleStartTranscriptionBtn = this;

    /** @type {HTMLButtonElement} */
    const snapToSegmentBtn = document.getElementById("snapToSegmentBtn");

    /** @type {HTMLButtonElement} */
    const scoreBtn = document.getElementById("scoreBtn");

    /** @type {HTMLInputElement} */
    const numSecondsOfVideoToTranscribe = document
      .getElementById("numSecondsOfVideoToTranscribe");

    /** @type {HTMLTextAreaElement} */
    const userTextArea = document.getElementById("userTextArea");

    const segments = state.transcript.segments;
    const segmentIndices = state.segmentIndices;
    if (state.isTranscribing) { // toggle off
      toggleStartTranscriptionBtn.innerHTML = "Start Transcribing"

      // enable elements
      snapToSegmentBtn.disabled = false;

      // disable user input
      userTextArea.disabled = true;
      scoreBtn.disabled = true;

      state.isTranscribing = false;

      state.player.pauseVideo();
    } else { // toggle on
      toggleStartTranscriptionBtn.innerHTML = "Stop Transcribing";

      // disable buttons
      snapToSegmentBtn.disabled = true;

      // enable user input
      scoreBtn.disabled = false;
      userTextArea.disabled = false;

      state.isTranscribing = true;

      // update the transcription times to limit whre the user can seek
      // and skip
      const firstSegment = segments[segmentIndices[0]]
      state.startTranscriptionTime = firstSegment.start;

      const lastSegment = segments[segmentIndices[segmentIndices.length - 1]]
      state.stopTranscriptionTime = lastSegment.start + lastSegment.duration;

      // Jump to the beginning of segment
      state.player.seekTo(firstSegment.start, true);
      state.player.playVideo();
    }
    return;
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
        state.languageCode = radio.value;
        break;
      }
    }
    return;
  }

  async function handleLoadVideo() {
    /** @type { HTMLInputElement } */
    const videoUrlInput = document.getElementById("videoUrlInput");
    const videoUrl = videoUrlInput.value;
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

    if (transcript == null) {
      alert("No transcript found. Make sure the 'Language to Transcribe' matches the language in the video!")
      return;
    }

    // warn against unofficial transcripts
    if (transcript.is_generated) {
      alert("Transcript was automatically generated. Beware scoring may be unreliable!")
    }

    // Reset state
    videoUrlInput.value = "";
    document.getElementById("snapToSegmentBtn").disabled = false;
    document.getElementById("segmentTimeSpan").innerHTML = "";

    document.getElementById("toggleStartTranscriptionBtn").disabled = true;

    document.getElementById("userTextArea").value = ""
    document.getElementById("userTextArea").disabled = true;

    document.getElementById("referenceTextArea").readOnly = false;
    document.getElementById("referenceTextArea").value = "";
    document.getElementById("referenceTextArea").readOnly = true;

    state.isTranscribing = false;

    // update transcript
    state.transcript = transcript;
    return;
  }

  async function handleScore() {
    // make payload
    /** @type {ScoreRequest} */
    let payload = {};

    /** @type {HTMLTextAreaElement} */
    const userTextArea = document.getElementById("userTextArea");
    payload.user_text = userTextArea.value;
    payload.segment_indices = state.segmentIndices;
    payload.video_id = state.videoId;
    payload.language_code = state.languageCode;

    // compute score
    const scoreResponse = await scoreTranscript(payload);
    if (scoreResponse == null) {
      alert("Something went wrong when scoring... no score computed.")
      return;
    }

    const score = Number(scoreResponse.score).toPrecision(2);

    // TODO: this just puts the score into the reference text area for now...
    /** @type {HTMLTextAreaElement} */
    const referenceTextArea = document.getElementById("referenceTextArea");
    referenceTextArea.readOnly = false;
    const referenceText = sanitize(scoreResponse.reference_text);
    referenceTextArea.value = `Your score is ${score}/1.0! The reference text is:\n${referenceText}
    `
    referenceTextArea.readOnly = true;
    return;
  }

  // -------------------
  // Utility functions
  // -------------------

  /**
    * @param {string} text
    * @returns {string}
    */
  function sanitize(text) {
    let sanitizedText = text
      .replace(/\r?\n/g, " ")
      .replace(/\s+/g, " ");
    return sanitizedText;
  }

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

  function constrainMaximumNumSecondsToTranscribe() {
    /** @type {HTMLInputElement} */
    const input = this;
    if (Number(input.value) > videoConfiguration.duration) {
      input.value = String(videoConfiguration.duration)
    }
  }


  function constrainMinimumNumSecondsToTranscribe() {
    /** @type {HTMLInputElement} */
    const input = this;
    if (Number(input.value) < Number(input.min)) {
      input.value = input.min
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
    * @returns {Promise<ScoreResponse> | null}
    */
  async function scoreTranscript(payload) {
    const resp = await fetchScoreTranscript(payload);
    const data = await resp.json();
    if (!resp.ok) {
      console.log(data)
      return null;
    }
    return data;
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

  // Youtube player stuff

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
    let nextTime = null;
    if (e.key === "ArrowRight") {
      nextTime = state.player.getCurrentTime() + videoConfiguration.skipIntervalInSeconds

      if (state.isTranscribing && nextTime > state.stopTranscriptionTime) {
        nextTime = state.stopTranscriptionTime;
      }

      state.player.seekTo(nextTime, true);
    }

    if (e.key === "ArrowLeft") {
      nextTime = state.player.getCurrentTime() - videoConfiguration.skipIntervalInSeconds

      if (state.isTranscribing && nextTime < state.startTranscriptionTime) {
        nextTime = state.startTranscriptionTime;
      }

      state.player.seekTo(nextTime, true);
    }
  });

  document
    .getElementById("numSecondsOfVideoToTranscribe")
    .addEventListener("input", replaceNonNumericInput)

  document
    .getElementById("numSecondsOfVideoToTranscribe")
    .addEventListener("input", constrainMaximumNumSecondsToTranscribe)

  document
    .getElementById("numSecondsOfVideoToTranscribe")
    .addEventListener("mouseleave", constrainMinimumNumSecondsToTranscribe)

  // All other event wiring

  document
    .getElementById("languageToTranscribeForm")
    .addEventListener("change", handleLanguageToTranscribeUpdate)

  document
    .getElementById("loadVideoBtn")
    .addEventListener("click", handleLoadVideo);

  document
    .getElementById("snapToSegmentBtn")
    .addEventListener("click", handleSnapToSegment);

  document
    .getElementById("toggleStartTranscriptionBtn")
    .addEventListener("click", handleToggleStartTranscription)

  document
    .getElementById("scoreBtn")
    .addEventListener("click", handleScore)


  // Disable elements until ready to transcribe
  document.getElementById("toggleStartTranscriptionBtn").disabled = true;
  document.getElementById("scoreBtn").disabled = true;
  document.getElementById("userTextArea").disabled = true;

  // disable snap to segment until player is loaded
  document.getElementById("snapToSegmentBtn").disabled = true;
})
