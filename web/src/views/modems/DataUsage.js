import PropTypes from 'prop-types';
import { Grid } from '@mui/material';
import Tooltip from '@mui/material/Tooltip';
import { IconArrowUp, IconArrowDown } from '@tabler/icons';

const DataUsage = ({ download, upload }) => {
    const iconProps = {
        size: 14,
        style: { position: 'relative', top: 1, marginRight: 2 }
    };
    const gridContainerProps = {
        justifyContent: 'end',
        alignItems: 'end',
        direction: 'row',
        sx: { p: 0.2, px: 0, borderRadius: 1 }
    };
    return (
        <>
            <Grid container justifyContent="space-between" alignItems="end" direction="column" sx={{ minWidth: '80px' }}>
                <Grid item>
                    <Grid container {...gridContainerProps}>
                        <Grid item>
                            <Tooltip title="Download">
                                <div>
                                    <IconArrowDown {...iconProps} />
                                </div>
                            </Tooltip>
                        </Grid>
                        <Grid item>{download}</Grid>
                    </Grid>
                </Grid>
                <Grid item>
                    <Grid container {...gridContainerProps}>
                        <Grid item>
                            <Tooltip title="Upload">
                                <div>
                                    <IconArrowUp {...iconProps} />
                                </div>
                            </Tooltip>
                        </Grid>
                        <Grid item>{upload}</Grid>
                    </Grid>
                </Grid>
            </Grid>
        </>
    );
};

DataUsage.propTypes = {};

export default DataUsage;
