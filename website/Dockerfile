FROM docker.io/rocm/pytorch

RUN apt update

RUN pip install torchvision h5py imutils sentencepiece matplotlib numpy pillow scikit-image scikit-learn scipy torch torchvision torchsummary transformers accelerate python-dotenv flask waitress sqlalchemy


WORKDIR /music_crs

COPY . .

ENV PYTORCH_ROCM_ARCH="gfx1031"
ENV HSA_OVERRIDE_GFX_VERSION=10.3.0


CMD ["python3", "source/test_llm.py"]
