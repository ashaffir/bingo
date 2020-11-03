$(document).ready(function () {
    let imagesLoaded = 0;
    // Total images is still the total number of <img> elements on the page.
    let totalImages = $('img').length;

    $('img').each(function (idx, img) {
        $('<img>').on('load', imageLoaded).attr('src', $(img).attr('src'));
    });

    function imageLoaded() {
        imagesLoaded++;
        if (imagesLoaded == totalImages) {
            allImagesLoaded();
        }
    }

    function allImagesLoaded() {
        resize();
        getData();
    }
});



function changeScenes() {
    document.querySelectorAll('#prize').forEach(el => {
        el.style.opacity = '1';
    });
    document.querySelectorAll('#winCondition').forEach(el => {
        el.style.opacity = '0';
    });

    setTimeout(() => {
        document.querySelectorAll('#prize').forEach(el => {
            el.style.opacity = '0';
        });
        document.querySelectorAll('#winCondition').forEach(el => {
            el.style.opacity = '1';
        });
    }, 3000);
}

let switcher = setInterval(() => {
    changeScenes();
}, 6000);