<template>
  <div>
    <h5>Goal</h5>
    <p>
      The goal of this small application is to quickly vizualize textual
      similarities between the SBL Greek New Testament texts.
    </p>
      <h5>Data</h5>
    <p>
      All of the data used for clustering is taken from the SBLGNT morphological
      tagging made available <a href="https://github.com/morphgnt/sblgnt">here</a> (warmest of thanks !)
    </p>
    <h5>Method</h5>
    <p>
      The application performs a <a href="https://en.wikipedia.org/wiki/Tf%E2%80%93idf">tf-idf vectorization</a> of the selected LXX texts,
      and then projects this data into a 3-Dimensional vizualization space using <a href="https://en.wikipedia.org/wiki/Principal_component_analysis">Principal Component Analysis</a>.
    </p>
    <h5>Coming later</h5>
    <p>
      The next inquired features are:
      <ul>
        <li>The computation of distances between verses / chapters</li>
        <li>
          The use of clustering algorithms to perform the clustering of the
          space
        </li>
      </ul>
    </p>
  </div>
</template>
