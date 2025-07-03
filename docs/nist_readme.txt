NIST Data Publication:
Noise Datasets for Evaluating Deep Generative Models
DOI: https://doi.org/10.18434/mds2-3034

Authors:
  Adam Wunderlich
    National Institute of Standards and Technology
  Jack Sklar
    National Institute of Standards and Technology

Contact:
  Adam Wunderlich
    adam.wunderlich@nist.gov

Description:

Synthetic training and test datasets for experiments on deep generative modeling
of noise time series.  Contains data for the following noise types: 1) band-
limited thermal noise, i.e., bandpass filtered white Gaussian noise, 2) power
law noise, including fractional Gaussian noise (FGN), fractional Brownian motion
(FBM), and fractionally differenced white noise (FDWN), 3) generalized shot
noise, 4) impulsive noise, including Bernoulli-Gaussian (BG) and symmetric alpha
stable (SAS) distributions.  Documentation of simulation methods and experiments 
with Generative Adversarial Networks (GANs) are given in the paper "Data-Driven Modeling 
of Noise Time Series with Convolutional Generative Adversarial Networks" 
preprint: https://arxiv.org/abs/2207.01110.  Associated software is publicly available 
at https://github.com/usnistgov/NoiseGAN.  

--------------
Data Use Notes
--------------

This data is publicly available according to the NIST statements of
copyright, fair use and licensing; see
https://www.nist.gov/director/copyright-fair-use-and-licensing-statements-srd-data-and-software

You may cite the use of this data as follows:

Wunderlich, Adam and Sklar, Jack (2023), Noise Datasets for Evaluating Deep
Generative Models, National Institute of Standards and Technology, 
https://doi.org/10.18434/mds2-3034 (Accessed: [give download date])

----------
References
----------

A. Wunderlich, J. Sklar, "Data-Driven Modeling of Noise Time Series with Convolutional Generative
Adversarial Networks", 2023, submitted. Preprint: https://arxiv.org/abs/2207.01110

A. Wunderlich, J. Sklar, "NoiseGAN: Software for Evaluating Convolutional Generative Adversarial Networks with Classical 
Random Process Noise Models," 2023. https://github.com/usnistgov/NoiseGAN

-------------
File List
-------------
A. bandpass.tar.gz 
   Short description: Training and test datasets of bandpass thermal noise
B. BG.tar.gz 
   Short description: Training and test datasets of Bernoulli-Gaussian (BG) impulsive noise
C. FBM.tar.gz 
   Short description: Training and test datasets of Fractional Brownian Motion (FBM)
D. FDWN.tar.gz 
   Short description: Training and test datasets ofFractionally Differenced White Noise (FDWN)
E. FGN.tar.gz 
   Short description: Training and test datasets of Fractional Gaussian Noise (FGN)
F. SAS.tar.gz 
   Short description: Training and test datasets of Symmetric Alpha Stable (SAS) impulsive noise
G. shot.tar.gz 
   Short description: Training and test datasets of generalized shot noise
H. model_results.tar.gz 
   Short description: GAN results for each target distribution.

-------------
Data Overview
-------------
Target distribution training and test sets for various classical noise models
are provided in the following tarball (tar.gz) files: bandpass.tar.gz, BG.tar.gz, 
FBM.tar.gz, FDWN.tar.gz, FGN.tar.gz, SAS.tar.gz, shot.tar.gz. 

Each file above has the same basic structure, consisting of subdirectories
with data for a given set of noise model parameters.  Specifically, each subdirectory 
contains a noise_params.json file listing target distrubution attributes and 
hierarchical data format 5 (HDF5) files named test.h5 and train.h5 with test and train 
datasets, respectively.  These files were created with the utils/noise_dataset.py module 
in the NoiseGAN software repository referenced above by running main() as a script.  
In the bandpass thermal noise subdirectories, there is an additional file, 
named sos_coeffs.json, containing second-order-section filter coefficients. 

The json files can be loaded with the following example python code, where
dir_path denotes the path string:

import json, os
with open(os.path.join(dir_path, 'noise_params.json')) as F:
	noise_dict = json.load(F)

The train and test datasets each contain 16384 and 4096 samples, respectively, of real-valued 
time series of length 4096.  The following example python code can be used to load the data files, 
where filename.h5 denotes the filename: 

import h5py, os
h5f = h5py.File(os.path.join(dir_path, 'filename.h5'), 'r')
dataset = h5f['train'][:]
h5f.close()
targ_param_values = dataset[:, 0])
targ_data = dataset[:, 1:]

In addition to the aforementioned target distribution data files, the file model_results.tar.gz 
contains GAN model results given in the paper referenced above, as well as additional 
results not presented in the paper.  Specifically, within directories for each 
noise type, there are subdirectories for each noise parameter value, themselves containing 
subdirectories for each model run, named with a date-time stamp.  Each model run directory 
consists of the following files:

gan_train_config.json 
   Short description: A json file specifying the GAN training configuration.
gen_distribution.h5 
   Short description: An HDF5 file containing GAN-generated test data, consisting 
                      of 4096 time series of length 4096.  
gan_training_history.csv
   Short description: A CSV (comma-separated values) file containing losses and 
                      discriminator outputs from GAN training.
Gan_training_loss.png
   Short description: Plot of generator and discriminator losses during training.
Gan_D_output.png
   Short description: Plot of discriminator outputs, 
                      as well as the gradient penalty term, during training.

Example python code to load the training configuration file is below:

import json, os
with open(os.path.join(dir_path, 'gan_train_config.json'), 'r') as fp:
	train_specs_dict = json.loads(fp.read())

Example python code to load the generated test data is below:

import h5py, os
h5f = h5py.File(os.path.join(dir_path, 'gen_distribution.h5'), 'r')
gen_data = h5f['test'][:]
h5f.close()