#!/usr/bin/env python
# coding: utf-8

"""Experiments Module."""

__author__ = "Dhanunjaya Elluri"
__mail__ = "dhanunjayet@gmail.com"

import argparse
import random

import numpy as np
import torch

from experiments.main import ExpMain

fix_seed = 2021
random.seed(fix_seed)
torch.manual_seed(fix_seed)
np.random.seed(fix_seed)


parser = argparse.ArgumentParser(
    description="[Autoformer, Transformer, LogSparse, Informer, FedFormer] Long Sequences Forecasting"
)

# basic config
parser.add_argument("--is_training", type=int, required=True, default=1, help="status")
parser.add_argument(
    "--train_only",
    type=bool,
    required=False,
    default=False,
    help="perform training on full input dataset without validation and testing",
)
parser.add_argument(
    "--model_id", type=str, required=True, default="test", help="models id"
)
parser.add_argument(
    "--model",
    type=str,
    required=True,
    default="Autoformer",
    help="models name, options: [Autoformer, Informer, Transformer, LogSparse, Fedformer]",
)

# LogSparse
parser.add_argument(
    "--win_len",
    type=int,
    default=6,
    help="Local attention length for LogSparse Transformer",
)
parser.add_argument(
    "--res_len",
    type=int,
    default=None,
    help="Restart attention length for LogSparse Transformer",
)
parser.add_argument(
    "--qk_ker",
    type=int,
    default=4,
    help="Key/Query convolution kernel length for LogSparse Transformer",
)
parser.add_argument(
    "--v_conv",
    type=int,
    default=0,
    help="Weather to apply ConvAttn for values (in addition to K/Q for LogSparseAttn",
)
parser.add_argument(
    "--sparse_flag",
    type=int,
    default=1,
    help="Weather to apply logsparse mask for LogSparse Transformer",
)
parser.add_argument(
    "--kernel_size",
    type=int,
    default=3,
    help="Kernel size for the 1DConv value embedding",
)

# supplementary config for FedFormer model
parser.add_argument(
    "--version",
    type=str,
    default="Fourier",
    help="for FedFormer, there are two versions to choose, options: [Fourier, Wavelets]",
)
parser.add_argument(
    "--mode_select",
    type=str,
    default="random",
    help="for FedFormer, there are two mode selection method, options: [random, low]",
)
parser.add_argument(
    "--modes", type=int, default=64, help="modes to be selected random 64"
)
parser.add_argument("--L", type=int, default=3, help="ignore level")
parser.add_argument("--base", type=str, default="legendre", help="mwt base")
parser.add_argument(
    "--cross_activation",
    type=str,
    default="tanh",
    help="mwt cross attention activation function tanh or softmax",
)

# data loader
parser.add_argument(
    "--data", type=str, required=True, default="ETTh1", help="dataset type"
)
parser.add_argument(
    "--root_path", type=str, default="./data/", help="root path of the data file"
)
parser.add_argument(
    "--data_path", type=str, default="ETT-small/ETTh1_lloyd.csv", help="data file"
)
parser.add_argument(
    "--boundaries_df",
    type=str,
    default="ETT-small/ETTh1_lloyd_boundaries.csv",
    help="boundaries dataset type",
)
parser.add_argument(
    "--features",
    type=str,
    default="M",
    help="forecasting task, options:[M, S, MS]; M:multivariate predict multivariate, S:univariate predict univariate, MS:multivariate predict univariate",
)
parser.add_argument(
    "--target",
    type=str,
    default="codewords",
    help="target feature in S or MS task",
)
parser.add_argument(
    "--freq",
    type=str,
    default="h",
    help="freq for time features encoding, options:[s:secondly, t:minutely, h:hourly, d:daily, b:business days, w:weekly, m:monthly], you can also use more detailed freq like 15min or 3h",
)
parser.add_argument(
    "--checkpoints",
    type=str,
    default="./checkpoints/",
    help="location of models checkpoints",
)

# forecasting task
parser.add_argument("--seq_len", type=int, default=96, help="input sequence length")
parser.add_argument("--label_len", type=int, default=48, help="start token length")
parser.add_argument(
    "--pred_len", type=int, default=96, help="prediction sequence length"
)


# DLinear
parser.add_argument(
    "--individual",
    action="store_true",
    default=False,
    help="DLinear: a linear layer for each variate(channel) individually",
)
# Formers
parser.add_argument(
    "--embed_type",
    type=int,
    default=1,
    help="1: value embedding + temporal embedding + positional embedding 2: value embedding + temporal embedding 3: value embedding + positional embedding 4: value embedding",
)
parser.add_argument(
    "--enc_in", type=int, default=1, help="encoder input size"
)  # DLinear with --individual, use this hyperparameter as the number of channels
parser.add_argument("--dec_in", type=int, default=1, help="decoder input size")
parser.add_argument("--c_out", type=int, default=1, help="output size")
parser.add_argument("--d_model", type=int, default=512, help="dimension of models")
parser.add_argument("--n_heads", type=int, default=8, help="num of heads")
parser.add_argument("--e_layers", type=int, default=2, help="num of encoder layers")
parser.add_argument("--d_layers", type=int, default=1, help="num of decoder layers")
parser.add_argument("--d_ff", type=int, default=2048, help="dimension of fcn")
parser.add_argument(
    "--moving_avg", type=int, default=25, help="window size of moving average"
)
parser.add_argument("--factor", type=int, default=1, help="attn factor")
parser.add_argument(
    "--distil",
    action="store_false",
    help="whether to use distilling in encoder, using this argument means not using distilling",
    default=True,
)
parser.add_argument("--dropout", type=float, default=0.05, help="dropout")
parser.add_argument(
    "--embed",
    type=str,
    default="timeF",
    help="time features encoding, options:[timeF, fixed, learned]",
)
parser.add_argument("--activation", type=str, default="gelu", help="activation")
parser.add_argument(
    "--output_attention",
    action="store_true",
    help="whether to output attention in ecoder",
)
parser.add_argument(
    "--do_predict", action="store_true", help="whether to predict unseen future data"
)

# optimization
parser.add_argument(
    "--num_workers", type=int, default=10, help="data loader num workers"
)
parser.add_argument("--itr", type=int, default=2, help="experiments times")
parser.add_argument("--train_epochs", type=int, default=10, help="train epochs")
parser.add_argument(
    "--batch_size", type=int, default=32, help="batch size of train input data"
)
parser.add_argument("--patience", type=int, default=3, help="early stopping patience")
parser.add_argument(
    "--learning_rate", type=float, default=0.0001, help="optimizer learning rate"
)
parser.add_argument("--des", type=str, default="test", help="exp description")
parser.add_argument("--loss", type=str, default="mse", help="loss function")
parser.add_argument("--lradj", type=str, default="type1", help="adjust learning rate")
parser.add_argument(
    "--use_amp",
    action="store_true",
    help="use automatic mixed precision training",
    default=False,
)

# GPU
parser.add_argument("--use_gpu", type=bool, default=True, help="use gpu")
parser.add_argument("--gpu", type=int, default=0, help="gpu")
parser.add_argument(
    "--use_multi_gpu", action="store_true", help="use multiple gpus", default=False
)
parser.add_argument(
    "--devices", type=str, default="0,1,2,3", help="device ids of multile gpus"
)
parser.add_argument(
    "--test_flop", action="store_true", default=False, help="See utils/tools for usage"
)

args = parser.parse_args()

args.use_gpu = True if torch.cuda.is_available() and args.use_gpu else False

if args.use_gpu and args.use_multi_gpu:
    args.dvices = args.devices.replace(" ", "")
    device_ids = args.devices.split(",")
    args.device_ids = [int(id_) for id_ in device_ids]
    args.gpu = args.device_ids[0]

print("Args in experiment:")
print(args)

Exp = ExpMain

if args.is_training:
    for ii in range(args.itr):
        # setting record of experiments
        setting = "et{}_{}_{}_{}_ft{}_sl{}_ll{}_pl{}_dm{}_nh{}_el{}_dl{}_df{}_fc{}_eb{}_dt{}_{}_{}".format(
            args.embed_type,
            args.model,
            args.model_id,
            args.data,
            args.features,
            args.seq_len,
            args.label_len,
            args.pred_len,
            args.d_model,
            args.n_heads,
            args.e_layers,
            args.d_layers,
            args.d_ff,
            args.factor,
            args.embed,
            args.distil,
            args.des,
            ii,
        )

        exp = Exp(args)  # set experiments
        print(">>>>>>>start training : {}>>>>>>>>>>>>>>>>>>>>>>>>>>".format(setting))
        exp.train(setting)

        if not args.train_only:
            print(
                ">>>>>>>testing : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<".format(setting)
            )
            exp.test(setting)

        if args.do_predict:
            print(
                ">>>>>>>predicting : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<".format(
                    setting
                )
            )
            exp.predict(setting, True)

        torch.cuda.empty_cache()
else:
    ii = 0
    setting = "et{}_{}_{}_{}_ft{}_sl{}_ll{}_pl{}_dm{}_nh{}_el{}_dl{}_df{}_fc{}_eb{}_dt{}_{}_{}".format(
        args.embed_type,
        args.model,
        args.model_id,
        args.data,
        args.features,
        args.seq_len,
        args.label_len,
        args.pred_len,
        args.d_model,
        args.n_heads,
        args.e_layers,
        args.d_layers,
        args.d_ff,
        args.factor,
        args.embed,
        args.distil,
        args.des,
        ii,
    )

    exp = Exp(args)  # set experiments

    if args.do_predict:
        print(">>>>>>>predicting : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<".format(setting))
        exp.predict(setting, True)
    else:
        print(">>>>>>>testing : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<".format(setting))
        exp.test(setting, test=1)
    torch.cuda.empty_cache()
