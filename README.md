# `SGATools`

## Usage

### Input folder

Your normalized and scored data folder will contain:
a) For each input image, one dat file. 
b) One combined data file: this file combines all files from a) and averages values (colony sizes, scores, etc..) of replicate arrays 
c) Scores only data file: this file contains only data rows with scores and has a much simpler format compared to that described below. There are 6 tab-delimited columns: query, array, score, standard deviation, p-value

### Input file

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
