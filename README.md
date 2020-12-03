# Line Segment Intersection

Given *n* line segments in a plane the goal is to find all *k* points where these line segments intersect. Trivially this can be done in *O(n<sup>2</sup>)* by looking at every pair. However, using a line sweep algorithm we can find all these points efficiently if *k < O(n<sup>2</sup>)*.

Here is an implementation that runs in *O((n+k)log(n))* accompanied by a graphical interface for testing. To start the interface run

```
python frontEnd.py
```

In the GUI window that pops up draw the line segments by marking two points using the mouse. Click on 'Start Evaluation' to run the line sweep algorithm (you'll be able to see the sweep line and the intersection points being marked in red as they are found).

A few sample test cases have already been saved. To see how to run them refer to the [run_tests.sh](https://github.com/gulu42/LineSegmentIntersection/blob/master/run_tests.sh) file in this repo.

This work was done as a part of CS715 Computational Geometry.
