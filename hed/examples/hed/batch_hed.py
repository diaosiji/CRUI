# HED batch processing script; modified from https://github.com/s9xie/hed/blob/master/examples/hed/HED-tutorial.ipynb
# Step 1: download the hed repo: https://github.com/s9xie/hed
# Step 2: download the models and protoxt, and put them under {caffe_root}/examples/hed/
# Step 3: put this script under {caffe_root}/examples/hed/
# Step 4: run the following script:
#       python batch_hed.py --images_dir=/data/to/path/photos/ --hed_mat_dir=/data/to/path/hed_mat_files/
# The code sometimes crashes after computation is done. Error looks like "Check failed: ... driver shutting down". You can just kill the job.
# For large images, it will produce gpu memory issue. Therefore, you better resize the images before running this script.
# Step 5: run the MATLAB post-processing script "PostprocessHED.m"


import numpy as np
from PIL import Image
import os
import argparse
import sys
import scipy.io as sio

# save ndarray to image
import scipy.misc as misc


def parse_args():
    parser = argparse.ArgumentParser(description='batch proccesing: photos->edges')
    # test
    # parser.add_argument('--caffe_root', dest='caffe_root', help='caffe root', default='../../', type=str)
    parser.add_argument('--caffe_root', dest='caffe_root', help='caffe root', default='/caffe/', type=str)
    parser.add_argument('--caffemodel', dest='caffemodel', help='caffemodel', default='./hed_pretrained_bsds.caffemodel', type=str)
    parser.add_argument('--prototxt', dest='prototxt', help='caffe prototxt file', default='./deploy.prototxt', type=str)
    parser.add_argument('--images_dir', dest='images_dir', help='directory to store input photos', type=str)
    parser.add_argument('--hed_mat_dir', dest='hed_mat_dir', help='directory to store output hed edges in mat file', type=str)
    parser.add_argument('--border', dest='border', help='padding border', type=int, default=128)
    # parser.add_argument('--gpu_id', dest='gpu_id', help='gpu id', type=int, default=1)
    # For pix2pix project cpu mode
    parser.add_argument('--gpu_id', dest='gpu_id', help='gpu id', type=int, default=0)
    args = parser.parse_args()
    return args


args = parse_args()
for arg in vars(args):
    print('[%s] =' % arg, getattr(args, arg))
# Make sure that caffe is on the python path:
caffe_root = args.caffe_root   # this file is expected to be in {caffe_root}/examples/hed/
sys.path.insert(0, caffe_root + 'python')
import caffe


if not os.path.exists(args.hed_mat_dir):
    print('create output directory %s' % args.hed_mat_dir)
    os.makedirs(args.hed_mat_dir)

imgList = os.listdir(args.images_dir)
nImgs = len(imgList)
print('#images = %d' % nImgs)

# try 
#caffe.set_mode_gpu()
caffe.set_mode_cpu()
# try
#caffe.set_device(args.gpu_id)
#caffe.set_device(0)

# load net
net = caffe.Net(args.prototxt, args.caffemodel, caffe.TEST)
# pad border
border = args.border

for i in range(nImgs):
    if i % 500 == 0:
        print('processing image %d/%d' % (i, nImgs))
    im = Image.open(os.path.join(args.images_dir, imgList[i]))

    in_ = np.array(im, dtype=np.float32)
    # There are 11 mode:constant,reflect,edge and so on
    in_ = np.pad(in_, ((border, border), (border, border), (0, 0)), 'reflect')

    in_ = in_[:, :, 0:3]
    # switch to BGR
    in_ = in_[:, :, ::-1]
    # subtract mean
    in_ -= np.array((104.00698793, 116.66876762, 122.67891434))
    # make dims C x H x W for Caffe
    in_ = in_.transpose((2, 0, 1))

    # remove the following two lines if testing with cpu

    # shape for input (data blob is N x C x H x W), set data
    net.blobs['data'].reshape(1, *in_.shape)
    net.blobs['data'].data[...] = in_
    # run net and take argmax for prediction
    net.forward()
    fuse = net.blobs['sigmoid-fuse'].data[0][0, :, :]
    # get rid of the border
    #fuse = fuse[border:-border, border:-border]
    # from 32+128 to 32+128+256,the 32 can be adjust! 34,35,
    fuse = fuse[163:419, 163:419]
    # save hed file to the disk
    # temporary ignore the following two lines for edge shift problem search
    name, ext = os.path.splitext(imgList[i])
    sio.savemat(os.path.join(args.hed_mat_dir, name + '.mat'), {'predict': fuse})
    
    # test code for fuse visualization
    # 1. get to know fuse data structure -> <type 'numpy.ndarray'>
    #print(type(fuse))
    #print(fuse.size)
    #print(fuse.shape)
    # clip float32 value range to [0.0-1.0]
    #fuse = np.clip(fuse, 0.0, 1.0)
    # output image
    #Image.fromarray(((fuse - 1.0) * (- 255.0)).astype(np.uint8)).save('./out.png')






