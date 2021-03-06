# EvaluationHelper-NN

## Introduction
---

This Project is an assignment for an introductory python course of the Institute of Technology Karlsruhe, Germany (KIT). It's a lightweight neural network model with one hidden layer and can be trained to analyze the KIT survey sheets for university courses. It is a simple implementation built from scratch using only numpy for computation and pillow for image processing.

## Brief Overview of the Model and Program Structure
---

An evaluation sheet consists of 14 multiple choice questions each providing five boxes for the students to check.

The network is trained to classify, whether a box is checked or not. The input layer with 1600 nodes corresponds to a picture of a box with size 40x40 pixels. It is implemented with one hidden layer using a sigmoid function as the activation function and the cross-entropy-cost function as a loss function. The default parameters for training are batches of 50 and 30 epochs of training.

When you start the evaluation, a corner detection routine is launched. With the detected corners, sheets that have been scanned with small displacements can be adjusted and the positions of all question boxes can be determined. Next, all boxes are cut out as a 40x40 pixel image and a pre-trained model will predict whether or not the box are checked. For each of the boxes this information is saved and the program will display interesting statistics to the user.

## How use EvaluationHelper-NN
---

### Start the evaluation


Download the project to your local machine. Make sure to have numpy and PIL installed. There are no additional dependencies required.
The main entry point to the program is launch.py located in the projects `src` directory. It can be started using the command line terminal. Navigate to the `src` directory in the project's root directory :
```
cd src
```
After starting the program with
```
python launch.py
```
you will be prompted to enter the path to a directory with the scanned surveys.

The terminal output will provide information about the progress of the EvaluationHelper and print interesting statistics for each of the analyzed survey sheets.

### How to Read the Survey Statistics

The create_print_statistics() routine will provide a block of information about each individual survey sheet.
```
Sheet number:  23
++(2): 5 , +(1): 3 , 0(0): 2 , -(-1): 1 , --(-2): 1
Answered questions: 12 / 14
Question was not answered:  [11, 12]
Average:  0.833
Variance: 1.639
```
The first line will tell you the number of the analyzed sheet.

Each question of the survey can be answered with five measures of agreement:
```
++ - fully agree
+  - agree somewhat
0  - indifferent
-  - disagree somewhat
-- - completely disagree
```

The second line of each statistics block tells you how often each of these five options have been checked. For instance, in the example above this would mean in sheet 23 "fully agree" has been checked five times.

The statistics of a survey sheet will also tell you how many of the  questions have been answered at all, which questions have been answered multiple times as well as the average and the variance of the five options to answer. With ++ equating to 2 down to -- equating to -2.



### How to Use Previously Detected Corners

To adjust slight displacement of the scanned sheets the `create_reference()` function called in launch.py will start a corner detection routine per default. The information about the detected corners is saved to `/data/corners.json`. If you want to use the detected corners from a previous run, change the first argument in the function call in line 35 of launch.py to `False` as seen below:

```python
create_reference(False, usr_boegen_path, paths[1], paths[0], paths[3], paths[2], reference_sheet_name)
```

### How to Retrain the Neural Network

Per default the program will use a pre-trained model. The information about its weights and biases are stored in `/data/model.json`. You can retrain the model using the existing dataset by navigating to the `nn` directory

```
cd src/nn
```
and starting the routine to train the model with

```
python train.py
```

It is possible to change the running parameters of the training like `batch size` or `number of epochs` by passing arguments.

```
python train.py -e 40 -b 60
```
This will train the model with 40 epochs and batches of 60. To see all the possible arguments, look at the argparser in `train.py`'s main function.

After training, your latest run will be saved to the `/data/runs/`directory. If you want the newly trained model to be used in launch.py, replace the `model.json` inside the `/data/` directory with the new `model.json` that was saved to the training run directory.

## Authors
???? Nikita Nesterov: https://github.com/SidanPukich

???? Johannes Viet An Nguyen: https://github.com/vietanng

???? Nando Suntoyo: https://github.com/NandoSun
