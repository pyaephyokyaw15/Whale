mainAudio = document.querySelector("#main-audio");
playPauseBtn = document.querySelector(".play-pause");
progressArea = document.querySelector(".progress-area");
progressBar = document.querySelector(".progress-bar");


function playMusic(){
    playPauseBtn.classList.add("paused");
    playPauseBtn.querySelector("i").innerText = "pause";
    mainAudio.play();
}

playMusic();
  
  //pause music function
function pauseMusic(){
    playPauseBtn.classList.remove("paused");
    playPauseBtn.querySelector("i").innerText = "play_arrow";
    mainAudio.pause();
}


playPauseBtn.addEventListener("click", ()=>{

    const isMusicPlay = playPauseBtn.classList.contains("paused");
    //if isPlayMusic is true then call pauseMusic else call playMusic
    isMusicPlay ? pauseMusic() : playMusic();
    
  });



// update progress bar width according to music current time
mainAudio.addEventListener("timeupdate", (e)=>{
  const currentTime = e.target.currentTime; //getting playing song currentTime
  const duration = e.target.duration; //getting playing song total duration
  let progressWidth = (currentTime / duration) * 100;
  progressBar.style.width = `${progressWidth}%`;


  let musicCurrentTime = document.querySelector(".current-time"),
  musicDuartion = document.querySelector(".max-duration");
 
    // update song total duration
  let mainAdDuration = mainAudio.duration;
    
  let totalMin = Math.floor(mainAdDuration / 60);
  let totalSec = Math.floor(mainAdDuration % 60);
  if(totalSec < 10){ //if sec is less than 10 then add 0 before it
    totalSec = `0${totalSec}`;
  }
  musicDuartion.innerText = `${totalMin}:${totalSec}`;
 
  // update playing song current time
  let currentMin = Math.floor(currentTime / 60);
  let currentSec = Math.floor(currentTime % 60);
  if(currentSec < 10){ //if sec is less than 10 then add 0 before it
    currentSec = `0${currentSec}`;
  }
  musicCurrentTime.innerText = `${currentMin}:${currentSec}`;
});

// update playing song currentTime on according to the progress bar width
progressArea.addEventListener("click", (e)=>{
  let progressWidth = progressArea.clientWidth; //getting width of progress bar
  let clickedOffsetX = e.offsetX; //getting offset x value
  let songDuration = mainAudio.duration; //getting song total duration
  

  console.log(clickedOffsetX);
  console.log(progressWidth);
  console.log(songDuration);
  mainAudio.currentTime = (clickedOffsetX / progressWidth) * songDuration;
  playMusic(); 
  console.log(mainAudio.currentTime);
  //calling playMusic function
  
});





