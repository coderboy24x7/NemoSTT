import pytorch_lightning as pl
import nemo.collections.asr as nemo_asr
from omegaconf import DictConfig

# Use 8 GPUs and enable Mixed Precision
trainer = pl.Trainer(gpus=8, max_epochs=50, accelerator='ddp', precision=16)
quartznet_model = nemo_asr.models.EncDecCTCModel(cfg=DictConfig(params['model']), trainer=trainer)

trainer.fit(quartznet_model)