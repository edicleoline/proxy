import Dexie from 'dexie';

export const db = new Dexie('myDatabase');
db.version(1).stores({
    modemLog: 'id, modem_id, owner, type, message, code, params, auto, description, logged_at'
});
