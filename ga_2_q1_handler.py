
def solve_ga_2_q1(question: str) -> dict:
    """
    Generates a Markdown document for an imaginary analysis of the number of steps walked each day for a week,
    comparing over time and with friends. The output follows the specified Markdown formatting requirements.
    """
    markdown_content = """# Weekly Step Count Analysis

## Methodology

1. **Data Collection**: Tracked steps daily using a fitness tracker.
2. **Comparison**: Compared my weekly steps with past data and friends' data.
3. **Visualization**: Created graphs and tables to summarize findings.

*Note*: This analysis uses the `matplotlib` library for plotting.

## Results

### Key Observations
- **Monday** had the highest step count.
- The weekend showed a *significant drop* in activity.
- My step count was **30% higher** than the group average on Thursday.

### Step Count Comparison Table

| Day        | Steps (Me) | Steps (Friends) | Difference |
|------------|------------|-----------------|------------|
| Monday     | 12,000     | 11,000          | +1,000     |
| Tuesday    | 10,500     | 10,800          | -300       |
| Wednesday  | 9,000      | 9,500           | -500       |
| Thursday   | 13,000     | 10,000          | +3,000     |
| Friday     | 8,000      | 8,500           | -500       |
| Saturday   | 7,000      | 8,200           | -1,200     |
| Sunday     | 6,500      | 7,000           | -500       |

> "Walking is the best possible exercise. Habituate yourself to walk very far."  
> - Thomas Jefferson

### Visualization Code

```python
import matplotlib.pyplot as plt

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
my_steps = [12000, 10500, 9000, 13000, 8000, 7000, 6500]
friends_steps = [11000, 10800, 9500, 10000, 8500, 8200, 7000]

plt.plot(days, my_steps, label="My Steps")
plt.plot(days, friends_steps, label="Friends' Steps")
plt.title("Weekly Step Count Comparison")
plt.xlabel("Days")
plt.ylabel("Steps")
plt.legend()
plt.show()
```

### Additional Information

![Steps Tracker](https://via.placeholder.com/300x200 "Steps Tracker")

- [This helpful guide](https://www.healthline.com/nutrition/fitness-tracking)
- [Another useful resource](https://www.webmd.com/fitness-exercise/ss/slideshow-walking-guide)
"""
    
    return {"answer": markdown_content}
