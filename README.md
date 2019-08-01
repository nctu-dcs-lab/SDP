# Software Defect Prediction

This project aims to make experiment for SDP much more easier. All the components are combined and examined the performance of every combinations.

## Requirement

- Python 3.5
- pip3

## Install & Run

1. (Optional) `virtualenv env -p python3` & `source env/bin/activate`
2. `pip3 install -r requirements.txt`
   - May have some errors while installing graphic related package on different system
3. `cd src`
4. `python3 run.py`

## Project Structure

- data
  - **Empty directory**, synchronized data will be saved at here
- origin_data
  - Original source of the dataset
- R
  - Implementation in R
- report
  - **Empty directory**, generated report will be here
- src
  - Source code

## Module Description

- [setting.py](src/setting.py)
  -  Contains all the framework variables ( e.g. dataset path, selected dataset, selected methods, selected feature selection methods )
- [run.py](src/run.py)
  - Entry module that trigger everyother modules to start the process
- [dataset.py](src/dataset.py)
  - Handling dataset preprocessing
- [feature.py](src/feature.py)
  - Contain functions that take feature and label as input and return the data with selected metrics depending on different implementations
- [models.py](src/models.py)
  - Core module of the framework that contain unsupervised methods for SDP. They are expected to take data as input, and output an one­dimensional array which classify every entities. 1 as defective and 0 as non­defective

## Default dataset link

- [AEEEM](http://bug.inf.usi.ch/index.php)
- [NASA](https://figshare.com/collections/NASA_MDP_Software_Defects_Data_Sets/4054940)
- [PROMISE](https://zenodo.org/search?page=1&size=20&q=Marian%20Jureckzo&file_type=csv#)

## Citation
