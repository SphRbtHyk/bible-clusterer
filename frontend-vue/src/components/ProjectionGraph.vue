<template>
  <b-row>
    <Plotly
      type="scatter3d"
      :data="data"
      :layout="layout"
      :config="config"
    ></Plotly>
  </b-row>
</template>

<script>
import { Plotly } from "vue-plotly";

export default {
  name: "ProjectionGraph",
  components: {
    Plotly,
  },
  data() {
    return {
      layout: { margin: { b: 0, t: 0, r: 0 } },
      config: {},
    };
  },
  props: {
    data: [],
  },
};
</script>

<style scoped>
.js-plotly-plot,
.plot-container {
  height: 90vh;
  width: 100%;
  padding: 0;
}
</style>
