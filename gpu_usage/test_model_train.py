# python test_model_train.py wrn50 8 512
import sys
import torch
from model.builder import build_model
from utils.utils_train import MultiProjectionLayer, Revisit_RDLoss, loss_function


device_num = 0
batch_size = int(sys.argv[2])
loop_num = 10
image_size = [int(sys.argv[3]), int(sys.argv[3])]
device = f"cuda:{device_num}"
accumulation_steps = 2

# model
encoder, decoder, bn, proj_layer = build_model(
    encoder=sys.argv[1],
    decoder=sys.argv[1],
    proj=True,
    device=device,
)
decoder.train()
bn.train()
if proj_layer is not None:
    proj_layer.train()

# loss
proj_loss = Revisit_RDLoss()

# optim
optimizer_proj = torch.optim.Adam(list(proj_layer.parameters()), lr=0.001, betas=(0.5,0.999))
optimizer_distill = torch.optim.Adam(list(decoder.parameters())+list(bn.parameters()), lr=0.005, betas=(0.5,0.999))


# input
img = torch.rand(batch_size, 3, *image_size)
img = img.to(device)

# infer
for i in range(loop_num):
    with torch.no_grad():
        inputs = encoder(img)
        inputs_noise = encoder(img)
    (feature_space_noise, feature_space) = proj_layer(inputs, features_noise = inputs_noise)
    b = bn(feature_space)
    outputs = decoder(b, sizes=[i.shape[-2:] for i in inputs[::-1]])
    # loss
    L_distill = loss_function(inputs, outputs)
    L_proj = proj_loss(inputs_noise, feature_space_noise, feature_space)
    loss = L_distill + 0.2 * L_proj
    # optim
    optimizer_proj.zero_grad()
    optimizer_distill.zero_grad()
    loss.backward()
    if (i + 1) % accumulation_steps == 0:
        optimizer_proj.step()
        optimizer_distill.step()
