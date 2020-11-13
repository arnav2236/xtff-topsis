def main():
    import pandas as pd
    import time as tt
    import numpy as np
    import sys
    import copy

    args= copy.deepcopy(sys.argv)
    time1=tt.time()
    if len(sys.argv) != 5:
        raise Exception("please enter four parameters")
    if sys.argv[1].endswith(('.csv')):
        pass
    else:
        raise Exception("input file type - csv")


    impacts = []
    for imp in sys.argv[3]:
        if imp == ',':
            pass
        elif imp == '+' or '-':
            impacts.append(imp)

        else:
            raise Exception("impact must be positive(+) or negative (-)")

    weights = []
    for w in args[2]:
        if w != ',':
            weights.append(int(w))

    print(impacts)
    print(weights)


    if len(weights) != len(impacts):
        raise Exception("impacts and weights are not of same length")

    print("Reading Input line")
    df = pd.read_csv(sys.argv[1])
    cols = len(df.columns)


    if cols < 3:
        raise Exception("input file should be of minimum  3 columns")

    if (len(impacts) != cols - 1):
        raise Exception("impacts, weights and number of columns  must be of same length")


    def square_sum(df, RSS):
        for i in range(1, len(df.columns)):
            col = df.iloc[:, i]
            sum = 0
            for j in col:
                if type(j) != int:
                    try:
                        val = int(j)
                    except:
                        raise Exception("all values must be numeric")
                sum += j * j
            sum = np.sqrt(sum)
            RSS.append(sum)
        return df


    # ***********************************
    # STEP2
    # implementing step 2 of TOPSIS
    def normalization(df, RSS):
        for i in range(1, len(df.columns)):
            col = df.iloc[:, i]
            sum = 0
            for j in col:
                j = (j / RSS[i - 1]) * weights[i - 1]
        return df


    def bestvalue(df, impacts, ideal_best):
        for i in range(1, len(df.columns)):
            if impacts[i - 1] == '-':
                # find minimum value in ith col
                col = df.iloc[:, i]
                mini = col[0]
                for j in col:
                    if j < mini:
                        mini = j;
                ideal_best.append(mini)

            else:
                col = df.iloc[:, i]
                maxi = col[0]
                for j in col:
                    if j > maxi:
                        maxi = j;
                ideal_best.append(maxi)
                # find max value in ith column


    def worstvalue(df, impacts, ideal_worst):
        for i in range(1, len(df.columns)):
            if impacts[i - 1] == '+':
                # find minimum value in ith col
                col = df.iloc[:, i]
                mini = col[0]
                for j in col:
                    if j < mini:
                        mini = j;
                ideal_worst.append(mini)

            else:
                col = df.iloc[:, i]
                maxi = col[0]
                for j in col:
                    if j > maxi:
                        maxi = j;
                ideal_worst.append(maxi)

    def euclidean_distances(df, dist_best, dist_worst, ideal_best, ideal_worst):
        for i in range(df.shape[0]):  # iterate per row
            plus = 0
            minus = 0
            for j in range(1, len(df.columns)):
                plus += ((ideal_best[j - 1] - df.iloc[i, j]) * (ideal_best[j - 1] - df.iloc[i, j]))
                minus += ((ideal_worst[j - 1] - df.iloc[i, j]) * (ideal_worst[j - 1] - df.iloc[i, j]))
            dist_best.append(np.sqrt(plus))
            dist_worst.append(np.sqrt(minus))
        return df



    RSS = [] 
    #sabhi square sum kiv alue store krnege list me
    df = square_sum(df, RSS)
    print("Square sum done")

    print("*********************")
    df = normalization(df, RSS)
    print("Normalization done")
    print("*********************")
    ibest = []
    iworst = []
    bestvalue(df, impacts, ibest)
    worstvalue(df, impacts, iworst)
    print("Best value and worst value using impact lists done")
    print("*********************")
    best = []
    worst = []
    df = euclidean_distances(df, best, worst, ibest, iworst)
    print("Finding Euclid Distancev done")

    print("*********************")
    print("*********************")
    print("*********************")
    print("Now we will find topsis score")
    Top = []

    for i in range(df.shape[0]):
        Top.append(worst[i] / (worst[i] + best[i]))

    df['TOPSIS_VALUE'] = Top

    print("Topsis value done")

    copyfile = pd.DataFrame(df)
    # print(copyfile)


    copyfile.sort_values(by=['TOPSIS_Score'], ascending=False, inplace=True)

    dictionary = {}

    rank = 1
    for i in range(df.shape[0]):
        dictionary[copyfile.iloc[i, 0]] = rank
        rank += 1

    ranks = []
    for i in range(df.shape[0]):
        ranks.append(dictionary[df.iloc[i, 0]])

    df['Rank'] = ranks


    time2=tt.time()
    print("processing time:",time2-time1)
    df.to_csv(args[4], index=False, header=True)
    time3=tt.time()
    print("making csv file time",time3-time2);
if __name__=='__main__':
    main()