import threading
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TextIteratorStreamer,
    StoppingCriteria,
    StoppingCriteriaList
)
from typing import (
    List,
    Dict,
    Iterator
)
from env import MODEL_PATH


class StopOnEvent(StoppingCriteria):
    """用于 Qwen3.terminate() 时强制停止生成"""
    def __init__(self, terminate_event):
        self.terminate_event = terminate_event
    def __call__(self, input_ids, scores, **kwargs):
        return self.terminate_event.is_set()


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
        self.__is_generating = False
        self.__terminate_event = threading.Event()

    def generate(self, messages: List[Dict]) -> Iterator[str]:
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
            "stopping_criteria": StoppingCriteriaList([StopOnEvent(self.__terminate_event)])
        }

        thread = threading.Thread(target=self.__model.generate, kwargs=kwargs)
        thread.start()

        self.__is_generating = True
        self.__terminate_event.clear()

        try:
            for token in streamer:
                if self.__terminate_event.is_set():
                    break
                yield token
        finally:
            self.__is_generating = False

    @property
    def is_generating(self) -> bool:
        return self.__is_generating

    def terminate(self):
        if self.is_generating:
            self.__terminate_event.set()


if __name__ == '__main__':
    llm = Qwen3()
    messages = [
        {
            "role": "system", "content": "You are a helpful assistant. Please translate the user input into Chinese.",
        },
        {
            "role": "user", "content": "mother fuck!"
        }
    ]
    for output in llm.generate(messages):
        print(output)