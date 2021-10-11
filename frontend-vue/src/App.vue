<template>
  <b-container>
    <b-row class="text-center mb-4">
      <b-col>
        <h1>SBL Greek New Testament book projecter</h1>
        <div>
          <!-- Using modifiers -->
          <b-button v-b-modal.info-modal>?</b-button>
          <!-- The modal -->
          <b-modal id="info-modal" title="About this project">
            <InfoButton />
          </b-modal>
        </div>
      </b-col>
    </b-row>
    <b-row>
      <b-col class="jumbotron" md="4" :offset="isProjection ? 0 : 4">
        <b>Select NT books:</b><br />

        <Checkboxes
          v-for="books in booksList"
          :key="books.group"
          :booklist="books.books"
          :bookgroup="books.group"
          :model="selected"
        />
        <b-button
          class="mx-auto"
          :disabled="selectedList.length < 3"
          v-on:click="launchClustering"
          >Clusterize</b-button
        >
      </b-col>
      <b-col md="8" v-if="isProjection">
        <ProjectionGraph :data="projectionsList" />
      </b-col>
      <b-col class="text-center" v-else> </b-col>
    </b-row>
  </b-container>
</template>

<script>
import Checkboxes from "./components/Checkboxes.vue";
import ProjectionGraph from "./components/ProjectionGraph.vue";
import InfoButton from "./components/InfoButton.vue";
var qs = require("qs");

export default {
  name: "App",
  components: { Checkboxes, ProjectionGraph, InfoButton },
  data() {
    return {
      projections: {},
      selectedGlobal: {
        Gospels: [],
        Pauline: [],
        Pastoral: [],
        "Deutero-Pauline": [],
        Other: [],
      },
      booksList: [],
      projectionsList: [],
    };
  },
  computed: {
    selectedList() {
      let selected = [];
      if (this.selectedGlobal) {
        for (const [, value] of Object.entries(this.selectedGlobal)) {
          selected = selected.concat(value);
        }
      }
      return selected;
    },
    isProjection() {
      return Object.keys(this.projectionsList).length > 0;
    },
  },
  mounted() {
    this.axios
      .get("http://localhost:8000/bookclasses")
      .then((response) => {
        this.booksList = response.data;
      })
      .catch((error) => {
        console.log(error);
      });
  },
  methods: {
    launchClustering() {
      if (this.selectedList.length > 0) {
        console.log(this.selectedList);
        this.axios
          .post("http://localhost:8000/clusterize?", null, {
            params: { book: this.selectedList },
            paramsSerializer: (params) => {
              return qs.stringify(params, { arrayFormat: "repeat" });
            },
          })
          .then((response) => {
            this.projectionsList = response.data;
            this.projectionsList.forEach((value) => {
              value["x"] = value.projection.x;
              value["y"] = value.projection.y;
              value["z"] = value.projection.z;
              value["type"] = "scatter3d";
              value["text"] = value.labels;
              value["mode"] = "markers+text";
              value["name"] = value.ground_truth[0];
            });
            console.log(this.projectionsList);
          })
          .catch((error) => {
            console.log(error);
            alert("Something went wrong with the clustering");
          });
      }
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
