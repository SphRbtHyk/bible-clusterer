<template>
  <div>
    <h1>Project chapters within books</h1>
    <b-col>
      <div>
        <!-- Using modifiers -->
        <b-button v-b-modal.info-modal>?</b-button>
        <!-- The modal -->
        <b-modal id="info-modal" title="About this project">
          <InfoButton />
        </b-modal>
      </div>
    </b-col>
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>
