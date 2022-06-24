import { AppBar, Box, Button, IconButton, Toolbar, Typography } from '@mui/material'
import React from 'react'
import AndroidIcon from '@mui/icons-material/Android';

import {useRouter} from 'next/router'
import { Logout } from '@mui/icons-material';
import { remove_auth_cookie } from '../src/helper';

const Navbar = () => {
    const router = useRouter()
    function logout()
    {
        remove_auth_cookie()
        router.push("/login")

    }
  return (
    <Box sx={{ flexGrow: 1 }} marginBottom={3}>
        <AppBar elevation={1} position='static' color='primary'>
            <Toolbar>
                <IconButton onClick={()=>router.push("/")}>
                    <AndroidIcon color='white'/>
                </IconButton>
                <Typography sx={{ flexGrow: 1 }}>
                    App Manager
                </Typography>
                {router.pathname != '/login'&&

                <Box>
                <Button onClick={()=>logout()} startIcon={<Logout/>} color='white'>
                    Logout
                </Button>
                </Box>

                }
                

            </Toolbar>
        </AppBar>
    </Box>
  )
}

export default Navbar