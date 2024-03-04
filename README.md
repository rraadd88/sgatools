# `SGATools`

## Installation

```
mamba env create environment.yml
mamba activate sgatools
```

Requirements in R:
```
mamba activate sgatools
R
install.packages("BiocManager")
library(BiocManager)
install(c("logger","logging","bootstrap"))
```

## Usage

### As a function in R

```
source("rscripts/SGAtools.R")
df = normalizeSGA(
    read.table(input_path, sep = "\t", header = TRUE),
    # replicates=,
    # linkage.cutoff=,
    # keep.large=,
    # overall.plate.median=,
    # max.colony.size=,
    # intermediate.data=,
    # linkage.file=, #todo
    # linkage.genes=,
    )
```

### As a command-line script

Requirements
```
python -m ipykernel install --user --name sgatools
```

#### Single file processing

```
papermill sgatools_test.ipynb output.ipynb --language R --kernel sgatools -p input_path examples/inputs/image_example1.dat -p output_path output.tsv
```

#### Batch-processing, with automated report generation

```
$ python run.py cli -h
usage: run.py cli [-h] [-r REPLICATES] [--linkage-cutoff] [--keep-large] [-o OVERALL_PLATE_MEDIAN] [-m MAX_COLONY_SIZE] [-i] [--linkage-file LINKAGE_FILE] [--linkage-genes LINKAGE_GENES]
                  [-w WD_PATH] [-t THREADS] [--kernel-name KERNEL_NAME] [-v VERBOSE] [-e EXT] [-f] [-d] [-s SKIP]
                  input-paths output-dir-path

sgatools command-line (CLI) 

Examples:
    # cd sgatools
    run.py cli "input-paths" "output-dir-path"

positional arguments:
  input-paths           -
  output-dir-path       -

options:
  -h, --help            show this help message and exit
  -r REPLICATES, --replicates REPLICATES
                        4
  --linkage-cutoff      False
  --keep-large          False
  -o OVERALL_PLATE_MEDIAN, --overall-plate-median OVERALL_PLATE_MEDIAN
                        510
  -m MAX_COLONY_SIZE, --max-colony-size MAX_COLONY_SIZE
                        -
  -i, --intermediate-data
                        False
  --linkage-file LINKAGE_FILE
                        -
  --linkage-genes LINKAGE_GENES
                        -
  -w WD_PATH, --wd-path WD_PATH
                        -
  -t THREADS, --threads THREADS
                        1
  --kernel-name KERNEL_NAME
                        'sgatools'
  -v VERBOSE, --verbose VERBOSE
                        'CRITICAL'
  -e EXT, --ext EXT     'tsv'
  -f, --force           False
  -d, --dbug            False
  -s SKIP, --skip SKIP  -
```

## Data

### Output

Your normalized and scored data folder will contain:
a) For each input image, one dat file. 
b) One combined data file: this file combines all files from a) and averages values (colony sizes, scores, etc..) of replicate arrays 
c) Scores only data file: this file contains only data rows with scores and has a much simpler format compared to that described below. There are 6 tab-delimited columns: query, array, score, standard deviation, p-value

#### Table

Each file in your directory will has a 9 columns tab-delimited format:

1. Row: the row of the colony
2. Column: the column of the colony
3. Raw colony size: the size of the colony as quantified by the image analysis software
4. Plate id: unique id for this plate, set as file name 
5. Query gene name/ORF: Name of the query ORF if image/dat files follow conventional file naming (see file naming in help). If they do not, a value of '1' is placed as the query ORF
6. Array gene name/ORF: Name of the array ORF if plate layout file supplied. If not, a unique value is assigned to each group of replicate arrays 
7. Normalized colony size: the raw colony size after normalization. The size is relative to plate median colony size, and a proxy for fitness. Normalized value of 1 is as fit as the average strain, 1.3 means it is 30% fitter than the average strain, and 0.4 that it's 40% as fit as the average strain.
8. Score: the colony fitness score computed using the normalized colony size (7) and the corresponding normalized colony size in the control screen
9. Additional information as key-value pairs
	* SD: Standard deviation of scores (in the combined file)
	* LK: Linkage effect- the array exists too close to the query on the chromosome
	* JK: Jackknife filter- This colony induces too much variance in the sizes of other colonies in the replicate group
	* BG: Big replicates- At least three colonies of this replicate are too large. The whole replicate is excluded
	* CP: Cap- Normalized colony size was too large (> 1000) and was capped at 1000

For more help, see [SGAtools help page](http://sgatools.ccbr.utoronto.ca/help).
