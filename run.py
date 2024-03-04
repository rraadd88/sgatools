#!usr/bin/python
"""Command-line options"""
import argh
import logging

# from os.path import exists
from pathlib import Path
try:
    from roux.lib.io import read_ps
    from roux.workflow.task import run_tasks
except:
    raise ImportError("requirements missing. install by running: pip install roux[workflow]")
    
def log_time_elapsed(start):
    """Log time elapsed.

    Args:
        start (datetime): start tile

    Returns:
        datetime: difference in time.
    """
    from datetime import datetime
    diff = datetime.now() - start
    return diff

def cli(
    input_paths,
    output_dir_path,
    replicates=4,
    linkage_cutoff=False,#-1,
    keep_large=False, #?
    overall_plate_median=510,
    max_colony_size=None, #1.5*overall.plate.median,
    intermediate_data=False,
    linkage_file=None,
    linkage_genes=None,#character(0)
    # # or
    # config_path: str = None,
    
    wd_path: str = None,
    threads: int = 1,
    kernel_name: str = "sgatools",
    verbose="CRITICAL",
    ext: str = 'tsv',
    force: bool = False,
    dbug: bool = False,
    skip=None,
    **kws,
):
    """sgatools command-line (CLI) 

    Examples:
        # cd sgatools
        run.py cli "input-paths" "output-dir-path"
    """
    from datetime import datetime
    from roux.lib.io import to_dict

    _start_time = datetime.now()
    if threads is None:
        threads = 1
    ## setting verbose
    logging.basicConfig(
        level=getattr(logging, verbose),
        format="[%(asctime)s] %(levelname)s\tfrom %(filename)s in %(funcName)s(..): %(message)s",
        force=True,
    )

    # if config_path is not None:
        #todo
        # from roux.lib.io import read_dict
        # parameters_list=read_dict(config_path)
    ## set the unset parameters 
    if max_colony_size is None:
        max_colony_size=1.5*overall_plate_median
    ## get the paths if multiple provided using glob syntax
    input_paths=read_ps(input_paths)
    
    ## list of parameters
    parameters_list=[]
    for p in input_paths:
         parameters_list.append(
             dict(
                input_path=p,
                output_path=f"{output_dir_path}/{Path(p).stem}.{ext}",
                replicates=replicates,
                linkage_cutoff=-1 if not linkage_cutoff else None,#-1,
                keep_large=keep_large, #?
                overall_plate_median=overall_plate_median,
                max_colony_size=max_colony_size, #1.5*overall.plate.median,
                intermediate_data=intermediate_data,
                linkage_file=linkage_file,#'',
                linkage_genes=linkage_genes,#character(0)
        ))
    paths = run_tasks(
        input_notebook_path=f"sgatools.ipynb",
        parameters_list=parameters_list,
        kernel=kernel_name,
        force=force,
        out_paths=True,
        fast=threads!=1,
        fast_workers=threads,
        language='R',
        **kws,
    )

    print(f"Time taken is saved at       : {log_time_elapsed(_start_time)}")
    print(f"The output is saved at       : {output_dir_path}")

parser = argh.ArghParser()
parser.add_commands(
    [
        cli,
    ]
)

if __name__ == "__main__":
    parser.dispatch()
