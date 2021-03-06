window.addEventListener('pywebviewready', function (data) {
    // let container = document.getElementById('webview-status')
    // container.innerHTML = '<i>pywebview</i> is ready';
    // initialize()

})

function cancel() {
    pywebview.api.cancel()
}

$(function (){
    $("#cancel-download").click(function (){
        alert("test")
    })
});
