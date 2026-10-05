# In-Depth Problem Analysis

## 1. Domain Failure Analysis of Traditional Irrigation
Agricultural water loss primarily stems from:
- **Temporal Blindness**: Timers turn sprinklers on regardless of whether a deluge occurred an hour prior.
- **Spatial Blindness**: A 100-acre farm contains significant topography, soil textural differences (clay vs. sand), and localized water holding capacities.
- **Resource Competition**: In water-scarce dry seasons, pumping water without economic and biological prioritization results in early reservoir exhaustion, leaving high-value perennial crops to wilt.

## 2. Mathematical Modeling of Field Irrigation Demand
Let field $k$ have:
- Soil moisture percentage: $m_k \in [0, 100]$
- Moisture threshold limit: $\theta_k \in (0, 100]$
- Base volumetric water requirement: $R_k \in \mathbb{R}^+$
- Precipitation probability: $p_{\text{rain}} \in [0, 100]$
- Economic priority rating: $\pi_k \in \{1, 2, 3, 4, 5\}$

### Deficit Volume Formulation
$$\Delta_k = \max\left(0, \, \frac{\theta_k - m_k}{\theta_k}\right)$$
$$\text{Water}_k = \left\lceil R_k \cdot \Delta_k \cdot \left(1 - \frac{p_{\text{rain}}}{100}\right) \right\rceil$$

### Urgency Benefit Score
$$V_k = \Delta_k \cdot \pi_k \cdot 100 \cdot \left(1 - \frac{p_{\text{rain}}}{100}\right)$$

This guarantees that:
1. Fields with moisture $\ge \theta_k$ receive $\text{Water}_k = 0$.
2. Higher rain forecast decreases water requirement while preserving priority ordering.
3. Critically dry, high-priority crops dominate the objective function.
