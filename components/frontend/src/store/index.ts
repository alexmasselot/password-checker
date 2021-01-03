import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    robustness: null,
    paf: 42
  },
  getters: {
    robustness: state => state.robustness
  },
  mutations: {
    clearRobustness: function (state) {
      state.robustness = null;
    },
    setRobustness: function (state, robustness) {
      state.robustness = robustness;
    }

  },
  actions: {
    checkPassword({state, commit}, password) {
      commit('clearRobustness');
      axios.post('/api/check', {password})
        .then((resp) => commit('setRobustness', resp.data))
        .catch((err) => console.error(err));
    }
  },
  modules: {}
});
