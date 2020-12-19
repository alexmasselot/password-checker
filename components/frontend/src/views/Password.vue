<template>
  <div class="Password">
    <input v-model="password" @change="changePassword">
    <div class="robustness" v-if="robustness"
    >{{robustness.bruteForceMs | humanizeDuration}}
    </div>
  </div>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'
import moment from 'moment'

export default {
  name: 'Password',
  created() {
    console.log('created', this.$store)
  },
  data: function() {
    return {
      password: '',
    }
  },
  computed:{
    ...mapGetters(['robustness']),
  },
  methods: {
    ...mapActions(['checkPassword']),
    changePassword: function () {
      this.checkPassword(this.password)
    }
  }
};
</script>

<style lang="stylus">

</style>
