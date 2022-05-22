SERVER_URL = "https://localhost:8080/"

function getCookies(domain, name, callback) {
    chrome.cookies.get({ "url": domain, "name": name }, function (cookie) {
        if (callback) {
            console.log(name);
            console.log(cookie);

            if (cookie === null) {
                return;
            }
            callback(cookie.value);
        }
    });
}

function onAlbumShow() {
    console.log("Clicked on show album")

    getCookies(SERVER_URL, "session", function (cookieValue) {
        console.log(cookieValue);
    });

    fetch(SERVER_URL + 'photo_albums/view/me', {
        method: "GET",
        mode: "no-cors",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        agent: {
            rejectUnauthorized: false,
        }
    })
        .then(r => r.text()).then(result => {
            console.log(result)
        })
}

function loadLoggedInUser() {
    fetch(SERVER_URL + 'user_auth', {
        method: "GET",
        mode: "no-cors",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        agent: {
            rejectUnauthorized: false,
        }
    })
        .then(r => r.text())
        .then(onUserApiResult)

    function onUserApiResult(user) {
        console.log("user>" + user + "<")
    
        if (user === "") {
            handleUserNotLoggedIn()
        } else {
            user = JSON.parse(user)
            handleUserLoggedIn(user)
        }
    }

    function handleUserLoggedIn(user) {
        user_id = user["id"]
        user_name = user["name"]
        user_pic = user["picture"]
        user_verified = user["verified_email"]

        $("#user_picture").attr("src", user_pic);
        $("#user_name").text(user_name);

        $("#wait").css('display', 'none');
        $("#loggin_prompt").css('display', 'none');
        $("#logged_user").css('display', 'block');
    }

    function handleUserNotLoggedIn() {
        $("#wait").css('display', 'none');
        $("#loggin_prompt").css('display', 'block');
        $("#logged_user").css('display', 'none');
    }
}

function logoutUser() {
    fetch(SERVER_URL + 'user_auth/logout', {
        method: "GET",
        mode: "no-cors",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        agent: {
            rejectUnauthorized: false,
        }
    })
        .then(r => r.json())
        .then(onLogoutApiResult)

    function onLogoutApiResult(user) {
        if (user === null || user["id"] === null) {
            return
        }
        handleUserLogout()
    }

    function handleUserLogout() {
        $("#user_picture").attr("src", "");
        $("#user_name").text("");

        $("#wait").css('display', 'none');
        $("#loggin_prompt").css('display', 'block');
        $("#logged_user").css('display', 'none');
    }
}

function loginWithGoogle() {
    window.open(SERVER_URL + 'user_auth', '_blank');
}

$(document).ready(function () {
    loadLoggedInUser()

    $('#google_login').click(loginWithGoogle);

    $('#logout').click(logoutUser);
});
