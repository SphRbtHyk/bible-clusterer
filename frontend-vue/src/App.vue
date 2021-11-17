<template>
  <b-container fluid>
    <div>
      <b-navbar toggleable="lg" type="dark" variant="info">
        <b-navbar-brand href="#">Bible projecter</b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav fill>
            <b-nav-item href="/books">Book level</b-nav-item>
            <b-nav-item href="/chapters">Chapter level</b-nav-item>
            <b-nav-item href="/verses">Verse level</b-nav-item>
            <b-nav-item href="/about">About this project</b-nav-item>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
    <router-view />
  </b-container>
</template>

<script>
export default {
  name: "App",
};
</script>
