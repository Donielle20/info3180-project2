<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <img :src="`/uploads/camera.png`" alt="Photogram" class="image"/>
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Photogram</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link active">Home</RouterLink>
            </li>
            <!-- <li class="nav-item">
              <RouterLink class="nav-link" to="/about">About</RouterLink>
            </li> -->
            <li class="nav-item">
              <RouterLink class="nav-link active" to="/register/user">Register</RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link active" to="/user/login">Login</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
  import { RouterLink } from "vue-router";
  import { computed } from "vue";
  import { useStore } from "vuex";

  const store = useStore();

  const isLoggedIn = computed(() => {
    return store.state.currentUser !== null;
  });
</script>

<style>
.image{
  width: 30px;
  height: 30px;
  margin-left: 10px;
}
.navbar-brand{
  font-family: Lucida Handwriting;
}
</style>