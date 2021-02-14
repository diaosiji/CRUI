# CRUI
Hybrid-Cloud Architecture Augmented Robotic Understanding: A Vision-based Application

## Introduction

Human-Robot Interaction (HRI) has recently re- ceived considerable attention in the communities, and robotic understanding is the foundation for HRI. With the success of deep learning (DL) approaches and rich computing resources provided by cloud services, robots can parse human’s intentions end-to- end more accurately. However, such comprehension capability is limited by the offline knowledge and trained models. In this paper, we propose CRUI, a novel Hybrid-Cloud architecture for better Robotic Understanding in Interaction. We put the DL models and static knowledge on the private cloud, deploy knowledge search service on the public cloud for task orders which beyond the robotic understanding capabilities. We success- fully apply this system to robotic specific object searching. By adopting conditional Generative Adversarial Network (cGAN) and Internet image services, our system can generate object photo-realistic images for searching as the understanding of human’s visual intentions with the augmentation from Internet services. The experiments on datasets show our method enables robot to comprehend human’s intention more accurately

## Dataset construction
We construct a dataset to meet the requirements of ex- periment setting. To train the cGAN, images in the dataset should be paired images, which include an object image and its corresponding sketch.

## Training Models
For every category we trained a cGAN model, and test the generation capacity of the architecture under the evaluation metric.

## Evaluation

### Metric

### Category Evaluation

### Cross Validation Experiment

