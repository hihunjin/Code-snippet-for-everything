# !pip install torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
# !wget https://file-examples-com.github.io/uploads/2017/11/file_example_WAV_1MG.wav -O ex.wav

import torchaudio

audio, sr = torchaudio.load('ex.wav')
print(audio.size(),sr)
print('time' : audio.size(-1)/sr)
