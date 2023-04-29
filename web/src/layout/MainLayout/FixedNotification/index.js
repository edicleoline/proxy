import { Box } from '@mui/material';
import Alert from '@mui/material/Alert';

const FixedNotification = () => {
    return (
        <>
            <Box sx={{ display: 'flex', marginBottom: '10px' }}>
                <Alert severity="error" sx={{ width: '100%' }}>
                    This is an error alert — check it out!
                </Alert>
            </Box>
        </>
    );
};

export default FixedNotification;
