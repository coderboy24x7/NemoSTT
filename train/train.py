from ruamel.yaml import YAML

config_path = './quartznet_15x5.yaml'

yaml = YAML(typ='safe')
with open(config_path) as f:
    params = yaml.load(f)

params['model']['train_ds']['manifest_filepath'] = '/home/csanta/lili-asr/dataset/jsons/train_trans.json'
params['model']['validation_ds']['manifest_filepath'] = '/home/csanta/lili-asr/dataset/jsons/dev_trans.json'


import pytorch_lightning as pl
import nemo.collections.asr as nemo_asr
from omegaconf import DictConfig

trainer = pl.Trainer(gpus=1, max_epochs=50)
quartznet_model = nemo_asr.models.EncDecCTCModel(cfg=DictConfig(params['model']), trainer=trainer)

trainer.fit(quartznet_model)

