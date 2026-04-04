
/**
 * @typedef {{ code: string, label: string }} LanguageCodeToLabel
 */

/**
 * @typedef {{ languages: LanguageCodeToLabel[] }} Languages
 */

/** @type {Languages} */
const { languages } = window.APP_CONFIG;

/** @type {YT.Player} */
let player;

let seekBar;
let volumeSlider;

let videoId = null;
let segments = [];
let currentSegment = 0;

function loadVideo() {
  // TODO: Should update the videoContainer id with the videoId and embed
  // of what you need....
  // should GET load video
  console.log("load video");

}

function submitSegment() {
  // TODO: should GET transcripts (based on segment???)
  // TODO: should POST the score
  console.log("submit segment");
}
