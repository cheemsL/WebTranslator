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
        this.buttonClear = this.shadowRoot.querySelector("#botton_clear");

        this.buttonTranslate.addEventListener("click", (e) => {
            const text = this.inputEdit.textContent.trim();
            if (!text) return;
            this.startTranslation(text)
        })

        this.buttonAudio.addEventListener("click", ()=>{
            const text = this.inputEdit.textContent.trim();
            if (!text) return;
            this.audioPlay(text);
        })

        this.buttonClear.addEventListener("click", ()=>{
            this.inputEdit.textContent="";
            this.outputEdit.textContent="";
        })
    }

    startTranslation(text){
        const url = `http://127.0.0.1:8050/translate/generate?prompt=${encodeURIComponent(text)}`
        const eventSource = new EventSource(url);

        let result = "";

        eventSource.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                result += data.token;
                
                this.outputEdit.textContent = result;
            } catch (err) {
                console.error("翻译出错: "+err)
            }
        }

        eventSource.onerror = (err) => {
            console.log("SSE 连接关闭或出错", err);
            eventSource.close();
        }

    }

    async audioPlay(text){
        try{
            // 1.调用接口
            const response = await fetch(
                `http://127.0.0.1:8050/audio/generate?prompt=${encodeURIComponent(text)}`
            );
            if (!response.ok){
                console.log("请求失败: "+response.statusText);
            }

            const data = await response.json();

            // 2.解析Base64音频
            const audioBase64 = data.audio_base64;
            const audioBlob = this.base64ToBlob(audioBase64, "audio/wav");
            const audioUrl = URL.createObjectURL(audioBlob);

            // 3.播放音频
            const audio = new Audio(audioUrl);
            audio.play();

        } catch (err){
            console.error(err);
        }
    }

    base64ToBlob(base64, mime){
        const bytes = atob(base64)
        const len = bytes.length;
        const buffer = new ArrayBuffer(len);
        const view = new Uint8Array(buffer);
        for (let i=0; i<len; i++){
            view[i] = bytes.charCodeAt(i);
        }
        return new Blob([buffer], {type: mime});
    }





}


customElements.define("element-translator", TranslatorElement);