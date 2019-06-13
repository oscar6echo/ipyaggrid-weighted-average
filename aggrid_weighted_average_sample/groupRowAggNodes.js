function groupRowAggNodes(nodes) {
  console.log(nodes);

  const buildWeightAverage = function(colName, refColName) {
    let sumCol = 0;
    let sumRef = 0;
    let sumProduct = 0;
    nodes.forEach(node => {
      const data = node.group ? node.aggData : node.data;
      sumRef += data[refColName];
      sumProduct += data[colName] * data[refColName];
    });
    return sumProduct / sumRef;
  };

  const buildSum = function(colName) {
    let sumCol = 0;
    nodes.forEach(node => {
      const data = node.group ? node.aggData : node.data;
      sumCol += data[colName];
    });
    return sumCol;
  };

  const colsToSum = ["price"];

  const refCol = "volume";
  const colsToWeightAverage = ["level"];

  const resultSum = colsToSum.reduce((acc, cur) => {
    acc[cur] = buildSum(cur);
    return acc;
  }, {});
  console.log(resultSum);

  const resultWeightAverage = colsToWeightAverage.reduce((acc, cur) => {
    acc[cur] = buildWeightAverage(cur);
    return acc;
  }, {});
  console.log(resultWeightAverage);

  const result = {
    ...{ [refCol]: buildSum(refCol) },
    ...resultSum,
    ...resultWeightAverage
  };

  console.log(result);
  return result;
}
