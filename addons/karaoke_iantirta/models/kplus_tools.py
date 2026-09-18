import kplus
import kplus.init

from kplus.pipelines.download import Downloader
from kplus.worker.gpu_worker import KaggleWorker

def extract_info(url: str, **kwargs) -> tuple[str, str, float]:
    default_kwargs = {
        "cookiefile": None
    }
    default_kwargs.update(kwargs)
    return Downloader(**default_kwargs)._extract_info(url)

def extract_lyrics(title: str, artist: str, duration: float) -> str:
    return Downloader().get_lyrics(title, artist, duration)
