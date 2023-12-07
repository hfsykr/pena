/* For Note Title Tooltip */
const title = document.querySelectorAll(".note-title");

title.forEach((element, index) => {
    var overflow = element.scrollWidth > element.offsetWidth;
    // Connect tooltip to the title if the title text is overflowing
    if (overflow) {
        element.setAttribute("data-tooltip-target", "tooltip-" + index);
        element.setAttribute("data-tooltip-placement", "bottom");
    } 
});

/* For Search */
const searchInput = document.getElementById('search-input');
const searchForm = document.getElementById("search-form")

searchForm.addEventListener("submit", (event) => {
    // Check if search input blank
    if (!searchInput.value) {
        event.preventDefault();
        return false;		
    }
    // Do nothing, the form will be submitted.
});
