<template>
  <b-col>
    <router-view></router-view>
    <b-row>
      <b-col md="4" class="text-center" offset="4">
        Select up to 4 books, in order to check the similarities between each of
        their chapters, through a PCA projection of their tf-idf similarities.
      </b-col></b-row
    >
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
            :disabled="selectedList.length > 14"
            v-on:click="launchClustering"
            variant="danger"
            >Project</b-button
          >
        </b-row>
      </b-col>
      <b-col md="7" v-if="isProjection">
        <ProjectionGraph :data="projectionsList" />
      </b-col>
      <b-col class="text-center" v-else> </b-col>
    </b-row>
  </b-col>
</template>

<script>
import Checkboxes from "../components/Checkboxes.vue";
import ProjectionGraph from "../components/ProjectionGraph.vue";
var qs = require("qs");

export default {
  name: "ChapterProjector",
  created() {
    document.title = "Bible projecter";
  },
  components: { Checkboxes, ProjectionGraph },
  data() {
    return {
      projections: {},
      selectedGlobal: {
        History: [],
        Prophets: [],
        Law: [],
        Wisdom: [],
        Gospels: [],
        Pauline: [],
        Pastoral: [],
        "Deutero-Pauline": [],
        Johannine: [],
        "Other epistles": [],
      },
      booksListOT: [],
      booksListNT: [],
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
      .get("localhost/api/bookclasses/nt")
      .then((response) => {
        this.booksListNT = response.data;
      })
      .catch((error) => {
        console.log(error);
      });
    this.axios
      .get("localhost/api/bookclasses/ot")
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
          .post("localhost/api/clusterize/chapters?", null, {
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
