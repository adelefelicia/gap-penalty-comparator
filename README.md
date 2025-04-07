# Gap Penalty Comparator

## Overview
The **Gap Penalty Comparator** is a bioinformatics tool designed to compare how different gap penalties impact pairwise global sequence alignments using the Needleman-Wunsch algorithm. It supports two scoring methods:
- **BLOSUM62**: Substitution matrix for protein sequence alignment.
- **Identity Scoring**: A simple scoring scheme with +1 for matches and -1 for mismatches.

This tool provides a graphical interface to visualize alignment matrices and compare results for different gap penalties.

The project was made for the course "MOL3022 Bioinformatics - Method Oriented Project" at the Norwegian University of Science and Technology (NTNU). 

## Features
- **Customizable Gap Penalties**: Compare alignments with three different gap penalties.
- **Scoring Methods**:
  - BLOSUM62 matrix for protein alignments.
  - Identity scoring for protein and gene alignments.
- **Interactive Visualization**: Displays alignment matrices with alignment scores and arrows showing backtracking logic, as well as highlighted alignment paths.
- **Gap information**: Shows the number of gaps and average length of gaps for each gap penalty.

## Getting started

### System requirements
The app has only been tested on computers with Windows 11 operating system. It requires Python version 3.11 or higher. Other dependencies can be installed as explained below.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/adelefelicia/gap-penalty-comparator.git
   ```
2. Navigate to the project directory:
   ```bash
   cd gap-penalty-comparator
   ```
3. Install the required dependencies (creating a virual environment first is recommended):
   ```bash
   pip install -r requirements.txt
   ```  
### Running the app
1. Navigate to the project's inner directory:
   ```bash
   cd gap-penalty-comparator
   ```
2. Run the main.py file to start the app:
   ```bash
   python main.py
   ```

## Acknowledgements
The BLOSUM62 matrix is provided by the [blosum](https://pypi.org/project/blosum/) Python package.
