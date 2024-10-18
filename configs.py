import ml_collections

def get_3DReg_config():
    config = ml_collections.ConfigDict()
    config.patches = ml_collections.ConfigDict({'size': (8, 8, 8)})
    config.patches.grid = (8, 8, 8)
    config.hidden_size = 252
    config.hidden_size1 = 33
    config.transformer = ml_collections.ConfigDict()
    config.transformer.mlp_dim = 3072
    config.transformer.num_heads = 12
    config.transformer.num_layers = 12
    config.transformer.attention_dropout_rate = 0.0
    config.transformer.dropout_rate = 0.1
    config.patch_size = 8
    config.in_chans = 2

    config.conv_first_channel = 96 #512
    config.conv_first_channel1 = 192
    config.encoder_channels = (16, 32, 32)
    config.encoder_channels1 = (16, 32, 64, 96)
    config.down_factor = 2
    config.down_num = 2
    config.down_num1 = 1
    config.decoder_channels = (96, 48, 32, 32, 16)#(96, 48, 32, 32, 16)
    config.decoder_channels1 = (96, 48, 32, 16, 16)
    config.skip_channels = (32, 32, 32, 32, 16)#(32, 32, 32, 32, 16) (256, 128, 64, 32, 16)
    config.n_dims = 3
    config.n_skip = 5
    config.dilation = 1
    config.ls_init_value = 1.0
    config.norm_layer = None
    config.if_transskip = True
    config.if_convskip = True
    # config.drop_path_rates = None or [0.] * 4
    return config
