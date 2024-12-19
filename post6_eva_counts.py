import numpy as np
from sklearn.metrics import r2_score
import ipdb
# ff = '/home/sizhuo/Downloads/8441_countss4.gpkg'
# load df
ff = '/home/sizhuo/Downloads/8101_counts4.gpkg'
import geopandas as gpd
df = gpd.read_file(ff)

# ipdb.set_trace()
# scatter plot for counts
# remove nan
df = df.dropna()
import matplotlib.pyplot as plt
print(df)
# plt.scatter(df['count_rounded_sum'], df['fid_count'])
# plt.show()
point_new_count  = df['fid_count_4']
old_dens_count = df['count_rounded_sum']
rr = r2_score(old_dens_count, point_new_count)
print('r2: ', rr)
# ensure no nan
print(point_new_count.isna().sum(), 'should be 0')
print(old_dens_count.isna().sum(), 'should be 0')
# total bias

print((point_new_count.sum() - old_dens_count.sum())/old_dens_count.sum()*100, '%')
print('old sum: ', old_dens_count.sum())
print('new sum: ', point_new_count.sum())
