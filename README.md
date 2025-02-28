![tests](https://github.com/Dhanunjaya-Elluri/master-thesis/actions/workflows/ci.yaml/badge.svg) 
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg) 
![Python version](https://img.shields.io/badge/Python-3.10-blue) 
![Wheel](https://img.shields.io/badge/wheel-yes-brightgreen) 
![Repo Status](https://img.shields.io/badge/status-active-brightgreen)

[//]: # (![Stars]&#40;https://img.shields.io/github/stars/Dhanunjaya-Elluri/master-thesis?style=social&#41;)


# Master's Thesis

## Transformers for quantized time series forecasting

This repository explores the use of Transformer models, traditionally applied in natural language processing, for time series forecasting. Transformers, known for learning sequential patterns and generating text akin to human writing, show promise in understanding and predicting time series data. The project focuses on quantizing continuous time series data into discrete symbols, simplifying the forecasting task and enhancing interpretability. It investigates novel positional encoding strategies for time-series data within quantized domains. Additionally, it compares two quantization methods: Vanilla Symbolic Aggregate Approximation (SAX) and Kernel SAX, the latter offering a flexible approach by estimating data density for quantization. This comparative analysis aims to reveal which method better suits various forecasting scenarios, combining advanced machine learning techniques with human interpretability for practical applications.
## Goal of the Thesis

The primary goal of this thesis is to investigate and enhance the effectiveness of time series forecasting through a comprehensive exploration of quantization and transformative modeling techniques.


## Getting Started

To reproduce the experiments and analyses conducted in this thesis, follow these steps:

1. Clone this repository: <br>
    `git clone https://github.com/Dhanunjaya-Elluri/master-thesis.git`


2. Run to install the required dependencies: <br>
    `pip install -e .`

## Usage
```python
import pandas as pd
from tqts.quantizer.kernel_sax import KernelSAX

# Load the data
df = pd.read_csv("../data/AirPassengers.csv")

kernel_sax = KernelSAX(kernel='epanechnikov', n_alphabet=12, bandwidth=10, epochs=70)
kernel_sax.fit(df['#Passengers'].values, paa_window_size=3, verbose=True)
kernel_sax.plot_with_boundaries(path="../images/", filename="kernel_sax_with_boundaries.png")
kernel_sax.save_alphabets("../data/alphabets_with_lloyd.txt")

kernel_sax = KernelSAX(kernel='epanechnikov', n_alphabet=12, bandwidth=10, boundary_estimator='quantile')
kernel_sax.fit(df['#Passengers'].values, paa_window_size=3, verbose=True)
kernel_sax.plot_with_quantiles(path="../images/", filename="kernel_sax_with_quantiles.png")
kernel_sax.save_alphabets("../data/alphabets_with_quantiles.txt")
```

## Results
This will save the alphabets and the corresponding boundaries/quantiles in the specified path. The plots and alphabets are saved in the following format:


<table>
  <tr>
    <td align="center">
      <h2>Lloyd-Max Boundaries</h2>
      <img src="./images/kernel_sax_with_boundaries.png" alt="Lloyd-Max Boundaries" width="900"/> <br>
        Alphabets Generated: A A A A A A B A B B C B C C E C D E F C D E G D F G H F G H I G H I J H H I K H I J L I J K L J
    </td>
    <td align="center">
      <h2>Lloyd-Max Boundaries with decomposition</h2>
      <img src="./images/kernel_sax_with_boundaries_no_trend.png" alt="Lloyd-Max Boundaries with decomposition" width="900"/> <br>
        Alphabets Generated: B B D C F G E E D D F E E H F C A B E D G H K H I J J F F H K G C B D B E I K K H K K G
    </td>
  </tr>
</table>

<table>
  <tr>
    <td align="center">
      <h2>Quantile Boundaries</h2>
      <img src="./images/kernel_sax_with_quantiles.png" alt="Quantile Boundaries" width="900"/> <br>
        Alphabets Generated: A A B A A B C A B C D B C D E D D E F D D F G E F G H F G H I G H I J H H I K H I J K I J K K J
    </td>
    <td align="center">
      <h2>Quantile Boundaries with decomposition</h2>
      <img src="./images/kernel_sax_with_quantiles_no_trend.png" alt="Quantile Boundaries with decomposition" width="900"/> <br>
        Alphabets Generated: A B C C F G E E D D G E E H F B A A E D H H K H I J J F F H K G C B C A F I K K H K K G
    </td>
  </tr>
</table>

## References

[1] Konstantinos Bountrogiannis, George Tzagkarakis, and Panagiotis Tsakalides. “Data-driven Kernelbased
Probabilistic SAX for Time Series Dimensionality Reduction”. In: 2020 28th European Signal
Processing Conference (EUSIPCO). 2021, pp. 2343–2347. DOI: 10.23919/Eusipco47968.2020.9287311.

[2] Rakshitha Godahewa et al. “Monash Time Series Forecasting Archive”. In: Neural Information
Processing Systems Track on Datasets and Benchmarks. 2021.

[3] Jessica Lin et al. “Experiencing SAX: a novel symbolic representation of time series”. In: Data
Mining and Knowledge Discovery 15.2 (2007), pp. 107–144.

[4] Ashish Vaswani et al. “Attention is all you need”. In: Advances in neural information processing
systems. Vol. 30. 2017.

[5] A. Zeng et al. “Are Transformers Effective for Time Series Forecasting?” In: ArXiv preprint
(2022). arXiv: 2205.13504 [cs.LG].

## Contact

If you have any questions, suggestions, or issues regarding this repository or the implemented model, please feel free to contact the author:

Dhanunjaya Elluri <br>
Email: <dhanunjayet@gmail.com> | <dhanunjaya.elluri@tu-dortmund.de>
