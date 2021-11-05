import os
import glob
import subprocess
import tarfile
import wget
import copy
from omegaconf import OmegaConf, open_dict
data_dir = 'datasets/'

if not os.path.exists(data_dir):
  os.makedirs(data_dir, exist_ok=True)

if not os.path.exists("scripts"):
  os.makedirs("scripts")



import nemo
import nemo.collections.asr as nemo_asr
from nemo.collections.asr.metrics.wer import word_error_rate
from nemo.utils import logging, exp_manager

VERSION = "v1.0.0"
LANGUAGE = "es"

tokenizer_dir = os.path.join('tokenizers', LANGUAGE)
manifest_dir = os.path.join('manifests', LANGUAGE)

train_manifest = f"{manifest_dir}/train_trans.json"
dev_manifest = f"{manifest_dir}/dev_trans.json"

