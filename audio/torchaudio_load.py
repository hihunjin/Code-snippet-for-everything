# !wget https://file-examples.com/storage/feb401d325641db2fa1dfe7/2017/11/file_example_WAV_1MG.wav -O ex.wav
# !wget http://www0.cs.ucl.ac.uk/teaching/GZ05/samples/tone.wav -O mono.wav
# !pip install torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html

import torch, torchvision
import torch.nn as nn
import torchaudio

audio, sr = torchaudio.load('mono.wav')
print(audio.size(),sr)
# torch.Size([1, 144000]) 48000 : [mono/stereo, number of frames] sample_rate
