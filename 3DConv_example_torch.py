import torch
import torch.nn as nn

class small(nn.Module):
    def __init__(self, args=None):
        super(small, self).__init__()
        self.args=args
        if args.aux:
            c=1
        else:
            c=3
        self.encoder = nn.Conv3d(in_channels=args.in_channels, out_channels=c, kernel_size=1)
        self.bn = nn.BatchNorm3d(c)
        self.decoder = nn.Conv3d(in_channels=3, out_channels=args.nclass, kernel_size=1)
    def forward(self, x):
        if args.aux:
            return tuple([self.decoder(x),self.bn (self.encoder(x))])
        else:
            return tuple([self.decoder(self.bn(self.encoder(x)))])

######### prepare args and model  #########
class args:
    aux=False
    nclass=2
    in_channels = 1

model = small(args).cuda()


######### inference   #########
ex = torch.rand(1, args.in_channels,40,100,100).cuda()
out = model(ex)[0]
# print(out)
print(out.size())
