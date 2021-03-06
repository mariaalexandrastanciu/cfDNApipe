from cfDNApipe import *
import argparse
import os

def main(args):
    if not os.path.exists(args.outputDir):
        os.mkdir(args.outputDir)
    
    pipeConfigure(
        threads=10,
        genome="hg19",
        refdir="/home/zhangwei/Genome/hg19_bowtie2",
        outdir=args.outputDir,
        data="WGS",
        type="paired",
        JavaMem="10G",
        build=True,
    )
    
    verbose = False
    
    bams = [args.input]

    res_cnvbatch = cnvbatch(
        casebamInput=bams,
        access=Configure.getConfig("access-mappable"),
        annotate=Configure.getConfig("refFlat"),
        verbose=verbose,
        caseupstream=True,
        stepNum="CNV01",
        other_params={"-m": "wgs", "-y": True, "--target-avg-size": 3000}
    )

    res_cnvTable = cnvTable(upstream=res_cnvbatch, genemetrics_params={"--threshold": 0.8, "--min-probes": 3, "-y": True,},
                            verbose=verbose, stepNum="CNV04",)
    # res_cnvTable = cnvTable(upstream=res_cnvbatch, verbose=verbose, stepNum="CNV02",)
    # res_cnvPlot = cnvPlot(upstream=res_cnvbatch, verbose=verbose, stepNum="CNV03",)
    # res_cnvHeatmap = cnvHeatmap(upstream=res_cnvbatch, verbose=verbose, stepNum="CNV04",)


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("outputDir", type=str)
    parser.add_argument("input", type=str)
    return parser.parse_args(argv)


if __name__ == "__main__":
    main(parse_arguments(sys.argv[1:]))