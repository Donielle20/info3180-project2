<template>
    <div v-if="success" class="alert alert-success">
        <h6>Posts Upload Successful</h6>
    </div>

    <div v-if="fail" class="alert alert-danger">
        <li v-for="error in error_message">{{error}}</li>
    </div>
    
    <div class="container-fluid">
        <div class="r_form">
            <h5>New Post</h5>
            <form @submit.prevent="userPost" id="PostForm">
                <div class="form-group mb-3">
                    <label for="photo" class="form-label">Photo</label>
                    <input id="first" type="file" name="photo" class="form-control" />
                </div>

                <div class="form-group mb-3">
                    <label for="caption" class="form-label">Caption</label>
                    <input id="second" type="text" name="caption" class="form-control" />
                </div>

                <br>

                <input id="btn_length" type="submit" value="Submit">
            </form>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted  } from "vue";
    let csrf_token = ref("");
    let user = localStorage.getItem('user');
    let item = user.split(",");
    let token = ref("");
    token.value = localStorage.getItem('token');
    let success = ref(false);
    let fail = ref(false);
    let error_message = ref('');

    onMounted(() => {
        getCsrfToken();
        success.value = false;
        fail.value = false;
    });

    function userPost()
    {
        let postForm = document.getElementById("PostForm");
        let form_data = new FormData(postForm);

            fetch("/api/users/"+ item[0] + "/posts", {
                method: 'POST',
                body: form_data,
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

                    console.log(data.message);

                    let i = 0;

                    for (i in data)
                    {
                        error_message = data[i];
                    }

                    if(document.getElementById('first').value == "" || document.getElementById('second').value == "")
                    {
                        fail.value = true;
                    }
                    else
                    {
                        success.value = true;
                    }
                    // console.log(data.message);
                    // if (data.message == "Login Successfull")
                    // {
                        // getAuthorizationToken();
                        // window.location.href = 'http://localhost:5173/';
                        // let list = [data.user_id,data.username,data.firstname,data.lastname,data.location,data.biography,data.photo,data.joined_on];
                        // console.log(data.user_id);
                        // console.log(data.username);
                        // console.log(data.firstname);
                        // console.log(data.lastname);
                        // console.log(data.location);
                        // console.log(data.biography);
                        // console.log(data.photo);
                        // console.log(data.joined_on);
                    //     localStorage.setItem('user', list);
                    // }
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
                    console.log(data.csrf_token);
                    csrf_token.value = data.csrf_token;
        })
    }
</script>

<style>
    .r_form{
        width: 400px;
    }
    .container-fluid{
        display: flex;
        align-items: center;
        justify-content: center;
    }
    form{
        padding: 2em;
        box-shadow: 3px 3px 3px rgb(191, 197, 199);
        border-radius: 5px;
        border: 2px solid rgb(191, 197, 199);
        background-color: rgb(244, 242, 242);
    }
    #btn_length{
        width: 100%;
        height: 40px;
        border-radius: 5px;
        border: none;
        background-color: #007bff;
        color: white;
    }
</style>