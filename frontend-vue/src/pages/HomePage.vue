<template>
  <b-container>
    <b-row class="text-center" align="vertical">
      <b-col>
        <h1>Welcome to the Greek Bible projecter project</h1>
      </b-col>
    </b-row>
    <b-row class="text-center mt-5">
      <MenuBox
        v-for="data in menuBoxes"
        :key="data.title"
        :title="data.title"
        :text="data.text"
        :textButton="data.textButton"
        :path="data.path"
        :img="data.img"
      />
    </b-row>
  </b-container>
</template>

<script>
import MenuBox from "../components/MenuBox";

export default {
  name: "HomePage",
  components: { MenuBox },
  data() {
    return {
      menuBoxes: [
        {
          title: "Book projector",
          text:
            "Select books among those of the Greek Bible and check their repartition in a 3D space",
          img: require("../assets/books.png"),
          textButton: "Get started !",
          path: "/books",
        },
        {
          title: "Chapter projector",
          text:
            "Select books among those of the Greek Bible and project their chapters into a 3D space",
          img: require("../assets/chapter.png"),
          textButton: "Get started !",
          path: "/chapters",
        },
        {
          title: "Verse projector",
          text:
            "Select books among those of the Greek Bible and project their verses into a 3D space",
          img: require("../assets/verses.png"),
          textButton: "Get started !",
          path: "/chapters",
        },
      ],
    };
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css?family=Roboto+Condensed");

h1 {
  padding-top: 10px;
  font-family: "Roboto Condensed";
}
</style>
