<script setup>
import { ref } from "vue";

let message = ref("Hello World! This is a VueJS and Flask Starter Template.")

</script>

<template>
    <div class="container">
      <div class="contain">
        <div class="center">
          <img :src="`/uploads/under.jpg`" alt="Photogram" class="bridge"/>
          <div class="secondary">
            <div class="together">
              <img :src="`/uploads/camera.png`" alt="Photogram" class="image2"/>
              <h2 class="title">Photogram</h2>
            </div>
            
            <hr>

            <div class="text">
              <h4>Share photos of your favorite moments with friends, family and the world</h4>
            </div>

            <br>
            <br>
            <br>

            <div class="buttons">
              <a href="/register/user" class="btn1">Register</a>
              <a href="/user/login" class="btn2">Login</a>
            </div>
          </div>
          <!-- <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
          <h1>{{ message }}</h1> -->
        </div>
      </div>
    </div>
</template>

<style>
  .btn1{
    background-color: #3ec93e;
    border: none;
    border-radius: 5px;
    color: white;
    height: 50px;
    width: 200px;
    align-items: center;
    display: flex;
    justify-content: center;
    text-decoration: none;
  }

  .btn2{
    background-color: #6379f7;
    border: none;
    border-radius: 5px;
    color: white;
    height: 50px;
    width: 200px;
    align-items: center;
    display: flex;
    justify-content: center;
    text-decoration: none;
  }

  .buttons{
    display: grid;
    grid-template-columns: 210px 210px;
    justify-content: center;
  }

  .image2{
    margin-right: 20px;
    width: 30px;
    height: 30px;
  }
  
  .together{
    display: flex;
    justify-content: center;
  }

  .center{
    display: grid;
    grid-template-columns: 610px 610px;
    width: 810px;
    position: absolute;
    top: 22.5%;
    left: 10.25%;
  }

  .bridge{
    width: 600px;
    height: 400px;
    border-radius: 5px;
    box-shadow: 3px 3px 3px rgb(191, 197, 199);
  }

  hr{
    /* width: 75%; */
  }

  .secondary{
    width: 600px;
    height: 400px;
    border-radius: 5px;
    box-shadow: 3px 3px 3px rgb(191, 197, 199);
    border: 2px solid rgb(191, 197, 199);
    padding: 30px;

  }

  .contain{
    width: 1300px;
    height: 600px;
  }
  
  .title{
    font-family: Lucida Handwriting;
    font-weight: 900;
  }
</style>