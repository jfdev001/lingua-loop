//  TODO: debugging only

window.addEventListener("DOMContentLoaded", () => {
  let player,
    duration = 0,
    lastVolume = 80;
  let seekBar, volumeSlider;

  window.onYouTubeIframeAPIReady = function() {
    player = new YT.Player("player", {
      videoId: "2FrCsScQ1-g",
      playerVars: {
        controls: 0,
        modestbranding: 1,
        rel: 0,
        showinfo: 1,
        autoplay: 1,
        mute: 1
      },
      events: { onReady: onPlayerReady, onStateChange: onPlayerStateChange }
    });
  };

  const tag = document.createElement("script");
  tag.src = "https://www.youtube.com/iframe_api";
  document.head.appendChild(tag);

  function onPlayerReady() {
    try {
      player.setVolume(lastVolume);
    } catch (e) { }
    player.playVideo();
    duration = player.getDuration();
    document.getElementById("duration").textContent = formatTime(duration);

    seekBar = document.getElementById("seekBar");
    volumeSlider = document.getElementById("volumeSlider");
    volumeSlider.value = lastVolume;
    updateSliderFill(seekBar);
    updateSliderFill(volumeSlider);

    document
      .getElementById("playPauseBtn")
      .addEventListener("click", togglePlayPause);
    document
      .getElementById("overlayPlay")
      .addEventListener("click", togglePlayPause);
    document.getElementById("muteBtn").addEventListener("click", function() {
      toggleMute.call(this);
    });
    volumeSlider.addEventListener("input", handleVolume);
    seekBar.addEventListener("input", handleSeek);
    document
      .getElementById("playbackSpeed")
      .addEventListener("change", handleSpeedChange);
    document
      .getElementById("fullscreenBtn")
      .addEventListener("click", toggleFullscreen);

    document.addEventListener("keydown", (e) => {
      if (e.key === " ") {
        e.preventDefault();
        togglePlayPause();
      }
      if (e.key === "ArrowRight")
        player.seekTo(player.getCurrentTime() + 5, true);
      if (e.key === "ArrowLeft")
        player.seekTo(player.getCurrentTime() - 5, true);
      if (e.key === "m") toggleMute.call(document.getElementById("muteBtn"));
      if (e.key === "f") toggleFullscreen();
    });

    setInterval(updateProgress, 500);
  }

  function togglePlayPause() {
    const state = player.getPlayerState();
    const overlay = document.getElementById("overlayPlay");
    const btn = document.getElementById("playPauseBtn");
    if (state === YT.PlayerState.PLAYING) {
      player.pauseVideo();
      overlay.style.opacity = "1";
      btn.innerHTML = '<i class="fas fa-play"></i>';
    } else {
      player.playVideo();
      overlay.style.opacity = "0";
      btn.innerHTML = '<i class="fas fa-pause"></i>';
    }
  }

  function toggleMute() {
    const btn = this;
    try {
      if (player.isMuted()) {
        player.unMute();
        btn.innerHTML = '<i class="fas fa-volume-high"></i>';
        volumeSlider.value = lastVolume;
        player.setVolume(lastVolume);
      } else {
        lastVolume = volumeSlider.value;
        player.mute();
        btn.innerHTML = '<i class="fas fa-volume-xmark"></i>';
        volumeSlider.value = 0;
      }
    } catch (e) { }
    updateSliderFill(volumeSlider);
  }

  function handleVolume(e) {
    const v = parseInt(e.target.value);
    lastVolume = v;
    try {
      if (v === 0) {
        player.mute();
        document.getElementById("muteBtn").innerHTML =
          '<i class="fas fa-volume-xmark"></i>';
      } else {
        player.unMute();
        player.setVolume(v);
        document.getElementById("muteBtn").innerHTML =
          '<i class="fas fa-volume-high"></i>';
      }
    } catch (e) { }
    updateSliderFill(volumeSlider);
  }

  function handleSeek(e) {
    player.seekTo((e.target.value / 100) * duration, true);
    updateSliderFill(seekBar);
  }

  function handleSpeedChange(e) {
    player.setPlaybackRate(parseFloat(e.target.value));
  }

  function toggleFullscreen() {
    const elem = document.querySelector(".player-card");
    const btn = document.getElementById("fullscreenBtn");
    if (!document.fullscreenElement) {
      elem.requestFullscreen().then(() => {
        btn.innerHTML = '<i class="fas fa-compress"></i>';
      });
    } else {
      document.exitFullscreen().then(() => {
        btn.innerHTML = '<i class="fas fa-expand"></i>';
      });
    }
  }

  function updateProgress() {
    if (!player || !player.getCurrentTime) return;
    const current = player.getCurrentTime();
    document.getElementById("currentTime").textContent = formatTime(current);
    seekBar.value = (current / duration) * 100;
    updateSliderFill(seekBar);
  }

  function updateSliderFill(slider) {
    const pct = ((slider.value - slider.min) / (slider.max - slider.min)) * 100;
    slider.style.background = `linear-gradient(to right, #c8ff00 ${pct}%, rgba(240,237,230,0.12) ${pct}%)`;
  }

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

  function formatTime(s) {
    const m = Math.floor(s / 60);
    const ss = Math.floor(s % 60)
      .toString()
      .padStart(2, "0");
    return `${m}:${ss}`;
  }
});
