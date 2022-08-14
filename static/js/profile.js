// follow-unfolow action without reloading the page
function followFunction() {
    let profile_user = document.querySelector("#username").innerHTML;
    let followBtn = document.querySelector("#follow-button");
    let followingCounts = document.querySelector("#following_counts");
    let followerCounts = document.querySelector("#follower_counts");
    // console.log(followBtn);

    const csrftoken = getCookie('csrftoken');
    const request = new Request(
        `/account/user/${profile_user}`,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    followBtn.addEventListener('click', () => {
        fetch(request, {
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
}


// change data accroding to tab selected on profile page(without reloading the page)
function infoTabFunction() {
    let uploadedSongs = document.querySelector("#uploaded-songs");
    let favouriteSongs = document.querySelector("#favourite-songs");
    // console.log(uploadedSongs);
    // console.log(favouriteSongs);

    let uploadedBtn = document.querySelector("#uploaded-btn");
    let favouriteBtn = document.querySelector("#favourite-btn");

    uploadedBtn.addEventListener('click', () => {
        favouriteSongs.style.display = "none";
        uploadedSongs.style.display = "table";

        uploadedBtn.classList.add("active");
        favouriteBtn.classList.remove("active");
    });

    favouriteBtn.addEventListener('click', () => {
        uploadedSongs.style.display = "none";
        favouriteSongs.style.display = "table";

        uploadedBtn.classList.remove("active");
        favouriteBtn.classList.add("active");
     });
}


document.addEventListener('DOMContentLoaded', function() {
    followFunction();
    infoTabFunction();
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