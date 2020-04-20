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

function go_to_page_using_select() {
    let pageNumberSelect = document.getElementById("pageNumberSelect");
    let selectPageNumber = pageNumberSelect.options[pageNumberSelect.selectedIndex].value;
    location.href = `?page=${selectPageNumber}`;
}

function go_to_page_using_input() {
    let pageNumberInput = document.getElementById("pageNumberInput");
    location.href = `?page=${pageNumberInput.value}`;
}