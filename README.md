# Control Course Project
## 1) GUI Application for visualizing and solving signal flow graph problem
A signal flow graph (SFG) is a graphical representation of a system or network using nodes and directed edges. It is commonly used in control systems engineering to analyze and design linear time-invariant (LTI) systems.

In an SFG, nodes represent variables or signals, and directed edges represent the flow of signals between nodes. The direction of the edges indicates the flow of signals from one node to another. Each edge is associated with a gain or transfer function that describes the relationship between the input and output signals.

The steps to construct a signal flow graph are as follows:

1. Identify the variables and signals involved in the system. These could be inputs, outputs, intermediate signals, or variables representing system components.

2. Represent each variable or signal as a node in the graph. Label the nodes accordingly.

3. Determine the flow of signals between nodes and represent it using directed edges. Assign a gain or transfer function to each edge that relates the input and output signals.

4. Draw the edges between nodes according to the direction of signal flow.

5. Simplify the graph by removing any unnecessary nodes or edges that do not contribute to the system's behavior or transfer function.

Signal flow graphs provide a visual representation of the system's dynamics and interconnections, allowing engineers to analyze its behavior using graph theory techniques. They can be used to derive transfer functions, compute system response, determine stability, and perform various other analyses.

By applying techniques such as Mason's gain formula or Kirchhoff's laws, engineers can manipulate and analyze signal flow graphs to obtain valuable insights into the behavior and performance of complex systems.
## 2) Routh Stability Criteria Detector
The Routh-Hurwitz stability criterion, commonly known as the Routh's criteria or Routh-Hurwitz criterion, is a mathematical method used to determine the stability of a linear time-invariant (LTI) system. It provides a systematic way to analyze the stability of a system by examining the coefficients of its characteristic equation.

The Routh-Hurwitz criterion is based on constructing a Routh array using the coefficients of the characteristic equation. The Routh array is a tabular representation of the coefficients that allows us to determine the number of poles of the system that have positive real parts, which indicates instability.

The steps to apply the Routh-Hurwitz criterion are as follows:

1. Write down the characteristic equation of the system in the form: 
   A(s^n) + B(s^(n-1)) + ... + C = 0, where n is the order of the system.

2. Create the first two rows of the Routh array using the coefficients of the characteristic equation. The first row consists of the coefficients of the even powers of s, while the second row consists of the coefficients of the odd powers of s.

3. Continue filling the remaining rows of the Routh array using the following formulas:
   - Compute the elements of each row based on the previous two rows.
   - Divide the determinant of the submatrix formed by the first two elements of the previous row by the first element of the previous row.
   - Multiply the result by the first element of the row above and subtract it from the corresponding element in the previous row.

4. Analyze the Routh array:
   - If all the elements in the first column have the same sign (either all positive or all negative), then the system is stable.
   - If any element in the first column is zero or has a different sign from the others, the system is unstable.

5. Count the number of sign changes in the first column of the Routh array. This gives the number of poles with positive real parts (unstable poles).

The Routh-Hurwitz criterion provides a powerful tool for stability analysis of linear systems, particularly in control systems engineering. By examining the Routh array, engineers can determine the stability of a system without explicitly solving the characteristic equation or finding the roots of the equation.
