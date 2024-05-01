import mimetypes
import pytesseract
import os
import re

from pypdf import PdfReader
from moviepy.editor import VideoFileClip


def get_file_mime_type(file_path: str) -> str:
    """
    Extrai os mimetypes de arquivos.
    """
    return mimetypes.guess_type(file_path)[0]


def get_audio_from_video(video_path: str) -> str:
    """
    Extrai o áudio de um vídeo e salva em uma pasta temporária.
    """
    file_name: str = video_path.split('/')[-1].split('.')[0]
    new_name: str = f'{file_name}.mp3'

    temp_dir: str = './temp'

    audio_path: str = f'{temp_dir}/{new_name}'

    if not os.path.isdir(temp_dir):
        os.mkdir(temp_dir)

    if os.path.isfile(audio_path):
        return audio_path

    video: VideoFileClip = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

    return audio_path


def get_text_from_image(file_path: str) -> str:
    """
    Obtém o texto a partir de uma imagem.
    """
    return pytesseract.image_to_string(file_path)


def get_text_from_pdf(file_path: str) -> str:
    """
    Obtém o texto a partir de um pdf.
    """
    reader: PdfReader = PdfReader(file_path)
    return "".join([x.extract_text() for x in reader.pages])


def get_simple_text(file_path: str) -> str:
    """
    Obtém o texto de arquivos simples
    """
    file = open(file_path, "r")

    # Remove espaços extras (extremamente útil com json)
    return re.sub(r" +", " ", file.read())
