import subprocess

INPUT_VCF_FILE = "data/ALL.chr6.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.vcf.gz"
REF_FILE = "data/ref_chr6.fa.gz"
chr = 6

with open("haploblock_boundaries_Halldorsson2019.txt", "r") as f:
    # skip header
    f.readline()

    for line in f:
        split_line = line.rstrip().split('\t')
        start, end = split_line

        output_vcf = f"data/{chr}_region_{start}-{end}.vcf.gz"

        # extract region start-end from VCF and index
        subprocess.run(["bcftools", "view",
                        "-r", f"{chr}:{start}-{end}",
                        INPUT_VCF_FILE,
                        "-o", output_vcf],
                        check=True)
        
        subprocess.run(["bcftools", "index",
                        output_vcf],
                        check=True)

        # extract region start-end from reference fasta
        subprocess.run(["samtools", "faidx",
                        REF_FILE,
                        f"chr{chr}:{start}-{end}"],
                        stdout=open(f"chr{chr}:{start}-{end}.fa", "w"),
                        check=True)

        # create a consensus sequence (fasta) from region reference and variants extracted from VCF

        break