import * as React from 'react';
import Box from '@mui/material/Box';
import Search from '../components/search';
import MyApps from '../components/recent_apps';
import { backend_base_url } from '../src/config';

export default function Index({recent_apps}) {
  return (
    <Box>
     <Search/>
     <MyApps data={recent_apps} />
    </Box>
  );
}


export async function getServerSideProps(context) {
  
  
  const response = await fetch(`${backend_base_url}/get-recent-apps?limit=15`)
  const data = await response.json()
  
  return {
    props: {
      recent_apps:data["data"]
    }, // will be passed to the page component as props
  }
}