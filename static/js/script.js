// change your domain
let loginRedirect = `http://127.0.0.1:8000/account/login/?next=${window.location.toString()}`;

// Add event-listener to favourite icon
document.addEventListener('DOMContentLoaded', function() {
    let songs = document.querySelectorAll(".song-wrapper");
    // console.log(songs);

    songs.forEach((song) => {
        let favouriteBtn = song.querySelector(".fa-heart");
        favouriteBtn.addEventListener('click', (element) => favourite_action(song));
    });
});


// show acitve page on the navbar
document.addEventListener('DOMContentLoaded', function() {
    let navSongs = document.querySelector("#nav-songs");
    let navFavourite = document.querySelector("#nav-favourite");
    let navMoods = document.querySelector("#nav-moods");
    let navGenres = document.querySelector("#nav-genres");
    let navUpload = document.querySelector("#nav-upload");
    let navFollowing = document.querySelector("#nav-following");

    // console.log(navSongs);
    // console.log(navFavourite);
    // console.log(navMoods);
    // console.log(navGenres);
    // console.log(navFollowing);

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
        navFollowing.classList.remove("active")
    }
});



function favourite_action(song) {
    let favouriteBtn = song.querySelector(".fa-heart");
    let song_id = song.dataset.id;
    // console.log(song_id);

    const csrftoken = getCookie('csrftoken');
    const request = new Request(
        `/songs/${song_id}/action/`,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    // toggle favourite-unfavourite
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
            // console.log("Error");
            // if not login, redirect to login_page
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

            // if the current page is favourite songs page, remove the song on this page.
            if (window.location.toString().includes("favourite")) {
                song.remove();
            }
        }
    });
}


// password hide-unhide feature(login/register form)
document.addEventListener('DOMContentLoaded', function() {
    let togglePasswordBtn = document.querySelector("#togglePassword");
    let passwordField = document.querySelector("#id_password");
    // console.log(togglePassword);

    if (togglePasswordBtn) {
        togglePasswordBtn.addEventListener('click', (element) => {
            let inputType = passwordField.getAttribute("type")
            if (inputType == "password") {
                passwordField.setAttribute("type","text");
                togglePasswordBtn.classList.remove("fa-eye-slash");
                togglePasswordBtn.classList.add("fa-eye");
            } else {
                passwordField.setAttribute("type","password");
                togglePasswordBtn.classList.remove("fa-eye");
                togglePasswordBtn.classList.add("fa-eye-slash");
            }
        });
    }
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