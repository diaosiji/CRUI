# Hybrid-Cloud architecture for better Robotic Understanding in Interaction

This is the project page of Hybrid-Cloud Architecture Augmented Robotic Understanding: A Vision-based Application.

## Introduction

We propose CRUI, a novel Hybrid-Cloud architecture for better Robotic Understanding in Interaction. We successfully apply this system to robotic specific object searching. By adopting conditional Generative Adversarial Network (cGAN) and Internet image services, our system can generate object photo-realistic images for searching as the understanding of human’s visual intentions with the augmentation from Internet services. 

Our project mainly benefit form [pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix), [HED](https://github.com/s9xie/hed) and [PerceptualSimilarity](https://github.com/richzhang/PerceptualSimilarity) project and their corresponding papers. If you want to run our code, be sure to meet the prerequisites of these projects.

## Dataset construction

### Construction detials

We construct a dataset to meet the requirements of experiment setting. To train the cGAN, images in the dataset should be paired images, which include an object image and its corresponding sketch. To test our idea, we met several challenges:
- It is difficulty to get the corresponding hand-draw sketch. even we hire some people to draw the sketches under Amazon Mechanical Turk (AMT) mechanism, the quality of sketches would be hard to control. Thus we adopt the [HED](https://github.com/s9xie/hed) and [post-process procedure](https://github.com/phillipi/pix2pix/tree/master/scripts/edges). Please note that the post-process is necessary, it not only transform the brushes into binary edges with one pixel, but also batch processe the abundant images.
- Combine operation. The data samples need to concatenate the object photo and the corresponding sketches. After the HED and post process procedure, we adopt this  [python script](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/docs/datasets.md) from pix2pix to generate training data in the form of pairs of images {A,B}, where A and B are two different depictions of the same underlying scene. The training samples are as follow:


![handbag](https://github.com/diaosiji/CRUI/blob/main/readme_fig/training_samples/27_AB.jpg) 

![backpack](https://github.com/diaosiji/CRUI/blob/main/readme_fig/training_samples/backpack_00029.jpg)

![mouse](https://github.com/diaosiji/CRUI/blob/main/readme_fig/training_samples/mouse_00004.jpg)

![shoe](https://github.com/diaosiji/CRUI/blob/main/readme_fig/training_samples/3_AB.jpg)

- Test datasets construction. Since most images lack key information such as brand logos and so on, we need to augmentate the informaiton to the object photos and do the same HED and post process procedure to get the corresponding edge images. It simulates the sketching procedure when human descrip object using visual informaiton. The edge images can be used as the test datasets for the following evaluation. The test datasets samples are as followed:

![1](https://github.com/diaosiji/CRUI/blob/main/readme_fig/test_samples/backpack_00231.jpg) ![2](https://github.com/diaosiji/CRUI/blob/main/readme_fig/test_samples/headphones_00148.jpg) ![3](https://github.com/diaosiji/CRUI/blob/main/readme_fig/test_samples/7_AB.jpg) ![4](https://github.com/diaosiji/CRUI/blob/main/readme_fig/test_samples/helmet_00126.jpg) ![5](https://github.com/diaosiji/CRUI/blob/main/readme_fig/test_samples/mug_00160.jpg) ![6](https://github.com/diaosiji/CRUI/blob/main/readme_fig/test_samples/calculator_00175.jpg)

- Key information augmentation. Thought cGAN can generate object images form edge images, it can not generate detail information well. We use our method to search and augmentate detail information on the object photos, it simulate the second round communicate of human-robot interaction in our method. The augementated images and their corresponding origin images are as followed:

![1](https://github.com/diaosiji/CRUI/blob/main/readme_fig/augment_samples/backpack_00228.png) ![2](https://github.com/diaosiji/CRUI/blob/main/readme_fig/augment_samples/calculator_00171.png) ![3](https://github.com/diaosiji/CRUI/blob/main/readme_fig/augment_samples/computer_00142.png)

![4](https://github.com/diaosiji/CRUI/blob/main/readme_fig/augment_samples/headphones_00148.png) ![5](https://github.com/diaosiji/CRUI/blob/main/readme_fig/augment_samples/helmet_00126.png) ![6](https://github.com/diaosiji/CRUI/blob/main/readme_fig/augment_samples/mouse_00190.png)

### Dataset and pretrained models download

We have published our datasets and pretrained models on google drive for common interests of researching. We probide 11 object category, you can download them at [here](). And also, we provide 11 pretrained models, you can download them at [here](). 

## Training Models

For every category we trained a cGAN model, and test the generation capacity of the architecture under the evaluation metric. The training tips are simple, we put our datasets in the right place and followed the [pix2pix training and test tips](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/docs/tips.md). Then we got 11 trained models, these models are right in the ```/pytorch-CycleGAN-and-pix2pix/checkpoints/``` catalogue. In the evaluation section, we utilize the trained models to generate the primal object images as the understanding of human visual description.

## Evaluation

### Metric

We adopt the [Learned Perceptual Image Patch Similarity (LPIPS)](https://github.com/richzhang/PerceptualSimilarity) as our perceptual similarity metric for its effectiveness. Utilizing the LPIPS trained models, we constructe jupyter notebook experiments to accomplish the evaluations. LPIPS simply compares two images and output a score, and **a lower LPIPS metric score means higher similarity between the compared images**.

### Category Evaluation

For every category we trained a cGAN model, and test the generation capacity of the architecture under the evaluation metric. There are three kinds of images that can be compared with the real object image in the test stage: the edge sketch, the primary images generated by cGAN alone, and the final synthesis image generated by our CRUI method. These images will compared with real object image and get three perceptual similarity scores under the LPIPS metric, different kinds of image samples are as followed:

![1](https://github.com/diaosiji/CRUI/blob/main/readme_fig/compare_samples/backpack_00228.png) ![2](https://github.com/diaosiji/CRUI/blob/main/readme_fig/compare_samples/backpack_00228.jpg)

![3](https://github.com/diaosiji/CRUI/blob/main/readme_fig/compare_samples/backpack_00228_2.png) ![4](https://github.com/diaosiji/CRUI/blob/main/readme_fig/compare_samples/backpack_00228_3.png)

For every category we mean three kinds of scores from all the test images to get three mean scores.

**The jupyter notebook experments file is under ```CRUI/tree/main/PerceptualSimilarity/compute_dists_cross_validation.ipynb```.**

### Cross Validation Experiment

For a image generated by cGAN and its corresponding synthesis image by CRUI method, we calculate the LPIPS scores with all test object photo, then compute the top1 and top3 precision to see whether the corresponding object can be correctly found in a pile of objects with the same category label. After the cross validation is finished, we get the top1 and top3 accuracy for every object category.

**The jupyter notebook experments file is under ```CRUI/tree/main/PerceptualSimilarity/compute_dists_cross_validation.ipynb```.**
