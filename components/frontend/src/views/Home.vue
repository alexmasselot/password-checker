<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <Password msg="Welcome to Your Vue.js + TypeScript App"/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Password from '@/views/Password.vue'; // @ is an alias to /src

@Component({
  components: {
    Password
  },
})
export default class Home extends Vue {}
</script>
