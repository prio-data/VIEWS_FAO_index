# Glossary of Terms and Concepts

## 1. **Event**
- **Definition:** A single observation or occurrence within a temporospatial grid cell. In this context, an event refers to the recorded value of fatalities per 100k population in a specific grid cell during a specific time period.
- **Example:** An event could be the number of fatalities per 100k population recorded in a grid cell during a specific month.

## 2. **(PRIO) Grid Cell**
- **Definition:** The smallest spatial unit in the analysis, defined by specific geographic coordinates and time intervals. It is the basic unit used to measure events (e.g., fatalities per 100k population).
- **Example:** A PRIO grid cell is a $0.5 \times 0.5$ decimal degrees geographic area observed over a month.

## 3. **Time Period**
- **Definition:** The temporal component of the grid cell. This could be a month, year, or any other defined period.
- **Example:** A time period could be a month when measuring monthly fatalities per 100k population.

## 4. **Potential Event**
- **Definition:** Any grid cell within the defined geographic and temporal scope that could potentially contain an event.
- **Example:** If a country is divided into 100 grid cells and observed over 400 months, there are 40,000 potential events.

## 5. **Cumulative Distribution Function (CDF)**
- **Definition:** A function that represents the cumulative probability of observing a value of a certain magnitude or lower. In this context, it shows the probability of seeing a certain number of fatalities per 100k population or less in any grid cell.
- **Example:** A CDF value of 0.7 at 10 fatalities per 100k means there's a 70% chance of observing 10 or fewer fatalities per 100k in a random grid cell.

## 6. **Event Probability (p_i)**
- **Definition:** The probability of observing an event of a specific size or larger in a single grid cell, derived from the CDF. It is essentially the complement of the CDF at a given value, representing the probability of exceeding that value.

- **Formula:** 
$$p_i = 1 - \text{CDF}(\text{value})$$

- **Example:** If the CDF at 10 fatalities per 100k is 0.7, then $p_i$ is 0.3, meaning there's a 30% chance of observing more than 10 fatalities per 100k in a random grid cell.

## 7. **Event Return Period (e_i)**
- **Definition:** The expected number of grid cells (trials) that need to be observed to see at least one event of a specific size or larger. If $p_i$ is the event probability, we have:

- **Formula:** 

$$e_i = \frac{1}{p_i}$$ 

- **Example:** If $p_i$ is 0.1, the event return period $e_i$ is 10, meaning you need to observe 10 grid cells on average to see an event of that size or larger.

## 8. **Time-Based Event Return Period (E_i)**
- **Definition:** The expected number of time periods (e.g., months, years) between occurrences of a specific event of a certain size or larger in a defined geographic area. The term is general and can be adapted to different time scales, such as the Annual Event Return Period ($E^a_i$) for years or the Monthly Event Return Period ($E^m_i$) for months. If $P_i$ is the probability of at least one occurrence in the given area and time period, we have:

- **Formula:** $$E_i = \frac{\text{Number of Time Periods}}{P_i}$$



- **Example (Annual):** If $P_i$ is 0.1 and you have 100 years of observation, $E^a_i$ would be 10 years, meaning the event is expected to occur once every 10 years.

- **Example (Monthly):** If $P_i$ is 0.1 and you have 100 months of observation, $E^m_i$ would be 10 months, meaning the event is expected to occur once every 10 months.

## 9. **At Least One Occurrence Probability (P_i)**
- **Definition:** The probability of observing at least one event of a specific size or larger across multiple grid cells within a specific time period. If $p_i$ is the event probability and $\text{num\_grid\_cells}$ is the total number of grid cells, we have:

- **Formula:** $$P_i = 1 - (1 - p_i)^{\text{num\_grid\_cells}}$$

- **Example:** If $p_i$ is 0.1 and you have 100 grid cells, $P_i$ represents the probability of seeing at least one event of the specified size in any of the 100 grid cells.

## 10. **Expected Annual Losses (EAL)**
- **Definition:** The average annual financial loss expected due to events of a certain size or larger. It integrates the probability of events with their associated costs.

- **Example:** If the average annual loss due to conflicts in a region is calculated to be $1 million, this would represent the EAL.

## 11. **Exceedance Probability (EP)**
- **Definition:** The probability that a specific event's magnitude will be exceeded within a given time period. It is often used in risk management to understand the likelihood of extreme events.

- **Example:** An exceedance probability of 0.05 for 100 fatalities per 100k population means there is a 5% chance of observing more than 100 fatalities per 100k population in a given time period.

## 12. **Parametric Insurance**
- **Definition:** A type of insurance that pays out when predefined conditions (parameters) are met, such as when an event of a certain magnitude occurs, rather than compensating for actual losses incurred.

- **Example:** A parametric insurance policy might pay out if the number of fatalities per 100k population exceeds a certain threshold within a given time period.

## 13. **Temporal Aggregation**
- **Definition:** The process of summing or averaging data over time to form a single time period. Temporal aggregation is used to create annual, monthly, or other time-based summaries from finer-grained data.

- **Example:** Aggregating daily fatalities per 100k population data to produce a monthly total.

## 14. **Spatial Aggregation**
- **Definition:** The process of combining data from multiple spatial units (e.g., grid cells) to form a larger spatial unit for analysis.

- **Example:** Aggregating fatalities data from individual grid cells to generate a country-level summary.

## 15. **Empirical Probability**
- **Definition:** The probability derived from observed data, as opposed to theoretical probability. In this context, it refers to the likelihood calculated from actual events in the dataset.

- **Example:** If 10 out of 100 observed grid cells have more than 50 fatalities per 100k population, the empirical probability of this event is 0.1.
