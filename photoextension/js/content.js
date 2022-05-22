var SERVER_URL = "http://localhost:8080"

var last_url = "";
function onImageClick() {
    console.log("On image click")
    // TODO: change this hardcoded div listener.

    // get the image URL
    var img_url = $(this).attr("data-latest-bg");

    if (img_url === undefined || img_url === "") {
        showToast("Failed to capture the url")
        return
    }

    console.log(img_url)
    // to prevent multi "Image URL copied to clipboard!" when zooming the image
    if (last_url != img_url) {
        last_url = img_url;
        chrome.storage.sync.get(
            { img_width: 10000 },
            function (items) {

                var width = items.img_width;
                var urlParts = img_url.split("=");
                // force width with 1000px and add an extension
                img_url = urlParts[0] + "=w" + width + "-h" + width + "-no?authuser=1"

                // put the new URL in clipboard
                copyTextToClipboard(img_url);

                // show a "toast" stile message
                showToast("Image URL copied to clipboard!");
            });
    }
}

function onSimilarImagesButtonClick(e, imageDiv) {


    var similarImagesDiv = jQuery('<div>', {
        id: 'similarimages',
        class: 'sidebar',
        title: 'now this div has a title!'
    }).appendTo('body');
    similarImagesDiv.html('<a class="active" href="#home">Home</a> <a href="#news">News</a> <a href="#contact">Contact</a> <a href="#about">About</a>')

    // var href_attr = $(imageDiv).attr("href");
    // var img_url_parts = href_attr.split("/")
    // var img_id = img_url_parts[img_url_parts.length - 1]

    // fetch(SERVER_URL + "/similar_images/" + img_id, {
    //     method: "GET",
    //     mode: "no-cors",
    //     headers: {
    //         "Accept": "application/json",
    //         "Content-Type": "application/json"
    //     },
    //     agent: {
    //         rejectUnauthorized: false,
    //     }
    // })
    //     .then(r => {
    //         console.log(r)
    //         r.text()
    //     })
    //     .then(onSimilarImagesResult)

    // function onSimilarImagesResult(similarImages) {
    //     console.log("similar images " + similarImages + "<")

    //     if (similarImages === undefined || similarImages === "") {
    //         return
    //     } else {
    //         similarImages = JSON.parse(similarImages)
    //         console.log(similarImages)
    //     }
    // }
}

function addMenuButtonOnImage(imageDiv, divToAddButtonOn) {
    var buttonId = 'mybtn'

    var buttonDiv = divToAddButtonOn.querySelectorAll("#" + buttonId)
    if (buttonDiv.length > 0) {
        return
    }

    var button = document.createElement("button")
    button.innerText = "Similar Images";
    button.id = buttonId
    button.className = "similarImagesButton"
    // button.type = "submit"
    // button.innerHTML = "<img src=\"" + browser.runtime.getURL('img/similar_image_icon.jpg') + "\" />"

    button.addEventListener("click", (e) => onSimilarImagesButtonClick(e, imageDiv))

    divToAddButtonOn.prepend(button)
    // console.log(divToAddButtonOn)
    // console.log("added button to the image")
}

var isImageClickAdded = false;
var extensionInterval;

function updateExtensionOnInterval() {
    allDivsThatCanHaveImage = document.querySelectorAll('[style]')
    classNameOfPhotos = ""

    // console.log(allDivsThatCanHaveImage)
    for (index in allDivsThatCanHaveImage) {
        div = allDivsThatCanHaveImage[index]
        if (div.style === undefined
            || div.style.length < 2
            || div.style[1] !== "background-image") {
            continue
        }

        classNameOfPhotos = div.className;
        addMenuButtonOnImage(div.parentElement, div.parentElement.parentElement)
    }
    // console.log("ClassName of photos: " + classNameOfPhotos)
    if (classNameOfPhotos === "") {
        console.log("couldn't find the classname for image divs")
    } else if (isImageClickAdded === false) {
        console.log("Setting onClick event on the class: " + classNameOfPhotos)
        $("." + classNameOfPhotos).on('click', onImageClick)
        isImageClickAdded = true
        window.clearInterval(extensionInterval)
        extensionInterval = window.setInterval(updateExtensionOnInterval, 500)
    }
}

function copyTextToClipboard(text) {

    var textArea = document.createElement("textarea");

    textArea.id = "faketext"

    // Place in top-left corner of screen regardless of scroll position.
    textArea.style.position = 'fixed';

    textArea.style.top = 0;
    textArea.style.left = 0;

    // Ensure it has a small width and height. Setting to 1px / 1em
    // doesn't work as this gives a negative w/h on some browsers.
    textArea.style.width = '2em';
    textArea.style.height = '2em';

    // We don't need padding, reducing the size if it does flash render.
    textArea.style.padding = 0;

    // Clean up any borders.
    textArea.style.border = 'none';
    textArea.style.outline = 'none';
    textArea.style.boxShadow = 'none';

    // Avoid flash of white box if rendered for any reason.
    textArea.style.background = 'transparent';

    textArea.value = text;

    document.body.appendChild(textArea);

    textArea.select();

    try {
        var successful = document.execCommand('copy');
        console.log('Copy: ', successful);
    } catch (err) {
        console.log('Error exec command copy.');
    }

    document.body.removeChild(textArea);
}

function showToast(text) {

    if (!$("#toast").length) {
        var toast = document.createElement("div");
        toast.id = "toast";
        toast.className = "toast";
        toast.style = "display:none";

        var label = document.createElement("Label");
        label.innerHTML = text;

        toast.appendChild(label);

        document.body.appendChild(toast);
    }

    $('.toast').fadeIn(400).delay(2000).fadeOut(400);
}



function onDocumentReady() {
    console.log("Document is ready now")
    extensionInterval = window.setInterval(updateExtensionOnInterval, 100)
    // window.setTimeout(cancelInterval, 1000)
}

$(document).ready(onDocumentReady);