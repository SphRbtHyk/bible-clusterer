<template>
  <b-container fluid>
    <b-row class="text-center mb-4">
      <b-col>
        <h1>LXX and SBLGNT book projecter</h1>
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
      <b-col
        class="jumbotron"
        :md="isProjection ? 4 : 6"
        :offset="isProjection ? 1 : 3"
      >
        <b-row>
          <b-col md="6">
            <b>Select NT books:</b><br />

            <Checkboxes
              v-for="books in booksListNT"
              :key="books.group"
              :booklist="books.books"
              :bookgroup="books.group"
              :model="selected"
            />
          </b-col>
          <b-col md="6">
            <b>Select OT books:</b><br />

            <Checkboxes
              v-for="books in booksListOT"
              :key="books.group"
              :booklist="books.books"
              :bookgroup="books.group"
              :model="selected"
            />
          </b-col>
        </b-row>
        <b-row class="text-center">
          <b-button
            class="mx-auto"
            :disabled="selectedList.length < 3"
            v-on:click="launchClustering"
            >Project</b-button
          >
        </b-row>
      </b-col>
      <b-col md="7" v-if="isProjection">
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
  created() {
    document.title = "SBG New Testament projecter";
  },
  components: { Checkboxes, ProjectionGraph, InfoButton },
  data() {
    return {
      projections: {},
      selectedGlobal: {
        Gospels: [],
        Pauline: [],
        Pastoral: [],
        "Deutero-Pauline": [],
        Johannine: [],
        "Other epistles": [],
        History: [],
        Prophets: [],
        Law: [],
        Wisdom: [],
      },
      booksListNT: [],
      booksListOT: [],
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
      .get("http://localhost:8000/bookclasses/nt")
      .then((response) => {
        this.booksListNT = response.data;
      })
      .catch((error) => {
        console.log(error);
      });
    this.axios
      .get("http://localhost:8000/bookclasses/ot")
      .then((response) => {
        this.booksListOT = response.data;
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
