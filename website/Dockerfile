FROM docker.io/rocm/pytorch

RUN apt update

RUN pip3 install h5py
RUN pip3 install imutils
RUN pip3 install tiktoken
RUN pip3 install blobfile
RUN pip3 install sentencepiece
RUN pip3 install matplotlib
RUN pip3 install numpy
RUN pip3 install pillow
RUN pip3 install scikit-image
RUN pip3 install scikit-learn
RUN pip3 install scipy
RUN pip3 install accelerate
RUN pip3 install python-dotenv
RUN pip3 install flask
RUN pip3 install waitress
RUN pip3 install sqlalchemy
RUN pip3 install optimum
RUN pip3 install auto-gptq --no-build-isolation --extra-index-url https://huggingface.github.io/autogptq-index/whl/rocm573/

# RUN pip3 install --force-reinstall 'https://github.com/bitsandbytes-foundation/bitsandbytes/releases/download/continuous-release_multi-backend-refactor/bitsandbytes-0.44.1.dev0-py3-none-manylinux_2_24_x86_64.whl'
RUN pip3 install "transformers>=4.45.1"


WORKDIR /music_crs

#COPY local_model_cache ./local_model_cache
COPY source ./source
COPY templates ./templates
COPY main.py ./main.py
COPY .env ./.env

ENV PYTORCH_ROCM_ARCH="gfx1031"
ENV HSA_OVERRIDE_GFX_VERSION=10.3.0
ENV AMD_LOG_LEVEL=0


CMD ["python3", "main.py"]
