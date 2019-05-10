# Tax-Fire

The Ultimate Tax Planning Software

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Input](#input)
4. [Code Description](#code-description)
5. [Authors](#authors)
6. [License](#license)

## Prerequisites

For easy running and development, download a python IDE. I like using PyCharm.

* [PyCharm](https://www.jetbrains.com/pycharm/)

## Setup

`tpmain.py` and its functions shall be located in the "main directory" from which code runs will be executed.
For example, the main directory might be named `tax_planner\`:
```
C:\Users\Matt\PycharmProjects\tax_planner\
```
A subdirectory shall be located in the main directory and defined as `cases\`: 
```
C:\Users\Matt\PycharmProjects\tax_planner\cases\
```
The `cases\` subdirectory shall contain the user's cases he/she will run. Each case will be a seperate folder. 
The user's cases shall be defined as the tax year. 
It is imperative that the working case is defined as the `Tax Year` input given in `tp.inp`.
For example, a user may want to plan taxes for 2019; therefore, a new folder in `cases\` will be created as `2019\`, and,
the `tp.inp` file will show the `Tax Year` input as `2019`.
The path to this working case would look like:
```
C:\Users\Matt\PycharmProjects\tax_planner\cases\2019\
```
The specific case-year folder shall contain the input files necessary to run the code successfully.
The required input files are listed below:

1. `fedwages.inp`
2. `fedwithholding.inp`
3. `'state abbreviation'wages.inp`, where 'state abbreviation' = the `State Abbreviations` used in `tp.inp`
4. `'state abbreviation'withholding.inp`, where 'state abbreviation' = the `State Abbreviations` you use in `tp.inp`

For example, if you lived in Maryland and Georgia in 2019 and were filing partial returns in each of these states,
and `tp.inp` listed the `State Abbreviations` as `md` and `ga`, the required input files found in
```
C:\Users\Matt\PycharmProjects\tax_planner\cases\2019\
``` 
would be:

1. `fedwages.inp`
2. `fedwithholding.inp`
3. `mdwages.inp`
4. `gawages.inp`
5. `mdwithholding.inp`
6. `gawithholding.inp`

Lastly, `tp.inp` itself shall be located in the main directory, or in this case, `tax_planner\`.

If using PyCharm IDE, and with the directories and case folders setup in this way, the user simply pushes the green
play button to run the case.

## Input

go through each input file

## Code Description

go through code descriptions

## Authors

* **Matt Thomas** - [MattThomas9](https://github.com/MattThomas9)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details
