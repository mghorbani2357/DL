window.addEventListener('pywebviewready', function () {
    // let container = document.getElementById('webview-status')
    // container.innerHTML = '<i>pywebview</i> is ready';
    // initialize()
})
/*

function showResponse(response) {
    let container = document.getElementById('response-container')
    container.innerText = response.message
    container.style.display = 'block'
}

function initialize() {
    pywebview.api.init().then(showResponse)
}
*/

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
    $(document).on('click', ".close-modal", function () {
        $(this).closest('.modal').hide();
    })
    $("#new-btn").click(function () {
        /*pywebview.api.new_download()*/
        $("#addNewDownloadModal").show();
    })
    $("#start-new-download").click(function () {
        /*pywebview.api.new_download()*/
        let url = $("#url").val();
        let name = url.split('/').pop();
        pywebview.api.new_download(url, name).then(function (response) {
            let template = `
                        <tr>
                    <td>
                        <label>
                            <input type="checkbox">
                            <span></span>
                        </label>
                    </td>
                    <td>
                        <img src="assets/svg/files/mp3.svg" alt="mp3">
                    </td>
                    <td>{name}</td>
                    <td class="progress-col">
                        <span class="progress">0%</span>
                        <span class="remaining">0</span>
                        <div class="progress-bar">
                            <div style="width: 0%"></div>
                        </div>
                    </td>
                    <td class="dl_speed">800 KB<sub>/</sub>s</td>
                    <td class="dl_size">{size}</td>
                    <td>03:25</td>
                    <td>
                        <div>
                            <div>
                                <a href="javascript:void(0)" class="btn-action btn-pause"></a>
                                <a href="javascript:void(0)" class="btn-action btn-stop"></a>
                                <a href="javascript:void(0)" class="btn-action btn-delete"></a>
                            </div>
                        </div>
                    </td>
                </tr>
        `;

            template = template.replace('{name}', response.name).replace('{size}', response.size);
            $("#info-url").val(response.name);
            $("#info-size").val(response.size);
            /*$("#downloads").append(template)*/
            /*let timer;
            pywebview.api.start_download();
            timer = setInterval(function () {
                pywebview.api.getStatus().then(function (res) {
                    $(".dl_speed").text(res.speed);
                    $(".progress").text(res.percent.toFixed(2) + "%")
                    $(".progress-bar > div").width(res.percent + "%")
                });
            }, 100)*/

        });
        // console.log(url,name);

        $("#addNewDownloadModal").hide();
    })
});

// initialize()