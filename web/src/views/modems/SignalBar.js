import PropTypes from 'prop-types';
import { IconAntennaBars1, IconAntennaBars2, IconAntennaBars3, IconAntennaBars4, IconAntennaBars5 } from '@tabler/icons';

const SignalBar = ({ signal }) => {
    const icons = {
        ['0']: <span>-</span>,
        ['1']: <IconAntennaBars1 title={signal} />,
        ['2']: <IconAntennaBars2 title={signal} />,
        ['3']: <IconAntennaBars3 title={signal} />,
        ['4']: <IconAntennaBars4 title={signal} />,
        ['5']: <IconAntennaBars5 title={signal} />
    };

    return icons[signal];
};

SignalBar.propTypes = {};

export default SignalBar;
