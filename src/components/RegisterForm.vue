<template>
    <div class="container-fluid">
        <div class="r_form">
            <h5>Register</h5>
            <form @submit.prevent="saveUser" id="RegisterForm">
                <div class="col-12">
                    <label for="username" class="form-label">Username</label>
                    <input id="first" type="text" name="username" class="form-control" />
                </div>

                <br>

                <div class="col-12">
                    <label for="password" class="form-label">Password</label>
                    <input id="second" type="password" name="password" class="form-control" />
                </div>

                <br>

                <div class="col-12">
                    <label for="firstname" class="form-label">Firstname</label>
                    <input id="third" type="text" name="firstname" class="form-control" />
                </div>

                <br>

                <div class="col-12">
                    <label for="lastname" class="form-label">Lastname</label>
                    <input id="fourth" type="text" name="lastname" class="form-control" />
                </div>

                <br>

                <div class="col-12">
                    <label for="email" class="form-label">Email</label>
                    <input id="fifth" type="text" name="email" class="form-control" />
                </div>

                <br>

                <div class="col-12">
                    <label for="location" class="form-label">Location</label>
                    <input id="sixth" type="text" name="location" class="form-control" />
                </div>

                <br>

                <div class="col-12">
                    <label for="biography" class="form-label">Biography</label>
                    <input id="seventh" type="text" name="biography" class="form-control" />
                </div>

                <br>

                <div class="col-12">
                    <label for="photo" class="form-label">Photo</label>
                    <input id="eighth" type="file" name="photo" class="form-control" />
                </div>

                <br>

                <div class="col-12">
                    <input id="btn_length" type="submit" value="Register">
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted  } from "vue";
    let csrf_token = ref("");

    onMounted(() => {
        getCsrfToken();
    });

    function saveUser()
    {
        let registerForm = document.getElementById("RegisterForm");
        let form_data = new FormData(registerForm);

            fetch("/api/v1/register", {
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

                    console.log(data);
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