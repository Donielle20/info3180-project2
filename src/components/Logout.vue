<template>
</template>

<script setup>
    import { ref, onMounted  } from "vue";
    let csrf_token = ref("");
    let token = ref("");
    token.value = localStorage.getItem('token');

    onMounted(async() => {
        await getCsrfToken();
        await logout();
    });

    async function logout()
    {
        await fetch("/api/v1/auth/logout", {
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
                    localStorage.clear();
                    console.log(data);
                    window.location.href = 'http://localhost:5173/';
                })
                .catch(function (error) {
                    console.log(error);
                });
    }

    async function getCsrfToken() 
    {
        await fetch('/api/v1/csrf-token')
            .then((response) => response.json())
                .then((data) => {
                    csrf_token.value = data.csrf_token;
                    console.log(csrf_token.value);
        })
    }
</script>