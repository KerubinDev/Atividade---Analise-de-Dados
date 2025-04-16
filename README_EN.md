# Data Analysis Project: Plant Growth with Different Types of Water

This project analyzes how different types of water affect the growth and development of bean plants over a 14-day period.

## Experiment Overview

In this experiment, we compared the growth of bean plants using three different types of water:
- Tap water  
- Mineral water  
- Sugar water (5g of sugar per 100ml of water)

For 14 days, we measured plant growth and recorded data for later analysis.

## Materials Used

- 30 bean seeds  
- 30 plastic cups  
- Cotton  
- Tap water  
- Mineral water  
- Sugar  
- Millimeter ruler  
- Notebook for notes  
- Camera for photographic documentation  
- Computer with Python installed for data analysis

## Methodology

1. **Cup preparation**: The bottom of each cup was lined with moistened cotton.  
2. **Group division**: 10 cups were assigned to each type of water.  
3. **Planting**: One bean seed was placed in each cup.  
4. **Identification**: Each group was labeled (A: tap, B: mineral, C: sugar).  
5. **Watering**: Each group was watered daily with its respective type of water.  
6. **Recording**: Plant height and number of leaves were measured and recorded daily.  
7. **Documentation**: Photos were taken every 3 days for visual documentation.

## Data Collection

For each plant, we recorded:
- Height in millimeters (from the cotton to the highest point)  
- Number of leaves  
- Germination rate (percentage of seeds that germinated)  
- Visual observations (color, appearance, etc.)

## Data Analysis

The analysis was conducted using Python with the following libraries:
- Pandas: for data organization  
- Matplotlib: for graph creation  
- NumPy: for statistical calculations

The analysis code is available in the file `analise/analisar_dados.py`.

## Repository Structure

```
/
├── README.md                  # This file
├── dados/                     # Folder with collected data
│   └── medicoes.xlsx          # Spreadsheet with daily measurements
├── fotos/                     # Experiment photos
│   ├── dia_1/                 # Day 1 photos
│   ├── dia_4/                 # Day 4 photos
│   ├── dia_7/                 # Day 7 photos
│   ├── dia_10/                # Day 10 photos
│   └── dia_14/                # Final day photos
├── analise/                   # Data analysis code
│   └── analisar_dados.py      # Python script for analysis
└── resultados/                # Generated graphs and results
    ├── grafico_crescimento.png  # Plant height chart
    ├── grafico_folhas.png       # Leaf count chart
    └── grafico_germinacao.png   # Germination rate chart
```

## Key Results

- **Germination Rate**: Mineral water had the highest germination rate (90%), followed by tap water (80%) and sugar water (60%).  
- **Height Growth**: Plants watered with tap water grew slightly taller (89mm) than those with mineral water (88mm). Plants watered with sugar water showed significantly less growth (60mm).  
- **Leaf Development**: Plants watered with mineral water developed more leaves (average of 6 leaves by the end of the experiment), compared to tap water (5 leaves) and sugar water (3 leaves).  
- **General Observations**: Plants watered with sugar water showed signs of stress, with yellowed leaves and stunted growth.

## Conclusions

This experiment shows that the type of water used for irrigation significantly affects plant development. Mineral water proved ideal for germination and leaf development, while tap water was slightly better for height growth. Sugar water impaired normal plant development, demonstrating that more nutrients do not always lead to better growth.

This simple project demonstrates how we can apply data analysis techniques to understand basic biological phenomena.

## How to Run the Analysis

1. Make sure Python is installed (version 3.6 or higher)  
2. Install the required libraries:
   ```
   pip install pandas matplotlib numpy
   ```
3. Run the analysis script:
   ```
   python analise/analisar_dados.py
   ```
4. The graphs will be generated and saved in the `resultados/` folder.
