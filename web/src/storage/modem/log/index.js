import { db } from 'storage/db';
import Dexie from 'dexie';

export const modemLog = db.modemLog;

export const storeModemLog = (log) => {
    return modemLog.add({
        id: log.id,
        modem_id: log.modem_id,
        owner: log.owner,
        type: log.type,
        message: log.message,
        code: log.code,
        params: log.params,
        auto: log.auto,
        description: log.description,
        logged_at: log.logged_at
    });
};

export const bulkStoreModemLog = (logs) => {
    return modemLog.bulkAdd(logs);
};
