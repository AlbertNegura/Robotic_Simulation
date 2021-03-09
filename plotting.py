import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'errorbar.capsize': 2})

generations = range(50)
best_fitness = [24.649,25.662,24.595,25.357,27.323,25.704,24.871,26.09,26.174,24.595,24.595,24.595,24.595,25.828,24.595,
                24.596,24.595,24.595,24.595,29.297,30.508,30.163,31.354,30.715,30.784,31.755,31.616,31.117,32.438,
                32.092,30.927,33.41,33.048,35.68,31.842,36.627,32.504,38.204,31.435,36.695,38.931,32.241,32.71,32.104,
                34.181,31.603,31.661,32.852,32.197,32.549]
best_fitness_error = [0.646,0.444,0.322,3.072,4.121,5.133,5.532,5.77,5.425,5.426,5.425,5.425,5.773,5.454,5.454,5.455,5.454,5.454,5.455,5.455,5.455,5.675,5.815,4.17,4.193,5.288,4.231,3.105,0.948,0.694,4.396,0.268,3.775,0.243,4.165,0.218,4.803,0.2,5.152,1.991,3.431,3.833,4.642,2.668,6.513,0.88,4.097,3.903,0.211,0.301]
most_area_cleaned = [12.528,13.035,12.5,12.882,22.931,13.056,12.639,13.25,13.299,12.5,12.5,12.5,12.5,13.118,12.5,12.5,12.5,12.5,12.5,16.868,15.472,15.299,15.896,15.576,15.611,16.097,16.028,15.778,16.438,16.264,15.681,21.931,16.743,18.062,16.139,18.535,16.472,19.326,15.937,18.569,19.688,16.34,16.576,16.271,17.312,16.021,16.049,16.646,16.319,16.493]
av_fitness = [3.355,3.827,4.537,8.17,9.346,12.433,13.673,18.804,19.824,19.744,19.745,19.745,18.544,19.781,19.719,19.719,19.719,19.719,19.719,19.955,20.017,18.055,17.2,22.696,22.748,20.775,23.1,24.754,26.796,30.098,27.384,30.802,29.181,30.696,28.232,31.032,27.529,31.133,27.175,29.639,29.296,29.163,27.879,29.374,23.932,30.197,28.036,28.204,30.47,30.594]
fitness_error = [2.505,3.228,3.747,4.79,5.058,5.018,4.993,4.66,4.27,4.25,4.25,4.25,4.593,4.288,4.273,4.273,4.273,4.273,4.273,4.347,4.374,4.703,4.926,3.4,3.381,4.435,3.519,2.702,1.329,0.596,3.396,0.385,2.919,0.557,3.226,0.641,3.728,0.756,3.979,1.718,2.791,2.948,3.611,2.07,5.314,0.716,3.187,3.058,0.298,0.427]
diversity = [2559.216,2385.165,2099.707,1725.014,1328.849,698.662,620.912,580.311,501.79,569.178,527.023,620.651,627.271,442.43,364.227,305.126,370.637,215.626,350.678,514.622,479.794,813.072,870.807,454.471,559.525,707.789,673.806,577.953,615.366,59.256,154.078,14.806,133.58,13.22,322.397,16.921,231.054,16.921,157.478,132.69,92.813,55.143,145.706,63.717,390.89,0,213.03,129.575,0,0]
diversity_error = [0.247,0.252,0.255,0.261,0.261,0.264,0.262,0.261,0.262,0.26,0.26,0.259,0.261,0.261,0.261,0.261,0.261,0.262,0.263,0.263,0.264,0.264,0.266,0.263,0.263,0.264,0.263,0.262,0.262,0.261,0.259,0.261,0.261,0.261,0.26,0.261,0.262,0.261,0.26,0.26,0.261,0.26,0.262,0.26,0.259,0.261,0.261,0.26,0.261,0.261]

plt.figure()
plt.errorbar(range(len(best_fitness)),best_fitness,yerr=best_fitness_error, color="b", ecolor='k')
plt.errorbar(range(len(av_fitness)),av_fitness,yerr=fitness_error, color="r", ecolor='gray')
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend(["Best Fitness","Average Fitness"])
plt.show()
plt.figure()
ax1 = plt.subplot()
plt.errorbar(range(len(best_fitness)),best_fitness,yerr=best_fitness_error,color="b", label="Fitness", ecolor='k')
plt.ylabel("Fitness")
ax2 = ax1.twinx()
ax2.errorbar(range(len(diversity)),av_fitness,yerr=diversity_error,color="r", label="Diversity", ecolor='gray')
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=0)
plt.xlabel("Generation")
plt.ylabel("Diversity")
plt.show()
plt.figure()
ax3 = plt.subplot()
plt.errorbar(range(len(best_fitness)),best_fitness,yerr=best_fitness_error,color="b", label="Fitness", ecolor='k')
plt.ylabel("Fitness")
ax4 = ax3.twinx()
ax4.plot(range(len(most_area_cleaned)),most_area_cleaned, color="r", label="Area cleaned")
lines, labels = ax3.get_legend_handles_labels()
lines2, labels2 = ax4.get_legend_handles_labels()
ax4.legend(lines + lines2, labels + labels2, loc=0)
plt.xlabel("Generation")
plt.ylabel("Area Cleaned")
plt.show()