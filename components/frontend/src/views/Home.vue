<template>
  <div class="home jumbotron">
    <h1>Assess Password Strength</h1>
    Although no password will be saved here, you should not provide any of your actual passwords to such a web site.
    Use password of similar complexity to assess their strength.
    <Password/>
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
export default class Home extends Vue {
}
</script>
<style lang="less">

</style>
