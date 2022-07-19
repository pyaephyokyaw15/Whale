let song_id = document.querySelector(".song-detail-wrapper").dataset.id;

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


function favouriteFunction() {

    let favouriteBtn = document.querySelector(".fa-heart");

    favouriteBtn.addEventListener("click", () => {

        fetch(`/songs/${song_id}/action/`, {
              method: 'PUT',
              body: JSON.stringify({
                  favourite: 'toggle',
              })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.status == "false") {
                console.log("Error");
                window.open(`http://127.0.0.1:5001/account/login/?next=${window.location.toString()}`,"_self")
            }

            else {
                if (favouriteBtn.classList.contains("favourite")) {
                    favouriteBtn.classList.remove("favourite");
                    favouriteBtn.classList.add("unfavourite");
                } else {
                    favouriteBtn.classList.add("favourite");
                    favouriteBtn.classList.remove("unfavourite");
                }


            }

        });
    });
}




function commentFunction() {
    let commentList = document.querySelector("#comment-list");
    let commentBtn = document.querySelector("#comment-btn");
    let commentBox = document.querySelector(".textarea");
    console.log(commentBtn);

    commentBtn.addEventListener('click', () => {
        console.log("Clicked");




        fetch(`/songs/${song_id}/action/`, {
              method: 'POST',
              body: JSON.stringify({
                  text: commentBox.value,
              })
        })
        .then(response => response.json())
        .then(result => {
            commentBox.value = '';
            console.log("Success");
            console.log(result);
            let comment = document.createElement("div");
            comment.classList.add("comment-box");
            comment.innerHTML = `
                <div class="comment-box row align-items-center">
                    <div class="col col-1">
                        <img class="profile-thumbnail" src=${result["image"]} alt="image">
                    </div>
                    <div class="col col-11">
                        <a href=${result["profile_link"]} class="comment-author">${result["owner"]}</a>
                        <p class="comment-date">${result["created_on"]}</p>
                    </div>
                </div>
                <div class="row align-items-center justify-content-end">
                      <div class="comment-text-box col col-11">
                          ${result["text"]}
                      </div>
                </div>
                <br>
            `

            let index=0;
            commentList.appendChild(comment);
            if (index >= commentList.children.length) {
                commentList.appendChild(comment);
            } else {
                commentList.insertBefore(comment, commentList.children[index]);
            }

        });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    songPlayFunction();
    favouriteFunction();
    commentFunction();

});

