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

    const csrftoken = getCookie('csrftoken');
    const request = new Request(
        `/songs/${song_id}/action/`,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    // toggle favourite-unfavourite
    favouriteBtn.addEventListener("click", () => {
        fetch(request, {
              method: 'PUT',
              body: JSON.stringify({
                  favourite: 'toggle',
              })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.status == "false") {
                console.log("Not login");
                // if not login, redirect to login-page
                window.open(loginRedirect, "_self")
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


function commentAction() {
    let comments = document.querySelectorAll(".comment");
    console.log(comments);

    const csrftoken = getCookie('csrftoken');


    comments.forEach((comment) => {
        let commentEditBtn = comment.querySelector(".comment-edit-button");
        let commentDeleteBtn = comment.querySelector(".comment-delete-button");
        let comment_id = comment.dataset.id;
        let commentTextBox = comment.querySelector(".comment-text-box")
        let commentUpdateBtn = comment.querySelector("#comment-update-btn")

        const request = new Request(
            `/songs/comments/${comment_id}/`,
            {headers: {'X-CSRFToken': csrftoken}}
        );

        // Delete Comment
        commentDeleteBtn.addEventListener('click', (element) => {
            // console.log("Delete Button!")


            fetch(request, {
                method: 'DELETE',
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
            comment.remove();
            })
        });

        // Edit Comment
        commentEditBtn.addEventListener('click', (element) => {
            console.log("Edit Button!")
            commentTextBox.setAttribute("contenteditable", "");
            commentTextBox.focus();
            commentEditBtn.style.display = 'none';
            commentDeleteBtn.style.display = 'none';
            commentUpdateBtn.style.display = 'block';

        });


        // Save the edited comment
        commentUpdateBtn.addEventListener('click', (element) => {
            console.log("Update Button!")

            fetch(request, {
                method: 'PUT',
                body: JSON.stringify({
                comment_text: commentTextBox.innerText
                })
            })
            .then(response => response.json())
            .then(data => {
            commentEditBtn.style.display = 'block';
            commentDeleteBtn.style.display = 'block';
            commentUpdateBtn.style.display = 'none';
            commentTextBox.removeAttribute("contenteditable");
            })
        });
    });
}



function commentCreateFunction() {
    let commentList = document.querySelector("#comment-list");
    let commentBtn = document.querySelector("#comment-btn");
    let commentBox = document.querySelector("#comment-box");
    // console.log(commentBtn);
    // console.log(commentBox.innerText);

    const csrftoken = getCookie('csrftoken');
    const request = new Request(
        `/songs/${song_id}/action/`,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    commentBtn.addEventListener('click', () => {
        fetch(request, {
              method: 'POST',
              body: JSON.stringify({
                  text: commentBox.innerHTML,
              })
        })
        .then(response => response.json())
        .then(result => {
            commentBox.innerHTML = '';
            // console.log("Success");
            // console.log(result);
            let comment = document.createElement("div");
            comment.classList.add("comment-box");
            comment.innerHTML = `
            <div class="comment" data-id=${result["id"]}>
                <div class="comment-box row align-items-center">
                    <div class="col col-1">
                        <img class="profile-thumbnail" src=${result["image"]} alt="image">
                    </div>
                    <div class="col col-11">
                        <a href=${result["profile_url"]} class="comment-author">${result["owner"]}</a>
                        <p class="comment-date"  style="margin-top: 0px;margin-bottom: 0px">${result["created_on"]}</p>
                    </div>
                </div>
                <div class="row align-items-center justify-content-end">
                      <div class="comment-text-box col col-11">
                          ${result["text"]}
                      </div>
                </div>
                <div class="row mt-2 comment-action">
                   <div class="col-auto ms-auto">
                       <button class="comment-edit-button">
                            <i class="fas fa-edit"></i>
                       </button>
                   </div>
                   <div class="col-auto">
                       <button class="comment-delete-button">
                            <i class="fa fa-trash"></i>
                       </button>
                   </div>
                    <div class="col-auto">
                       <button id="comment-update-btn" class="btn" type="button">Save</button>
                   </div>
                </div>
                <br>
            <div>
            `

            // append new comment on the top of other comments
            let index=0;
            commentList.appendChild(comment);
            if (index >= commentList.children.length) {
                commentList.appendChild(comment);
            } else {
                commentList.insertBefore(comment, commentList.children[index]);
            }

            // add blue-mark for authentic user
            if (result["is_authentic_owner"]) {
                let blueMark = document.createElement("i");
                blueMark.classList.add('fas', 'fa-check-circle', 'me-1');
                console.log("Blue Mark");
                commentAuthor = document.querySelector(".comment-author");
                commentAuthor.parentNode.insertBefore(blueMark, commentAuthor);
            }
        })
        .then(() => {
            // recall commentAction function to add event listener for new comment
            commentAction();
        })
    });
}

document.addEventListener('DOMContentLoaded', function() {
    songPlayFunction();
    favouriteFunction();
    commentCreateFunction();
    commentAction();
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}