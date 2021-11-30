Hello!

I'm using prophet to predict future sales.

In input data, the sales volume treated with squared root is used as 'y' value.
And ​cap and floor are 100 and 0. 
Additionally, price information is added with`add_regressor`

But some of products, its results is very strange. 
Like below graph, the value is increasing abnormally in the prediction section.

Input Data



ds | y | avg_prc | cap | floor
-- | -- | -- | -- | --
2020-11-01 | 3.464102 | 970.0 | 100.0 | 0.0
2020-11-02 | 1.000000 | 970.0 | 100.0 | 0.0
2020-11-03 | 3.000000 | 970.0 | 100.0 | 0.0
2020-11-04 | 3.000000 | 970.0 | 100.0 | 0.0
2020-11-05 | 3.741657 | 970.0 | 100.0 | 0.0
... | ... | ... | ... | ...
2021-10-21 | 2.449490 | 990.0 | 100.0 | 0.0
2021-10-22 | 2.449490 | 990.0 | 100.0 | 0.0
2021-10-23 | 2.236068 | 990.0 | 100.0 | 0.0
2021-10-24 | 2.449490 | 990.0 | 100.0 | 0.0
2021-10-25 | 1.732051 | 990.0 | 100.0 | 0.0


Why is this happening