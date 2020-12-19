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
      console.log('checkPassword', password);
      console.log('checkPassword', arguments);
      commit('clearRobustness');
      axios.get('/api/' + password)
        .then((resp) => commit('setRobustness', resp.data))
        .catch((err) => console.error(err));
    }
  },
  modules: {}
});
