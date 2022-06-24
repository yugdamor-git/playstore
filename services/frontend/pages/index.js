import * as React from 'react';
import Box from '@mui/material/Box';
import Search from '../components/search';
import MyApps from '../components/recent_apps';
import { backend_base_url, backend__internal_base_url } from '../src/config';
import { get_auth_token } from '../src/helper';
import { useRouter } from 'next/router';

export default function IndexRoute() {
  
  const router = useRouter()

  router.push("/home")
  

  

  return (

     <Box></Box>
  );
}