import humanizeDuration from 'humanize-duration';
import Vue from "vue";

// const year = 31557600000;

export default Vue.filter('humanizeDuration', (ms) => {
  if (ms < 1) {
    return '< 1ms';
  }
  if (ms < 10) {
    return '< 10ms';
  }
  if (ms < 100) {
    return '< 100ms';
  }
  if (ms < 1000) {
    return '< 1s';
  }
  return humanizeDuration(ms, {round: true, largest: 2});
})

