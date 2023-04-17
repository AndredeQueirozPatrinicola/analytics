async function dropdown(element) {
    element.classList.add("dropdown-is-toggled")
}

async function addDropdownListener() {
    const element = document.getElementById("dropdown")
    if (element) {
        const elementChildren = Array.from(element.children)
        elementChildren[0].addEventListener('click', function () {
            dropdown(elementChildren[1])
        })

        window.onclick = (event) => {

            if (!event.target.matches('span') && !event.target.matches('.dropdown-items') && !event.target.matches('.dropdown-button') && !event.target.matches('.fa-arrow-down')) {
                element.children[1].classList.remove("dropdown-is-toggled")
            }
        }
    }
}

export default addDropdownListener;

