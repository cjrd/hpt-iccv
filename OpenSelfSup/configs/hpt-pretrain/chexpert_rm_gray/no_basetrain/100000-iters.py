_base_="../base-chexpert_rm_gray-config.py"

# this will merge with the parent

# epoch related
total_iters=100000
checkpoint_config = dict(interval=total_iters)
checkpoint_config = dict(interval=total_iters//2)
