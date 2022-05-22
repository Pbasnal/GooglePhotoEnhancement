SERVER_URL = "https://localhost:8080/"

function reloadAlbumsFromGoogle() {
    console.log("ReloadImages from google")
    fetch(SERVER_URL + 'photo_albums/reload', {
        method: "GET",
        mode: "no-cors",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        agent: {
            rejectUnauthorized: false,
        }
    }).then(r => r.text())
        .then(onAlbumReloaded)

    function onAlbumReloaded(albumReloadResponse) { 
        console.log(albumReloadResponse)
    }
}

function refreshSimilarImageAlbums() {
    fetch(SERVER_URL + 'similar_images/start', {
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
}

function getSimilarImageStats() {
    fetch(SERVER_URL + 'similar_images/stats', {
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
        .then(onSimilarImageStatsResult)

    function onSimilarImageStatsResult(similarImageStats) {
        console.log("similar image stats>" + similarImageStats + "<")

        if (similarImageStats === "") {
            return
        } else {
            similarImageStats = JSON.parse(similarImageStats)
            handleSimilarImageStats(similarImageStats)
        }
    }

    function handleSimilarImageStats(similarImageStats) {
        text = "Albums " + similarImageStats["count_of_albums_which_have_process_attached"]
            + "/" + similarImageStats["count_of_albums"]
        $("#album_stats").text(text)
        $("#similar_image_refresh").click(refreshSimilarImageAlbums);
        $("#load_from_google").click(reloadAlbumsFromGoogle);
    }
}


$(document).ready(function () {
    getSimilarImageStats()
});