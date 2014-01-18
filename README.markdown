# snogweb

## Installation
First, clone the repository

    git clone git://github.com/bwesterb/snogweb

### Dependencies
Then, install the dependency: TeXlive and pydot.

#### Ubuntu

    apt-get install texlive python-pydot

## Usage
In the data folder, create a snog file.  For instance:

    Alice [v] - (Bob [m] - Eve [v]), Henk[m]
    Alice - Renee, Bart[m]
    Eve - Karel[m], (Claire[v] - Henk)
    Renske[v] - A1, A2, A3, A4, A5, A6, A7, (A8 - A7)

To create a PDF, run the following command while in the data folder:

    make example.pdf

To create a PNG, run

    make example.png

The result is:

![](data/example.png)

