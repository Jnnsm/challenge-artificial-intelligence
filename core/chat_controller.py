import queue
import chevron

from typing import Union
from database.Database import Database
from core.llm import LLM
from langchain_core.documents import Document


class ChatController():
    def __init__(self, memory_size: int = 5, chat_prompt: str = None):
        if chat_prompt:
            self.chat_prompt: str = chat_prompt
        else:
            self.chat_prompt: str = """You are a helpful assistant. Your name is Edu. You are trying to help the user
to find useful files to help their studies. Use only the files and content listed down below, along with their
content fell free to use their content or point the user which file they must search for.
List of contents:
{{{contents}}}"""
        self.memory_size: int = memory_size
        self.messages_queue: queue.Queue = queue.Queue(memory_size)
        self.llm: LLM = LLM()

    def init_database(self, path='resources') -> None:
        self.db: Database = Database('resources')

    def add_new_message(self, message: Union[dict[str, str], str]) -> None:
        if isinstance(message, str):
            message = {
                "role": "user",
                "content": message
            }

        if self.messages_queue.full():
            self.messages_queue.get()

        self.messages_queue.put(message)

    def generate_response(self) -> str:
        documents: list[Document] = self.db.query(
            list(self.messages_queue.queue)[-1]['content'])

        messages: str = self.format_messages(
            "".join([self.format_knowledge_base(document) for document in documents]))

        response: dict[str, str] = self.llm.get_chat_completion(
            messages=messages)
        self.add_new_message(response)

        return response['content']

    def format_knowledge_base(self, document: Document):
        return f"{"{"}\n    metadata: {document.metadata}\n    page_content: {document.page_content}\n{"}"}"

    def format_messages(self, knowledge_base: str = "") -> list[dict[str, str]]:
        prompt_message = {"role": "system", "content": chevron.render(
            self.chat_prompt, {"contents": knowledge_base})}
        alternating_messages = list(self.messages_queue.queue)

        return [prompt_message] + alternating_messages
