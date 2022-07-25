function followFunction() {

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

}

function infoTabFunction() {

    let uploadedSongs = document.querySelector("#uploaded-songs");
    let favouriteSongs = document.querySelector("#favourite-songs");

    console.log(uploadedSongs);
    console.log(favouriteSongs);

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
});



document.addEventListener('DOMContentLoaded', function() {
    infoTabFunction();
});