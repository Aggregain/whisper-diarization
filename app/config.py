import os

class Config:
    WHISPER_MODEL = os.getenv("WHISPER_MODEL", "large-v3")
    DEVICE = os.getenv("DEVICE", "cuda")
    COMPUTE_TYPE = os.getenv("COMPUTE_TYPE", "float16")
    HF_TOKEN = os.getenv("HF_TOKEN")  # set this in .env or environment