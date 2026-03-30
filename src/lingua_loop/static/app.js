// TODO:
const appState = {
    videoId: null,
    segments: [],
    currentSegment: 0
};

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

/*
 let player; // YouTube player instance
const state = {
    videoId: null,
    segments: [],
    currentSegment: 0
};

// -------------------- Extract video ID --------------------
function extractVideoId(url) {
    try {
        const urlObj = new URL(url);
        if (urlObj.hostname.includes("youtube.com")) return urlObj.searchParams.get("v");
        if (urlObj.hostname === "youtu.be") return urlObj.pathname.slice(1);
        if (urlObj.pathname.startsWith("/embed/")) return urlObj.pathname.split("/")[2];
    } catch (err) { console.error("Invalid URL", err); }
    return null;
}

// -------------------- YouTube API setup --------------------
function onYouTubeIframeAPIReady() {
    player = new YT.Player('video-player', {
        height: '360',
        width: '640',
        videoId: '',
        playerVars: { 'controls': 1 }
    });
}

// -------------------- Load Video --------------------
async function loadVideo() {
    const url = document.getElementById("video-url").value;
    const videoId = extractVideoId(url);
    if (!videoId) { alert("Invalid URL"); return; }

    const res = await fetch(`/api/video/load/${videoId}`);
    const data = await res.json();

    state.videoId = data.video_id;
    state.segments = data.segments;
    state.currentSegment = 0;
    document.getElementById("video-title").innerText = data.title;

    // load video in iframe
    if (player.loadVideoById) {
        player.loadVideoById(videoId);
    } else {
        player = new YT.Player('video-player', {
            height: '360',
            width: '640',
            videoId: videoId
        });
    }

    renderSegmentButtons(data.segments);
}

// -------------------- Render Segment Buttons --------------------
function renderSegmentButtons(segments) {
    const container = document.getElementById("segments");
    container.innerHTML = "";
    segments.forEach((seg, i) => {
        const btn = document.createElement("button");
        btn.innerText = `Segment ${i+1}: ${seg.text.slice(0,30)}...`;
        btn.onclick = () => {
            state.currentSegment = i;
            setVideoTime(seg.start);
        };
        container.appendChild(btn);
    });
}

// -------------------- Jump to segment --------------------
function setVideoTime(time) {
    if (player && player.seekTo) {
        player.seekTo(time, true); // second arg = allowSeekAhead
        player.playVideo();
    }
}

// -------------------- Submit Segment --------------------
async function submitSegment() {
    const seg = state.segments[state.currentSegment];
    const userText = document.getElementById("transcription-input").value;

    const res = await fetch("/api/score", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            video_id: state.videoId,
            segment_id: seg.id,
            user_text: userText
        })
    });

    const data = await res.json();
    document.getElementById("score-output").innerText =
        `Score: ${data.score.toFixed(2)} | Expected: ${data.expected_text}`;

    state.currentSegment += 1;
    if (state.currentSegment < state.segments.length) {
        setVideoTime(state.segments[state.currentSegment].start);
    }
}
 * */
