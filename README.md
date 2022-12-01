# Python_BI_2022

Functions described in functional.py:

## 1. sequential_map
### This functions takes any amount of functions and a container as an input
### It returns a list of values from initial container modified by consequent use of functions from input

## 2. consensus_filter
### This functions takes any amount of functions (which return True or False) and a container as an input
### It returns a list of values from initial container which are returned with True from functions from input
    
## 3. conditional_reduce
### This functions takes 2 functions (first one returns True or False, second one acts as the reduce function) and a container as an input
### It returns a value received from second function used only on values from initial container which are returned with True from the first function

## 4. func_chain
### This functions takes any amount of functions
### It returns a function uniting all given functions by condequent using one after another

## 5. sequential_map_chain
### This functions does the same as the sequential_map function but it uses the func_chain function to unite all given functions consequently
### It returns a list of values from initial container modified by consequent use of functions from input


Surprisingly this functional.py script doesn't require any requirements.
