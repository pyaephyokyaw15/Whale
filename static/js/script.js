document.addEventListener('DOMContentLoaded', function() {
    let songs = document.querySelectorAll(".song-wrapper");
    console.log(songs);

    songs.forEach((song) => {
        let favouriteBtn = song.querySelector(".fa-heart");
        favouriteBtn.addEventListener('click', (element) => favourite_action(song));
    });

});

document.addEventListener('DOMContentLoaded', function() {
    let navSongs = document.querySelector("#nav-songs");
    let navFavourite = document.querySelector("#nav-favourite");
    let navMoods = document.querySelector("#nav-moods");
    let navGenres = document.querySelector("#nav-genres");
    let navUpload = document.querySelector("#nav-upload");
    let navFollowing = document.querySelector("#nav-following");

    console.log(navSongs);
    console.log(navFavourite);
    console.log(navMoods);
    console.log(navGenres);
    console.log(navFollowing);

    if (window.location.toString().includes("favourite")) {
        navSongs.classList.remove("active");
        navFavourite.classList.add("active");
        navMoods.classList.remove("active");
        navGenres.classList.remove("active");
        navUpload.classList.remove("active");
        navFollowing.classList.remove("active");
    }

    else if (window.location.toString().includes("following")) {
        navSongs.classList.remove("active");
        navFavourite.classList.remove("active");
        navMoods.classList.remove("active");
        navGenres.classList.remove("active");
        navUpload.classList.remove("active");
        navFollowing.classList.add("active");
    }

     else if (window.location.toString().includes("mood")) {
        navSongs.classList.remove("active");
        navFavourite.classList.remove("active");
        navMoods.classList.add("active");
        navGenres.classList.remove("active");
        navUpload.classList.remove("active");
        navFollowing.classList.remove("active");
    }

    else if (window.location.toString().includes("genre")) {
        navSongs.classList.remove("active");
        navFavourite.classList.remove("active");
        navMoods.classList.remove("active");
        navGenres.classList.add("active");
        navUpload.classList.remove("active");
        navFollowing.classList.remove("active");
    }

    else if (window.location.toString().includes("upload")) {
        navSongs.classList.remove("active");
        navFavourite.classList.remove("active");
        navMoods.classList.remove("active");
        navGenres.classList.remove("active");
        navUpload.classList.add("active");
        navFollowing.classList.remove("active");
    }

    else {
        navSongs.classList.add("active");
        navFavourite.classList.remove("active");
        navMoods.classList.remove("active");
        navGenres.classList.remove("active");
        navUpload.classList.remove("active");
        navFollowing.classList.remove("active");

    }

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
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.status == "false") {
            console.log("Error");
            window.open(`http://127.0.0.1:8000/account/login/?next=${window.location.toString()}`,"_self")
        }

        else {
            if (favouriteBtn.classList.contains("favourite")) {
                favouriteBtn.classList.remove("favourite");
                favouriteBtn.classList.add("unfavourite");
            } else {
                favouriteBtn.classList.add("favourite");
                favouriteBtn.classList.remove("unfavourite");
            }

            if (window.location.toString().includes("favourite")) {
                song.remove();
            }
        }

    });





}








