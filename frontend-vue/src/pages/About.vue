<template>
  <b-col sm="1" md="6" offset-md='3'>
    <h5>Goal</h5>
    <p>
      The goal of this small application is to quickly vizualize textual
      similarities between the Bible books, its different chapters and its different verses, respectively taken from the LXX and the SBLGNT texts.
    </p>
      <h5>Data</h5>
    <p>
      All of the data used for clustering is taken from the SBLGNT morphological
      tagging made available <a href="https://github.com/morphgnt/sblgnt">here</a> for the SBLGNT and from
      <a href="https://github.com/openscriptures/GreekResources/tree/master/LxxLemmas">here</a> for the LXX. Warmest of thanks to all those who have made this data freely available.
    </p>
    <h5>Method</h5>
    <p>
      The application performs a <a href="https://en.wikipedia.org/wiki/Tf%E2%80%93idf">tf-idf vectorization</a> of the selected SBLGNT texts,
      and then projects this data into a 3-Dimensional vizualization space using <a href="https://en.wikipedia.org/wiki/Principal_component_analysis">Principal Component Analysis</a>.
    </p>
    <h5>Coming later</h5>
    <p>
      The next inquired features are:
      <ul>
        <li>An easier to read representation of verses/chapters for large books </li>
        <li>
          The use of clustering algorithms to perform the clustering of the
          space
        </li>
        <li>Some explainability tools</li>
      </ul>
    </p>
    <h5>About the author</h5>
    <p>I have a master's in applied Mathematics and a PhD in computer science, and I've worked mostly on the use of artificial intelligence in order to optimize High Performance Computing system. I'm also a Bible studies enthusiast, hence this project at the intersection of my two hobbies !
    </p>
  </b-col>
</template>
