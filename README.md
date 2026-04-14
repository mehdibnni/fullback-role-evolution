# How Fullbacks Changed: Less Progression, More Creation

## Overview

This project investigates how the role of fullbacks has evolved between the early 2000s and modern football. Using event data from La Liga, it compares the 2004/05 season with the 2020/21 season to quantify changes in positioning, progression, creation, and build-up behaviour.

---

## Key Insight

Modern fullbacks operate higher on the pitch, are less responsible for progressing the ball from deep areas, and contribute more to chance creation within structured possession systems.

---

## Visual Analysis

### Activity Zones (Heatmap)

![Heatmap](images/Heat Map.png)

The heatmaps highlight a clear positional shift. Fullbacks in 2020/21 operate significantly higher up the pitch, with increased presence in advanced areas compared to 2004/05.

---

### Quantitative Comparison

![Table](images/Table.png)

The table summarises the evolution across four dimensions: positioning, progression, creation, and build-up. It shows a consistent shift away from long-distance progression towards shorter passing and increased attacking contribution.

---

## Key Findings

### Positioning
- Final third involvement increased significantly (+50%)
- Average field height increased, indicating a more advanced starting position
- Slight reduction in width from centre, suggesting marginally more central involvement

### Progression
- Progressive passes per match decreased substantially (−45%)
- Average progression distance dropped sharply (−74%)
- Indicates reduced responsibility for advancing the ball from deeper areas

### Creation
- Key passes per match increased significantly (+63.9%)
- Cross volume remained broadly stable
- Suggests a shift toward chance creation rather than progression

### Build-Up
- Short passing increased (+48.8%)
- Average pass length decreased (−24.5%)
- Reflects a transition toward possession-based play

---

## Interpretation

The results indicate a structural shift in the role of the fullback. Rather than acting as primary progressors from deep positions, modern fullbacks operate higher on the pitch and play a more complementary role within possession systems.

This evolution reflects broader tactical trends, including:
- Redistribution of build-up responsibility to central players
- Increased emphasis on positional play and short passing
- Greater specialisation of attacking roles

---

## Methodology

- Data source: StatsBomb event data
- Competition: La Liga
- Seasons analysed: 2004/05 and 2020/21
- Positions: Left Back and Right Back
- Metrics grouped into four categories:
  - Positioning
  - Progression
  - Creation
  - Build-up
- All metrics normalised per match to ensure comparability

---

## Repository Structure

```
fullback-role-evolution/
│
├── analysis.py
├── requirements.txt
├── README.md
└── images/
    ├── heatmap.png
    └── table.png
```

---

## Future Work

- Extend the analysis to additional leagues and competitions
- Compare fullback roles across different tactical systems
- Analyse interaction between fullbacks and midfield progression
- Incorporate player-level and team-level comparisons
