class TranslatorElement extends HTMLElement{
    constructor() {
        super();
        this.attachShadow({mode: "open"})

        this.isTranslating = false; // 是否正在翻译

        fetch("./static/elements/templates/translator.html")
            .then((response) => response.text())
            .then((html) => {
                const document = new DOMParser().parseFromString(html, "text/html");
                const template = document.querySelector("#template_translator");
                const content = template.content.cloneNode(true);
                this.shadowRoot.appendChild(content);
                
                this.inputEdit = this.shadowRoot.querySelector("#input_edit");
                this.outputEdit = this.shadowRoot.querySelector("#output_edit");

                this.buttonTranslate = this.shadowRoot.querySelector("#botton_translate");
                this.buttonTranslateAllow = this.buttonTranslate.querySelector("#allow");
                this.buttonTranslateSquare = this.buttonTranslate.querySelector("#square");
                this.buttonTranslate.addEventListener("click", (e) => {
                    if (this.buttonTranslateAllow.style.display !== "none"){
                        this.buttonTranslateAllow.style.display = "none";
                        this.buttonTranslateSquare.style.display = "block";
                    } else {
                        this.buttonTranslateAllow.style.display = "block";
                        this.buttonTranslateSquare.style.display = "none";
                    }

                    // 获取输入栏的文本内容
                    const text = this.inputEdit.textContent;

                    this.outputEdit.textContent = text;

                    // 清空输入栏的文本内容
                    this.inputEdit.textContent = "";
                })
            })
    }

    

}


customElements.define("element-translator", TranslatorElement);