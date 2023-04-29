<template>
    <div class="everything">
        <div>
            <div v-for="post in posts" class="hold-posts">
                <div class="username">
                    <img :src="`/uploads/${post.user_photo}`" alt="User Image" class="user_image"/>
                    <button class="invi" v-on:click="page(post.user_id)">{{post.username}}</button>
                </div>
                <img :src="`/uploads/${post.photo}`" alt="Posts Image" class="posts_image"/>
                <div class="post-info">
                    <p>{{post.caption}}</p>
                    
                    
                    <h6 class="likes"><button class="invi" v-on:click="like(post.id)"><img :src="`/uploads/heart.png`" alt="Heart Image" class="heart_image"/></button> {{post.likes}} Likes</h6>
                    <h6>{{post.created_on}}</h6>
                </div>
            </div>  
        </div>

        <div class="btn-new">
            <button v-on:click="post" class="new_posts">New Post</button>
        </div>
    </div>  
</template>

<script setup>
    import { ref, onMounted  } from "vue";
    let csrf_token = ref("");
    let posts = ref([]);
    let token = ref("");
    token.value = localStorage.getItem('token');

    onMounted(() => {
        getCsrfToken();
    });

    fetch("/api/v1/posts", {
                method: 'GET',
                headers: 
                {
                    'Authorization': "Bearer " + token.value
                }
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {

                    // console.log(data.users);
                    posts.value = data.posts;
                })
                .catch(function (error) {
                    console.log(error);
                });

    function post()
    {
        window.location.href = 'http://localhost:5173/posts/new';

    }

    function like(id)
    {
        fetch("/api/posts/" + id +"/like", {
            method: 'POST',
            headers: 
            {
                'X-CSRFToken': csrf_token.value,
                'Authorization': "Bearer " + token.value
            }
        })
        .then(function (response) {
        return response.json();
        })
        .then(function (data) {
        console.log(data);

        // Chain the second fetch request here
        return fetch("/api/v1/posts", {
            method: 'GET',
            headers: 
            {
                'Authorization': "Bearer " + token.value
            }
        });
        })
        .then(function (response) {
        return response.json();
        })
        .then(function (data) {
        console.log(data.users);
        posts.value = data.posts;
        })
        .catch(function (error) {
        console.log(error);
        });
    }

    function page(id)
    {
        // console.log(id);

        fetch("/api/users/" + id, {
                method: 'GET',
                headers: 
                {
                    'Authorization': "Bearer " + token.value
                }
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {

                    let list = [data.user_id,data.username,data.firstname,data.lastname,data.location,data.biography,data.photo,data.joined_on];
                    localStorage.setItem('visit', list);
                    window.location.href = 'http://localhost:5173/users/' + id;
                    console.log(list);
                    // posts.value = data.posts;
                })
                .catch(function (error) {
                    console.log(error);
                });
    }

    function getCsrfToken() 
    {
        fetch('/api/v1/csrf-token')
            .then((response) => response.json())
                .then((data) => {
                    // console.log(data.csrf_token);
                    csrf_token.value = data.csrf_token;
        })
    }
</script>
    
<style>
    .posts_image{
        width: 800px;
        height: 500px;
    }
    .hold-posts{
        margin-left: 6em;
        margin-top: 4em;
        border: 2px solid rgb(191, 197, 199);
        box-shadow: 3px 3px 3px rgb(191, 197, 199);
        background-color: rgb(244, 242, 242);
        border-radius: 5px;
        width: 802px;
    }
    .new_posts{
        background-color: #007bff;
        border: none;
        border-radius: 5px;
        color: white;
        height: 45px;
        width: 250px;
    }
    .everything{
        display: grid;
        grid-template-columns: 1fr 1fr;
    }
    .btn-new{
        padding: 80px;
        margin-left: 130px;
    }
    .post-info{
        width: 800px;
        height: 200px;
        padding: 1em;
        position: relative;
    }
    .post-info h6:last-child {
        position: absolute;
        bottom: 0;
        right: 0;
        padding: 1em;
    }
    .likes{
        position: absolute;
        bottom: 0;
        left: 0;
        padding: 1em;
        display: flex;
        align-items: center;
    }
    .username{
        width: 800px;
        height: 80px;
        display: grid;
        grid-template-columns: 60px 60px;
        padding: 30px;
        align-items: center;
        /* margin-left: 30px; */
    }
    .user_image{
        width: 40px;
        height: 40px;
        border-radius: 50%;
    }
    .invi{
        border: none;
        background: none;
    }
    .heart_image{
        height: 20px;
        width: 20px;
    }
</style>