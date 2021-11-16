<template>
  <b-container>
    <b-row class="text-center" align="vertical">
      <b-col>
        <h1>Welcome to the Greek Bible analyzer !</h1>
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
          img: require("../assets/bookshelf.png"),
          textButton: "Get started !",
          path: "/books",
        },
        {
          title: "Chapter projector",
          text:
            "Select chapters within the different books and project them into a 3D space (only available for the OT)",
          img: require("../assets/chapter.png"),
          textButton: "Get started !",
          path: "/chapters",
        },
      ],
    };
  },
};
</script>
