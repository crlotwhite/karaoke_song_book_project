$(function(){
    console.log(`    /\\_____/\\
   /  o   o  \\
  ( ==  ^  == )
   )         (
  (           )
 ( (  )   (  ) )
(__(__)___(__)__)
여기서 나쁜짓하면 않된다냥!!!
    `);
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
