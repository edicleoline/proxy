import PropTypes from 'prop-types';
import { Box, Card } from '@mui/material';

const ModemStatusBox = ({ bgcolor, title, dark }) => {
    return (
        <>
            <Card sx={{ mb: 0, width: '100%' }}>
                <Box
                    sx={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        p: 1,
                        bgcolor,
                        color: dark ? 'grey.800' : '#ffffff',
                        position: 'relative'
                    }}
                >
                    <span>{title}</span>
                </Box>
            </Card>
        </>
    );
};

ModemStatusBox.propTypes = {
    bgcolor: PropTypes.string,
    title: PropTypes.string,
    dark: PropTypes.bool
};

export default ModemStatusBox;
