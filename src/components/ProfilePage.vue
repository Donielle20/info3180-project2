<template>
    <div class="hold">
        <div class="profile_contain">
            <img :src="`/uploads/${item[7]}`" alt="Profile Picture" class="image_profile">
            
            <div class="info">
                <h2>{{item[2]}} {{item[3]}}</h2>
                <br>
                <h6>{{item[4]}}, {{item[5]}}</h6>
                <h6>Member since {{date[2]}} {{date[3]}}</h6>
                <br>
                <p>{{item[6]}}</p>
            </div>

            <div class="info_2">
                <div class="numbers">
                    <h2>6</h2>
                    <h2>10</h2>
                </div>

                <div class="labels">
                    <h2>Posts</h2>
                    <h2>Followers</h2>
                </div>
                
                <br>
                <br>

                <div class="button">
                    <button class="new_posts">New Post</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    let user = localStorage.getItem('user');
    let item = user.split(",");
    let date = item[9].split(" ");
    console.log(user);
</script>

<style>
    .profile_contain{
        width: 90%;
        height: 70%;
        box-shadow: 3px 3px 3px rgb(191, 197, 199);
        border-radius: 5px;
        border: 2px solid rgb(191, 197, 199);
        display: flex;
        align-items: center;
    }
    .hold{
        width: 100%;
        height: 400px;
        display: flex;
        justify-content: center;
    }
    .image_profile{
        border-radius: 50%;
        width: 250px;
        height: 250px;
        margin-left: 20px;
    }
    .info{
        width: 750px;
        height: 250px;
        margin-left: 50px;
    }
    .info_2{
        height: 250px;
        width: 280px;
    }
    .numbers{
        display: grid;
        grid-template-columns: 150px 150px;
        padding: 1em;
    }
    .labels{
        display: grid;
        grid-template-columns: 120px 120px;
        color: rgb(145, 144, 144);
    }
    .new_posts{
        background-color: #007bff;
        border: none;
        border-radius: 5px;
        color: white;
        height: 45px;
        width: 100%;
    }
</style>