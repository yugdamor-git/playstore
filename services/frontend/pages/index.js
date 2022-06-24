import * as React from 'react';
import Box from '@mui/material/Box';
import Search from '../components/search';
import MyApps from '../components/recent_apps';
import { backend_base_url, backend__internal_base_url } from '../src/config';
import { get_auth_token } from '../src/helper';
import { useRouter } from 'next/router';

export default function Index() {
  
  const router = useRouter()
  function fetch_recent_apps()
  {

    let auth_toke = get_auth_token()
        let headers = {}
        if(auth_toke != undefined)
        {
            headers['Authorization'] = `Bearer ${auth_token}`
        }
    
    const response = fetch(`${backend_base_url}/get-recent-application?limit=15`,{
      headers:headers
    })

    if (response.status != 200)
    {
      router?.push("/login")
      return
    }

    const data = response.json()
    return data["data"]
  }
  let [recentApps,setRecentApps] = React.useState(null)


  React.useEffect(() => {
    let recent_apps = fetch_recent_apps()
    setRecentApps(recent_apps)
  },[])

  

  return (
    <Box>
     <Search/>
     {recentApps &&
      <MyApps data={recentApps} />
     }
     
    </Box>
  );
}