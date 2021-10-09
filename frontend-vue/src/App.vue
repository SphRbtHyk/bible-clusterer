<template>
  <b-container>
    <b-row class="text-center ">
      <b-col>
        <h1>LXX Clusterer</h1>
      </b-col>
    </b-row>
    <b-row class="jumbotron">
      <b>Select NT book:</b><br />

      <Checkboxes
        v-for="books in booksList"
        :key="books.class"
        :booklist="books.booklist"
        :bookgroup="books.class"
        :model="selected"
      />
    </b-row>
    {{ selectedList }}
    <b-row class="text-center">
      <b-col>
        <b-button>Clusterize</b-button>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import Checkboxes from "./components/Checkboxes.vue";

export default {
  name: "App",
  components: { Checkboxes },
  data() {
    return {
      selectedGlobal: { Gospels: [], Pauline: [], Other: [] },
      booksList: [
        { class: "Gospels", booklist: ["Mt", "Lk", "Jn", "Mk"] },
        { class: "Pauline", booklist: ["Th", "Co"] },
        { class: "Other", booklist: ["Ac", "Rev"] },
      ],
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
