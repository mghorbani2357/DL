window.addEventListener('pywebviewready', function () {
    // let container = document.getElementById('webview-status')
    // container.innerHTML = '<i>pywebview</i> is ready';
    // initialize()
})

function showResponse(response) {
    let container = document.getElementById('response-container')
    container.innerText = response.message
    container.style.display = 'block'
}

function initialize() {
    pywebview.api.init().then(showResponse)
}

$(function () {
    $("#aside ul li > a").click(function () {
        let self = $(this);
        let li = self.parent();
        if (li.find(">ul").length > 0) {
            let slideDuration = 500;
            if (li.hasClass('open')) {
                li.find('>ul').stop().slideUp(slideDuration);
                li.removeClass('open');
            } else {
                let opens = $("#aside li.open");
                opens.find('>ul').stop().slideUp(slideDuration);
                opens.removeClass('open');
                li.find(">ul").stop().slideToggle(slideDuration);
                li.toggleClass('open');
            }
        }
    })
    $("#aside > ul > li:not(.label):first > a:first").click();
});

// initialize()