import os
import sys
import logging
import argparse
import pathlib


# set up logger, using inherited config, in case we get called as a module
logger = logging.getLogger(__name__)

import subprocess


def parse_haploblock_boundaries(boundaries_file):
    """
    Parses haploblock boundaries with 2 columns: start end

    arguments:
    - boundaries_file
    
    returns:
    - haploblock_boundaries: list of tuples with haploblock boundaries (start, end)
    """
    haploblock_boundaries = []

    try:
        f = open(boundaries_file, 'r')
    except Exception as e:
        logger.error("Opening provided boundaries file %s: %s", boundaries_file, e)
        raise Exception("Cannot open provided boundaries file")
    
    # skip header
    line = f.readline()
    if not line.startswith("START\t"):
        logging.error("boundaries file %s is headerless? expecting headers but got %s",
                      boundaries_file, line)
        raise Exception("boundaries file problem")
    
    for line in f:
        split_line = line.rstrip().split('\t')

        if len(split_line) != 2:
            logger.error("Boundaries file %s has bad line (not 5 tab-separated fields): %s",
                         boundaries_file, line)
            raise Exception("Bad line in the boundaries file")
        
        (start, end) = split_line

        haploblock_boundaries.append((start, end))

    return(haploblock_boundaries)


def extract_region_from_vcf(vcf, chr, chr_map, start, end, out):
    """
    Extract a specific region from a VCF file

    Generates the following files in out/ :
    - {chr}_region_{start}-{end}.vcf.gz
    - {chr}_region_{start}-{end}.vcf.gz.csi
    - chr{chr}_region_{start}-{end}.vcf
    - chr{chr}_region_{start}-{end}.vcf.gz
    - chr{chr}_region_{start}-{end}.vcf.gz.csi
    """
    if chr.startswith("chr"):
        chr = chr.replace("chr", "")

    # extract region start-end from VCF and index
    subprocess.run(["bcftools", "view",
                    "-r", f"{chr}:{start}-{end}",
                    vcf,
                    "-o", os.path.join(out, f"{chr}_region_{start}-{end}.vcf.gz")],
                    check=True)

    subprocess.run(["bcftools", "index",
                    os.path.join(out, f"{chr}_region_{start}-{end}.vcf.gz")],
                    check=True)
    
    # VCF has 6 instead of chr6, which is required by bcftools consensus
    # create file chr_map: "6 chr6" one mapping per line
    # map chr6 to 6, bgzip and index
    subprocess.run(["bcftools", "annotate",
                    "--rename-chrs", chr_map,
                    os.path.join(out, f"{chr}_region_{start}-{end}.vcf.gz")],
                    stdout=open(os.path.join(out, f"chr{chr}_region_{start}-{end}.vcf"), "w"),
                    check=True)
    
    subprocess.run(["bgzip",
                    os.path.join(out, f"chr{chr}_region_{start}-{end}.vcf")],
                    check=True)

    subprocess.run(["bcftools", "index",
                    "-c",
                    "-o", os.path.join(out, f"chr{chr}_region_{start}-{end}.vcf.gz.csi"),
                    os.path.join(out, f"chr{chr}_region_{start}-{end}.vcf.gz")],
                    check=True)

def generate_consensus_seq(ref, chr, start, end, out):
    """
    Apply variants from previously generated VCF to reference sequence

    Generates the following files in out/ :
    - ref_chr6.fa.gz.fai
    - ref_chr6.fa.gz.gzi
    - chr{chr}_region_{start}-{end}.fa.gz
    """
    if chr.startswith("chr"):
        chr = chr.replace("chr", "")

    # index reference
    subprocess.run(["samtools", "faidx",
                    ref],
                    check=True)
    
    # extract region start-end from reference fasta
    subprocess.run(["samtools", "faidx",
                    ref,
                    f"chr{chr}:{start}-{end}"],
                    stdout=open(os.path.join(out, f"chr{chr}_region_{start}-{end}.fa"), "w"),
                    check=True)
    
    # create a consensus sequence (fasta) from region reference and variants extracted from VCF
    subprocess.run(["bcftools", "consensus",
                    "-f", ref,
                    os.path.join(out, f"chr{chr}_region_{start}-{end}.vcf.gz")],
                    stdout=open(os.path.join(out, f"chr{chr}_region_{start}-{end}.fa"), "w"),
                    check=True)

    subprocess.run(["bgzip",
                    os.path.join(out, f"chr{chr}_region_{start}-{end}.fa")],
                    check=True)


def main(boundaries_file, vcf, ref, chr_map, chr, out):
    logger.info("Parsing haploblock boundaries")
    haploblock_boundaries = parse_haploblock_boundaries(boundaries_file)

    for (start, end) in haploblock_boundaries:
        logger.info(f"Generating phased VCF for haploblock {start}-{end}")
        extract_region_from_vcf(vcf, chr, chr_map, start, end, out)

    for (start, end) in haploblock_boundaries:
        logger.info(f"Generating phased fasta for haploblock {start}-{end}")
        generate_consensus_seq(ref, chr, start, end, out)


if __name__ == "__main__":
    script_name = os.path.basename(sys.argv[0])
    # configure logging, sub-modules will inherit this config
    logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)
    # set up logger: we want script name rather than 'root'
    logger = logging.getLogger(script_name)

    parser = argparse.ArgumentParser(
        prog=script_name,
        description="TODO"
    )
    
    parser.add_argument('--boundaries_file',
                        help='Path to boundaries file generated from Halldorsson et al., 2019',
                        type=pathlib.Path,
                        required=True)
    parser.add_argument('--vcf',
                        help='Path to phased VCF file (bgzipped) from 1000Genomes',
                        type=pathlib.Path,
                        required=True)
    parser.add_argument('--ref',
                        help='Path to reference sequence (bgzipped)',
                        type=pathlib.Path,
                        required=True)
    parser.add_argument('--chr_map',
                        help='Path to chr_map: one mapping per line, ie "6 chr6"',
                        type=pathlib.Path,
                        required=True)
    parser.add_argument('--chr',
                        help='chromosome',
                        type=str,
                        required=True)
    parser.add_argument('--out',
                        help='Path to output folder',
                        type=pathlib.Path,
                        required=True)

    args = parser.parse_args()

    try:
        main(boundaries_file=args.boundaries_file,
             vcf=args.vcf,
             ref=args.ref,
             chr_map=args.chr_map,
             chr=args.chr,
             out=args.out)

    except Exception as e:
        # details on the issue should be in the exception name, print it to stderr and die
        sys.stderr.write("ERROR in " + script_name + " : " + repr(e) + "\n")
        sys.exit(1)