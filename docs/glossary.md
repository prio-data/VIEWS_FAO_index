# Glossary of Terms and Concepts

## 1. **Event**
**Definition:** A single observation of non-zero values within a well-defined temporospatial unit. The exact definition of an event is influenced by the specific spatial and temporal aggregation used for a given analysis. This may include aggregations at various levels such as a 1x1 PRIO-GRID cell month, a 3x3 PRIO-GRID cell year, an administrative unit month, a country year, or any other applicable and defined units. The primary feature measured for an event is total conflict-related fatalities and total conflict-related fatalities per 100 000 people. The measure of conflict-related fatalities is defined by the Uppsala Conflict Data Program (UCDP), capturing all state-based, non-state and one-sided conflict. A non-zero value may represent one of a few varying measures of fatalities -- depending on the data used (see codebook for details) -- since total fatalities may be disaggregated into state-based, non-state, and one-sided conflict. The base level of analysis is a monthly 1x1 PRIO-GRID cell, which can be aggregated to other temporospatial units.

**Example:** An event is the total number of conflict-related fatalities recorded in a specific grid cell in a specific month. This may be aggregated to the total number of conflict-related fatalities per 100 000 in all grid cells within an administrative unit in a particular year. It would include all non-zero values of fatalities related to conflict issues exceeding 25 battle-related deaths in a given calendar year. 

## 2. **PRIO-GRID Cell**
**Definition:** The smallest spatial unit, defined by specific geographic coordinates and time intervals. It is the basic unit used to measure events (e.g., fatalities per 100k population). One PRIO-GRID cell is $0.5 \times 0.5$ decimal degrees or approximately 55 \times 55 kilometers at the Equator with cell area decreasing at higher latitudes because of the earth's curvature. This may be referred to simply as a *grid cell* with the spatial aggregation specified such as 1 \times 1, referring to a single PRIO-GRID cell, or 3 \times 3, referring to an aggregation of three neighbouring PRIO-GRID cells. A PRIO-GRID cell may be presented at either a monthly or yearly temporal unit. 

**Example:** One *grid cell* of a $0.5 \times 0.5$ decimal degrees geographic area observed over a month.

## 3. **Time Period**
**Definition:** The temporal component associated with a grid cell. The smallest temporal unit is one month and may be aggregated to larger units. Therefore, a time period may represent a month, year, or any other defined period consisting of aggregated monthly units over which data is recorded or analyzed.

**Example:** December 2023 is a *monthly* time period, while 2023 is a *yearly* time period. Each time period example would measure the non-zero count of total fatalities or total fatalities per 100 000 people for a specific geographic unit. Thus, December 2023 could measure the count of total fatalities in a single grid cell. A time period of 2023 would aggregate all observations across every month within the calendar year. It would be all non-zero events from January 2023 through December 2023. 

## 4. **Potential Event**
**Definition:** Any temporospatial unit within the defined geographic and temporal scope that could potentially contain an event. The exact definition of a potential event is influenced by the specific spatial and temporal aggregation used in the analysis. This may include aggregations at various levels such as a 1 \times 1 PRIO-GRID cell month, a 3 \times 3 PRIO grid cell year, an administrative unit month, a country year, or other defined unit.

**Example:** If a country is divided into 100 grid cells and observed over 400 months, there are 40,000 potential events. Naturally, this number is dependent on the defined spatial and temporal scale.

## 5. **Cumulative Distribution Function (CDF)**
**Definition:** A function that represents the cumulative probability of observing a value of a certain magnitude or lower. In this context, it shows the probability of seeing a certain number of fatalities (total or per 100 000 people) or fewer in any given grid cell.

**Example:** A CDF value of 0.7 at 10 fatalities per 100k means there's a 70% chance of observing 10 or fewer fatalities per 100 000 people in a random grid cell.

## 6. **Event Probability (p_i)**
**Definition:** The probability of observing an event of a specific magnitude or larger in a single grid cell, derived from the CDF. It is essentially the complement of the CDF at a given value, representing the probability of exceeding that value.

**Formula:** 
$$p_i = 1 - \text{CDF}(\text{value})$$

Where $p_i$ represents the probability of observing an event with more than a specified number of fatalities per 100 000 people.

**Example:**  If the CDF at 10 fatalities per 100 000 is 0.7, then $p_i$ is 0.3, meaning there's a 30% chance of observing more than 10 fatalities per 100 000 people in a random grid cell.

## 7. **Event Return Period (e_i)**
**Definition:** The expected number of potential events (e.g. monthly grid cells) that need to be observed to detect at least one event of a specific magnitude or larger. In probability theory, this concept is akin to "trials," which refer to independent experiments or observations with binary outcomes of success or failure. In our context, a "trial" corresponds to observing a single potential event within a defined temporal and spatial scope (e.g. monthly grid cell) to determine whether an event of a specified magnitude or larger occurs. Given this perspective, each "trial" is conducted within a "potential event" space with each defined temporospatial grid cell representing a potential event. In mathematical terms, a "trial" would then be a "success" if the observed value in that grid cell was equal to or above a predefined feature value. If $p_i$ is the probability of such an event, then:

**Formula:** 

$$e_i = \frac{1}{p_i}$$ 

Where $e_i$ represents the expected number of trials (i.e. potential events, e.g. monthly grid cells observed) needed in order to observe at least one event of the specified size or larger. This inverse relationship reflects that as the probability of the event ($p_i$) decreases, the expected number of observations needed increases.

**Example:** If $p_i$ is 0.1 and the event return period $e_i$ is 10, then, on average 10 potential events (e.g., non-zero values in monthly grid cells) must be observed to capture at least one event of the specified size or larger. 

It is important to note that despite the use of the term "period" here, these observations do not have to be distributed across time. Using monthly 1 \times 1 grid cells as an example: if there is a small defined country of only 10 1 \times 1 grid cells, then there are 10 potential events within a single month. Subsequently, if a return period is defined as 10, then only 10 "trials" are needed in order to observe an event and, therefore, within a country of only 10 grid cells at an event (observation of non-zero values) would be observed on average every month since there are only 10 potential events. 


## 8. **At Least One Occurrence Probability (P_i)**
**Definition:** The probability of observing at least one event of a specific magnitude or larger across multiple spatial units (e.g. grid cells) within a defined time period (e.g. month). This is an expansion of $p_i$, incorporating a define temporal scope into the probability of observing at least one occurrence of an event. Taking the probability theory concept of "trials" again, a specific combined spatial unit (e.g. grid cell, 1 \times 1, 3 \times 3, etc.) and temporal unit (e.g. month) within the spatial area under consideration (such as a country) is treated as an independent "trial" with a binary outcome – success (non-zero event occurs) or failure (no non-zero event occurs). 

$P_i$ reflects the likelihood of observing at least one event within the spatial area during a given time period, accounting for the number of potential events (grid cells). This normalization by the number of spatial units (e.g. grid cells) ensures that $P_i$ is independent of the size of the area, focusing solely on the likelihood of event occurrence during that time period.

This is in contrast to $p_i$ where a large country will experience more "rare" events than a small country since it contains more potential events each time period. As such, $P_i$ serves as a time-based measure, representing the likelihood of observing an event in any specified given period (e.g., month), regardless of the size of the spatial area. If $p_i$ is the event probability and $n^{pg}$ is the total number of PRIO grid cells, we have:

**Formula:** $$P_i = 1 - (1 - p_i)^{n^{pg}}$$

Where $P_i$ is the probability of observing at least one event of the specified magnitude across the grid cells ("trials"), assuming each grid cell acts independently. When num_grid_cells = 1, the probability of observing at least one event $P_i$​ is simply equal to the event probability $p_i$​, as there is only one trial (one grid cell) to consider.

**Example:** For instance, if $p_i$ is 0.1 and you have 100 grid cells, $P_i$ would be approximately 0.999, indicating a 99.9% chance of observing at least one event of the specified magnitude across those grid cells within a single time period. However, if you only have 1 grid cell, $P_i$ simplifies to $p_i$, meaning there would be a 10% chance of observing the event in that single grid cell.

## 9. **Time-Based Event Return Period (E_i)**
**Definition:** The expected number of time periods (e.g., months, years) between occurrences of a specific event of a certain magnitude or larger in a defined geographic area (e.g. country). This concept is adaptable to different time scales, such as the Annual Event Return Period ($E^a_i$​) for years or the Monthly Event Return Period ($E^m_i$) for months. The return period reflects how often such an event is expected to occur within the specified area and time frame, effectively normalizing the size of the area. If $P_i$ is the probability of at least one occurrence in the given area and time period, we have:

**Formula:** 
$$E_i = \frac{1}{P_i}$$

**Example (Annual):** If $P_i$ is 0.1 and you have 100 years of observation, $E^a_i$ would be 10 years, meaning the event is expected to occur once every 10 years on average within the specific geographic region (e.g. country).

**Example (Monthly):** If $P_i$ is 0.1 and you have 100 months of observation, $E^m_i$ would be 10 months, meaning the event is expected to occur once every 10 months on average within the specific geographical region (e.g. country).

**Consideration for Single Grid Cell:** If there is only one spatial unit within a geographical area (a contrived example would be on grid cell covering a full country), $P_i$ simplifies to $p_i$. For example, if $p_i$ is 0.1 and you have 100 time periods (e.g., 100 months), $E_i$ would be 10 time periods, meaning the event is expected to occur once every 10 periods on average within that single full country grid cell.

## 10. **Expected Annual Losses (EAL)**
**Definition:** The average annual financial loss expected due to events of a certain magnitude or larger, calculated by integrating the probability of such events with their associated costs over time. This measure provides a long-term estimate of potential financial impact.

**Example:** For example, if the calculated average annual loss due to conflicts in a region is \$1 million, this represents the EAL, providing a benchmark for potential financial impact each year.

## 11. **Exceedance Probability (EP)**
**Definition:** The probability that the magnitude of a specific event will be exceeded within a given time period. This metric is commonly used in risk management to assess the likelihood of extreme or rare events, helping to inform preparedness and mitigation strategies.

**Example:** For example, an exceedance probability of 0.05 for 100 fatalities per 100 000 people means that there is a 5% chance of exceeding 100 fatalities per 100 000 people within the specified time period.

## 12. **Parametric Insurance**
**Definition:** A type of insurance that triggers a payout when predefined conditions or parameters are met, such as when an event of a specific magnitude occurs. This differs from traditional insurance, which compensates for actual losses incurred.

**Example:** For example, a parametric insurance policy might pay out if the number of fatalities per 100 000 people exceeds a predefined threshold within a given month.

## 13. **Temporal Aggregation**
**Definition:** The process of combining data over time by summing or averaging to form a single summary for a defined time period. Temporal aggregation is used to create annual, monthly, or other time-based summaries from finer-grained data, providing a broader view of trends.

**Example:** For example, aggregating daily fatalities per 100 000 population data to produce a monthly total gives a more comprehensive overview of fatalities over that month.

## 14. **Spatial Aggregation**
**Definition:** The process of combining data from multiple smaller spatial units (e.g., grid cells) to form a larger spatial unit for analysis, such as aggregating grid cells to create a regional or national summary.

**Example:** For example, aggregating fatalities data from individual grid cells to generate a country-level summary provides an overall picture of the impact across the entire country.

## 15. **Empirical Probability**
**Definition:** The probability derived directly from observed data, rather than from theoretical models. In this context, it represents the likelihood of an event based on actual occurrences recorded in the dataset.

**Example:** For example, if 10 out of 100 observed grid cells report more than 50 fatalities per k population, the empirical probability of this event occurring is 0.1, indicating a 10% likelihood based on past data.

