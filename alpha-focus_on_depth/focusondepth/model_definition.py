from transformers import PreTrainedModel
import timm
import torch.nn as nn
import numpy as np

from .model_config import FocusOnDepthConfig
from .reassemble import Reassemble
from .fusion import Fusion
from .head import HeadDepth, HeadSeg


class FocusOnDepth(PreTrainedModel):
    config_class = FocusOnDepthConfig

    def __init__(self, config):
        super().__init__(config)
        self.transformer_encoders = timm.create_model(config.model_timm, pretrained=True)
        self.type_ = config.type_

        #Register hooks
        self.activation = {}
        self.hooks = config.hooks
        self._get_layers_from_hooks(self.hooks)

        #Reassembles Fusion
        self.reassembles = []
        self.fusions = []
        for s in config.reassemble_s:
            self.reassembles.append(Reassemble(config.image_size, config.read, config.patch_size, s, config.emb_dim, config.resample_dim))
            self.fusions.append(Fusion(config.resample_dim))
        self.reassembles = nn.ModuleList(self.reassembles)
        self.fusions = nn.ModuleList(self.fusions)

        #Head
        if self.type_ == "full":
            self.head_depth = HeadDepth(config.resample_dim)
            self.head_segmentation = HeadSeg(config.resample_dim, nclasses=config.nclasses)
        elif self.type_ == "depth":
            self.head_depth = HeadDepth(config.resample_dim)
            self.head_segmentation = None
        else:
            self.head_depth = None
            self.head_segmentation = HeadSeg(config.resample_dim, nclasses=config.nclasses)

    def forward(self, img):
        _ = self.transformer_encoders(img)
        previous_stage = None
        for i in np.arange(len(self.fusions)-1, -1, -1):
            hook_to_take = 't'+str(self.hooks[i])
            activation_result = self.activation[hook_to_take]
            reassemble_result = self.reassembles[i](activation_result)
            fusion_result = self.fusions[i](reassemble_result, previous_stage)
            previous_stage = fusion_result
        out_depth = None
        out_segmentation = None
        if self.head_depth != None:
            out_depth = self.head_depth(previous_stage)
        if self.head_segmentation != None:
            out_segmentation = self.head_segmentation(previous_stage)
        return out_depth, out_segmentation

    def _get_layers_from_hooks(self, hooks):
        def get_activation(name):
            def hook(model, input, output):
                self.activation[name] = output
            return hook
        for h in hooks:
            self.transformer_encoders.blocks[h].register_forward_hook(get_activation('t'+str(h)))