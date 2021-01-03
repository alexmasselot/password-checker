import humanizeDuration from '@/filters/humanize-duration';

const second = 1000;
const minute = 60 * second;
const hour = 60 * minute;
const day = 24 * hour;
const week = 7 * day;
const month = 2629800000;
const year = 31557600000;


test.each`
      ms     | expected
      ${0.9}  | ${'< 1ms'}
      ${1}  | ${'< 10ms'}
      ${1.3}  | ${'< 10ms'}
      ${10.2}  | ${'< 100ms'}
      ${102}  | ${'< 1s'}
      ${1000}  | ${'1 second'}
      ${2000}  | ${'2 seconds'}
      ${60 * second}  | ${'1 minute'}
      ${1.5 * minute}  | ${'1 minute and 30 seconds'}
      ${1.5 * minute + 20}  | ${'1 minute and 30 seconds'}
      ${5 * minute + 3 * second}  | ${'5 minutes and 3 seconds'}
      ${1 * day}  | ${'1 day'}
      ${1 * day + 29 * minute}  | ${'1 day'}
      ${1 * day + 31 * minute}  | ${'1 day and 1 hour'}
      ${1 * month}  | ${'1 month'}
      ${5 * week}  | ${'1 month and 1 week'}
      ${1 * year}  | ${'1 year'}
      ${123 * year}  | ${'123 years'}
    `('humanize $ms to $expected', ({ms, expected}) => {
    expect(humanizeDuration(ms)).toEqual(expected);
});

