import * as React from 'react';
import Box from '@mui/material/Box';
import Search from '../components/search';
import MyApps from '../components/recent_apps';

export default function Index() {
  return (
    <Box>
     <Search/>
     <MyApps/>
    </Box>
  );
}
