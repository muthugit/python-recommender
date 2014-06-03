import customers    as c
import products     as p
import recommending as r
import silhouette   as s
import clustering   as cl
import numpy        as np

products = p.products
names = []

def subMatrices(clusters):
    results = []
    maps = []
    indexMap = []
    for i in range(0,len(clusters)):
        clusterMat = []
        clusterMap = {}
        indexProds = []
        for j in range(0, len(clusters[i])):
            clusterMat.append(transpose[p.productsMap[clusters[i][j]]])
            clusterMap[clusters[i][j]] = j
            indexProds.append(clusters[i][j])
        mat = np.array(clusterMat).transpose()
        results.append(mat)
        maps.append(clusterMap)
        indexMap.append(indexProds)
    return [results, maps, indexMap]

def createSubcluster(indexMap, subMatrix, aMap):
    cl.__init__(subMatrix, c.customers, aMap)
    clust = []
    clust.append(cl.kMeans(25,8))
    clust.append(cl.centroidList)
    clust.append(cl.clusterMap)
    clust.append(indexMap)
    clust.append(s.averageSilhouettes(clust[0], subMatrix))
    return clust

def run(names):
    results = [names, c.customersMap]

    global transpose
    transpose = c.matrix.transpose()
    cl.__init__(transpose, p.products)
    catNum = len(p.products)/8
    prodClusters = cl.kMeans(catNum,8)
    results.append(prodClusters)

    inputs = subMatrices(prodClusters)
    subMats = inputs[0]
    maps = inputs[1]
    indexMap = inputs[2]
    subClusters = []
    for i in range(0, len(subMats)):
        subCluster = createSubcluster(indexMap[i], subMats[i], maps[i])
        subClusters.append(subCluster)
    totCluster = createSubcluster(products, c.matrix, p.productsMap)

    powerClusters = []
    powerSil = []
    results.append('unfiltered results: ' + str(totCluster[4]))
    for i in range(0, len(subClusters)):
        if subClusters[i][4] > totCluster[4]:
            powerClusters.append(subClusters[i])
            powerSil.append(subClusters[i][4])
    results.append('filtered average: ' + str(sum(powerSil)/len(powerSil)))

    powerClusters.append(totCluster)
    results.append(powerClusters)
    r.buildRecommendations(names, powerClusters)
    results.append(r.recommendationMatrix)
    return results