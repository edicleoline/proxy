import { db } from 'storage/db';

export const modemLog = db.modemLog;

export const storeModemLog = (log) => {
    const id = modemLog.add({
        id: log.id,
        modem_id: log.modem_id,
        owner: log.owner,
        type: log.type,
        message: log.message,
        code: log.code,
        params: log.params,
        logged_at: log.logged_at
    });
};
