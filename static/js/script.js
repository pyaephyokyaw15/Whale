function songPlayFunction() {
    let mainAudio = document.querySelector("#main-audio");
    let playPauseBtn = document.querySelector(".play-pause");
    let progressArea = document.querySelector(".song-progress-area");
    let progressBar = document.querySelector(".song-progress-bar");


    // play music function
    function playMusic() {
        playPauseBtn.classList.add("paused");
        playPauseBtn.querySelector("i").innerText = "pause";
        mainAudio.play();
    }


    //pause music function
    function pauseMusic() {
        playPauseBtn.classList.remove("paused");
        playPauseBtn.querySelector("i").innerText = "play_arrow";
        mainAudio.pause();
    }

    playPauseBtn.addEventListener("click", ()=>{

        const isMusicPlay = playPauseBtn.classList.contains("paused");
        console.log(isMusicPlay);

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

    // update playing song currentTime on according to the progress bar width(user press)
    progressArea.addEventListener("click", (e)=>{
        let progressWidth = progressArea.clientWidth; //getting width of progress bar
        let clickedOffsetX = e.offsetX; //getting offset x value
        let songDuration = mainAudio.duration; //getting song total duration

        console.log(clickedOffsetX);
        console.log(progressWidth);
        console.log(songDuration);

        mainAudio.currentTime = (clickedOffsetX / progressWidth) * songDuration;
        console.log(mainAudio.currentTime);
        playMusic();
        console.log(mainAudio.currentTime);
    });

}


document.addEventListener('DOMContentLoaded', function() {
    let songs = document.querySelectorAll(".song-wrapper");
    console.log(songs);

    songs.forEach((song) => {
        let favouriteBtn = song.querySelector(".fa-heart");
        favouriteBtn.addEventListener('click', (element) => favourite_action(song));
    });

});

document.addEventListener('DOMContentLoaded', function() {

        let profile_user = document.querySelector("#username").innerHTML;
        let followBtn = document.querySelector("#follow-button");
        let followingCounts = document.querySelector("#following_counts");
        let followerCounts = document.querySelector("#follower_counts");
        console.log(followBtn);


        followBtn.addEventListener('click', () => {
            fetch(`/account/user/${profile_user}`, {
                  method: 'PUT',
                  body: JSON.stringify({
                     "followingStatus": followBtn.innerHTML
                  })
            })
            .then(response => response.json())
            .then(data=>{
                followBtn.innerHTML = data["followingStatus"];
                followingCounts.innerHTML = data["following_counts"];
                followerCounts.innerHTML = data["follower_counts"];
            });
        });
});



function favourite_action(song) {


    let favouriteBtn = song.querySelector(".fa-heart");
    let song_id = song.dataset.id;
    console.log(song_id);

    fetch(`/songs/${song_id}/action/`, {
          method: 'PUT',
          body: JSON.stringify({
              favourite: 'toggle',
          })
    })
    .then(response => response.json());



    if (favouriteBtn.classList.contains("favourite")) {
        favouriteBtn.classList.remove("favourite");
    } else {
        favouriteBtn.classList.add("favourite");
    }

    if (window.location.toString().includes("favourites")) {
        song.remove();
    }

}


document.addEventListener('DOMContentLoaded', function() {
    songPlayFunction();



});
