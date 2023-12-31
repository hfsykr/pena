/* Make <p> default as wrapper for new element instead of <div> for <div> contenteditable
   <div>example</div> --> <p>example</p> */
document.execCommand("defaultParagraphSeparator", false, "p");
const formEditor = document.getElementById("form-editor");
var editor = document.getElementById("editor");
const content = document.getElementById("id_content");

// For placeholder handling
editor.addEventListener("input", () => {
    // Check if editor only have 1 child then the event continue
    if (editor.childNodes.length !== 1) {
        return;
    }
    
    /* Check if the only child of editor is <br> or <p><br></p>
       It's look empty on visual but actualy have one element inside of it */
    const editorFirstChild = editor.firstChild;

    // For <br>
    if (editorFirstChild.tagName === "BR") {
        editor.replaceChildren();
    }

    // For <p><br></p>
    if (editorFirstChild.firstChild) {
        if (editorFirstChild.firstChild.tagName === "BR") {
            editor.replaceChildren();
        }
    }
});

// Wrap element with another element
function wrap(element, wrapperElement) {
    element.parentNode.insertBefore(wrapperElement, element);
    wrapperElement.appendChild(element);
}

// Unwrap an element
function unwrap(element) {
    element.replaceWith(...element.childNodes);
    return element;
}
