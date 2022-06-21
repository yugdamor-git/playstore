import { Container } from '@mui/material'
import { Box } from '@mui/system'
import React from 'react'
import Footer from './footer'
import Navbar from './navbar'

const Layout = ({children}) => {
  return (
    <Box>
      <Navbar/>
      <Container maxWidth="xl">{children}</Container>
      <Footer/>
    </Box>
  )
}

export default Layout