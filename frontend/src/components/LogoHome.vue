<script>
    import UFC_logo from '@/assets/UFC_logo.png';
</script>
<template>
    <div class="logo-home">
        <img :src="UFC_logo" alt="Logo da UFC" class="logo-image" />
        <router-link to="/" class="home-link">Jornal UFC</router-link>
    </div>
</template>