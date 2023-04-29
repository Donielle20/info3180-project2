<template>
    <div class="container-fluid">
        <div class="r_form">
            <h5>Login</h5>
            <form @submit.prevent="loginUser" id="UserForm">
                <div class="form-group mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input id="first" type="text" name="username" class="form-control" />
                </div>

                <div class="form-group mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input id="second" type="password" name="password" class="form-control" />
                </div>

                <br>

                <input id="btn_length" type="submit" value="Login">
            </form>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted  } from "vue";
    let csrf_token = ref("");
    let auth_token = ref("");

    onMounted(() => {
        getCsrfToken();
    });

    function loginUser()
    {
        let userForm = document.getElementById("UserForm");
        let form_data = new FormData(userForm);

            fetch("/api/v1/auth/login", {
                method: 'POST',
                body: form_data,
                headers: 
                {
                    'X-CSRFToken': csrf_token.value
                }
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {

                    // console.log(data.message);
                    if (data.message == "Login Successfull")
                    {
                        getAuthorizationToken();
                        window.location.href = 'http://localhost:5173/explore';
                        let list = [data.user_id,data.username,data.firstname,data.lastname,data.location,data.biography,data.photo,data.joined_on];
                        localStorage.setItem('user', list);
                        console.log(data.trouble);
                    }
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

    function getAuthorizationToken() 
    {
        fetch('/api/v1/generate-token')
            .then((response) => response.json())
                .then((data) => {
                    // console.log(data.token);
                    // auth_token.value = data.token;
                    localStorage.setItem('token', data.token);
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