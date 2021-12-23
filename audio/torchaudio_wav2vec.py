# !wget https://file-examples-com.github.io/uploads/2017/11/file_example_WAV_1MG.wav -O ex.wav
# !wget http://www0.cs.ucl.ac.uk/teaching/GZ05/samples/tone.wav -O mono.wav
# !pip install torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
import torch, torchvision
import torch.nn as nn
import torchaudio

import torchaudio.models

### load
audio, sr = torchaudio.load('ex.wav')
n_fea = sr*3
audio = audio[:1]
audio = audio[:,:(audio.size(-1)-audio.size(-1)%n_fea)]
print(audio.size())
# torch.Size([1, 264000])

## resize
audio = audio.unsqueeze(0).unsqueeze(-1)
audio = audio.reshape((1,1,audio.size(-2)//n_fea,n_fea))



### model
model = torchaudio.models.DeepSpeech(n_feature =n_fea,n_hidden=512, n_class=1)
model.fc1.fc = nn.Linear(in_features=n_fea, out_features=2048, bias=True)
model.fc2.fc = nn.Linear(in_features=2048, out_features=1024, bias=True)
model.fc3.fc = nn.Linear(in_features=1024, out_features=512, bias=True)
model.fc4.fc = nn.Linear(in_features=512, out_features=256, bias=True)
model.out = nn.Identity(256)
print(model)
# DeepSpeech(
#   (fc1): FullyConnected(
#     (fc): Linear(in_features=144000, out_features=2048, bias=True)
#   )
#   (fc2): FullyConnected(
#     (fc): Linear(in_features=2048, out_features=1024, bias=True)
#   )
#   (fc3): FullyConnected(
#     (fc): Linear(in_features=1024, out_features=512, bias=True)
#   )
#   (bi_rnn): RNN(512, 512, bidirectional=True)
#   (fc4): FullyConnected(
#     (fc): Linear(in_features=512, out_features=256, bias=True)
#   )
#   (out): Identity()
# )



### result
out = model(audio)
out.size()
# torch.Size([1, 11, 256])
fea = out.mean(dim=-2)
fea.size()
# torch.Size([1, 256])
