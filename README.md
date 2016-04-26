bioinfo-scripts
===============

Scripts used for bioinformatics and phylogenetics.

Index
-----

### [Converters](https://github.com/zxjsdp/bioinfo-scripts/tree/master/Converters):

- [fasta2phylip.py](https://github.com/zxjsdp/bioinfo-scripts/blob/master/Converters/fasta2phylip.py)

    Convert FASTA file to nicely aligned Phylip file.

- [phylip2fasta.py](https://github.com/zxjsdp/bioinfo-scripts/blob/master/Converters/phylip2fasta.py)

    Convert Phylip file to FASTA file.

### [PCA](https://github.com/zxjsdp/bioinfo-scripts/tree/master/PCA):

- [Randomly_select_and_do_multiple_PCAs](https://github.com/zxjsdp/bioinfo-scripts/tree/master/PCA/Randomly_select_and_do_multiple_PCAs)

    Randomly select data (similar to bootstrap method) and do PCA, draw PCA plots.

- [PCA_with_name](https://github.com/zxjsdp/bioinfo-scripts/tree/master/PCA/PCA_with_name)

    Do PCA and draw PCA plots with names.

### [Dictionary](https://github.com/zxjsdp/bioinfo-scripts/tree/master/Dictionary):

- [CSV_Dictionary](https://github.com/zxjsdp/bioinfo-scripts/tree/master/Dictionary/CSV_Dictionary)

    Query multiple lines by first column values in CSV file.

### [Haplotype Related](https://github.com/zxjsdp/bioinfo-scripts/tree/master/Haplotype_Related):

- [change_fdi_file_color](https://github.com/zxjsdp/bioinfo-scripts/blob/master/Haplotype_Related/change_fdi_file_color)

    Script to change color, propertion of sector, or maximum node size of fdi file which can be opened Network software.

    Needed txt files (please see example files in `txt_files` folder) from DNASP and original fdi files (without color information, see `fdi_files` folder).

- [modify_fdi_file_color_with_given_data](https://github.com/zxjsdp/bioinfo-scripts/blob/master/Haplotype_Related/modify_fdi_file_color_with_given_data)

    Script to modify color, proportion of sector, and max node size of fdi file with given proportion data (see `frequency.raw.txt`) and fdi file (see `1.fdi`).

### [Molecular_Computation](https://github.com/zxjsdp/bioinfo-scripts/tree/master/Molecular_Computation)

- [multiprocessing_jdock](https://github.com/zxjsdp/bioinfo-scripts/blob/master/Molecular_Computation/multiprocessing_jdock)

    多进程使用JDOCK运算分子 docking 的脚本。

