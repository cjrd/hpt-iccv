_base_="../base-bdd_crop_only-config.py"

# this will merge with the parent
model=dict(pretrained='data/basetrain_chkpts/imagenet_r50_supervised.pth')

# epoch related
total_iters=5000
checkpoint_config = dict(interval=total_iters)
