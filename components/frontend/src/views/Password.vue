<template>
  <div class="password">
    <div class="row">
      <div class="col-md-3"></div>
      <div class="col-md-6 ">
        <div class="form-group">
          <input
              class="form-control input-lg"
              v-model="password"
              @change="changePassword"
              placeholder="Enter a password"
              type="password"
          >
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-3"></div>

      <div class="robustness col-md-2 text-center" v-if="robustness"
      >
        <div class="robustness-title">Length score (/100)</div>
        <div class="score">{{ robustness.lengthScore }}</div>

      </div>
      <div class="robustness col-md-2 text-center" v-if="robustness"
      >
        <div class="robustness-title">Brute forced in</div>
        <div class="score">{{ robustness.bruteForceMs | humanizeDuration }}</div>

      </div>
      <div class="robustness col-md-2 text-center" v-if="robustness"
      >
        <div v-if="robustness.existsInDictionary"
        >
          <div class="robustness-title">Found in dictionary</div>
          <BIconBook class="icon score"/>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'
import {BIconBook} from 'bootstrap-vue'

export default {
  name: 'Password',
  created() {
    console.log('created', this.$store)
  },
  components: {BIconBook},
  data: function () {
    return {
      password: '',
    }
  },
  computed: {
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

<style lang="less" scoped>
.password {
  margin-top: 1em;
}

.score {
  font-size: 200%;
  font-weight: bold;
}

.icon.score {
  font-size: 300%;
  font-weight: bold;
}


</style>
