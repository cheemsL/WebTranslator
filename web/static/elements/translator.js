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

                this.initialize();
            })
    }

    initialize(){
        this.inputEdit = this.shadowRoot.querySelector("#input_edit");
        this.outputEdit = this.shadowRoot.querySelector("#output_edit");

        this.buttonTranslate = this.shadowRoot.querySelector("#botton_translate");
        this.buttonAudio = this.shadowRoot.querySelector("#botton_audio");

        this.buttonTranslate.addEventListener("click", (e) => {
            
            // 获取输入栏的文本内容
            const text = this.inputEdit.textContent;

            this.outputEdit.textContent = text;

            // 清空输入栏的文本内容
            this.inputEdit.textContent = "";
        })
    }



}


customElements.define("element-translator", TranslatorElement);