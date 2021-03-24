_base_ = '../../base.py'

# model settings
model = dict(
    type='MOCO',
    pretrained='data/basetrain_chkpts/resnet34-333f7ec4.pth',
    queue_len=65536,
    feat_dim=128,
    momentum=0.999,
    backbone=dict(
        type='ResNet',
        depth=34,
        in_channels=3,
        out_indices=[4],  # 0: conv-1, x: stage-x
        norm_cfg=dict(type='BN')),
    neck=dict(
        type='NonLinearNeckV1',
        auto_channels=True,
        out_channels=128,
        with_avg_pool=True),
    head=dict(type='ContrastiveHead', temperature=0.2))
# dataset settings
data_source_cfg = dict(
    type='ImageNet',
    memcached=False,
    mclient_path='/not/used')

data_train_list = "/rscratch/cjrd/basetraining/OpenSelfSup/data/dn-exp/meta/clipart-all-sketch-train.txt"
data_train_root = "/rscratch/cjrd/basetraining/OpenSelfSup/data/dn-exp"

dataset_type = 'ContrastiveDataset'
img_norm_cfg = dict(mean=[0.7362, 0.7167, 0.6834], std=[0.3642, 0.3654, 0.3887])
train_pipeline = [
    dict(type='RandomResizedCrop', size=224, scale=(0.2, 1.)),
    dict(
        type='RandomAppliedTrans',
        transforms=[
            dict(
                type='ColorJitter',
                brightness=0.4,
                contrast=0.4,
                saturation=0.4,
                hue=0.4)
        ],
        p=0.8),
    dict(type='RandomGrayscale', p=0.2),
    dict(
        type='RandomAppliedTrans',
        transforms=[
            dict(
                type='GaussianBlur',
                sigma_min=0.1,
                sigma_max=2.0,
                )
        ],
        p=0.5),
    dict(type='RandomHorizontalFlip'),
    dict(type='ToTensor'),
    dict(type='Normalize', **img_norm_cfg),
]
data = dict(
    imgs_per_gpu=64,  # total 64*4=256
    workers_per_gpu=4,
    drop_last=True,
    train=dict(
        type=dataset_type,
        data_source=dict(
            list_file=data_train_list, root=data_train_root,
            **data_source_cfg),
        pipeline=train_pipeline))
# optimizer
optimizer = dict(type='SGD', lr=0.03, weight_decay=0.0001, momentum=0.9)
# learning policy
lr_config = dict(policy='CosineAnnealing', min_lr=0.)

# cjrd added this flag, since OSS didn't support training by iters(?)
by_iter=True

log_config = dict(
    interval=25,
    by_epoch=False,
    hooks=[
        dict(type='TextLoggerHook', by_epoch=False),
        dict(type='TensorboardLoggerHook', by_epoch=False)
    ])

# epoch related
total_iters=50000
checkpoint_config = dict(interval=total_iters)
