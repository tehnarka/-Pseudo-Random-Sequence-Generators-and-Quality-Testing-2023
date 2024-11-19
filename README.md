# Pseudo-Random Sequence Generators and Statistical Quality Testing

## Description
This repository contains a Python implementation of pseudo-random sequence generators and statistical tests to evaluate their quality. Designed for educational purposes, the project supports the generation and testing of binary sequences that can be applied in cryptographic systems.

## Contents
- Implementation of multiple pseudo-random sequence generators.
- Statistical tests to evaluate uniformity, independence, and homogeneity of sequences.
- Interactive console interface for user-driven testing and generation.

## Features
- Generate binary sequences of any desired length.
- Perform statistical tests for:
  - Uniformity.
  - Independence.
  - Homogeneity.
- Generate sequences using various algorithms:
  - **Lehmer (Low and High)**.
  - **L20 and L89**.
  - **Blum-Micali (bits and bytes)**.
  - **BBS (bits and bytes)**.
  - **Geffe**.
  - **Wolfram**.
  - **Librarian (based on textual input)**.
- Export generated sequences to a `.txt` file.

## Usage
1. Run the script:  
   ```bash
   python AsymCryptoLab1-Python-2023-Marynin_fi94-Nemkovych_fi-94.py
   ```
2. Follow the interactive console prompts to:
   - Generate a sequence using a selected algorithm.
   - Load an external sequence for testing.
   - Choose sequence length and test parameters.

## Requirements
- Python 3.9 or later.
- Required libraries:  
  - `math`  
  - `random`  
  - `collections`  
  - `pandas`  
  - `datetime`  
  - `numpy`

