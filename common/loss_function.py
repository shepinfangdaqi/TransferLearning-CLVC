from torch import nn


class Tacotron2Loss(nn.Module):
    def __init__(self, mel_weight=1, gate_weight=0.005):
        super(Tacotron2Loss, self).__init__()
        self.w_mel = mel_weight
        self.w_gate = gate_weight

    def forward(self, model_output, targets):
        mel_target, gate_target = targets[0], targets[1]
        mel_target.requires_grad = False
        gate_target.requires_grad = False
        gate_target = gate_target.view(-1, 1)

        mel_out, mel_out_postnet, gate_out, _ = model_output
        gate_out = gate_out.view(-1, 1)
        mel_loss = nn.MSELoss()(mel_out, mel_target) + nn.MSELoss()(mel_out_postnet, mel_target)
        # mel_loss = nn.MSELoss()(mel_out_postnet, mel_target)
        # mel_loss_l1 = nn.L1Loss()(mel_out, mel_target) + nn.L1Loss()(mel_out_postnet, mel_target)
        gate_loss = nn.BCEWithLogitsLoss()(gate_out, gate_target)
        return self.w_mel * mel_loss + self.w_gate * gate_loss
        # return 0.5 * self.w_mel * (mel_loss + mel_loss_l1) + self.w_gate * gate_loss