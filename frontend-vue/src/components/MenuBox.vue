<template>
  <b-col class="text-center">
    <b-card
      height="5rem"
      :title="title"
      :img-src="img"
      img-alt="Image"
      img-top
      class="box"
    >
      <b-card-text>
        {{ text }}
      </b-card-text>
      <router-link :to="path" tag="button">{{ textButton }}</router-link>
    </b-card>
  </b-col>
</template>

<script>
export default {
  name: "MenuBox",
  props: {
    title: String,
    text: String,
    img: String,
    textButton: String,
    path: String,
  },
};
</script>

<style>
.box img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}
</style>
