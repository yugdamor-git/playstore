
import Box from '@mui/material/Box';
import { useRouter } from 'next/router';
import { useEffect } from 'react';

export default function IndexRoute() {
  
  const router = useRouter()
  
  useEffect(() => {
        
    router.push("/login")

  },[])
  

  return (

     <Box></Box>
  );
}