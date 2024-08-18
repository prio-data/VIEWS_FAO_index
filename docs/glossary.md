# Glossary of Terms and Concepts

## 1. **Event**
**Definition:** A single observation of non-zero values within a well-defined temporospatial unit. The exact definition of an event is influenced by the specific spatial and temporal aggregation used for a given analysis. This may include aggregations at various levels such as a 1x1 PRIO grid cell month, a 2x2 PRIO grid cell year, an administrative unit month, a country year, or other defined units. The non-zero value could represent one of several different measures of fatalities contained in the data (see codebook for details). While various measures exist, the primary feature used is the total conflict-related fatalities per 100k population, with the base level of analysis being the monthly PRIO grid cell.

**Example:** An event could be the number of fatalities per 100k population recorded in a grid cell during a specific month. An event could be the number of conflict-related fatalities per 100k population recorded in a specific grid cell during a particular month.

## 2. **(PRIO) Grid Cell**
**Definition:** The smallest spatial unit in the analysis, defined by specific geographic coordinates and time intervals. It is the basic unit used to measure events (e.g., fatalities per 100k population).
**Example:** A PRIO grid cell is a $0.5 \times 0.5$ decimal degrees geographic area observed over a month.

## 3. **Time Period**
**Definition:** The temporal component associated with a grid cell. This could represent a month, year, or any other defined period during which data is recorded or analyzed.
**Example:** If the time period unit is months, December 2023 is an example of a time period, which would measure monthly fatalities per 100k population. If the time period unit is years, then 2023 is an example of a time period, which would measure annual fatalities per 100k population.

## 4. **Potential Event**
**Definition:** Any temporospatial unit within the defined geographic and temporal scope that could potentially contain an event. The exact definition of a potential event is influenced by the specific spatial and temporal aggregation used in the analysis. This may include aggregations at various levels such as a 1x1 PRIO grid cell month, a 2x2 PRIO grid cell year, an administrative unit month, a country year, or other defined unit

**Example:** If a country is divided into 100 grid cells and observed over 400 months, there are 40,000 potential events. Naturally, this number is very dependent on the spatial and temporal scale defined for the analysis.

## 5. **Cumulative Distribution Function (CDF)**
**Definition:** A function that represents the cumulative probability of observing a value of a certain magnitude or lower. In this context, it shows the probability of seeing a certain number of fatalities per 100k population or fewer in any grid cell.

**Example:** A CDF value of 0.7 at 10 fatalities per 100k means there's a 70% chance of observing 10 or fewer fatalities per 100k in a random grid cell.

## 6. **Event Probability (p_i)**
**Definition:** The probability of observing an event of a specific magnitude or larger in a single grid cell, derived from the CDF. It is essentially the complement of the CDF at a given value, representing the probability of exceeding that value.

**Formula:** 
$$p_i = 1 - \text{CDF}(\text{value})$$

Where $p_i$ represents the probability of observing an event with more than a specified number of fatalities per 100k population.

**Example:**  If the CDF at 10 fatalities per 100k is 0.7, then $p_i$ is 0.3, meaning there's a 30% chance of observing more than 10 fatalities per 100k in a random grid cell.

## 7. **Event Return Period (e_i)**
**Definition:** The expected number of potential events (e.g. monthly grid cells) that need to be observed to detect at least one event of a specific magnitude or larger. In probability theory, this concept is akin to "trials," which refer to independent experiments or observations with binary outcomes—success or failure. In our context, a "trial" corresponds to observing a single potential event (e.g. monthly grid cell) within a defined temporal and spatial scope to determine whether an event of a specified magnitude or larger occurs. Given this perspective, each "trial" is conducted within a "potential event" space, where, for instance, each monthly grid cell represents a potential event. In mathematical terms, a "trail" would then be a "success" if the observed value in that grid cell was equal to or above a predefined feature value. If $p_i$ is the probability of such an event, then:

**Formula:** 

$$e_i = \frac{1}{p_i}$$ 

Where $e_i$ represents the expected number of trials (i.e. potential events, e.g. monthly grid cells observed) needed to see at least one event of the specified size or larger. This inverse relationship reflects that as the probability of the event ($p_i$) decreases, the expected number of observations needed increases.

**Example:** If $p_i$ is 0.1, the event return period $e_i$ is 10, meaning that, on average, you would need to observe 10 potential events (e.g., monthly grid cells) to see at least one event of that size or larger. It is important to note that despite the use of the term "period" here, these observations do not have to be distributed across time. For example, using monthly grid cells: If a small country consists of only ten grid cells, these would all be potential events within a single month. An event return period of 10 would mean that we expect to see such an event, on average, every month since each month provides ten potential events.


## 8. **At Least One Occurrence Probability (P_i)**
**Definition:** The probability of observing at least one event of a specific magnitude or larger across multiple spatial units (e.g. grid cells) within a defined time period (e.g. month). Again, we can think of this as "trials" in probability theory, where each trial has a binary outcome - success (event occurs) or failure (no event occurs). Here, each spatial unit (e.g. grid cell) within the spatial area under consideration (such as a country) during a specific time period (e.g., one month) is treated as an independent trial.

$P_i$ reflects the likelihood of observing at least one event within the spatial area during a given time period, accounting for the number of potential events (grid cells). This normalization by the number of spatial units (e.g. grid cells) ensures that $P_i$ is independent of the size of the area, focusing solely on the likelihood of event occurrence during that time period.

This is in contrast to $p_i$ where a large country will experience more "rare" events than a small country since it contains more potential events each time period. As such, $P_i$ serves as a time-based measure, representing the likelihood of observing an event in any given period (e.g., month) regardless of the size of the spatial area. If $p_i$ is the event probability and $n^{pg}$ is the total number of PRIO grid cells, we have:

**Formula:** $$P_i = 1 - (1 - p_i)^{n^{pg}}$$

Where $P_i$ is the probability of observing at least one event of the specified magnitude across the grid cells (trials), assuming each grid cell acts independently. When num_grid_cells = 1, the probability of observing at least one event $P_i$​ is simply equal to the event probability $p_i$​, as there is only one trial (one grid cell) to consider.

**Example:** For instance, if $p_i$ is 0.1 and you have 100 grid cells, $P_i$ would be approximately 0.999, indicating a 99.9% chance of observing at least one event of the specified magnitude across those grid cells within a single time period. However, if you only have 1 grid cell, $P_i$ simplifies to $p_i$, meaning there would be a 10% chance of observing the event in that single grid cell.

## 9. **Time-Based Event Return Period (E_i)**
**Definition:** The expected number of time periods (e.g., months, years) between occurrences of a specific event of a certain magnitude or larger in a defined geographic area (e.g. country). This concept is adaptable to different time scales, such as the Annual Event Return Period ($E^a_i$​) for years or the Monthly Event Return Period ($E^m_i$) for months. The return period reflects how often such an event is expected to occur within the specified area and time frame, effectively normalizing the size of the area. If $P_i$ is the probability of at least one occurrence in the given area and time period, we have:

**Formula:** 
$$E_i = \frac{1}{P_i}$$

**Example (Annual):** If $P_i$ is 0.1 and you have 100 years of observation, $E^a_i$ would be 10 years, meaning the event is expected to occur once every 10 years on average within the specific geographical region (e.g. country).

**Example (Monthly):** If $P_i$ is 0.1 and you have 100 months of observation, $E^m_i$ would be 10 months, meaning the event is expected to occur once every 10 months on average within the specific geographical region (e.g. country).

**Consideration for Single Grid Cell:** If there is only one spatial unit within a geographical area (a contrived example would be on grid cell covering a full country), $P_i$ simplifies to $p_i$. For example, if $p_i$ is 0.1 and you have 100 time periods (e.g., 100 months), $E_i$ would be 10 time periods, meaning the event is expected to occur once every 10 periods on average within that single full country grid cell.

## 10. **Expected Annual Losses (EAL)**
**Definition:** The average annual financial loss expected due to events of a certain magnitude or larger, calculated by integrating the probability of such events with their associated costs over time. This measure provides a long-term estimate of potential financial impact.

**Example:** For example, if the calculated average annual loss due to conflicts in a region is \$1 million, this represents the EAL, providing a benchmark for potential financial impact each year.

## 11. **Exceedance Probability (EP)**
**Definition:** The probability that the magnitude of a specific event will be exceeded within a given time period. This metric is commonly used in risk management to assess the likelihood of extreme or rare events, helping to inform preparedness and mitigation strategies.

**Example:** For example, an exceedance probability of 0.05 for 100 fatalities per 100k population means there is a 5% chance of exceeding 100 fatalities per 100k population within the specified time period.

## 12. **Parametric Insurance**
**Definition:** A type of insurance that triggers a payout when predefined conditions or parameters are met, such as when an event of a specific magnitude occurs. This differs from traditional insurance, which compensates for actual losses incurred.

**Example:** For example, a parametric insurance policy might pay out if the number of fatalities per 100k population exceeds a predefined threshold within a given month.

## 13. **Temporal Aggregation**
**Definition:** The process of combining data over time by summing or averaging to form a single summary for a defined time period. Temporal aggregation is used to create annual, monthly, or other time-based summaries from finer-grained data, providing a broader view of trends.

**Example:** For example, aggregating daily fatalities per 100k population data to produce a monthly total gives a more comprehensive overview of fatalities over that month.

## 14. **Spatial Aggregation**
**Definition:** The process of combining data from multiple smaller spatial units (e.g., grid cells) to form a larger spatial unit for analysis, such as aggregating grid cells to create a regional or national summary.

**Example:** For example, aggregating fatalities data from individual grid cells to generate a country-level summary provides an overall picture of the impact across the entire country.

## 15. **Empirical Probability**
**Definition:** The probability derived directly from observed data, rather than from theoretical models. In this context, it represents the likelihood of an event based on actual occurrences recorded in the dataset.

**Example:** For example, if 10 out of 100 observed grid cells report more than 50 fatalities per k population, the empirical probability of this event occurring is 0.1, indicating a 10% likelihood based on past data.

