class TranslatorElement extends HTMLElement{
    constructor() {
        super();
        this.attachShadow({mode: "open"})

        fetch("./static/elements/templates/translator.html")
            .then((response) => response.text())
            .then((html) => {
                const document = new DOMParser().parseFromString(html, "text/html");
                const template = document.querySelector("#template_translator");
                const content = template.content.cloneNode(true);
                this.shadowRoot.appendChild(content);
            })
    }
}


customElements.define("element-translator", TranslatorElement);