$(function(){
    modal_controler();
});

function get_params_parser() {
    let params = location.search.substr(location.search.indexOf("?")+1).split("&");
    let mappedParams = {};
    let temp;
    for (let index in params) {
        temp = params[index].split("=");
        mappedParams[temp[0]] = temp[1];
    }
    return mappedParams;
}

function go_to_page(pageNumber) {
    let getParamsObject = get_params_parser();
    let href;
    if (getParamsObject["category"] !== undefined) {
        href = `?category=${getParamsObject["category"]}&query=${getParamsObject["query"]}&page=${pageNumber}`;
    } else {
        href = `?page=${pageNumber}`;
    }
    location.href = href;
}

function go_to_page_using_select() {
    let pageNumberSelect = document.getElementById("pageNumberSelect");
    let selectPageNumber = pageNumberSelect.options[pageNumberSelect.selectedIndex].value;
    go_to_page(selectPageNumber);
}

function go_to_page_using_input() {
    let pageNumberInput = document.getElementById("pageNumberInput");
    go_to_page(pageNumberInput.value);
}

function modal_controler() {
    $('#detailModal').on('show.bs.modal', function (event) {
        let pk = $(event.relatedTarget).data('pk');
        let modal = $(this);
        $.ajax({
            url: `/song/${pk}`,
            type: "GET",
            dataType: "json",
            success: function (json) {
                modal.find('#detailModalLabel').text(json.song_name_korean);
                modal.find('#id_title_kor').text(json.song_name_korean);
                modal.find('#id_title_jpn').text(json.song_name_origin);
                modal.find('#id_singer').text(json.singer);
                modal.find('#id_group').text(json.group);
                modal.find('#id_tj').text(json.tj !== null ? json.tj : "없음");
                modal.find('#id_ky').text(json.ky !== null ? json.ky : "없음");
                modal.find('#id_dam').text(json.dam !== null ? json.dam : "없음");
                modal.find('#id_uga').text(json.uga !== null ? json.uga : "없음");
                modal.find('#id_joy').text(json.joy !== null ? json.joy : "없음");
                $('#id_help_google').click(function () {
                    let googleSearchUrl = `https://www.google.com/search?q=${json.song_name_korean}+가사`
                    let win = window.open(googleSearchUrl, '_blank');
                    win.focus();
                })


            },
        });

    })
}
