<template>
  <b-container fluid>
    <div>
      <b-navbar toggleable="lg" type="dark" variant="info">
        <b-navbar-brand href="#">Bible projecter</b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav fill>
            <b-nav-item><b-link to="books">Book level</b-link></b-nav-item>
            <b-nav-item>
              <b-link to="/chapters">Chapter level</b-link></b-nav-item
            >
            <b-nav-item> <b-link to="/verses">Verse level</b-link></b-nav-item>
            <b-nav-item>
              <b-link to="/about">About this project</b-link></b-nav-item
            >
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

<style>
.nav-item.nav-item.nav-item a a {
  color: white;
}

hover .nav-item.nav-item.nav-item a a:hover {
  color: blue;
}
</style>
