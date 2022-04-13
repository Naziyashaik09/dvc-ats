from transformers import PretrainedConfig
from typing import List


class FocusOnDepthConfig(PretrainedConfig):
    model_type = "focusondepth"

    def __init__(
        self,
        image_size         = (3, 384, 384),
        patch_size         = 16,
        emb_dim            = 768,
        resample_dim       = 256,
        read               = 'projection',
        num_layers_encoder = 24,
        hooks              = [2, 5, 8, 11],
        reassemble_s       = [4, 8, 16, 32],
        transformer_dropout= 0,
        nclasses           = 2,
        type_               = "full",
        model_timm         = "vit_base_patch16_384",
        **kwargs,
    ):
        if type_ not in ["full", "depth", "segmentation"]:
            raise ValueError(f"`type_` must be 'full' or depth' or 'segmentation, got {type_}.")
        if read not in ["ignore", "add", "projection"]:
            raise ValueError(f"`read` must be '', 'ignore' or 'add' or 'projection, got {read}.")
        if image_size[0] != 3 and image_size[1] != 384 and image_size[2] != 384:
            raise ValueError(f"`image_size` must be 3, 384, 384, got {image_size}.")
        if patch_size != 16:
            raise ValueError(f"`patch_size` must be 16, got {patch_size}.")

        self.image_size = image_size
        self.patch_size = patch_size
        self.emb_dim = emb_dim
        self.resample_dim = resample_dim
        self.read = read
        self.num_layers_encoder = num_layers_encoder
        self.hooks = hooks
        self.reassemble_s = reassemble_s
        self.transformer_dropout = transformer_dropout
        self.nclasses = nclasses
        self.type_ = type_
        self.model_timm = model_timm
        super().__init__(**kwargs)