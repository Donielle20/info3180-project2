<template>
    <div class="container-fluid">
        <form @submit.prevent="loginUser" id="UserForm">
            <div class="form-group mb-3">
                <label for="username" class="form-label">Username</label>
                <input id="first" type="text" name="username" class="form-control" />
            </div>

            <div class="form-group mb-3">
                <label for="password" class="form-label">Password</label>
                <input id="second" type="password" name="password" class="form-control" />
            </div>

            <input type="submit" class="btn btn-primary" value="Submit">
        </form>
    </div>
</template>

<script setup>
    import { ref, onMounted  } from "vue";
    let csrf_token = ref("");

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