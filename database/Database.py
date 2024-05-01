import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from core.utils.file_utils import (
    get_file_mime_type, get_audio_from_video, get_text_from_image,
    get_text_from_pdf, get_simple_text
)
from core.whisper import Whisper


class Singleton(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=Singleton):
    persist_directory: str = './chroma_db'
    embedding_function = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2")

    def __init__(self, base_dir: str = None, recover_from_file=True) -> None:
        if recover_from_file and os.path.isdir(self.persist_directory):
            self.db = Chroma(persist_directory=self.persist_directory,
                             embedding_function=self.embedding_function)
            return

        if base_dir is None or not os.path.isdir(base_dir):
            raise BaseException(f'Diretório "{base_dir}" não existe')

        files: list[str] = os.listdir(base_dir)
        contents: list[str] = self.get_content_from_files(base_dir, files)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False,
        )

        metadata = [{"source": x} for x in files]
        split_contents: list[str] = text_splitter.create_documents(
            contents, metadata)

        self.db: Chroma = Chroma.from_documents(
            split_contents, self.embedding_function,
            persist_directory=self.persist_directory
        )

    def query(self, string: str, n_of_documents: int = 5) -> list[str]:
        return self.db.similarity_search(string, n_of_documents)

    def get_content_from_files(self,
                               base_dir: str,
                               files: list[str]
                               ) -> list[str]:
        """
        Lê os arquivos e aplica o tratamento necessário
        """
        types: list[str] = [get_file_mime_type(x) for x in files]
        contents: list[str] = []

        if base_dir[-1] != '/':
            base_dir += '/'

        for idx, f in enumerate(files):
            match types[idx]:
                case 'application/pdf':
                    contents.append(get_text_from_pdf(base_dir + f))
                case 'video/mp4':
                    whisper = Whisper()
                    contents.append(whisper.extract_text_from_audio(
                        get_audio_from_video(base_dir + f)))
                case 'image/jpeg':
                    contents.append(get_text_from_image(base_dir + f))
                case _:
                    contents.append(get_simple_text(base_dir + f))

        return contents
