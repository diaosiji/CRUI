# Hybrid-Cloud architecture for better Robotic Understanding in Interaction

This is the project page of Hybrid-Cloud Architecture Augmented Robotic Understanding: A Vision-based Application.

## Introduction

We propose CRUI, a novel Hybrid-Cloud architecture for better Robotic Understanding in Interaction. We successfully apply this system to robotic specific object searching. By adopting conditional Generative Adversarial Network (cGAN) and Internet image services, our system can generate object photo-realistic images for searching as the understanding of human’s visual intentions with the augmentation from Internet services. The experiments on datasets show our method enables robot to comprehend human’s intention more accurately.

## Dataset construction

We construct a dataset to meet the requirements of experiment setting. To train the cGAN, images in the dataset should be paired images, which include an object image and its corresponding sketch. To test our idea, we met several challenges:
- It is difficulty to get the corresponding hand-draw sketch. even we hire some people to draw the sketches under Amazon Mechanical Turk (AMT) mechanism, the quality of sketches would be hard to control. Thus we adopt the [HED](https://github.com/s9xie/hed) and [post-process procedure](https://github.com/phillipi/pix2pix/tree/master/scripts/edges). Please note that the post-process is necessary, it not only transform the brushes into binary edges with one pixel, but also batch processe the abundant images.
- Combine operation. The data samples need to concatenate the object photo and the corresponding sketches. After the HED and post process procedure, we adopt this  [python script](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/docs/datasets.md) from pix2pix to generate training data in the form of pairs of images {A,B}, where A and B are two different depictions of the same underlying scene. The training samples are as follow:

Some training samples from different categories.

- Test datasets construction. Since most images lack key information such as brand logos and so on, we need to augmentate the informaiton to the object photos and do the same HED and post process procedure to get the corresponding edge images. It simulates the sketching procedure when human descrip object using visual informaiton. The edge images can be used as the test datasets for the following evaluation. The test datasets samples are as followed:

Some test samples from different categories.

- Key information augmentation. Thought cGAN can generate object images form edge images, it can not generate detail information well. We use our method to search and augmentate similar information on the object photos, it simulate the second round communicate of human-robot interaction. The augementated images and their corresponding images are as followed:

Some augmentated images for evaluation.

## Training Models

For every category we trained a cGAN model, and test the generation capacity of the architecture under the evaluation metric. The training tips are simple, we put our datasets in the right place and followed the [pix2pix training and test tips](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/docs/tips.md). Then we got 11 trained models.

## Evaluation

### Metric

Once the final synthesis image is generated, the robot needs to roam in environment and search for a object which is similar to the synthesis image, especially by comparing different objects in the same category to find the specific one. Forexample, according to a lady’s sketch, the robot needs to find a “Louis Vuitton” bag in all her bags.We adopt the [Learned Perceptual Image Patch Similarity (LPIPS)](https://github.com/richzhang/PerceptualSimilarity) as our perceptual similarity metric for its effectiveness. Utilizing the LPIPS trained models, we constructe jupyter notebook experiments to do the evaluations.

### Category Evaluation

For every category we trained a cGAN model, and test the generation capacity of the architecture under the evaluation metric. There are three kinds of images that can be compared with the real object image in the test stage: the edge sketch, the primary images generated by cGAN alone, and the final synthesis image generated by our CRUI method. These images will compared with real object image and get three perceptual similarity scores under the LPIPS metric. And for every category we mean three kinds of scores from all the test images to get three mean scores.

The jupyter notebook experments file is under PerceptualSimilarity catalogue.

### Cross Validation Experiment

For a image generated by cGAN and its corresponding synthesis image by CRUI method, we calculate the LPIPS scores with all test object photo, then compute the top1 and top3 precision to see whether the corresponding object can be correctly found in a pile of objects with the same category label. After the cross validation is finished, we get the top1 and top3 accuracy for every object category.

The jupyter notebook experments file is under PerceptualSimilarity catalogue.
