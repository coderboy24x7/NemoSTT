from ruamel.yaml import YAML

config_path = './examples/asr/conf/quartznet_15x5.yaml'

yaml = YAML(typ='safe')
with open(config_path) as f:
    params = yaml.load(f)

params['model']['train_ds']['manifest_filepath'] = train_manifest
params['model']['validation_ds']['manifest_filepath'] = test_manifest
params['model']['validation_ds']['manifest_filepath'] = test_manifest