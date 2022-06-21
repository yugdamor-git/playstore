import { AppBar, Box, IconButton, Toolbar, Typography } from '@mui/material'
import React from 'react'
import AndroidIcon from '@mui/icons-material/Android';

const Navbar = () => {
  return (
    <Box marginBottom={3}>
        <AppBar elevation={1} position='static' color='primary'>
            <Toolbar>
                <IconButton>
                    <AndroidIcon color='white'/>
                </IconButton>
                <Typography>
                    App Manager
                </Typography>
            </Toolbar>
        </AppBar>
    </Box>
  )
}

export default Navbar