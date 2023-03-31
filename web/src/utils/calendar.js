import moment from 'moment';

export const toMoment = (dateTime) => {
    return moment(dateTime);
};

export const fromNow = (dateTime) => {
    const v = dateTime.fromNow();
    return v;
};
