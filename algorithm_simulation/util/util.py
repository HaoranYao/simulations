
def getCDFValue(cdf,key):
    #print("cdf: " + str(cdf))
    #print("   key: " + str(key))
    for x in sorted(cdf.keys()):
        if key < float(x):
            return cdf[x]
    return None


def getCDFAverage(cdf):
    average = 0
    previous_x =0
    for x in sorted(cdf.keys()):
        average += cdf[x]*(float(x)-previous_x)
        previous_x = float(x)
    return average