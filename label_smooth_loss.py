'''
classification, 2D segmentation, 3D segmentation
All round loss function
Label smoothing loss
'''
import torch
import torch.nn as nn


class LabelSmoothing(nn.Module):
    """
    NLL loss with label smoothing.
    """

    def __init__(self, smoothing=0.0, reduction='mean'):
        """
        Constructor for the LabelSmoothing module.
        :param smoothing: label smoothing factor
        """
        super(LabelSmoothing, self).__init__()
        self.confidence = 1.0 - smoothing
        self.smoothing = smoothing
        self.reduction = reduction

    def forward(self, x, target):
        logprobs = torch.nn.functional.log_softmax(x, dim=1)

        nll_loss = -logprobs.gather(dim=1, index=target.unsqueeze(1))
        nll_loss = nll_loss.squeeze(1)
        smooth_loss = -logprobs.mean(dim=1)
        loss = self.confidence * nll_loss + self.smoothing * smooth_loss        # loss.size()==target.size()
        if self.reduction == 'mean':
            return loss.mean()
        else:
            return loss.mean(dim = list(range(1, loss.ndim  )))
          
if __name__=='__main__':
    criteria = LabelSmoothing(smoothing=0.1, reduction=None)
    logits = torch.randn(8, 19, 384, 384) # nchw, float/half
    lbs = torch.randint(0, 19, (8, 384, 384)) # nhw, int64_t
    loss = criteria(logits, lbs)
    print(loss)
