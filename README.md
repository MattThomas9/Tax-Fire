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

1. [Main Input](#main-input)
2. [Federal and State Wages and Withholding Input](#federal-and-state-wages-and-withholding-input)
3. [Input Summary](#input-summary)

### Main Input

`tp.inp` is the main input file used for the tax planner program.
`tpmain.py` reads `tp.inp` by parsing through the file using python configparser and searching
for pre-determined phrases (see `tpmain.py` input processing section). For example, in `tp.inp`, `Tax Year` is a pre-determined
phrase to prompt the user to enter which tax year he/she is planning. `Tax Year` is what tpmain.py parses for to
read in the corresponding variable `ntaxyear`.

If input needs to be added to `tp.inp`, simply follow the same format as other variables. However, if you need to add input,
you will also need to modify the input processing section of `tpmain.py`, in order to get the program to read in the additional input. 
You'll determine a phrase which represents the variable you will read in. For
example, lets say you want to modify the code to read in a new variable, call it, `headtype`. So in `tp.inp` you should
determine a phrase that will help the user understand what they need to input. For example, `tp.inp` would have a line
that looks like this:
```
Head Type: football
```
So in the example above, the variable is `headtype` (i.e. `tpmain.py` will read in as variable `headtype`), 
the input line is `Head Type:` and the input value is `football`. Next, you'll need to add a `config.get` line in `tpmain.py` input
processing section that will read in this new variable. It'll look like this:
```
headtype = config.get('Code Control', 'Head Type')
```
Note that the first argument of `config.get` is the corresponding `[Section]` of `tp.inp`. So `Head Type: football`
would be found in the `[Code Control]` section of tp.inp.

**DO NOT put in-line comments in `tp.inp`. The configparser class by default does not allow in-line comments and may screw
up your input processing.**

`Detailed Print:` - is essentially just a debug mode - its purpose is to print various variables used along the way
in the code. Using Detailed Print helps you double check that things are being calculated correctly. However, it
is currently not implemented in `tpmain.py`. If it is to be used in `tpmain.py`, or any other routine, simply use:
```
if idetprnt == 'yes':
    print('WhateverVariableYouWantToSeeToScreen')
```
`Number of Completed Pay Periods:` - is used for tax planning and optimizing your predicted refund based on your
current withholding status. So if you just got pay period 15 pay check, and have updated your withholding and wages
input file, you'll put `15` in for this variable. When its the last pay period, the code will recognize it and
essentially not try to optimize your refund anymore because you wouldn't be able to make any changes to your
biweekly withholding anyways.

`Previous Year Federal Standard Deduction:` - is required for help in determining if any state refunds you got last
year are federally taxable in the current year.

For `[State Tax Information]` section in `tp.inp`, you'll input this information in horizontally, so side by side.
For example:
```
[State Tax Information]
Number of States Lived in:  3
State Abbreviations:           md       tn       ga
State Deduction Method:  standard standard standard
State Standard Deduction: 1500.00     0.00  4600.00
State Exemption:          3200.00     0.00  2700.00
State Additions:          2400.00  1900.00   900.00
State Subtractions:       2750.00  2750.00     0.00
```
If only lived in one state, then just put in one state's worth of information.

**Note: The order of the states listed in `State Abbreviations` is important and must be consistent with the ordering of the
`State Tax Brackets and Rates` input of the `[Tax Brackets, Rates, Etc.]` section of `tp.inp`.**

In the `[Income Information]` and `[Adjustments to Income]` sections, put self and spouse's information in side-by-side.

In the `[State Tax Refunds from Previous Year (1099-G)]` section of `tp.inp`, this information must be put in to determine
if any prior year state tax refunds are taxable in the current year. So you are inputting your prior year information here.

Itemized deduction information is inputted in the `[Itemized Deduction Information]` section of `tp.inp`. Note, you are
**NOT** to manually enter your year-to-date state tax withholding here. That is automatically determined by `tpmain.py`
and automatically factored into the itemization routine.

Tax bracket input is written in `tp.inp` under `[Tax Brackets, Rates, Etc.]` section in the following format:
```
# Long Term Capital Gains Rates
Number of LTCG Brackets: 3
LTCG Brackets and Rates: 0.00  39375.00  0.00
                     39375.00 434550.00 15.00
                    434550.00       inf 20.00
```
The above example shows the required format for inputting tax bracket information. The `Number of LTCG Brackets:`
input is so that the code knows there are `3` discrete brackets and corresponding rates for the LTCG tax bracket
table. The tax table consists of a minimum, maximum, and tax rate on each line corresponding to each bracket.
Same goes for federal and state tax brackets.

As an example for multi-state tax planning cases with this program, below is an example of how multiple state tax
brackets are formatted in `tp.inp`:
```
# State Income Tax Brackets (put in same order as istateab)
# state 2 brackets below state 1 brackets, state 3 below state 2, etc.
Number of State Tax Brackets: 8 1 6
State Tax Brackets and Rates: 0.00   1000.00  2.00
                           1000.00   2000.00  3.00
                           2000.00   3000.00  4.00
                           3000.00 100000.00  4.75
                         100000.00 125000.00  5.00
                         125000.00 150000.00  5.25
                         150000.00 250000.00  5.50
                         250000.00       inf  5.75
                              0.00       inf  0.00
                              0.00    750.00  1.00
                            750.00   2250.00  2.00
                           2250.00   3750.00  3.00
                           3750.00   5250.00  4.00
                           5250.00   7000.00  5.00
                           7000.00       inf  5.75
```
In the above state tax bracket example, you'll see there are `3` states for which you are planning taxes.
`Number of State Tax Brackets: 8 1 6` is put in horizontally. This means that state #1 has `8` brackets, state #2 has
`1` bracket, and state #3 has `6` brackets. The corresponding brackets are then input in vertically using the format:
```
min max rate 
```
You'll note that for state #2, which has `1` bracket, it's bracket is `0` to `inf` at a `0.0%` rate (i.e. no state
taxes in this state). Also, enter the rates of each bracket in as a percent.

**Note: The order of the `State Tax Brackets and Rates` shall follow the same order of the states listed in `State Abbreviations`
in the `[State Tax Information]` section of `tp.inp`**

The below is an example for inputting in the local tax rates:
```
# Local Income Tax Rates (put in same order as istateab)
# probably will only ever have 1 local per state.
# number of local tax rates go in side by side, and tax rates themselves go in side by side too
Number of Local Tax Rates: 1 0 3
Local Tax Rates (%): 3.20 1.50 2.40 1.70
```
So above, this input means for your first state, you have `1` local tax rate that will be included in your state tax
calculation. You have `0` local tax rates for state #2, and `3` local tax rates for state #3. Another example given
below:
```
Number of Local Tax Rates: 1 2 1
Local Tax Rates (%): 3.20 1.50 2.40 1.70
```
The above scheme means that there is `1` local tax rate for state #1 of `3.2%`, `2` local tax rates for state #2 of `1.5%`
and `2.4%`, and `1` local tax rate for state #3 of `1.7%`

See Appendix A for an example of an entire functioning `tp.inp` file with important comments about various inputs.

### Federal and State Wages and Withholding Input



### Input Summary



## Code Description

go through code descriptions

## Authors

* **Matt Thomas** - [MattThomas9](https://github.com/MattThomas9)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details
