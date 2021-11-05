import pytorch_lightning as pl
import nemo.collections.asr as nemo_asr
from omegaconf import DictConfig

trainer = pl.Trainer(gpus=1, max_epochs=50)
quartznet_model = nemo_asr.models.EncDecCTCModel(cfg=DictConfig(params['model']), trainer=trainer)

trainer.fit(quartznet_model)