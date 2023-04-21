<template>
</template>

<script setup>
    import { ref, onMounted  } from "vue";
    let csrf_token = ref("");

    onMounted(() => {
        getCsrfToken();
    });

    function logout()
    {
        fetch("/api/v1/auth/logout", {
                method: 'POST',
                headers: 
                {
                    'X-CSRFToken': csrf_token.value,
                    'Authorization': "Bearer "+ localStorage.getItem("token")
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

    logout()

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