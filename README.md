<img src="https://github.com/SphRbtHyk/bible-clusterer/blob/main/frontend-vue/src/assets/full_logo.png" width="400">

# Bible projecter project

## Goal

      The goal of this small application is to quickly vizualize textual
      similarities between the Bible books, its different chapters and its different verses, respectively taken from the LXX and the SBLGNT texts.

## Data

      All of the data used for clustering is taken from the SBLGNT morphological
      tagging made available <a href="https://github.com/morphgnt/sblgnt">here</a> for the SBLGNT and from
      <a href="https://github.com/openscriptures/GreekResources/tree/master/LxxLemmas">here</a> for the LXX. Warmest of thanks to all those who have made this data freely available.

## Method

      The application performs a <a href="https://en.wikipedia.org/wiki/Tf%E2%80%93idf">tf-idf vectorization</a> of the selected SBLGNT texts,
      and then projects this data into a 3-Dimensional vizualization space using <a href="https://en.wikipedia.org/wiki/Principal_component_analysis">Principal Component Analysis</a>.

## Coming later

The next inquired features are:

- An easier to read representation of verses/chapters for large books </li>
- The use of automatic decision tools to determine text groups
- Improved explainability tools

## About the author

    I have a master's in applied Mathematics and a PhD in computer science, and I've worked mostly on the use of artificial intelligence in order to optimize High Performance Computing system. I'm also a Bible studies enthusiast, hence this project at the intersection of my two hobbies !

This project is a simple Web Application to vizualize the results obtained when using Tf-Idf followed by a PCA on the Greek Bible texts, respectively taken from the SBLGNT and the LXX.
