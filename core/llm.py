from huggingface_hub import hf_hub_download
from llama_cpp import Llama


class Singleton(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LLM(metaclass=Singleton):

    def __init__(self):
        downloaded_model: str = hf_hub_download(
            repo_id='QuantFactory/Meta-Llama-3-8B-Instruct-GGUF',
            filename='Meta-Llama-3-8B-Instruct.Q4_K_M.gguf'
        )

        self.model: Llama = Llama(downloaded_model,
                                  verbose=False,
                                  n_gpu_layers=-1,
                                  embedding=True,
                                  n_ctx=0)

    def get_embedding(self, text: str) -> str:
        return self.model.create_embedding(text)[
            'data'][0]['embedding'][0]

    def get_chat_completion(self,
                            messages: list[str],
                            temperature: float = 0,
                            max_tokens: int = None,
                            stream: bool = False,
                            response_format: dict[str] = {"type": 'text'}) -> dict[str, str]:

        return self.model.create_chat_completion(messages=messages,
                                                 temperature=temperature,
                                                 max_tokens=max_tokens,
                                                 stream=stream,
                                                 response_format=response_format
                                                 )['choices'][0]['message']
