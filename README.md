# Hybrid-Cloud architecture for better Robotic Understanding in Interaction

This is the project page of Hybrid-Cloud Architecture Augmented Robotic Understanding: A Vision-based Application.

## Introduction

Human-Robot Interaction (HRI) has recently received considerable attention in the communities, and robotic understanding is the foundation for HRI. With the success of deep learning (DL) approaches and rich computing resources provided by cloud services, robots can parse human’s intentions end-to-end more accurately. However, such comprehension capability is limited by the offline knowledge and trained models. In this paper, we propose CRUI, a novel Hybrid-Cloud architecture for better Robotic Understanding in Interaction. We put the DL models and static knowledge on the private cloud, deploy knowledge search service on the public cloud for task orders which beyond the robotic understanding capabilities. We successfully apply this system to robotic specific object searching. By adopting conditional Generative Adversarial Network (cGAN) and Internet image services, our system can generate object photo-realistic images for searching as the understanding of human’s visual intentions with the augmentation from Internet services. The experiments on datasets show our method enables robot to comprehend human’s intention more accurately.

## Dataset construction
We construct a dataset to meet the requirements of experiment setting. To train the cGAN, images in the dataset should be paired images, which include an object image and its corresponding sketch. To test our idea, we met several challenges:
- It is difficulty to get the corresponding hand-draw sketch. even we hire some people to draw the sketches under Amazon Mechanical Turk (AMT) mechanism, the quality of sketches would be hard to control. Thus we adopt the [HED](https://github.com/s9xie/hed) 
- and [post-process procedure](https://github.com/phillipi/pix2pix/tree/master/scripts/edges). Please note that the post-process is necessary, it not only transform the brushes into binary edges with one pixel, but also batch processe the abundant images.
- combine operation.
- Key information augmentation.


## Training Models
For every category we trained a cGAN model, and test the generation capacity of the architecture under the evaluation metric. 

## Evaluation

### Metric

Once the final synthesis image is generated, the robot needs to roam in environment and search for a object which is similar to the synthesis image, especially by comparing different objects in the same category to find the specific one. Forexample, according to a lady’s sketch, the robot needs to find a “Louis Vuitton” bag in all her bags.We adopt the [Learned Perceptual Image Patch Similarity (LPIPS)](https://github.com/richzhang/PerceptualSimilarity) as our perceptual similarity metric for its effectiveness.


### Category Evaluation

### Cross Validation Experiment

