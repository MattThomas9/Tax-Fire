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

`fedwages.inp` is the file you use to input your federal wages. This file is read by `tpmain.py` in the same way
`tpmain.py` reads `tp.inp`, that is, with the `configparser` class. Therefore, proper formatting of this file is required
and in-line comments are not to be used. Each line corresponds to the pay period, your wages, then spouse's wages.

An example of `fedwages.inp` formatting is below:
```
[Federal Wage Information]
Federal Wages: 1        3000.00        0.00
               2        2900.00        0.00
               3        3100.00        0.00
               4        2800.00        0.00
               5        2950.00        0.00
```
`fedwages.inp` shall contain a Section defined as `[Federal Wage Information]`. 

`fedwages.inp` should also contain an input line defined as `Federal Wages:` and from there the user should input 
the federal wage information in the defined format as seen above.

**NOTES:**

**1. The sum of `Federal Wages` found in `fedwages.inp` should ultimately equal the value provided in `tp.inp` under the `[Income Information]` section for `Wages Salary Tips:`. If these values do not equal one another, the user will see a warning appear in the output printed to screen.**

**2. Currently, because this is a tax calculator/planner program, the wages that are inputted into this program via `fedwages.inp` and `tp.inp` are wages that SHOULD NOT include pre-tax benefits. In other words, the wages that are inputted into this program should be gross pay less pre-tax benefits (e.g. pre-tax health insurance benefits, traditional 401k/TSP contributions, etc.). If you put in wages that include your pre-tax benefits (i.e. gross pay alone) the program will calculate tax on income that shouldn't be taxed and thus overestimate your taxes.**

If you are filing single, put in `0.00` as your spouse's wages, which is inputted right beside your wages, as seen in the format
for `fedwages.inp` above. The same input format is used for your state wage input as well.

In `tp.inp`, you will have inputted each state's abbreviated name for which you are planning taxes. So for example,
`tp.inp` might have something like:
```
Number of States Lived in:  3
State Abbreviations:           md       tn       ga
```
which means you also need `3` corresponding state wages files. The state wages files must also be preceded by the same
abbreviation you input into `tp.inp`. So considering the 3-state filing example above, the user will need to have:
```
mdwages.inp
tnwages.inp
gawages.inp
```
Each `'state'wages.inp` file is in the same format as `fedwages.inp`. An example of `'state'wages.inp` format is below:
```
[State Wage Information]
State Wages: 1        3000.00        0.00
             2        2900.00        0.00
             3        3100.00        0.00
             4        2800.00        0.00
             5        2950.00        0.00
```
Same goes for `fedwithholding.inp` and your `'state'withholding.inp` files. Following the 3-state filing example above,
all of your withholding files will be named:
```
fedwithholding.inp
mdwithholding.inp
tnwithholding.inp
gawithholding.inp
```
An example of `fedwithholding.inp` format is provided below:
```
[Federal Withholding Information]
Federal Withholding: 1          540.62            0.0
                     2          1025.4            0.0
                     3          642.96            0.0
```
For `'state'withholding.inp`, it would look like this:
```
[State Withholding Information]
State Withholding: 1          273.31            0.0
                   2          458.84            0.0
                   3          111.95            0.0
```
**NOTES:**

**1. Inside each `'state'wages.inp` and `'state'withholding.inp file`, there is no specific designation within these files that indicates which state the information is for. The only designation for which state the wage and withholding information is for is contained only in the file name itself.**

**2. In the Federal and State wage and withholding input file examples above, each line corresponds to the pay-period's wage or withholding. Therefore, if in `tp.inp` you have `Number of Total Pay Periods:  26`, you ought to have `26` line items worth of wage/withholding information in each respective file.**

### Input Summary



## Code Description

go through code descriptions

## Authors

* **Matt Thomas** - [MattThomas9](https://github.com/MattThomas9)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details
