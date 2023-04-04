import { store } from 'store';
import { commandStatus } from 'store/serverControlReducer';
import addCommandServerControl from 'store/actions/addCommandServerControl';
import setCommandsServerControl from 'store/actions/setCommandsServerControl';
import objectHash from 'object-hash';

export const commandsInQueue = () => {
    return store.getState().serverControl.commands;
};

export const pendingReloadModemsInQueue = () => {
    const commands = commandsInQueue();
    return commands ? commands.filter((x) => x.status === commandStatus.pending && x.action === 'reload_modem') : [];
};

export const addCommandInQueue = (command) => {
    store.dispatch(addCommandServerControl(command));
};

export const removeCommandsFromQueue = (commands = []) => {
    const commandsQueue = commandsInQueue();
    const newCommands = commandsQueue.filter((oldCommand) => {
        const oldCommandHash = objectHash({
            action: oldCommand.action,
            data: oldCommand.data
        });

        let found = false;
        commands.forEach((command) => {
            const commandHash = objectHash({
                action: command.action,
                data: command.data
            });
            if (oldCommandHash === commandHash) {
                found = true;
            }
        });

        return !found;
    });

    store.dispatch(setCommandsServerControl(newCommands));
};
