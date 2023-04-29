import PropTypes from 'prop-types';
import { Grid } from '@mui/material';
// import Tooltip from '@mui/material/Tooltip';
// import { IconCheck, IconBan } from '@tabler/icons';

const ProxyConnection = ({ type, port /*, ip, status*/ }) => {
    // let icon = '';

    // if (status === 'fail') {
    //     icon = (
    //         <Tooltip title="Desconectado">
    //             <div>
    //                 <IconBan size={12} style={{ position: 'relative', top: 0, marginLeft: 2, color: '#c62828' }} />
    //             </div>
    //         </Tooltip>
    //     );
    // } else if (status === 'success') {
    //     icon = (
    //         <Tooltip title="Conectado">
    //             <div>
    //                 <IconCheck size={14} style={{ position: 'relative', top: 1, marginLeft: 2, color: '#00c853' }} />
    //             </div>
    //         </Tooltip>
    //     );
    // }

    return (
        <>
            <Grid container justifyContent="flex-start" alignItems="start" direction="row" sx={{ p: 0, minWidth: '160px' }}>
                <Grid item>{type}</Grid>
                {/* <Grid item>/</Grid> */}
                {/* <Grid item>{ip}</Grid> */}
                <Grid item>://</Grid>
                <Grid item>{port}</Grid>
                {/* <Grid item>{icon}</Grid> */}
            </Grid>
        </>
    );
};

ProxyConnection.propTypes = {
    type: PropTypes.string.isRequired,
    port: PropTypes.number.isRequired,
    ip: PropTypes.string,
    status: PropTypes.string
};

export default ProxyConnection;
