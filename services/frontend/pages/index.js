import * as React from 'react';
import Box from '@mui/material/Box';
import Search from '../components/search';
import MyApps from '../components/recent_apps';
import { backend_base_url, backend__internal_base_url } from '../src/config';
import { get_auth_token } from '../src/helper';

export default function Index() {
  
  function fetch_recent_apps()
  {
    const response = fetch(`${backend_base_url}/get-recent-application?limit=15`,{
      headers:{
        'Authorization':`Bearer ${get_auth_token()}`
      }
    })

    if (response.status != 200)
    {
      return
    }

    const data = response.json()
    return data["data"]
  }
  

  const recent_apps = fetch_recent_apps()

  return (
    <Box>
     <Search/>
     {recent_apps &&
      <MyApps data={recent_apps} />
     }
     
    </Box>
  );
}