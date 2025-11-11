import threading
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TextIteratorStreamer
)
from typing import (
    List,
    Dict,
    Iterator
)
from env import MODEL_PATH
print(MODEL_PATH)


class Qwen3:


    def __init__(self):
        self.__model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH,
            dtype="auto",
            device_map="auto"
        )
        self.__tokenizer = AutoTokenizer.from_pretrained(
            MODEL_PATH,
        )

    def generate(self, messages: List[Dict]) -> Iterator:
        text = self.__tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False  # Switches between thinking and non-thinking modes. Default is True.
        )
        model_inputs = self.__tokenizer([text], return_tensors="pt").to(self.__model.device)

        streamer = TextIteratorStreamer(
            self.__tokenizer,
            skip_prompt=True,
            skip_special_tokens=True
        )

        kwargs = {
            **model_inputs,
            "max_new_tokens": 32768,
            "streamer": streamer,
            "do_sample": False,
        }

        thread = threading.Thread(target=self.__model.generate, kwargs=kwargs)
        thread.start()

        for new_text in streamer:
            yield new_text


if __name__ == '__main__':
    llm = Qwen3()
    messages = [
        {
            "role": "system", "content": "You are a helpful assistant. Please translate the user input into Chinese.",
        },
        {
            "role": "user", "content": "你好"
        }
    ]
    for output in llm.generate(messages):
        print(output)