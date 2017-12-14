# Titanic Data Visualization


## Summary
This project charts 3 different graphs. It shows the number of survivals based on age groups, classes, and gender.

1. Titanic survival by age group: The Children have the highest survival rate.
2. Titanic survival by class: First class passengers have the highest survival rate among all the different classes.
3. Titanic survival by gender: Survival rate of the female is 3.89 times than male, 74% vs 19%. 

## Design
* Chart type: I re-evaluated different chart type by tweaking few line of code and confirm a bar chart is the best way to see trends in the titanic survival.
* Layout: Since only two survivorship status exist so stacked bar chart layout is best suited to visualize the data.
* Legend: Data are represented in the ratios, the stacked bar chart of y-axis is same for all the categories so, the legend is moved to the right-hand side of the chart.
* Visual encodings: X-axis represents different categories of an information and y-axis represents the ratio of passengers. Sequential colors are used to differentiate between 'survived' and 'perished'. The shape of the stacked bar chart is a rectangle. 

## Feedback
I gathered feedback from 3 different people and tried to follow Udacity questions guideline and here are the abridged responses.
### 1
It would be best to use 'perished' instead of 'died' as this tense matches that of 'survived'.

### 2
It would be best to increase the font size of x and y-axis. because the default font size is too small.

### 3
Color in the stacked bar chart can be improved. The color which is used is good but more conventional and sequential color can improve the visualization. 

## Resources

* [mbostock](https://bl.ocks.org/mbostock)
* [dimple.js Documentation](http://dimplejs.org/)
* [d3 documentation's](https://github.com/d3/d3/blob/master/API.md)



