import * as React from 'react';
import Box from '@mui/material/Box';
import { useRouter } from 'next/router';

export default function IndexRoute() {
  
  const router = useRouter()
  
  useEffect(() => {
        
    router.push("/home")

  },[])
  

  return (

     <Box></Box>
  );
}