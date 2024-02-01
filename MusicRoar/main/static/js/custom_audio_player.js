  var audioPlayer = document.getElementById("audio-player");
  var progress = document.getElementById("audio-progress");
  var progressValue = document.querySelector("#audio-progress .progress-value");
  var playButton = document.querySelector(".play-button");
  var timer = document.getElementById("audio-timer");

  function toggleAudio() {
    if (audioPlayer.paused) {
      audioPlayer.play();
      playButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" fill="currentColor" class="bi bi-pause-circle" viewBox="0 0 16 16"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/><path d="M6 11h2V5H6v6zm4 0h2V5h-2v6z"/></svg>';
    } else {
      audioPlayer.pause();
      playButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" fill="currentColor" class="bi bi-play-circle" viewBox="0 0 16 16"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/><path d="M6.271 5.055a.5.5 0 0 1 .52.038l3.5 2.5a.5.5 0 0 1 0 .814l-3.5 2.5A.5.5 0 0 1 6 10.5v-5a.5.5 0 0 1 .271-.445"/></svg>';
    }
  }

  function updateProgressBar() {
    var value = (audioPlayer.currentTime / audioPlayer.duration) * 100;
    progressValue.innerHTML = Math.round(value) + "%";
    progress.style.width = value + "%";
  }

  function seekAudio(event) {
    var percent = (event.offsetX / progress.clientWidth);
    audioPlayer.currentTime = percent * audioPlayer.duration;
  }

  audioPlayer.addEventListener("timeupdate", function () {
    var minutes = Math.floor(audioPlayer.currentTime / 60);
    var seconds = Math.floor(audioPlayer.currentTime % 60);
    timer.innerHTML = minutes + ":" + (seconds < 10 ? "0" : "") + seconds;
    updateProgressBar();
  });