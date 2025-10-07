> Elixir BioHackathon November 3-7, 2025

# Elixir-BH-2025

# Methods

All code is in [haploblock_breakpoints.ipynb](haploblock_breakpoints.ipynb)

### Recombination map from Palsson et al., 2024

Download deCODE recombination maps including both crossover (CO) and non-crossover (NCO) recombination: https://doi.org/10.5281/zenodo.14025564

How the data looks:

| Chr | Position | map (cM) | cMperMb | DSBs/Mb per meiosis | deltaDSB | oNCO |
|-----|----------|----------|---------|---------------------|----------|------|
| chr1 | 500000 | 0.0465734638273716 | 0.051548998802900314 | 0.18732483685016632 | 0.9579851031303406 | 0.00024600245524197817 |
| chr1 | 1500000 | 0.05668618530035019 | 0.36985400319099426 | 0.23414182662963867 | 0.7754221558570862 | 0.0006765067810192704 |
| chr1 | 2500000 | 0.08809421956539154 | 1.2260290384292603 | 0.3768974542617798 | 0.5750330686569214 | 0.0022755227982997894 |
| chr1 | 3500000 | 0.07209863513708115 | 1.9589810371398926 | 0.3275741636753082 | 0.3099609315395355 | 0.0027675277087837458 |
| chr1 | 4500000 | 0.06319160014390945 | 2.5238749980926514 | 0.3032439053058624 | 0.1271921992301941 | 0.002952029462903738 |

Are map (cM), cMperMb, DSBs/Mb per meiosis, deltaDSB and oNCO correlated?

![alt text](figures/Palsson2024/recomb_map_chr6_mat_all_columns_one_plot_norm.png)

![alt text](figures/Palsson2024/recomb_map_chr6_mat_all_columns_corr.png)


### Recombination map from Halldorsson et al., 2019

Download the recombination map from Supp Mat. The map has the following columns: Chr, Begin, End, **cMperMb**, cM


# Results

### Recombination map from Palsson et al., 2024; we used DSB rate to find haploblock boundaries

1) We found 12 positions with high recombination rates defined as **rate > 2*average**:

![alt text](figures/Palsson2024/recomb_map_chr6_mat_outliersAVG.png)

| Position | Recombination rate (DSBs/Mb per meiosis) |
|----------|------------------------------------------|
| chr6:4500000 | 0.2726089060306549 |
| chr6:5500000 | 0.2507183849811554 |
| chr6:6500000 | 0.34163784980773926 |
| chr6:7500000 | 0.2730921804904938 |
| chr6:11500000 | 0.24522000551223755 |
| chr6:15500000 | 0.27179062366485596 |
| chr6:16500000 | 0.24810494482517242 |
| chr6:43500000 | 0.24928732216358185 |
| chr6:57500000 | 0.27551886439323425 |
| chr6:58500000 | 0.37233930826187134 |
| chr6:59500000 | 0.7373786568641663 |
| chr6:166500000 | 0.25078296661376953 |


2) We found 7 positions with high recombination rates defined as **rate > 1.5*IQR**:

![alt text](figures/Palsson2024/recomb_map_chr6_mat_boxplot.png)

![alt text](figures/Palsson2024/recomb_map_chr6_mat_outliersIQR.png)

| Position | Recombination rate (DSBs/Mb per meiosis) |
|----------|------------------------------------------|
| chr6:4500000 | 0.2726089060306549 |
| chr6:6500000 | 0.34163784980773926 |
| chr6:7500000 | 0.2730921804904938 |
| chr6:15500000 | 0.27179062366485596 |
| chr6:57500000 | 0.27551886439323425 |
| chr6:58500000 | 0.37233930826187134 |
| chr6:59500000 | 0.7373786568641663 |

3) We found 6 positions with high recombination rates defined as **peaks after Gaussian smooting**:

![alt text](figures/Palsson2024/recomb_map_chr6_mat_GS_peaks.png)

| Position | Recombination rate (DSBs/Mb per meiosis) |
|----------|------------------------------------------|
| chr6:7500000 | 0.2730921804904938 |
| chr6:38500000 | 0.08716981112957001 |
| chr6:58500000 | 0.37233930826187134 |
| chr6:90500000 | 0.12601755559444427 |
| chr6:106500000 | 0.13935035467147827 |
| chr6:165500000 | 0.2063562124967575 |

For more information about Gaussian smoothing see: https://en.wikipedia.org/wiki/Gaussian_filter

We compared different sigma for Gaussian smoothing:

![alt text](figures/Palsson2024/recomb_map_chr6_mat_GS_compare_sigma.png)


### Recombination map from Halldersson et al., 2019; we used cMperMb to find haploblock boundaries

1) We found 1398 positions with high recombination rates defined as **rate > 10*average**.

2) We found 11855 positions with high recombination rates defined as **rate > 1.5*IQR**.

3) We found 2287 positions with high recombination rates defined as **peaks after Gaussian smooting** (sigma=5). Zoom in on the first peak:

![alt text](figures/Halldorsson2019/recomb_map_chr6_Halldorsson2019_GS_peaks_zoom_in.png)

# Python environment

Installed via [Python venv](https://docs.python.org/3/library/venv.html) with the following command:

```
python -m venv --system-site-packages ~/pyEnv_ElixirBH2025
source ~/pyEnv_ElixirBH2025/bin/activate
pip install --upgrade pip
pip install numpy pandas scipy matplotlib
```

Check [requirements.txt](requirements.txt) for versioning.


# References

1. Palsson, G., Hardarson, M.T., Jonsson, H. et al. Complete human recombination maps. Nature 639, 700–707 (2025). https://doi.org/10.1038/s41586-024-08450-5
